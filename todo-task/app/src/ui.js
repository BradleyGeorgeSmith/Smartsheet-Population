/* ToDo Task Builder: the page. SPEC and Core are defined above this script by the build. */

(() => {
  const $ = (id) => document.getElementById(id);
  const el = (tag, props = {}, ...kids) => {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props)) {
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else if (key.startsWith("data-")) node.setAttribute(key, value);
      else node[key] = value;
    }
    node.append(...kids);
    return node;
  };
  const pad = (n) => String(n).padStart(2, "0");
  const today = () => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };
  const clone = (value) => JSON.parse(JSON.stringify(value));
  const store = {
    get(key, fallback) { try { const v = localStorage.getItem(key); return v == null ? fallback : JSON.parse(v); } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* storage can be blocked; the page works without it */ } },
  };

  const caps = { sample: null, db: null, mcp: null, downloads: null };
  let task = exampleTask();
  let saved = [];
  let draftMeta = null;        // where a pulled entry came from, until it is expanded
  let stopper = null;
  let storeOnDevice = false;   // true when the shared store cannot be used in this view
  let firstList = true;
  let touched = false;
  let pendingTodoist = null;
  let writeChain = Promise.resolve();

  function exampleTask() {
    return Object.assign(Core.normalise(SPEC.example), { id: null, example: true, stage: "Briefed", session_url: "", created_at: "" });
  }

  function say(id, text, kind) {
    const node = $(id);
    node.textContent = text || "";
    node.className = "note" + (kind ? " " + kind : "");
  }

  // ------------------------------------------------------------------ render

  function renderRail() {
    const at = Core.STAGES.indexOf(task.stage);
    $("rail").replaceChildren(...Core.STAGES.map((name, i) =>
      el("li", { text: name, class: i === at ? "now" : i < at ? "past" : "" })));
    const select = $("stage");
    if (!select.options.length) Core.STAGES.forEach((name) => select.append(el("option", { value: name, text: name })));
    select.value = task.stage;
    select.disabled = task.example;
  }

  function marked(text, labels) {
    // Bold the labels inside one highlighted run, e.g. "Description:", "Status:".
    const mark = el("mark");
    let rest = text;
    for (const label of labels) {
      const at = rest.indexOf(label);
      if (at < 0) continue;
      if (at > 0) mark.append(rest.slice(0, at));
      mark.append(el("strong", { text: label }));
      rest = rest.slice(at + label.length);
    }
    mark.append(rest);
    return mark;
  }

  function renderBrief() {
    $("brief-entry").textContent = task.entry.text;
    $("brief-hint").replaceChildren(...(task.example
      ? [el("span", { class: "tag", text: "Example" }), " This brief was written from the entry below. Yours will take its place."]
      : ["Read it through. Fix anything marked (to confirm), then use it."]));
    const view = $("brief-view");
    view.replaceChildren();
    for (const [kind, text] of Core.briefLines(task, SPEC.rules)) {
      const labels = kind === "meta" ? ["Description:", "Status:", "Calendar date:"]
        : kind === "field" || kind === "rules" ? [text.slice(0, text.indexOf(":") + 1)] : [];
      view.append(el("p", { class: kind }, marked(text, labels)));
    }
    const found = task.example ? [] : Core.problems(task);
    $("checks").hidden = !found.length;
    $("checks").replaceChildren(...found.map((text) => el("li", { text })));
    $("edit").hidden = $("again").hidden = task.example;
    $("word").hidden = !caps.downloads;
  }

  function count(id, length, limit) {
    const node = $(id);
    node.textContent = `${length} of ${limit} characters`;
    node.className = "count" + (length > limit ? " over" : "");
  }

  function renderWriteback() {
    if (document.activeElement !== $("w-title")) $("w-title").value = task.writeback.title;
    if (document.activeElement !== $("w-description")) $("w-description").value = task.writeback.description;
    count("w-title-count", task.writeback.title.length, Core.LIMITS.writebackTitle);
    count("w-description-count", task.writeback.description.length, Core.LIMITS.writebackDescription);
    $("w-title").disabled = $("w-description").disabled = task.example;
    const button = $("todoist-write");
    button.hidden = !caps.mcp || task.example;
    button.textContent = fromTodoist() ? "Update the task in Todoist" : "Add this task to Todoist";
  }

  function renderSession() {
    $("start").hidden = !caps.mcp || task.example || caps.noSessions === true;
    $("open-code").href = Core.sessionLink(briefText(), $("s-repo").value);
    if (task.session_url) {
      $("session-note").replaceChildren("A session was started for this task. ",
        el("a", { href: task.session_url, target: "_blank", rel: "noopener", text: "Open it in Claude Code" }), ".");
      $("session-note").className = "note good";
    } else if (!$("session-note").dataset.sticky) say("session-note", "");
  }

  function renderTasks() {
    const listNode = $("tasks-list");
    $("tasks-empty").hidden = saved.length > 0;
    listNode.hidden = saved.length === 0;
    $("tasks-hint").textContent = storeOnDevice
      ? "Briefs are saved on this device only."
      : "Briefs are saved here so nothing is left as a one-line entry.";
    listNode.replaceChildren(...saved.map((row) => {
      const open = el("button", { class: "btn", type: "button", text: row.id === task.id ? "Open now" : "Open" });
      open.disabled = row.id === task.id;
      open.addEventListener("click", () => openSaved(row));
      const remove = el("button", { class: "btn quiet", type: "button", text: "Remove" });
      remove.addEventListener("click", () => {
        if (remove.dataset.armed) return removeSaved(row);
        remove.dataset.armed = "1";
        remove.textContent = "Confirm remove";
      });
      const when = (row.updated_at || "").slice(0, 10);
      return el("li", {},
        el("span", { class: "name", text: (row.brief && row.brief.title) || row.title || "Untitled" }),
        el("span", { class: "meta" }, el("span", { class: "chip", "data-stage": row.stage || "Briefed", text: row.stage || "Briefed" }),
          ` ${when}${row.entry && row.entry.source ? " · " + row.entry.source : ""}`),
        el("span", { class: "act" }, open, remove));
    }));
  }

  function renderAll() { renderRail(); renderBrief(); renderWriteback(); renderSession(); renderTasks(); }

  // ----------------------------------------------------------------- storage

  function body(t) {
    const now = new Date().toISOString();
    t.created_at = t.created_at || now;
    return { title: t.brief.title, entry: t.entry, task_type: t.task_type, brief: t.brief, writeback: t.writeback,
      stage: t.stage, session_url: t.session_url || "", created_at: t.created_at, updated_at: now };
  }

  function persist() {
    if (task.example) return Promise.resolve();
    const data = clone(body(task));
    if (caps.db && !storeOnDevice) {
      const briefs = caps.db.collection("briefs");
      const ref = task.id ? briefs.doc(task.id) : briefs.doc();
      task.id = ref.id;
      // One write at a time per document: each save waits for the one before it.
      writeChain = writeChain.then(() => ref.set(data)).catch((error) => {
        if (error && (error.code === "invalid_argument" || error.code === "revoked" || error.code === "not_granted")) {
          storeOnDevice = true;
          saveOnDevice(data);
        } else say("brief-note", "This brief could not be saved just now. It is still on screen; try again shortly.", "warn");
      });
      return writeChain;
    }
    saveOnDevice(data);
    return Promise.resolve();
  }

  function saveOnDevice(data) {
    task.id = task.id || "local-" + Date.now().toString(36);
    const rows = store.get("todo-task-briefs", []).filter((row) => row.id !== task.id);
    rows.unshift(Object.assign({ id: task.id }, data));
    store.set("todo-task-briefs", rows.slice(0, 200));
    saved = rows;
    renderTasks();
  }

  function subscribe() {
    const slow = setTimeout(() => { $("tasks-hint").textContent = "Your saved briefs cannot be reached yet. They will appear when the connection returns."; }, 10000);
    caps.db.collection("briefs").orderBy("updated_at", "desc").limit(200).onSnapshot((snap) => {
      if (!snap.metadata.fromCache) clearTimeout(slow);
      saved = snap.docs.map((doc) => Object.assign({ id: doc.id }, clone(doc.data())));
      if (firstList && saved.length && task.example && !touched) openSaved(saved[0], true);
      firstList = false;
      renderTasks();
    }, () => {
      clearTimeout(slow);
      storeOnDevice = true;
      saved = store.get("todo-task-briefs", []);
      renderTasks();
    });
  }

  function openSaved(row, quiet) {
    task = Object.assign(Core.normalise(clone(row)), {
      id: row.id, example: false, stage: row.stage || "Briefed", session_url: row.session_url || "", created_at: row.created_at || "",
    });
    $("entry").value = task.entry.text;
    $("notes").value = task.entry.notes;
    $("edit-form").hidden = true;
    renderAll();
    if (!quiet) $("brief").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function removeSaved(row) {
    if (caps.db && !storeOnDevice) caps.db.collection("briefs").doc(row.id).delete().catch(() => {});
    else { saved = saved.filter((r) => r.id !== row.id); store.set("todo-task-briefs", saved); }
    if (row.id === task.id) { task = exampleTask(); $("entry").value = ""; $("notes").value = ""; }
    saved = saved.filter((r) => r.id !== row.id);
    renderAll();
  }

  // ------------------------------------------------------------------ expand

  const SAMPLE_COPY = {
    cancelled: "Stopped.",
    rate_limited: "Claude is busy, or your usage limit has been reached. Try again later.",
    session_expired: "Sign in to Claude again, then press Expand.",
    refused: "Claude declined this entry as written. Reword it and try again.",
    invalid_json: "The reply could not be read as a brief. Press Expand to try again.",
    empty_completion: "Claude returned nothing for this entry. Add a few more words and try again.",
    prompt_too_large: "That entry is too long. Shorten it and try again.",
    upstream_error: "Something interrupted the reply. Press Expand to try again.",
  };
  const SAMPLE_OFF = ["not_granted", "sampling_disabled", "not_declared", "capability_disabled", "capability_removed"];

  function busy(on) {
    $("expand").disabled = $("again").disabled = on;
    $("stop").hidden = !on;
  }

  function adopt(raw, text, notes) {
    const meta = draftMeta || {};
    const entry = { text, notes, source: meta.source || "Manual", list: meta.list || "", task_id: meta.task_id || "",
      captured_on: meta.captured_on || today(), labels: meta.labels || [] };
    task = Object.assign(Core.normalise(raw, entry), { id: null, example: false, stage: "Briefed", session_url: "", created_at: "" });
    draftMeta = null;
    $("edit-form").hidden = true;
    persist();
    renderAll();
    $("brief").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function expand(fresh) {
    const text = $("entry").value.trim();
    const notes = $("notes").value.trim();
    if (!text) { say("capture-note", "Type or paste an entry first.", "warn"); $("entry").focus(); return; }
    if (!caps.sample) { $("manual").hidden = false; say("capture-note", ""); return; }
    stopper = new AbortController();
    busy(true);
    say("capture-note", "Thinking…");
    try {
      const captured = (draftMeta && draftMeta.captured_on) || today();
      const raw = await caps.sample.json(Core.expandPrompt(SPEC, text, notes, captured), {
        modelTier: "complex", model: SPEC.model, signal: stopper.signal, cache: !fresh,
        onText: ({ text: soFar }) => say("capture-note", `Writing the brief… ${soFar.length} characters so far`),
      });
      adopt(raw, text, notes);
      say("capture-note", "Brief written. It is saved under Your tasks.", "good");
    } catch (error) {
      const code = error && error.code;
      if (SAMPLE_OFF.includes(code)) { caps.sample = null; $("manual").hidden = false; say("capture-note", "Claude is not allowed for this page in this view."); }
      else say("capture-note", SAMPLE_COPY[code] || SAMPLE_COPY.upstream_error, code === "cancelled" ? "" : "bad");
    } finally {
      busy(false);
      stopper = null;
    }
  }

  function useManualReply() {
    const text = $("entry").value.trim();
    const reply = $("manual-reply").value;
    const first = reply.indexOf("{"), last = reply.lastIndexOf("}");
    if (!text) { say("capture-note", "Type or paste an entry first.", "warn"); return; }
    try {
      adopt(JSON.parse(reply.slice(first, last + 1)), text, $("notes").value.trim());
      $("manual-reply").value = "";
      say("capture-note", "Brief built from the reply.", "good");
    } catch {
      say("capture-note", "That reply does not hold a brief. Paste the whole reply, from the first { to the last }.", "bad");
    }
  }

  // -------------------------------------------------------------------- copy

  async function copy(text, noteId, label) {
    try {
      await navigator.clipboard.writeText(text);
      $("copy-fallback").hidden = true;
      say(noteId, `${label} copied.`, "good");
    } catch {
      const box = $("copy-fallback");
      box.hidden = false;
      box.value = text;
      box.focus();
      box.select();
      say(noteId, "Copying is blocked in this view. The text is selected at the bottom of the page; copy it from there.", "warn");
    }
  }
  const briefText = () => Core.briefPrompt(task, SPEC.rules);

  // -------------------------------------------------------------------- Word

  let docxLoading = null;
  function loadDocx() {
    if (window.docx) return Promise.resolve(window.docx);
    docxLoading = docxLoading || new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/docx@9.7.1/dist/index.iife.js";
      script.onload = () => (window.docx ? resolve(window.docx) : reject(new Error("docx missing")));
      script.onerror = () => { docxLoading = null; reject(new Error("docx blocked")); };
      document.head.append(script);
    });
    return docxLoading;
  }

  async function saveWord() {
    if (!caps.downloads) return;
    $("word").disabled = true;
    say("brief-note", "Building the Word document…");
    try {
      const docx = await loadDocx();
      const packed = await docx.Packer.toBlob(Core.buildDocx(docx, task, SPEC));
      const blob = new Blob([Core.stripZipFolders(await packed.arrayBuffer())],
        { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
      const name = `${task.entry.captured_on || today()}-${Core.slug(task.writeback.title || task.brief.title)}.docx`;
      await caps.downloads.save({ filename: name, data: blob });
      say("brief-note", "Word document saved. Open it in Word to refine it with the green prompt.", "good");
    } catch (error) {
      const code = error && error.code;
      if (code === "declined") say("brief-note", "Not saved.");
      else if (code === "rate_limited") say("brief-note", "Another save is still open. Finish that one, then try again.", "warn");
      else if (code) { caps.downloads = null; $("word").hidden = true; say("brief-note", "Saving files is not available in this view. Copy the brief instead.", "warn"); }
      else say("brief-note", "The Word document could not be built here. Copy the brief instead.", "bad");
    } finally {
      $("word").disabled = false;
    }
  }

  // ----------------------------------------------------------------- Todoist

  const TODOIST = "Todoist";
  const CODE = "Claude Code Remote";
  const fromTodoist = () => task.entry.source === TODOIST && !!task.entry.task_id;
  const payloadOf = (result) => {
    const p = result && result.payload;
    if (typeof p === "string") { try { return JSON.parse(p); } catch { return {}; } }
    return p && typeof p === "object" ? p : {};
  };

  function mcpCopy(error, server, wasWrite) {
    const code = error && error.code;
    if (code === "needs_reauth") return `Reconnect ${server} in Claude: Settings, then Connectors.`;
    if (code === "server_not_connected" || code === "selection_required" || code === "server_not_found") return `Add ${server} in Claude: Settings, then Connectors.`;
    if (["not_in_manifest", "blocked_by_policy", "approval_required", "not_granted", "consent_required"].includes(code)) return `${server} is not allowed for this page. Allow it when Claude asks, then try again.`;
    if (code === "tool_error") return `${server} answered with an error: ${String(error.message || "").slice(0, 200)}`;
    if (code === "cancelled") return "Stopped.";
    return wasWrite
      ? `${server} did not confirm the change. Check ${server} before you try again, because it may have gone through.`
      : `${server} could not be reached just now. Try again in a moment.`;
  }

  async function pull() {
    $("pull").disabled = true;
    say("capture-note", "Asking Todoist…");
    try {
      // Labels are checked here, not in the filter: Todoist is changing how filters write them.
      const skip = ["briefed", "skip-ai", "from-email"];
      const result = await caps.mcp.callTool(TODOIST, "find-tasks", { filter: "created after: -14 days & !recurring", limit: 100 });
      const rows = (payloadOf(result).tasks || [])
        .filter((t) => t && t.id && t.content && !(t.labels || []).some((label) => skip.includes(label)))
        .sort((a, b) => String(b.addedAt || "").localeCompare(String(a.addedAt || "")));
      $("picker").hidden = false;
      $("picker-list").replaceChildren(...rows.map((t) => {
        const use = el("button", { class: "btn", type: "button", text: "Use this" });
        use.addEventListener("click", () => {
          touched = true;
          $("entry").value = t.content;
          $("notes").value = t.description || "";
          $("notes-box").open = !!t.description;
          draftMeta = { source: TODOIST, task_id: String(t.id), list: String(t.projectId || ""), labels: Array.isArray(t.labels) ? t.labels : [],
            captured_on: String(t.addedAt || "").slice(0, 10) || today() };
          $("picker").hidden = true;
          say("capture-note", "Loaded from Todoist. Press Expand into a brief.", "good");
          $("entry").focus();
        });
        return el("li", {}, el("span", { class: "name", text: t.content }),
          el("span", { class: "meta", text: `${String(t.addedAt || "").slice(0, 10)}${t.description ? " · has notes" : ""}` }),
          el("span", { class: "act" }, use));
      }));
      say("capture-note", rows.length ? "" : "No new Todoist tasks without a brief in the last 14 days.");
    } catch (error) {
      say("capture-note", mcpCopy(error, TODOIST), "bad");
    } finally {
      $("pull").disabled = false;
    }
  }

  function askTodoist() {
    const found = Core.problems(task).filter((p) => p.includes("write-back"));
    if (found.length) { say("writeback-note", found[0], "warn"); return; }
    pendingTodoist = fromTodoist() ? "update" : "add";
    $("todoist-confirm-text").textContent = pendingTodoist === "update"
      ? "This replaces the task’s title and description in Todoist and adds the label “briefed”. Your original entry is kept underneath the new description."
      : "This adds a new task to your Todoist Inbox with this title and description and the label “briefed”.";
    $("todoist-confirm").hidden = false;
  }

  async function writeTodoist() {
    const mode = pendingTodoist;
    pendingTodoist = null;
    $("todoist-confirm").hidden = true;
    if (!mode) return;
    $("todoist-write").disabled = true;
    say("writeback-note", "Writing to Todoist…");
    const note = Core.writebackNote(task);
    try {
      if (mode === "update") {
        const labels = [...new Set([...(task.entry.labels || []), "briefed"])];
        await caps.mcp.callTool(TODOIST, "update-tasks", { tasks: [{ id: task.entry.task_id, content: task.writeback.title, description: note, labels }] });
        task.entry.labels = labels;
      } else {
        const result = await caps.mcp.callTool(TODOIST, "add-tasks", { tasks: [{ content: task.writeback.title, description: note, labels: ["briefed"] }] });
        const made = (payloadOf(result).tasks || [])[0];
        if (made && made.id) { task.entry.source = TODOIST; task.entry.task_id = String(made.id); task.entry.labels = ["briefed"]; }
      }
      if (Core.STAGES.indexOf(task.stage) < 1) task.stage = "Briefed";
      persist();
      renderAll();
      say("writeback-note", mode === "update" ? "The task in Todoist now has the new title and description." : "Added to your Todoist Inbox.", "good");
    } catch (error) {
      say("writeback-note", mcpCopy(error, TODOIST, true), "bad");
    } finally {
      $("todoist-write").disabled = false;
    }
  }

  // ----------------------------------------------------------------- session

  async function loadEnvironments() {
    const result = await caps.mcp.callTool(CODE, "list_environments", { limit: 20 });
    const rows = (payloadOf(result).environments || []).filter((e) => e && e.environment_id && e.state !== "archived");
    const select = $("s-env");
    const keep = select.value || store.get("todo-task-env", "");
    select.replaceChildren(el("option", { value: "", text: "Choose where the session runs" }),
      ...rows.map((e) => el("option", { value: e.environment_id, text: `${e.name}${e.kind === "bridge" ? " (your computer)" : " (cloud)"}` })));
    if (rows.some((e) => e.environment_id === keep)) select.value = keep;
    return rows.length;
  }

  function sessionsOff(message) {
    caps.noSessions = true;
    renderSession();
    $("session-note").dataset.sticky = "1";
    say("session-note", message, "warn");
  }

  async function startSession() {
    const found = Core.problems(task);
    if (found.length) { say("session-note", "Fix the brief first: " + found[0], "warn"); return; }
    $("start").disabled = true;
    delete $("session-note").dataset.sticky;
    try {
      if (!$("s-env").value) {
        say("session-note", "Asking Claude Code where sessions can run…");
        await loadEnvironments();
        if (!$("s-env").value) {
          $("session-settings").open = true;
          $("session-note").dataset.sticky = "1";
          say("session-note", "Choose an environment under Session settings, then press Start again.", "warn");
          return;
        }
      }
      say("session-note", "Starting the session…");
      const input = { prompt: briefText(), title: task.brief.title.slice(0, 200), tags: ["todo-task"], environment_id: $("s-env").value };
      const repo = Core.repoName($("s-repo").value);
      const model = $("s-model").value.trim();
      if (repo) input.source_url = "https://github.com/" + repo;
      if (model) input.model = model;
      const result = await caps.mcp.callTool(CODE, "create_session", input);
      const id = (JSON.stringify(payloadOf(result)).match(/session_[A-Za-z0-9]+/) || [])[0];
      task.session_url = id ? "https://claude.ai/code/" + id : "https://claude.ai/code";
      task.stage = "In session";
      persist();
      renderAll();
    } catch (error) {
      const code = error && error.code;
      if (["not_in_manifest", "blocked_by_policy", "server_not_connected", "selection_required", "server_not_found", "not_granted", "capability_disabled", "capability_removed"].includes(code)) {
        sessionsOff("Starting a session from this page is not available here. Copy the brief, open Claude Code, and paste it into a new session.");
      } else {
        $("session-note").dataset.sticky = "1";
        say("session-note", code === "tool_error" || code === "needs_reauth" || code === "approval_required" || code === "consent_required"
          ? mcpCopy(error, CODE)
          : "Claude Code did not confirm the session. Check Claude Code before you try again, because it may have started.", "bad");
      }
    } finally {
      $("start").disabled = false;
    }
  }

  // -------------------------------------------------------------------- edit

  const FIELDS = { "f-title": "title", "f-description": "description", "f-status": "status", "f-date": "calendar_date", "f-heading": "context_heading" };
  const PLAN = { "f-output": "output", "f-tools": "tools", "f-rhythm": "rhythm", "f-done": "done_when" };

  function openEdit() {
    for (const [id, key] of Object.entries(FIELDS)) $(id).value = task.brief[key];
    for (const [id, key] of Object.entries(PLAN)) $(id).value = task.brief.plan[key];
    $("f-context").value = task.brief.context.join("\n\n");
    $("f-actions").value = task.brief.actions.join("\n");
    $("f-steps").value = task.brief.plan.steps.join("\n");
    $("edit-form").hidden = false;
    $("f-title").focus();
  }

  function saveEdit(event) {
    event.preventDefault();
    const lines = (id, gap) => $(id).value.split(gap).map((s) => s.trim()).filter(Boolean);
    const brief = {};
    for (const [id, key] of Object.entries(FIELDS)) brief[key] = $(id).value;
    brief.context = lines("f-context", /\n\s*\n/);
    brief.actions = lines("f-actions", "\n");
    brief.plan = { steps: lines("f-steps", "\n") };
    for (const [id, key] of Object.entries(PLAN)) brief.plan[key] = $(id).value;
    const next = Core.normalise({ task_type: task.task_type, brief, writeback: task.writeback }, task.entry);
    Object.assign(task, { brief: next.brief });
    $("edit-form").hidden = true;
    persist();
    renderAll();
    say("brief-note", "Changes saved.", "good");
  }

  // -------------------------------------------------------------------- wire

  $("expand").addEventListener("click", () => { touched = true; expand(false); });
  $("again").addEventListener("click", () => {
    $("entry").value = task.entry.text;
    $("notes").value = task.entry.notes;
    draftMeta = { source: task.entry.source, task_id: task.entry.task_id, list: task.entry.list, labels: task.entry.labels, captured_on: task.entry.captured_on };
    $("capture").scrollIntoView({ behavior: "smooth", block: "start" });
    expand(true);
  });
  $("stop").addEventListener("click", () => stopper && stopper.abort());
  $("pull").addEventListener("click", pull);
  $("fresh").addEventListener("click", () => {
    touched = true;
    task = exampleTask();
    draftMeta = null;
    $("entry").value = $("notes").value = "";
    $("edit-form").hidden = true;
    say("capture-note", "");
    renderAll();
    $("entry").focus();
  });
  $("entry").addEventListener("input", () => { touched = true; });
  $("copy-request").addEventListener("click", () => {
    const text = $("entry").value.trim();
    if (!text) { say("capture-note", "Type or paste an entry first.", "warn"); return; }
    copy(Core.expandPrompt(SPEC, text, $("notes").value.trim(), today()), "capture-note", "Request");
  });
  $("manual-use").addEventListener("click", useManualReply);

  $("copy-brief").addEventListener("click", () => copy(briefText(), "brief-note", "Brief"));
  $("copy-brief-2").addEventListener("click", () => copy(briefText(), "session-note", "Brief"));
  $("word").addEventListener("click", saveWord);
  $("edit").addEventListener("click", openEdit);
  $("edit-cancel").addEventListener("click", () => { $("edit-form").hidden = true; });
  $("edit-form").addEventListener("submit", saveEdit);

  $("w-title").addEventListener("input", () => { task.writeback.title = $("w-title").value; renderWriteback(); });
  $("w-description").addEventListener("input", () => { task.writeback.description = $("w-description").value; renderWriteback(); });
  $("w-title").addEventListener("change", persist);
  $("w-description").addEventListener("change", persist);
  $("copy-title").addEventListener("click", () => copy(task.writeback.title, "writeback-note", "Title"));
  $("copy-description").addEventListener("click", () => copy(Core.writebackNote(task), "writeback-note", "Description"));
  $("todoist-write").addEventListener("click", askTodoist);
  $("todoist-yes").addEventListener("click", writeTodoist);
  $("todoist-no").addEventListener("click", () => { pendingTodoist = null; $("todoist-confirm").hidden = true; });

  $("start").addEventListener("click", startSession);
  $("stage").addEventListener("change", () => { if (task.example) return; task.stage = $("stage").value; persist(); renderAll(); });
  $("s-env").addEventListener("change", () => store.set("todo-task-env", $("s-env").value));
  $("s-repo").value = store.get("todo-task-repo", "");
  $("s-model").value = store.get("todo-task-model", SPEC.model);
  $("s-repo").addEventListener("change", () => { store.set("todo-task-repo", $("s-repo").value.trim()); renderSession(); });
  $("s-model").addEventListener("change", () => store.set("todo-task-model", $("s-model").value.trim()));

  // ------------------------------------------------------------ capabilities

  const use = (name) => (window.claude && typeof window.claude.use === "function"
    ? window.claude.use(name).catch(() => null) : Promise.resolve(null));

  renderAll();
  use("sample").then((sample) => { caps.sample = sample; });
  use("downloads").then((downloads) => { caps.downloads = downloads; renderBrief(); });
  use("mcp").then((mcp) => { caps.mcp = mcp; $("pull").hidden = !mcp; renderWriteback(); renderSession(); });
  use("db").then((db) => {
    caps.db = db;
    if (db) return subscribe();
    storeOnDevice = true;
    saved = store.get("todo-task-briefs", []);
    renderTasks();
  });
})();
