/* ToDo Task Builder: the parts with no page in them.
   The same rules as the Python package (todotask/models.py and render.py), so a brief made
   on the phone and a brief made by the command line are the same brief. */

const Core = (() => {
  const STAGES = ["Captured", "Briefed", "In session", "Waiting on me", "Done"];
  const TASK_TYPES = ["content", "plan", "learning", "idea", "health", "errand", "appointment", "purchase", "person", "reflection", "unclear"];
  const LIMITS = { title: 120, writebackTitle: 90, writebackDescription: 600 };
  const ACTIONS_HEADING = "Information Needed and Next Actions";
  const PLAN_HEADING = "Execution Plan for Claude";
  const ORIGIN_LABEL = "Original entry (word for word):";
  const NOTES_LABEL = "Notes on the task (word for word):";

  const str = (v) => (typeof v === "string" ? v.trim() : v == null ? "" : String(v).trim());
  const list = (v) => (Array.isArray(v) ? v.map(str).filter(Boolean) : str(v) ? [str(v)] : []);
  const stop = (t) => (/[.!?]$/.test(t.trim()) ? t.trim() : t.trim() + ".");
  // Models sometimes number list items themselves; the page numbers them, so strip a leading "1." or "1)".
  const unnumber = (t) => t.replace(/^\s*\d{1,2}[.)]\s+/, "");

  /** Coerce whatever came back (from Claude, from storage) into the brief shape. */
  function normalise(data, entry) {
    const d = data && typeof data === "object" ? data : {};
    const b = d.brief && typeof d.brief === "object" ? d.brief : {};
    const p = b.plan && typeof b.plan === "object" ? b.plan : {};
    const w = d.writeback && typeof d.writeback === "object" ? d.writeback : {};
    const e = entry || d.entry || {};
    return {
      entry: {
        text: str(e.text), notes: str(e.notes), source: str(e.source) || "Manual", list: str(e.list),
        task_id: str(e.task_id), captured_on: str(e.captured_on), labels: list(e.labels),
      },
      task_type: TASK_TYPES.includes(d.task_type) ? d.task_type : "idea",
      brief: {
        title: str(b.title), description: str(b.description), status: str(b.status),
        calendar_date: str(b.calendar_date) || "Not supplied",
        context_heading: str(b.context_heading) || "Context",
        context: list(b.context), actions: list(b.actions).map(unnumber),
        plan: {
          output: str(p.output), steps: list(p.steps).map(unnumber), tools: str(p.tools),
          rhythm: str(p.rhythm), done_when: str(p.done_when),
        },
      },
      writeback: { title: str(w.title), description: str(w.description) },
    };
  }

  /** Everything that breaks the brief structure. Empty means the brief is sound. */
  function problems(task) {
    const found = [];
    const b = task.brief, w = task.writeback;
    if (!b.title) found.push("The brief has no title.");
    else if (b.title.length > LIMITS.title) found.push(`The title is ${b.title.length} characters; the limit is ${LIMITS.title}.`);
    if (!b.description) found.push("The brief has no description.");
    if (!b.status) found.push("The brief has no status.");
    if (b.context.length < 1 || b.context.length > 4) found.push(`Context has ${b.context.length} paragraphs; it needs 1 to 4.`);
    if (b.actions.length < 2 || b.actions.length > 6) found.push(`There are ${b.actions.length} actions; the list needs 2 to 6.`);
    if (b.actions.length && !/^next action:/i.test(b.actions[0])) found.push("The first action must start with “Next action:”.");
    if (!b.plan.output) found.push("The execution plan has no Output.");
    if (!b.plan.steps.length) found.push("The execution plan has no Steps.");
    if (!b.plan.done_when) found.push("The execution plan has no “Done when”.");
    if (!w.title) found.push("The write-back has no title.");
    else if (w.title.length > LIMITS.writebackTitle) found.push(`The write-back title is ${w.title.length} characters; the limit is ${LIMITS.writebackTitle}.`);
    if (!w.description) found.push("The write-back has no description.");
    else if (w.description.length > LIMITS.writebackDescription) found.push(`The write-back description is ${w.description.length} characters; the limit is ${LIMITS.writebackDescription}.`);
    return found;
  }

  /** The yellow section as [kind, text] pairs, in reading order. */
  function briefLines(task, rules) {
    const b = task.brief;
    const lines = [["rules", rules], ["title", b.title]];
    lines.push(["meta", `Description: ${b.description} Status: ${b.status} Calendar date: ${stop(b.calendar_date)}`]);
    lines.push(["heading", b.context_heading]);
    b.context.forEach((t) => lines.push(["para", t]));
    lines.push(["heading", ACTIONS_HEADING]);
    b.actions.forEach((t, i) => lines.push(["item", `${i + 1}. ${t}`]));
    lines.push(["heading", PLAN_HEADING]);
    lines.push(["field", `Output: ${b.plan.output}`]);
    lines.push(["field", "Steps:"]);
    b.plan.steps.forEach((t, i) => lines.push(["item", `${i + 1}. ${t}`]));
    lines.push(["field", `Tools, skills and apps: ${b.plan.tools}`]);
    lines.push(["field", `Rhythm: ${b.plan.rhythm}`]);
    lines.push(["field", `Done when: ${b.plan.done_when}`]);
    // The brief is pasted into a session with nothing else attached, so it carries the entry.
    lines.push(["field", `${ORIGIN_LABEL} ${task.entry.text}`]);
    if (task.entry.notes) lines.push(["field", `${NOTES_LABEL} ${task.entry.notes}`]);
    return lines;
  }

  /** The yellow section as plain text: what is pasted into a Claude Code session. */
  function briefPrompt(task, rules) {
    const out = [];
    for (const [kind, text] of briefLines(task, rules)) {
      if (kind === "title" || kind === "heading") out.push("", text, "");
      else if (kind === "item") out.push(text);
      else out.push(text, "");
    }
    return out.join("\n").replace(/\n{3,}/g, "\n\n").trim() + "\n";
  }

  /** The text for the task's note or description: the new description, then the original. */
  function writebackNote(task) {
    const parts = [task.writeback.description, "Original entry: " + task.entry.text];
    if (task.entry.notes) parts.push("Original notes: " + task.entry.notes);
    return parts.filter(Boolean).join("\n\n");
  }

  /** The instruction sent to Claude to expand one entry into brief JSON. */
  function expandPrompt(spec, entryText, notes, today) {
    const example = { task_type: spec.example.task_type, brief: spec.example.brief, writeback: spec.example.writeback };
    const values = {
      EXAMPLE_ENTRY: spec.example.entry.text, EXAMPLE_JSON: JSON.stringify(example, null, 2),
      TODAY: today, ENTRY: entryText, NOTES: notes || "None",
    };
    // One pass, so an entry that happens to contain "{{NOTES}}" is left exactly as written.
    return spec.expand.replace(/\{\{(EXAMPLE_ENTRY|EXAMPLE_JSON|TODAY|ENTRY|NOTES)\}\}/g, (_, key) => values[key]);
  }

  /** "owner/name" from "owner/name" or a GitHub address; empty when it is neither. */
  function repoName(value) {
    const m = String(value || "").trim().replace(/\.git$/, "").match(/(?:github\.com[/:])?([\w.-]+\/[\w.-]+)\/?$/);
    return m ? m[1] : "";
  }

  /** A link that opens a new Claude Code session with the brief already typed in. */
  function sessionLink(prompt, repo) {
    const name = repoName(repo);
    return "https://claude.ai/code/new?q=" + encodeURIComponent(prompt) + (name ? "&repo=" + encodeURIComponent(name) : "");
  }

  function slug(text) {
    const words = (text.toLowerCase().match(/[a-z0-9]+/g) || []).slice(0, 6).join("-").slice(0, 48).replace(/-+$/, "");
    return words || "task";
  }

  function splitMeta(text) {
    const labels = ["Description:", " Status:", " Calendar date:"];
    const at = labels.map((l) => text.indexOf(l));
    return labels.map((label, i) => [label, text.slice(at[i] + label.length, i + 1 < at.length ? at[i + 1] : text.length)]);
  }

  /** Build the Word document with the docx library. Returns a docx.Document. */
  function buildDocx(docx, task, spec) {
    const { Document, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, HeadingLevel, Footer, PageNumber } = docx;
    const INK = "1F2A37", MUTED = "5B6570", ACCENT = "1F4E79", PANEL = "F3F5F7", RULE = "C5CCD3";
    const run = (text, o = {}) => new TextRun({ text, size: (o.size || 11) * 2, bold: !!o.bold, italics: !!o.italic, color: o.color || INK,
      highlight: o.highlight, highlightComplexScript: false }); // the library's extra highlightCs element is not in the Word schema
    const para = (runs, o = {}) => new Paragraph({
      children: Array.isArray(runs) ? runs : [runs],
      spacing: { before: (o.before || 0) * 20, after: (o.after == null ? 6 : o.after) * 20, line: 268 },
      keepNext: !!o.keepNext, pageBreakBefore: !!o.newPage, indent: o.indent, border: o.border, shading: o.shading,
      heading: o.heading,
    });
    const section = (title, hint, newPage) => {
      const out = [para(run(title, { size: 13, bold: true, color: ACCENT }), { heading: HeadingLevel.HEADING_2, before: 16, after: 2, keepNext: true, newPage })];
      if (hint) out.push(para(run(hint, { size: 9.5, italic: true, color: MUTED }), { keepNext: true }));
      return out;
    };
    const edge = (side) => ({ [side]: { style: BorderStyle.SINGLE, size: 6, space: 2, color: RULE } });
    const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: RULE };
    const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
    const cell = (text, width, o = {}) => new TableCell({
      width: { size: width, type: WidthType.DXA }, borders,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      shading: o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined,
      children: [para(run(text, { size: 10, bold: !!o.bold }), { after: 2 })],
    });
    const table = (widths, rows) => new Table({
      width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
      rows: rows.map((cells) => new TableRow({ children: cells.map((c, i) => cell(c.text, widths[i], c)) })),
    });
    const keyValue = (rows) => table([2040, 7598], rows.map(([k, v]) => [{ text: k, bold: true, fill: PANEL }, { text: v }]));

    const Y = "yellow", G = "green"; // Word shows "green" as Bright Green
    const kids = [];
    kids.push(para(run("ToDo Task Brief", { size: 22, bold: true, color: ACCENT }), { after: 2 }));
    kids.push(para(run("One document for one To Do entry.  To Do → Word → Claude", { size: 10.5, color: MUTED }), { after: 10 }));

    kids.push(...section("1 · Original To Do entry", "Type or paste the entry exactly as you captured it. It is never tidied up here."));
    kids.push(para(run(task.entry.text, { size: 12 }), {
      after: 4, indent: { left: 200 }, shading: { type: ShadingType.CLEAR, color: "auto", fill: PANEL },
      border: { left: { style: BorderStyle.SINGLE, size: 18, space: 8, color: ACCENT } },
    }));
    kids.push(para([run("More from the task’s notes (optional): ", { bold: true }), run(task.entry.notes || "None")]));

    kids.push(...section("2 · Expansion prompt (green)", "Copy all of the green text into the Claude panel in Word and send it."));
    spec.green.forEach((t) => kids.push(para(run(t, { size: 10.5, highlight: G }), { after: 5 })));

    kids.push(...section("3 · Task brief (yellow)", "Claude rewrites this section. When it reads correctly, copy all of the yellow text into a new Claude Code session.", true));
    kids.push(para(run("▼ TASK BRIEF STARTS", { size: 8.5, bold: true, color: MUTED }), { before: 2, after: 4, keepNext: true, border: edge("bottom") }));
    for (const [kind, text] of briefLines(task, spec.rules)) {
      if (kind === "rules") {
        const cut = text.indexOf(":") + 1;
        kids.push(para([run(text.slice(0, cut), { size: 10, bold: true, highlight: Y }), run(text.slice(cut), { size: 10, highlight: Y })], { after: 8 }));
      } else if (kind === "title") kids.push(para(run(text, { size: 14, bold: true, highlight: Y }), { before: 4, keepNext: true }));
      else if (kind === "meta") kids.push(para(splitMeta(text).flatMap(([l, v]) => [run(l, { bold: true, highlight: Y }), run(v, { highlight: Y })]), { after: 8 }));
      else if (kind === "heading") kids.push(para(run(text, { size: 12, bold: true, highlight: Y }), { before: 6, after: 4, keepNext: true }));
      else if (kind === "item") kids.push(para(run(text, { highlight: Y }), { after: 3, indent: { left: 340, hanging: 340 } }));
      else if (kind === "field") {
        const cut = text.indexOf(":") + 1;
        kids.push(para([run(text.slice(0, cut), { bold: true, highlight: Y }), run(text.slice(cut), { highlight: Y })], { after: 4 }));
      } else kids.push(para(run(text, { highlight: Y })));
    }
    kids.push(para(run("▲ TASK BRIEF ENDS", { size: 8.5, bold: true, color: MUTED }), { before: 2, after: 4, border: edge("top") }));

    kids.push(...section("4 · To Do write-back", "Paste these into the task in Microsoft To Do or Todoist. Keep the original entry underneath."));
    kids.push(keyValue([["Title", task.writeback.title], ["Description", task.writeback.description], ["Original entry", task.entry.text]]));

    kids.push(...section("5 · Progress log", "Add one row for every update. An update without evidence is not finished."));
    const logWidths = [1247, 2268, 1814, 2041, 2268];
    kids.push(table(logWidths, [
      ["Date", "Completed", "Waiting on", "Next action", "Completion evidence"].map((t) => ({ text: t, bold: true, fill: PANEL })),
      ...[0, 1, 2].map(() => logWidths.map(() => ({ text: "" }))),
    ]));
    kids.push(para(run("Decisions and lessons: ", { bold: true }), { before: 8 }));

    kids.push(...section("Task record", "Where this task lives, so the three places stay linked."));
    kids.push(keyValue([
      ["Captured on", task.entry.captured_on], ["Source", task.entry.source], ["List or project", task.entry.list],
      ["Task link or ID", task.entry.task_id], ["Claude session link", task.session_url || ""], ["Stage", task.stage || "Briefed"],
    ]));

    kids.push(...section("How this document works", ""));
    spec.how.forEach((t, i) => kids.push(para(run(`${i + 1}. ${t}`, { size: 10.5 }), { after: 3 })));

    return new Document({
      creator: "ToDo Task", title: task.brief.title, description: "One document for one To Do entry.",
      styles: {
        default: {
          document: { run: { font: "Calibri", size: 22 } },
          heading2: { run: { font: "Calibri", size: 26, bold: true, color: ACCENT }, paragraph: { spacing: { before: 320, after: 40 }, keepNext: true } },
        },
      },
      sections: [{
        properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1020, bottom: 1020, left: 1134, right: 1134 } } },
        footers: { default: new Footer({ children: [new Paragraph({ children: [
          new TextRun({ text: "ToDo Task  ·  To Do → Word → Claude  ·  page ", size: 17, color: MUTED }),
          new TextRun({ children: [PageNumber.CURRENT], size: 17, color: MUTED }),
        ] })] }) },
        children: kids,
      }],
    });
  }

  /** Remove folder entries from a ZIP. The docx library writes them, and Word has refused
      files that carry them when a document is opened through OneDrive or SharePoint. */
  function stripZipFolders(input) {
    const src = input instanceof Uint8Array ? input : new Uint8Array(input);
    const view = new DataView(src.buffer, src.byteOffset, src.byteLength);
    let eocd = -1;
    for (let i = src.length - 22; i >= Math.max(0, src.length - 65557); i--) {
      if (view.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
    }
    if (eocd < 0) return src;
    const total = view.getUint16(eocd + 10, true);
    const cdOffset = view.getUint32(eocd + 16, true);
    if (total === 0xffff || cdOffset === 0xffffffff) return src; // ZIP64: leave untouched
    const entries = [];
    let p = cdOffset;
    for (let n = 0; n < total; n++) {
      if (p + 46 > src.length || view.getUint32(p, true) !== 0x02014b50) return src;
      const nameLen = view.getUint16(p + 28, true);
      const size = 46 + nameLen + view.getUint16(p + 30, true) + view.getUint16(p + 32, true);
      entries.push({ cdStart: p, cdSize: size, offset: view.getUint32(p + 42, true), folder: nameLen > 0 && src[p + 46 + nameLen - 1] === 0x2f });
      p += size;
    }
    if (!entries.some((e) => e.folder)) return src;
    const byOffset = [...entries].sort((a, b) => a.offset - b.offset);
    byOffset.forEach((e, i) => { e.end = i + 1 < byOffset.length ? byOffset[i + 1].offset : cdOffset; });
    const keep = entries.filter((e) => !e.folder);
    const tail = 22 + view.getUint16(eocd + 20, true);
    const cdSize = keep.reduce((sum, e) => sum + e.cdSize, 0);
    const out = new Uint8Array(keep.reduce((sum, e) => sum + e.end - e.offset, 0) + cdSize + tail);
    const outView = new DataView(out.buffer);
    let at = 0;
    for (const e of keep) { out.set(src.subarray(e.offset, e.end), at); e.moved = at; at += e.end - e.offset; }
    const cdStart = at;
    for (const e of keep) { out.set(src.subarray(e.cdStart, e.cdStart + e.cdSize), at); outView.setUint32(at + 42, e.moved, true); at += e.cdSize; }
    out.set(src.subarray(eocd, eocd + tail), at);
    outView.setUint16(at + 8, keep.length, true);
    outView.setUint16(at + 10, keep.length, true);
    outView.setUint32(at + 12, cdSize, true);
    outView.setUint32(at + 16, cdStart, true);
    return out;
  }

  return { STAGES, TASK_TYPES, LIMITS, ACTIONS_HEADING, PLAN_HEADING, normalise, problems, briefLines, briefPrompt, writebackNote, expandPrompt, slug, repoName, sessionLink, buildDocx, stripZipFolders };
})();

if (typeof module !== "undefined") module.exports = Core;
