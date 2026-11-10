#!/usr/bin/env python3
"""Generate one contextual prompt file per Todoist task.

Reads every `data/todoist_tasks*.tsv` (columns: id, project_id, priority, due,
content, description), classifies each task, and writes:

  todo-prompts/<category>/<slug>.md     one file per task
  todo-prompts/index.md                 table of every task with links
  todo-prompts/_reports/duplicates.md   near-duplicate clusters
  todo-prompts/_reports/stale.md        tasks with due dates > 60 days past
  todo-prompts/_reports/by-project.md   counts per Todoist project
  todo-prompts/_proposed-moves.md       proposals the owner can approve

Nothing is sent to Todoist. The TSV is the export; this script only writes
files inside the repository.

Usage: python todoist_prompt_generator.py [--out ../todo-prompts]
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
DEFAULT_OUT = HERE.parent / "todo-prompts"
TODAY = date(2026, 11, 10)

# Todoist project id -> human name (from the account's project list).
PROJECTS = {
    "6RvpWgG7XgpVFc67": "Inbox",
    "6RvpWhmwhrf6wxQg": "Home",
    "6RvpWhxGXRq5H6QV": "My work",
    "6hfJVJqC693HRg3W": "2026-2030 Goals and Visions",
    "6h7CCMxvXj6px8Vq": "Diary/Journal/Notes 17-02-2026",
    "6h7CCP3fg5MFw54v": "Tasks (migrated from To Do)",
    "6h7CCMxvhh5h86Px": "Toop Street",
    "6h7F787p7M4RrgV5": "S-Works Bike Maintenance",
    "6h7F787rr8P6xrVm": "Notes Dump - Work",
    "6h7F786ccQp3qP3F": "Building Up My Body (Morley Studio)",
    "6h7F7JJ2PC9q4RVF": "Tasks 6",
    "6h7F786gWQ54GQW4": "ENT (medical)",
    "6h7F79fvm5mJM2gW": "Travel List",
    "6h7F79frJwCQ95xP": "High Priority - Reminders",
    "6h7F79cV2pH6Vv2R": "Big Whales - Optimism/Drive/Purpose",
    "6h7F79fWvhChPP42": "Every Day Practising/Stop/Start/Keep",
    "6h7F79cWgPvmHR4g": "Latest Tech and AI",
    "6h7F79gqxJQWmXvh": "Notes Dump - Personal",
    "6h7F7JMJcFrR9Xp2": "Tasks 7",
    "6h7F79cwqF8cgj8r": "MedSafe - Medication",
    "6h7F7FFjFhWgQRvH": "Doctors and SMEs",
    "6h7F7FFm6jXPh3Qw": "Important Events Dates",
    "6h7F7JJHxRF3MqVw": "Tasks 8",
    "6h7F7FF7jxRvCgjp": "Greatest Disappointments / Biggest Fears",
    "6h7F7Gj48qJj94jM": "Create prompts from every Google search",
    "6h7F7GpPJ99j9XpM": "Bone Marrow Transplant",
    "6h7F7JMGRrpHWQQV": "Tasks 3",
    "6h7F7GpHgW8rQ9c4": "Fabric AI Keyboard Shortcuts",
    "6h7F7GmXQCXPqG75": "Learn the Bible",
    "6h7F7Gm4QQjWVcVQ": "Leg mass growth",
    "6h7F7GmFRRQr9Vg5": "Theme 10-02-2026 Task and Time Management",
    "6h7F7Gp6xHfMgJ64": "50 Year Anniversary Video Project",
    "6h7F7Gj826qR9QQh": "Supplements to order (1)",
    "6h7F7GhmHfmcj3Pg": "Theme 12-02-2026 Cloud Storage / Google AI",
    "6h7F7864jjQRMM29": "Follow Up Today",
    "6h7F7Gp4jPqfvmrp": "2026 Goals and Habit Stacking",
    "6h7F7Ghqhh4hvMpm": "MAIN GOALS (also in ClickUp)",
    "6h7F74hWP2P3Xm4c": "Flagged Emails",
    "6h7F7Gp22wpw8j38": "Supplements to order",
    "6h7F7JJxF9pc9wpR": "Web Access with no security",
    "6h7F7JJRm7ChWHHg": "Action ASAP",
    "6h7F7JHcCWxRqcVr": "Girls - 2026",
    "6h7F7JJ85CGp7WpF": "Action first thing",
    "6h7F7JQmv9gR7434": "Gratitude and Appreciation",
    "6h7F7JJJGxRxhgFC": "Tasks 4",
    "6h7F7JM29pG2C7WH": "Prompt Ideas for Replit, Lovable, OpenClaw",
    "6h7F7JH3p5wc9cMJ": "Systems and Workflow Ideas",
    "6h7F7JJrfcG2pGPq": "Forget Remembering",
    "6h7F7JJgFfC655x7": "Guy Thomas - Stay Close and Learn From",
    "6h7F7JP55p63fCj7": "Workflows using software stacking",
    "6h7F7JJv65hJhhPw": "Action First Thing 02",
    "6h7F79f7vXgcRcJp": "Lachie - Collaboration",
    "6h7F7FFQphPjGX3X": "Grant - Tasks",
    "6h7F7FCf5cQFqp54": "IT Queries - Shared",
    "6h7F7FG9QXvmp4h3": "IT Queries - Personal",
    "6h7F7FChFMJwWfM8": "Ordering and Purchasing - Personal Wishlist",
    "6h7F7FF8RQRRRw5R": "Ordering and Purchasing - Work",
    "6h7F7879WGR2r4fM": "Productivity - Procedures",
    "6h7F7GhpHFrfw8qC": "To investigate",
}

# Category rules: (category, keyword regex). First match wins; order matters.
RULES = [
    ("health-medical", r"\b(peptide|hgh|growth hormone|vyvanse|dex(amphetamine)?|lorazepam|quetiapine|quatiapine|fluox|naltrexone|ondansetron|sildenafil|sidinafil|prescri|pharmac|medication|meds?\b|doctor|\bgp\b|\bent\b|nose|\bhips?\b|shoulder|scan\b|x-?ray|mri|blood|haematolog|hematolog|oncolog|psychiatr|dentist|dental|teeth|veneer|braces|cbd|thc|kava|fortisip|ambrotose|fadogia|tongkat|tonkat|prelox|creatine|spirulina|spiralina|hydroxycut|hydroxcut|supplement|supps|nitric|norateen|la muscle|rybraxx|methylfolate|sam-e|tebonin|dopaboost|avenol|melatonin|methylene|milk thistle|fish oil|vitamin|ester-c|liver|heart|gut|stomach|bone|marrow|transplant|graft|fertil|hypogonad|klinefelter|testicul|gonad|nuts? (check|growth)|\bed\b|erectile|trt|testosterone|cholesterol|triglycer|epilep|sclerosis|mitochondria|memory loss|chemo|cancer|freckle|throat|tongue|back pain|\bpain\b|adhd|anxiety|antidepress|sleeping pill|health|medical|appointment with dr|dr\b|specialist|executive check|well for life|body relief|canopy imaging|trg imaging|awanui|hastings health|mahora|stortford|managemyhealth|medisafe)"),
    ("faith-character", r"\b(pray|prayer|god\b|lord|jesus|christ|holy spirit|bible|scripture|ministry|brethren|fellowship|mr hales|conversion|righteous|sin\b|sinning|devil|evil|faith|spiritual|gratitude|humble|integrity|loyal|kindness|esteem|short accounts|convictions|temptation|adult|porn|lust|repent|impression)"),
    ("relationships-personal", r"\b(dad|mum|mother|father|family|brother|sister|lachie|riley|willard|honor|tarah|girl|wife|marriage|married|partner|friends?|mentor|social(is|iz)|approach|date\b|engadine|san fran|usa|america|sydney|flights?|trip|holiday|gerald|guy\b|charlie|caleb|jason|duncan|grant|morgan|yorke|aroha|donna|steph|josh|armand|stella|sarah|willy|alister|jacob hart|david smith|bill murray|richard stanners|beatrice|fredella|jaimie|bobby|nico|leigh|pete|joe\b)"),
    ("home-property", r"\b(toop|morley|studio|gym|shed|garage|house|home\b|driveway|boundary|dam\b|houseboat|house boat|raft|sauna|landscap|fence|letterbox|olive|rat|possum|fibre|router|fridge|bed\b|shelv|shelf|shiplap|cedar|wharf|mirror|lighting|lights|tiles|mats|bench|dumbbell|weights|rack|pulley|ladder|air ?condition|ecoflow|ikea|screws|brackets|deltex|desk|table|chair|stool|blinds|doors?|ceiling|pivot|appraisal|valuation|council|harbour|keirunga|greenwood|fire evacuation|carpet|batts|leak|water|outdoor)"),
    ("it-devices-storage", r"\b(nas\b|qnap|onedrive|dropbox|google drive|backblaze|iconik|lucidlink|canto|dam\b|ssd|hard ?drive|t9\b|samsung|zbook|lenovo|legion|laptop|computer|pc\b|windows|chrome|edge\b|streamline|forticlient|vpn|domain|group policy|managed by|eset|antivirus|crowdstrike|ubt\b|onehq|it support|it queries|ticket|nvidia|driver|gpu|file explorer|opus|onecommander|amerigo|treesize|bulk rename|pixillion|kmplayer|mpv|one photo|catalyst|mercalli|plugin|install|download|reinstall|uninstall|cheatkeys|keyrocket|text expander|bluestacks|windhawk|vagon|smartthings|hdmi|cable|keyboard|mouse|battery|charger|screen|monitor|dell|8k|conference camera|webcam|wifi|network|internet|ethernet|server|hinge|repair|data recovery|partition|hbs|sync|migrat|backup|file path|folder|bookmark|takeout|history|password|1password|passkey|account|gmail|outlook|email|workspace|login|log in|sign in|facebook|spotify|lg\b|microsoft|office 365|copilot|google (cloud|play|photos|alerts|ai|workspace)|samsung account|phone|zfold|iphone|ipad|tablet|remarkable|fastmail|canary|slack|teams|zoom)"),
    ("ai-agents-automation", r"\b(ai\b|agent|openclaw|nemoclaw|claude|chatgpt|chat ?gpt|gemini|grok|perplexity|manus|notebooklm|notebook lm|fabric|mymind|prompt|whisper|n8n|zapier|make\b|rossum|abbyy|kaseya|automation|automate|workflow|playbook|procedure|sop\b|notion|clickup|todoist|to do\b|to-do|todo|smartsheet|morgen|habitnow|habitshare|habit share|reflect\.io|reflect\b|second brain|para\b|code\b|tiago|forte|master prompt|system prompt|vibe cod|replit|lovable|cordova|nexus|app\b|apps\b|json|python|linux|antigravity|apex|higgsfield|veed|descript|grammarly|momentum|exo\b|retell|semrush|cdata|hubspot|apollo|frame\.io|camera to cloud|c2c|dropbox replay|wistia|loom|webflow|wix|godaddy|domain name|website|seo|aeo|rank)"),
    ("marketing-content", r"\b(video|edit\b|edits|footage|shoot|photo|photograph|drone|gimbal|camera|lens|sony|fujifilm|gopro|brochure|spec sheet|advert|ad\b|campaign|email blast|newsletter|social|linkedin|instagram|behance|substack|youtube|podcast|post\b|posting|blog|content|brand|branding|logo|hexagon|slant|poster|decal|mission|vision|values|testimonial|boast|case study|arjes|bandit|pellenc|tow and blow|mango|trimmer|chipper|stumpgrinder|cage|insulated|640|802|440|540|750i|360|nblosi|avocado|harvest|winegrower|avoscene|biorich|groundcling|portal|asset library|lightroom|photoshop|premiere|after effects|firefly|substance|keyshot|sketchup|blender|express|canva|figma|indesign|illustrator|typography|colour|gradient|layers|design|graphic|artlist|envato|music|song|guitar|piano|drum|hymn|record|voiceover|mic\b|rode|bose|pa system|sennheiser|headphone|earbud|beoplay|metricool|marketing|sales|crm|lead|pipeline|prospect|customer|director|shareholder|value proposition|org chart|quote cover|quotes?\b)"),
    ("finance-admin", r"\b(pay\b|paid|invoice|refund|subscription|renew|cancel|budget|money|cash|finance|accounting|xero|kubera|bank|asb|anz|loan|contras|charge|credit|cost|price|\$|crypto|insurance|tax|form\b|terms of service|tos\b|billing)"),
    ("purchases-gear", r"\b(order|purchase|buy|wishlist|new\b|shoes|sneakers|boots|loafers|jacket|shirt|pants|trousers|underwear|hat|clothes|clothing|watch|strap|sunglasses|glasses|backpack|arc'teryx|boss|rm williams|new balance|crockett|berluti|mytheresa|amarok|ute|rs4|audi|landcruiser|car\b|wheels|lift kit|radar|starlink|e-bike|levo|kenevo|s-works|bike|commencal|turbo|present|gift|controller|game|xbox|table tennis|rowing|treadmill|step machine|weight vest|fid bench|smith machine|leg extension|headphones|earbuds|speaker|drone)"),
    ("habits-productivity", r"\b(habit|routine|daily|every day|everyday|morning|evening|night before|plan|schedule|calendar|time ?block|prioriti|procrastinat|focus|discipline|organis|organiz|structure|system|finish|complete|action|execute|productiv|efficien|tidy|declutter|clean ?out|review|reflect|journal|diary|bullet|notes?\b|capture|save all|remember|forget remembering|memor|learn|read\b|reading|book\b|study|course|training|skill|typing|shortcut|keyboard warrior|energy|sleep|rest|nap|meditat|breath|vagus|boredom|multitask|overthink|stress|nervous|confiden|public speak|speaker|writer|vocabulary|words|critical thinking|neuroplastic|mindset|goal|vision|comeback|ownership|accountab|delegate|reliable|commit|believe|bravery|just go|take action|get ahead|value my time|signal|noise|one thing|theme for each day)"),
    ("faith-character", r"^(disappointment|fear|gratitude note|faith)"),
    ("habits-productivity", r"^(be|become|don'?t|do|stop|start|keep|get|have|make|take|use|try|go|just|always|never|practi[sc]e|learn|improve|overcome|work|find|fix|finish|ask|think|share|reply|follow|listen|value|stay|save|commit|believe|refuse|respect|love|look|treat|grow|less|more|fill|clear|organise|organize|check|review|plan|write|read)\b"),
]

# Keywords that mark a task as sensitive; its prompt stays minimal.
SENSITIVE = re.compile(r"\((private|private medical|private reflection|personal)\)|private\b|personal reflection|names kept out", re.I)
AGGREGATE = re.compile(r"names kept out|kept to one row|about \d+ (single-item|names)", re.I)

CATEGORY_META = {
    "health-medical": ("20_Areas/Health", "Health and medical"),
    "faith-character": ("20_Areas/Spirituality", "Faith and character"),
    "relationships-personal": ("20_Areas/Relationships-and-Associations", "Relationships and personal"),
    "home-property": ("20_Areas/Toop-Street-Property or 20_Areas/Morley-Studio", "Home, property and studio"),
    "it-devices-storage": ("20_Areas/IT-Devices-and-Storage", "IT, devices, accounts and storage"),
    "ai-agents-automation": ("10_Projects/2026-11_second-brain-system or 30_Resources/Prompts", "AI, agents, tools and automation"),
    "marketing-content": ("20_Areas/Hydralada-Marketing or 10_Projects/<campaign>", "Marketing, content and creative"),
    "finance-admin": ("20_Areas/Finance-and-Subscriptions", "Finance, subscriptions and admin"),
    "purchases-gear": ("30_Resources/Wishlist", "Purchases and gear"),
    "habits-productivity": ("20_Areas/Habits or 20_Areas/Vision-Mission-Values", "Habits, productivity and self-improvement"),
    "uncategorised": ("00_Inbox", "Uncategorised"),
}

# Per-category prompt skeletons. {content}, {description}, {project}, {due},
# {priority} are filled in.
TEMPLATES = {
    "health-medical": """You are helping me organise, not advise. Here is a health-related item from my task list:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}. Priority: {priority}.

1. Restate the task in one clear sentence using only my words.
2. Classify: appointment to book, prescription or supply to manage, question for a clinician, habit, or research note.
3. If it is a question for a clinician, write it as a short, specific question I can read out, plus two follow-up questions.
4. If it is a supply or appointment, list what I need to have in hand (who to contact, what reference numbers, which account) and a calendar line for Morgen.
5. Suggest where it lives: 20_Areas/Health/<subfolder>.
6. Do not give dosing, treatment or medical advice. Do not interpret symptoms. If the task implies urgency or risk, say "raise this with your GP or specialist first" and stop there.""",
    "faith-character": """This is an item from my list about faith or character:
Task: {content}
Notes: {description}
From Todoist project: {project}.

1. Restate it as a practice I can do, in my own words, under 20 words.
2. Suggest a cue (when and where) and a two-minute version, in the style of Atomic Habits.
3. Give one reflective question I could write about in my journal this week.
4. If it refers to scripture or ministry, note that I will add the reference myself; do not invent one.
5. PARA home: 20_Areas/Spirituality/<practice or impressions>.
Keep it to under 150 words. Respect that this is private and sincere.""",
    "relationships-personal": """This is a personal or relationship item from my list:
Task: {content}
Notes: {description}
From Todoist project: {project}.

1. Restate it as a concrete, kind next step (a message to send, a call to make, a time to offer), under 20 words.
2. Draft the message or opening line in my voice, plain and warm, under 60 words. Mark [NAME] where a name goes.
3. Suggest a date within 14 days and a calendar line for Morgen.
4. PARA home: 20_Areas/Relationships-and-Associations/<person or group>.
Do not speculate about other people's feelings or motives. Keep anything sensitive out of the output.""",
    "home-property": """This is a home, property or studio item:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}.

1. Restate as a single outcome ("done means ...").
2. Break into 3 to 6 physical steps, each under 12 words, verb first.
3. List materials, tools, measurements or contacts needed; mark unknowns [MEASURE] or [ASK].
4. Estimate time and cost band (under 1 hour / half day / full day / multi-day; under $100 / $100 to $500 / $500 plus).
5. Say whether it needs council, a tradesperson, a neighbour or Dad, and who to talk to first.
6. PARA home: 20_Areas/Toop-Street-Property or 20_Areas/Morley-Studio, or 10_Projects/2026-02_toop-street-alterations if it is part of the alterations project.""",
    "it-devices-storage": """This is an IT, device, account or storage item:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}.

1. Restate as a single verifiable outcome.
2. Diagnose: list the two or three most likely causes or prerequisites, in order of likelihood.
3. Give the exact steps for Windows 11 (or the named device), including menu paths or commands, under 10 steps. Mark anything that needs admin rights or IT (OneHQ, UBT) approval.
4. Data-safety check: what must be backed up or verified before any delete, de-sync or reinstall. Never propose deleting data that has not been verified on the NAS and one other place.
5. If this relates to Streamline, group policy or "managed by your organisation", explain in two sentences what is likely happening and what the owner can and cannot change on a device they own.
6. PARA home: 20_Areas/IT-Devices-and-Storage/<device or service>.
7. Passwords: recommend unique generated passwords in 1Password, never a shared base password.""",
    "ai-agents-automation": """This is an item about AI, agents, tools or automation:
Task: {content}
Notes: {description}
From Todoist project: {project}.

1. Restate as the capability I want ("I can ..."), one sentence.
2. Map it onto my second-brain system (second-brain/ in this repo): which agent, prompt, routine or script already covers part of it, and what is missing.
3. Propose the smallest working version I can run this week, with exact steps or a prompt I can paste.
4. Name the data and connectors it needs (Todoist, Dropbox, HubSpot, Smartsheet, Notion, Google Takeout) and any token or permission to set up first.
5. Guardrails: what it must never do without me (post, delete, spend, share).
6. PARA home: 10_Projects/2026-11_second-brain-system if it extends the system, otherwise 30_Resources/Prompts or 20_Areas/IT-Devices-and-Storage.
7. Done means: a one-line test I can run to prove it works.""",
    "marketing-content": """This is a marketing, content or creative item for Hydralada or my own brands:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}.

1. Restate as a deliverable with format and audience ("a 60-second vertical cut for growers on LinkedIn").
2. Fill the brief fields: objective, audience, key message, mandatory brand elements (logo, 31.15 degree slant, colours), format and versions (extra long, long, short, social short, vertical where video), approver, distribution (HubSpot, socials, YouTube, DAM, NAS).
3. List inputs I already have and where (Dropbox Hydralada Marketing folders, NAS paths, Smartsheet rows); mark gaps [NEED].
4. Production steps, under 8, with a time estimate each.
5. The single next physical action for today.
6. PARA home: 10_Projects/<campaign or video> if it has an end date, else 20_Areas/Hydralada-Marketing.
Write nothing that would be published; drafts only.""",
    "finance-admin": """This is a finance, subscription or admin item:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}.

1. Restate as a decision or an action with a deadline.
2. List what I need to see first: account, last charge, renewal date, who pays (me, Hydralada, Caleb), where the invoice lives.
3. If it is a subscription: give the keep/cancel/downgrade test (used in the last 30 days? duplicates another tool? needed for an active project?) and a recommendation with the reason.
4. If it is a payment or refund: the exact steps and the message to send, under 60 words.
5. Add a line for 20_Areas/Finance-and-Subscriptions/subscriptions.md (name, cost, cycle, renewal, decision).
6. Calendar line for the renewal or follow-up in Morgen.
No financial advice beyond organising the decision.""",
    "purchases-gear": """This is a purchase or gear item:
Task: {content}
Notes: {description}
From Todoist project: {project}.

1. Restate as a specific product decision with 2 or 3 candidate options (name, key spec, approximate NZ price band; write [CHECK] rather than guessing a number).
2. Decision criteria: what it must do for me, what it must fit with (Zbook outputs, Sony lenses, studio space), and the dealbreaker.
3. Where to compare in NZ (named retailers only if known; otherwise "two NZ retailers").
4. Should this be funded by me, by Hydralada (work tool), or deferred? One sentence.
5. Wishlist line for Smartsheet: item | category | price band | link [ADD] | picture [ADD] | priority.
6. PARA home: 30_Resources/Wishlist (or 10_Projects/<project> if it unblocks one).""",
    "habits-productivity": """This is a habit, productivity or self-improvement item:
Task: {content}
Notes: {description}
From Todoist project: {project}. Due: {due}.

1. Is this a task, a habit, a goal, or a value statement? Say which. If a value or mantra, write a one-line version for 20_Areas/Vision-Mission-Values and stop at step 2.
2. If a habit: design it with Atomic Habits (cue, two-minute version, reward, tracker line for HabitNow or ClickUp) in under 120 words.
3. If a goal: write the outcome, a target date, and the first three tasks (verb first, under 12 words).
4. If a task: the next physical action and a 25-minute time block suggestion.
5. Point to the matching system piece in second-brain/ (routines/morning-plan.md, routines/daily-shutdown.md, routines/weekly-review.md, agents/09-journal-agent.md, or a prompt in 30_Resources/Prompts) so I use the system rather than rebuild it.
6. PARA home as stated.""",
    "uncategorised": """Here is an item from my list that did not fit a category:
Task: {content}
Notes: {description}
From Todoist project: {project}.

1. Restate it clearly in one sentence, or say "unclear; ask Brad what this means" if the words do not carry enough meaning.
2. Classify it: task, note, idea, goal, person, or reference.
3. Suggest a PARA home and one next action under 12 words.""",
}


def slugify(text: str, limit: int = 48) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return (text or "task")[:limit].rstrip("-")


def classify(content: str, description: str) -> str:
    hay = f"{content} {description}".lower()
    for cat, pattern in RULES:
        if re.search(pattern, hay, flags=re.I):
            return cat
    return "uncategorised"


def load_tasks() -> list[dict]:
    tasks: list[dict] = []
    seen_ids: set[str] = set()
    for path in sorted(DATA_DIR.glob("todoist_tasks*.tsv")):
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in reader:
                if not row.get("id") or row["id"] in seen_ids:
                    continue
                seen_ids.add(row["id"])
                row["description"] = (row.get("description") or "").strip()
                row["content"] = (row.get("content") or "").strip()
                row["due"] = (row.get("due") or "").strip()
                row["priority"] = (row.get("priority") or "p4").strip()
                row["project"] = PROJECTS.get(row["project_id"], f"project {row['project_id']}")
                row["category"] = classify(row["content"], row["description"])
                row["sensitive"] = bool(SENSITIVE.search(row["content"] + " " + row["description"]))
                row["aggregate"] = bool(AGGREGATE.search(row["content"]))
                tasks.append(row)
    return tasks


def elaborate(task: dict) -> str:
    """A short contextual note on why the task matters and what done looks like."""
    cat = task["category"]
    c = task["content"]
    if task["aggregate"]:
        return ("This row stands for a group of similar one-line entries in Todoist. Treat the group as one "
                "recurring supply or contact-management routine rather than many tasks. Names and item lists "
                "stay in Todoist by design.")
    if task["sensitive"]:
        return ("Kept deliberately brief. This touches health, family or personal matters. The prompt only "
                "organises the item and points to the right person; it does not elaborate the content.")
    hints = {
        "health-medical": "Health is Area number one in Brad's own words. The value of writing it down is that nothing gets lost between appointments; the system's job is logistics and good questions, never advice.",
        "faith-character": "These items are the values layer of PARA. They rarely need a task; they need a place (20_Areas/Vision-Mission-Values, 20_Areas/Spirituality) and a habit that keeps them visible.",
        "relationships-personal": "Relationships compound like everything else here. One small, timely message beats a perfect plan. The weekly review's waiting-for list is where these live.",
        "home-property": "Toop Street and Morley Studio are long-running Areas with occasional Projects inside them. Done is physical: something installed, moved, booked or drawn.",
        "it-devices-storage": "Most of these trace back to one root cause: files spread over OneDrive, NAS, external drives and three laptops, plus a managed-device policy from work. Every fix should move toward one PARA tree on the NAS with verified backups.",
        "ai-agents-automation": "This is the engine room of the second-brain system. Before building anything new, check second-brain/agents, routines and 30_Resources/Prompts; most of these ideas already have a home there.",
        "marketing-content": "Hydralada content work is the day job. The win is a repeatable pipeline: brief, inputs from the DAM, edit on local SSD, five versions, approval, distribution through HubSpot. Every task here should slot into that pipeline.",
        "finance-admin": "Subscriptions have been leaking money (four Lovable top-ups in one day, renewals on tools no longer used). The weekly review's transactions step is where this gets caught.",
        "purchases-gear": "Wishlists are fine as Resources. They become Projects only when a purchase unblocks real work (a monitor for editing, a camera for shoots). Separate wants from tools.",
        "habits-productivity": "Brad's words: be a finisher, journal every day, capture and save everything using PARA. The routines in second-brain/routines are the implementation. Each habit should attach to one of them.",
        "uncategorised": "Could not be classified from the words alone. Ask or discard at the next weekly review.",
    }
    return hints.get(cat, "")


def next_steps(task: dict) -> list[str]:
    cat = task["category"]
    due = task["due"]
    steps: list[str] = []
    if task["aggregate"]:
        return ["Decide whether this group becomes one recurring Todoist task (monthly order, quarterly contact review).",
                "Archive the individual one-line entries once the recurring task exists."]
    if task["sensitive"]:
        return ["Keep in Todoist; bring to the next relevant appointment or conversation.",
                "File under the PARA home above. Do not elaborate further in shared tools."]
    generic = {
        "health-medical": ["Check whether an appointment, repeat or referral already covers this.",
                           "Add the clinician question to a running list for the next visit.",
                           "Put any date in Morgen and link it from 20_Areas/Health."],
        "faith-character": ["Write the one-line version into 20_Areas/Vision-Mission-Values/inbox.md.",
                            "Pick the cue and add the habit to HabitNow or ClickUp.",
                            "Reflect on it in Sunday's weekly reflection."],
        "relationships-personal": ["Send the message or make the call within 48 hours.",
                                   "Add the person to the People list in the master prompt.",
                                   "Log the follow-up date as @waiting-for in Todoist."],
        "home-property": ["Take a photo and a measurement; drop both in 00_Inbox.",
                          "Decide: DIY this weekend, or get a quote.",
                          "Add to the Toop or Morley project README as a next action."],
        "it-devices-storage": ["Back up or verify before changing anything.",
                               "Do the steps; if blocked by policy, raise a OneHQ ticket with the exact error.",
                               "Record the fix in 20_Areas/IT-Devices-and-Storage/runbook.md."],
        "ai-agents-automation": ["Check second-brain/agents and 30_Resources/Prompts for an existing fit.",
                                 "Build the smallest version and run it once, dry-run where possible.",
                                 "If it works, add it to routines/schedules.md; if not, archive the idea."],
        "marketing-content": ["Create or update the brief with 30_Resources/Prompts/08_marketing/marketing-brief.md.",
                              "Pull inputs from Dropbox Hydralada Marketing and the Smartsheet row.",
                              "Block two hours in Morgen; edit from the local SSD; export the five versions."],
        "finance-admin": ["Find the last invoice or charge and the renewal date.",
                          "Decide keep, cancel or downgrade; act the same day.",
                          "Record it in 20_Areas/Finance-and-Subscriptions/subscriptions.md."],
        "purchases-gear": ["Add the item to the Smartsheet wishlist with price band, link and picture.",
                           "Decide funding: personal, work, or defer.",
                           "Only move to a Project if it unblocks real work."],
        "habits-productivity": ["Decide: value, habit, goal or task.",
                                "Attach it to a routine in second-brain/routines.",
                                "Track it for two weeks before judging it."],
        "uncategorised": ["Clarify or discard at the weekly review."],
    }
    steps = list(generic.get(cat, []))
    if due:
        try:
            d = datetime.strptime(due, "%Y-%m-%d").date()
            if d < TODAY:
                steps.insert(0, f"Due date {due} has passed: reschedule or archive at the next review.")
            else:
                steps.insert(0, f"Due {due}: block time before then.")
        except ValueError:
            pass
    return steps


def render(task: dict) -> str:
    cat = task["category"]
    para_home, cat_label = CATEGORY_META[cat]
    tmpl = TEMPLATES["uncategorised"] if task["sensitive"] and cat != "health-medical" else TEMPLATES[cat]
    if task["sensitive"] and cat == "health-medical":
        tmpl = TEMPLATES["health-medical"]
    prompt = tmpl.format(
        content=task["content"],
        description=task["description"] or "(none)",
        project=task["project"],
        due=task["due"] or "none",
        priority=task["priority"],
    )
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(next_steps(task), 1))
    todoist_link = f"https://app.todoist.com/app/task/{task['id']}"
    return f"""# {task['content']}

| Field | Value |
|---|---|
| Todoist | [{task['id']}]({todoist_link}) |
| Project | {task['project']} |
| Priority | {task['priority']} |
| Due | {task['due'] or 'none'} |
| Category | {cat_label} |
| PARA home | `{para_home}` |
| Sensitivity | {'private' if task['sensitive'] else 'normal'} |

## As captured
{task['content']}
{('> ' + task['description']) if task['description'] else ''}

## Context
{elaborate(task)}

## Prompt (paste into Claude, ChatGPT or an agent run)
```text
{prompt}
```

## Next steps
{steps}

## Session suggestion
Run this together with the other items in `todo-prompts/{cat}/` (one Claude Code
session per category, oldest first). Related agent: see `second-brain/agents/README.md`.
"""


def near_duplicates(tasks: list[dict], threshold: float = 0.85) -> list[list[dict]]:
    """Cluster tasks whose normalised titles are identical or very similar.

    Exact matches are grouped directly. Fuzzy matching only runs inside
    buckets that share the first word, which keeps this fast on thousands of
    rows.
    """
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
    exact: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        exact[norm(t["content"])].append(t)
    clusters: list[list[dict]] = [g for g in exact.values() if len(g) > 1]
    reps = [(k, g) for k, g in exact.items() if len(k) > 12]
    buckets: dict[str, list[tuple[str, list[dict]]]] = defaultdict(list)
    for k, g in reps:
        buckets[k.split(" ", 1)[0]].append((k, g))
    merged: set[str] = set()
    for items in buckets.values():
        for i, (ka, ga) in enumerate(items):
            if ka in merged:
                continue
            group = list(ga)
            for kb, gb in items[i + 1:]:
                if kb in merged or abs(len(ka) - len(kb)) > 12:
                    continue
                sm = SequenceMatcher(None, ka, kb)
                if sm.real_quick_ratio() >= threshold and sm.quick_ratio() >= threshold and sm.ratio() >= threshold:
                    group.extend(gb)
                    merged.add(kb)
            if len(group) > len(ga):
                merged.add(ka)
                clusters.append(group)
    return clusters


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    out = Path(args.out)
    tasks = load_tasks()
    if not tasks:
        print("no tasks found in data/*.tsv", file=sys.stderr)
        return 1

    # Clean previous generated files (only inside category folders and reports).
    for sub in list(CATEGORY_META) + ["_reports"]:
        d = out / sub
        if d.exists():
            for f in d.glob("*.md"):
                f.unlink()
    (out / "_reports").mkdir(parents=True, exist_ok=True)

    counts: Counter = Counter()
    used_names: set[str] = set()
    index_rows: list[str] = []
    for t in sorted(tasks, key=lambda x: (x["category"], x["project"], x["content"].lower())):
        cat = t["category"]
        counts[cat] += 1
        d = out / cat
        d.mkdir(parents=True, exist_ok=True)
        base = slugify(t["content"])
        name = base
        n = 2
        while name in used_names:
            name = f"{base}-{n}"
            n += 1
        used_names.add(name)
        path = d / f"{name}.md"
        path.write_text(render(t), encoding="utf-8")
        t["path"] = f"{cat}/{name}.md"
        flag = " (private)" if t["sensitive"] else ""
        index_rows.append(f"| [{t['content'][:70].replace('|', '/')}{flag}]({t['path']}) | {t['project']} | {t['priority']} | {t['due'] or ''} | {cat} |")

    # Index
    lines = [
        "# To-do prompts index",
        "",
        f"Generated {TODAY.isoformat()} from {len(tasks)} open Todoist tasks. One prompt file per task, grouped by category.",
        "Run a category as one session: open Claude Code on this repo and say \"work through todo-prompts/<category>/, oldest first, and write results to the PARA homes named in each file\".",
        "",
        "## Counts by category",
        "",
        "| Category | Tasks | PARA home |",
        "|---|---|---|",
    ]
    for cat, (home, label) in CATEGORY_META.items():
        lines.append(f"| [{label}]({cat}/) | {counts.get(cat, 0)} | `{home}` |")
    lines += ["", "## All tasks", "", "| Task | Todoist project | Priority | Due | Category |", "|---|---|---|---|---|"]
    lines += index_rows
    (out / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Reports: duplicates
    clusters = near_duplicates(tasks)
    dl = ["# Near-duplicate tasks", "", f"{len(clusters)} clusters where titles match at 85 percent or better. Propose merging each cluster into one task.", ""]
    for c in clusters:
        dl.append(f"- **{c[0]['content'][:80]}**")
        for t in c:
            dl.append(f"  - `{t['id']}` {t['content'][:80]} ({t['project']})")
    (out / "_reports" / "duplicates.md").write_text("\n".join(dl) + "\n", encoding="utf-8")

    # Reports: stale
    stale = []
    for t in tasks:
        if t["due"]:
            try:
                d = datetime.strptime(t["due"], "%Y-%m-%d").date()
                if (TODAY - d).days > 60:
                    stale.append((d, t))
            except ValueError:
                pass
    stale.sort(key=lambda x: x[0])
    sl = ["# Stale tasks (due more than 60 days ago)", "", f"{len(stale)} tasks. Reschedule, complete or archive.", "", "| Due | Task | Project |", "|---|---|---|"]
    sl += [f"| {d} | [{t['content'][:70]}]({t['path']}) | {t['project']} |" for d, t in stale]
    (out / "_reports" / "stale.md").write_text("\n".join(sl) + "\n", encoding="utf-8")

    # Reports: by project
    pc: Counter = Counter(t["project"] for t in tasks)
    pl = ["# Tasks by Todoist project", "", "| Project | Open tasks |", "|---|---|"]
    pl += [f"| {p} | {n} |" for p, n in pc.most_common()]
    (out / "_reports" / "by-project.md").write_text("\n".join(pl) + "\n", encoding="utf-8")

    # Proposed moves
    pm = [
        "# Proposed Todoist moves (nothing applied)",
        "",
        "Review, delete what you disagree with, then ask a session to apply the rest through the Todoist connector.",
        "",
        "## Merge near-duplicates",
        f"See `_reports/duplicates.md` ({len(clusters)} clusters). Keep the most recent, complete the others.",
        "",
        "## Archive or reschedule stale items",
        f"See `_reports/stale.md` ({len(stale)} tasks).",
        "",
        "## Re-home by category",
        "Suggested Todoist project per category so Todoist mirrors PARA:",
        "",
    ]
    for cat, (home, label) in CATEGORY_META.items():
        pm.append(f"- {label} ({counts.get(cat, 0)} tasks) -> project matching `{home}`")
    pm += [
        "",
        "## Add labels",
        "- `@health` on every item in health-medical (keeps them out of work views).",
        "- `@waiting-for` on items that depend on another person.",
        "- `@someday` on value statements and mantras that are not tasks.",
    ]
    (out / "_proposed-moves.md").write_text("\n".join(pm) + "\n", encoding="utf-8")

    print(f"tasks={len(tasks)} files written under {out}")
    for cat, n in counts.most_common():
        print(f"  {cat}: {n}")
    print(f"duplicates={len(clusters)} stale={len(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
