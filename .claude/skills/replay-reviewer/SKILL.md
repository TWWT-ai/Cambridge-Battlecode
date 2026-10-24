---
name: replay-reviewer
description: Review CAMBC replay bundles, platform logs, match summaries, or league CSVs to explain wins and losses and identify actionable bot changes.
---

# Replay Reviewer

Explain how the match was won or lost from recorded evidence, without inventing events.

## Procedure

- Identify the source format, match ID, map, side, versions, and whether logs cover both teams or only our bot.
- Reconstruct a timeline around score swings, camp clear/capture, tribute starts/completions, kills/deaths, gem transfers/losses, recalls, purchases, and altar contests.
- Separate the final score mechanism from contributing factors. Prioritize permanent tributed gems, recoverable carried gems, and deaths over proxy metrics such as damage or camp-clear count alone.
- Attribute a failure only when the record supports it. Mark missing opponent actions or hidden state explicitly.
- Compare the observed play with the bot's intended policy and code path; cite the source file, function, log line, or replay event when possible.
- Rank findings by likely impact, repeatability, confidence, and implementation effort. Recommend one change per experiment where possible.
- Compare candidate and baseline over both sides, multiple maps, and multiple opponents. Do not treat one deterministic match as proof; preserve sample counts and variance.

## Output

Summarize result, decisive timeline, root causes, successful decisions, evidence gaps, and prioritized experiments with measurable success criteria.
