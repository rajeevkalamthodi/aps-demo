---
name: pension-statement
description: 'Generate a formatted APS member pension statement from the sample data. Use when someone asks to "generate / produce / show a pension statement" for a member id (for example M-1003), or to summarise a member''s pension and retirement forecast. Runs a Python script over demos/sample-data/members.json and formats the result.'
argument-hint: 'a member id, e.g. M-1003'
---

# APS Member Pension Statement

Produce a clean, member-friendly pension statement for one member, using the
fictional sample data and the bundled script. This skill shows how an agent loads
**instructions + a script + a reference file** on demand.

## When to use
- "Generate a pension statement for **M-1003**."
- "Summarise Priya Nair's pension and forecast."
- "Show the retirement projection for member 1002."

## Procedure
1. Identify the member id from the request (look it up by name in
   [members.json](../../../sample-data/members.json) if only a name is given).
2. Run the generator script from the `demos/` folder:
   ```bash
   python .github/skills/pension-statement/scripts/generate_statement.py --member M-1003
   ```
   - The script reads `demos/sample-data/members.json`, computes a simple
     retirement projection, and prints a plain-text statement.
   - Pass `--format json` if the caller wants structured data instead of text.
3. Present the result to the member following the layout in
   [statement-format.md](./references/statement-format.md):
   summary line → savings breakdown → accrued value → retirement forecast → note.
4. Keep all figures exactly as the script returns them. Always include the
   "illustrative, fictional data" note.

## Boundaries
- Do **not** invent members or numbers — only use ids present in the sample data.
- If the member id is not found, say so and list the available ids.
- The projection is a simplified teaching estimate, not an official APS quote.
