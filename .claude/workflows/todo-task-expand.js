export const meta = {
  name: 'todo-task-expand',
  description: 'Expand a list of To Do entries into checked briefs: one writer and one reviewer per entry, with one repair pass',
  whenToUse: 'A sweep with five or more entries, or a backlog run. Pass the entries as args: [{id, text, notes, labels, source, captured_on}].',
  phases: [
    { title: 'Write', detail: 'one brief-writer per entry' },
    { title: 'Check', detail: 'one brief-checker per brief' },
    { title: 'Repair', detail: 'fix medium and high failures once, then re-check' },
  ],
}

// args: an array of entries, or {entries: [...]}. Each entry: {id, text, notes, labels, source, captured_on}.
const entries = (Array.isArray(args) ? args : (args && args.entries) || []).filter(e => e && e.text)
if (!entries.length) {
  log('No entries were passed in args. Nothing to do.')
  return []
}

// The roles live in .claude/agents so the skills and this workflow share one definition.
const WRITER = 'Read .claude/agents/brief-writer.md and follow it exactly. It is your role for this task.'
const CHECKER = 'Read .claude/agents/brief-checker.md and follow it exactly. It is your role for this task.'

const BRIEF = {
  type: 'object',
  properties: {
    path: { type: 'string', description: 'Path of the finished brief.json' },
    title: { type: 'string' },
    task_type: { type: 'string' },
    to_confirm: { type: 'array', items: { type: 'string' } },
  },
  required: ['path', 'title', 'task_type', 'to_confirm'],
}
const VERDICT = {
  type: 'object',
  properties: {
    pass: { type: 'boolean', description: 'False when there is at least one medium or high failure' },
    failures: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          rule: { type: 'string' },
          quote: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'rule', 'quote', 'fix'],
      },
    },
  },
  required: ['pass', 'failures'],
}

const describe = e => [
  `Entry, word for word: <<<${e.text}>>>`,
  `Notes already on the task: <<<${e.notes || 'None'}>>>`,
  `Source: ${e.source || 'Todoist'}`,
  `Task id: ${e.id || ''}`,
  `Labels on the task: ${(e.labels || []).join(', ') || 'none'}`,
  `Capture date: ${e.captured_on || ''}`,
].join('\n')

const serious = v => (v && Array.isArray(v.failures) ? v.failures.filter(f => f.severity === 'medium' || f.severity === 'high') : [])

const write = (e, _e, i) =>
  agent(`${WRITER}\n\n${describe(e)}`, { label: `write:${i + 1}`, phase: 'Write', schema: BRIEF })

const check = (brief, _e, i) => {
  if (!brief) return null
  return agent(`${CHECKER}\n\nThe brief to review: ${brief.path}`, { label: `check:${i + 1}`, phase: 'Check', schema: VERDICT })
    .then(verdict => ({ brief, verdict }))
}

const repair = async (r, e, i) => {
  if (!r || !r.verdict) return r ? { ...r, passed: false } : null
  const found = serious(r.verdict)
  if (!found.length) return { ...r, passed: true }
  const fixed = await agent(
    `${WRITER}\n\nThe brief already exists at ${r.brief.path}. A reviewer found these failures. Fix each one and nothing else.\n${JSON.stringify(found, null, 1)}\n\n${describe(e)}`,
    { label: `repair:${i + 1}`, phase: 'Repair', schema: BRIEF })
  if (!fixed) return { ...r, passed: false }
  const again = await agent(`${CHECKER}\n\nThe brief to review: ${fixed.path}`, { label: `recheck:${i + 1}`, phase: 'Repair', schema: VERDICT })
  return { brief: fixed, verdict: again || r.verdict, passed: !!again && serious(again).length === 0 }
}

const results = await pipeline(entries, write, check, repair)

const report = results.map((r, i) => ({
  id: entries[i].id || '',
  entry: entries[i].text,
  path: r && r.brief ? r.brief.path : '',
  title: r && r.brief ? r.brief.title : '',
  task_type: r && r.brief ? r.brief.task_type : '',
  to_confirm: r && r.brief ? r.brief.to_confirm : [],
  passed: !!(r && r.passed),
  failures: r && r.verdict ? serious(r.verdict) : [],
}))

const passed = report.filter(r => r.passed).length
log(`${passed} of ${entries.length} briefs passed review. ${entries.length - passed} need a person to look at them.`)
return report
