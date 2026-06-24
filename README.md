# Copilot Skills &amp; Agents — Live Demo Pack (APS)

A **self-contained folder** for demoing GitHub Copilot **skills** and **custom
agents** live, from basic to intermediate, using the APS pension story.

> Everything here is fictional sample data — no real member information.

---

## How to run the demos

These are real VS Code Copilot customization files. VS Code discovers them from
the `.github/` folder **of the workspace folder you have open**, so:

1. In VS Code: **File → Open Folder…** and open **this `demos/` folder**
   (or add it to your workspace: **File → Add Folder to Workspace…**).
2. Open the **Copilot Chat** view.
3. The skills load automatically; the agents appear in the **agent picker**
   (the mode dropdown at the top of the chat box).

You need Python on PATH for the intermediate skill (`python --version`).

---

## What's in here

```
demos/
├── .github/
│   ├── skills/
│   │   ├── pension-glossary/        # Demo 1 — BASIC skill (auto-loaded knowledge)
│   │   │   └── SKILL.md
│   │   └── pension-statement/       # Demo 3 — INTERMEDIATE skill (skill + script + reference)
│   │       ├── SKILL.md
│   │       ├── scripts/generate_statement.py
│   │       └── references/statement-format.md
│   └── agents/
│       ├── pension-explainer.agent.md    # Demo 2 — BASIC agent (read-only persona)
│       └── pension-app-builder.agent.md  # Demo 4 — INTERMEDIATE agent (tools + skill, multi-step)
└── sample-data/members.json         # Fictional members (M-1001…M-1004)
```

---

## The 4 demos, in order

### Demo 1 — Basic **skill**: knowledge on a shelf
**File:** `.github/skills/pension-glossary/SKILL.md`

A skill is a written playbook the agent picks up **on demand**. This one teaches
Copilot APS pension wording — no scripts, just instructions.

**Try it (default agent, Ask mode):**
> `What does "commuted value" mean? Explain it for a new member.`

**What to point out**
- You never told Copilot to "use a skill." It matched your question to the
  skill's **description** and loaded it automatically.
- Ask a term that is *not* in the glossary (e.g. "what is a spousal rollover?")
  → it follows the skill's boundary rule and says so instead of guessing.

---

### Demo 2 — Basic **agent**: a focused persona
**File:** `.github/agents/pension-explainer.agent.md`

An agent is a **doer with a role and a tool budget**. This one is a patient
explainer with **read-only** tools — it *can't* edit code or run commands.

**Try it:** pick **Pension Explainer** in the agent picker, then:
> `Explain the Overview tab of the dashboard to someone who has never seen a pension statement.`

**What to point out**
- Same AI brain, but a **persona + guardrails**: friendly tone, plain language,
  ends with a follow-up question.
- Tools are limited to `read, search` — ask it to "delete a file" and it won't;
  that's the tool restriction in the frontmatter doing its job.
- It reuses **Demo 1's glossary** for consistent wording → skills + agents compose.

---

### Demo 3 — Intermediate **skill**: instructions + a real script
**File:** `.github/skills/pension-statement/SKILL.md`

Skills can bundle **scripts and reference files**. This one runs a Python script
over the sample data and formats the result with a reference layout.

**Try it (default agent, Agent mode):**
> `Generate a pension statement for member M-1003.`

**What to point out**
- The agent reads the skill, **runs the bundled script**
  (`generate_statement.py --member M-1003`), then formats the output using
  `references/statement-format.md`.
- Try a name instead of an id: *"Show Priya Nair's statement"* → it looks up the
  id first. Try a bad id → it lists the valid ones (boundary rule).
- **Progressive loading:** only the description loads until it's needed; the
  script and reference load only when the task matches.

**Run the script yourself (optional, from the `demos/` folder):**
```bash
python .github/skills/pension-statement/scripts/generate_statement.py --member M-1003
```

---

### Demo 4 — Intermediate **agent**: tools + skill, multi-step
**File:** `.github/agents/pension-app-builder.agent.md`

This agent **plans**, uses **terminal + file editing**, and **reuses Demo 3's
skill** instead of reinventing the math.

**Try it:** pick **Pension App Builder** in the agent picker, then:
> `Generate a statement for every member and save them as text files in an out/ folder.`

**What to point out**
- It **plans first** with a visible todo list, then executes step by step.
- It **delegates to the skill's script** (doesn't re-derive the projection).
- It **verifies** — re-reads/re-runs to confirm — then summarises what changed
  and how to check it.
- Contrast with Demo 2: same idea (an agent), but a bigger tool budget and a
  multi-step workflow = "intermediate."

---

## One-line talking points

| Concept | One sentence |
|---|---|
| **Skill** | Know-how on a shelf the agent loads when your request matches its description. |
| **Agent** | A doer with a persona and a tool budget that works toward a goal. |
| **Discovery** | The **description** field is everything — that's how Copilot decides to load a skill or pick an agent. |
| **Composition** | Agents reuse skills; skills bundle scripts — small pieces combine. |
| **Guardrails** | Tools in the frontmatter define what an agent *can* and *can't* touch. |

## Reset between runs
Demo 4 creates an `out/` folder. To reset:
```bash
# from the demos/ folder
rm -r out    # PowerShell: Remove-Item -Recurse -Force out
```
