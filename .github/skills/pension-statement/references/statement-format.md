# Pension statement — layout reference

Use this layout when presenting the output of `generate_statement.py` to a member.
Keep it warm, plain-language, and in Canadian dollars (CAD).

```
APS PENSION STATEMENT  ·  As of <asOf>
Member: <name> (<id>)

Your pension savings        $<monthlyContribution>/month
  Public      $<public/month-ish split is illustrative>
  Workplace   $...
  Personal    $...

Your accrued pension        $<accruedValue>
  Public      $<sources.public>
  Workplace   $<sources.workplace>
  Personal    $<sources.personal>

Your forecast at retirement $<projectedMonthlyPension>/month before tax
  Retiring at age <targetRetirementAge> (in <yearsToRetirement> years)
  Estimated value at retirement: $<projectedValue>

Note: Illustrative figures based on fictional sample data and a simplified
projection. Not an official APS quote. For decisions about your own pension,
contact APS directly.
```

## Formatting rules
- Currency: prefix `$`, group thousands with commas, no decimals for whole dollars.
- Lead with the single most useful number (monthly savings), then detail.
- Never show more precision than the script returns.
- Always end with the illustrative-data note.
