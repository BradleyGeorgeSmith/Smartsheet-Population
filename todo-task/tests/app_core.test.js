// Checks for the page's brief logic. Run with: node --test tests/
const test = require("node:test");
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const Core = require("../app/src/core.js");
const root = path.join(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");
const example = JSON.parse(read("spec/examples/tomato-timelapse.json"));
const rules = read("spec/working-rules.txt").trim();
const spec = {
  rules,
  green: read("spec/expansion-prompt.txt").split("\n\n").map((s) => s.trim()).filter(Boolean),
  expand: read("spec/expand-json-prompt.txt").trim(),
  example,
  how: ["Make a copy.", "Paste the entry."],
};

test("the example brief is sound", () => {
  assert.deepStrictEqual(Core.problems(Core.normalise(example)), []);
});

test("normalise survives junk and strips numbering a model added", () => {
  const t = Core.normalise({ brief: { actions: ["1. Next action: do it", "2) then this"], context: "one paragraph", plan: { steps: "single" } } }, { text: "x" });
  assert.deepStrictEqual(t.brief.actions, ["Next action: do it", "then this"]);
  assert.deepStrictEqual(t.brief.context, ["one paragraph"]);
  assert.deepStrictEqual(t.brief.plan.steps, ["single"]);
  assert.strictEqual(t.brief.calendar_date, "Not supplied");
  assert.strictEqual(Core.normalise(null, { text: "x" }).task_type, "idea");
});

test("problems catches the structure rules", () => {
  const t = Core.normalise(example);
  t.brief.actions[0] = "Choose the plant.";
  t.writeback.title = "x".repeat(91);
  const found = Core.problems(t).join(" ");
  assert.match(found, /Next action:/);
  assert.match(found, /write-back title is 91/);
});

test("the page and the Python package produce the same prompt and note", () => {
  const t = Core.normalise(example);
  const py = (code) => execFileSync("python3", ["-c", code], { cwd: root, encoding: "utf8" });
  const load = "from todotask.models import model_example; from todotask import render; import sys; t = model_example();";
  assert.strictEqual(Core.briefPrompt(t, rules), py(load + "sys.stdout.write(render.brief_prompt(t))"));
  assert.strictEqual(Core.writebackNote(t), py(load + "sys.stdout.write(render.writeback_note(t))"));
});

test("the request sent to Claude carries the entry, the notes and the example", () => {
  const prompt = Core.expandPrompt(spec, "buy $& shoes", "", "2026-11-19");
  assert.ok(prompt.includes("Entry: <<<buy $& shoes>>>"));
  assert.ok(prompt.includes("Notes already on the task: <<<None>>>"));
  assert.ok(prompt.includes(example.brief.title));
  assert.ok(!prompt.includes("{{"));
  const tricky = Core.expandPrompt(spec, "what is {{NOTES}}?", "real notes", "2026-11-19");
  assert.ok(tricky.includes("Entry: <<<what is {{NOTES}}?>>>") && tricky.includes("task: <<<real notes>>>"));
});

test("the session link carries the brief and the repository", () => {
  assert.strictEqual(Core.repoName("https://github.com/Owner/My-Repo.git"), "Owner/My-Repo");
  assert.strictEqual(Core.repoName("owner/name"), "owner/name");
  assert.strictEqual(Core.repoName("not a repo"), "");
  const link = Core.sessionLink("Working rules: a & b?\nline", "owner/name");
  assert.ok(link.startsWith("https://claude.ai/code/new?q=Working%20rules%3A%20a%20%26%20b%3F%0Aline"));
  assert.ok(link.endsWith("&repo=owner%2Fname"));
  assert.ok(!Core.sessionLink("x", "").includes("repo="));
});

test("slug", () => {
  assert.strictEqual(Core.slug("Buy shoes for Honor"), "buy-shoes-for-honor");
  assert.strictEqual(Core.slug("???"), "task");
});

test("the Word document builds with yellow and green highlights and both markers", async () => {
  const docx = require("docx");
  const t = Object.assign(Core.normalise(example), { stage: "Briefed", session_url: "" });
  const packed = await docx.Packer.toBuffer(Core.buildDocx(docx, t, spec));
  const buffer = Buffer.from(Core.stripZipFolders(new Uint8Array(packed)));
  assert.ok(buffer.length < packed.length, "folder entries were removed");
  const out = path.join(process.env.TODOTASK_TEST_OUT || require("node:os").tmpdir(), "app-core-test.docx");
  fs.writeFileSync(out, buffer);
  const xml = execFileSync("python3", ["-c", "import zipfile,sys; sys.stdout.write(zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode())", out], { encoding: "utf8", maxBuffer: 1 << 26 });
  assert.ok(xml.includes('w:highlight w:val="yellow"'));
  assert.ok(xml.includes('w:highlight w:val="green"'));
  assert.ok(xml.includes("TASK BRIEF STARTS") && xml.includes("TASK BRIEF ENDS"));
  assert.ok(xml.includes("Working rules for Claude:"));
  const names = execFileSync("python3", ["-c", "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); assert z.testzip() is None; print('\\n'.join(z.namelist()))", out], { encoding: "utf8" });
  assert.ok(!names.split("\n").some((n) => n.endsWith("/")), "no folder entries remain");
  assert.ok(names.includes("word/document.xml") && names.includes("[Content_Types].xml"));
});

test("stripZipFolders leaves anything that is not a ZIP with folders alone", () => {
  const junk = new Uint8Array([1, 2, 3, 4]);
  assert.strictEqual(Core.stripZipFolders(junk), junk);
});
