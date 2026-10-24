---
name: opponent-modeler
description: Infer opponent plans and choose counters from CAMBC drafts, match records, replays, and visible actions. Use when predicting responses or adapting a bot to opponents.
---

# Opponent Modeler

Model only what evidence supports, then choose a safe response to plausible opponent actions.

## Procedure

- Establish the opponent sample: team identity, match dates, maps, sides, draft, versions if known, number of games, and whether records are complete.
- Separate observed behavior from inferred policy. Quantify rates with denominators; mark small or stale samples as weak evidence.
- Look for recurring choices: champion drafts, camp routes, capture assignment, gem carrying and banking, altar contests/locks, recalls, engagement timing, target priority, and equipment purchases.
- Represent uncertainty with a short set of plausible opponent policies rather than a single assumed script.
- For each policy, identify the opponent's likely best response to our route or fight. Compare responses using score, time, exposure, and champion survival; consider mixed or delayed responses when predictable play is exploitable.
- Choose a counter that remains useful across several plausible policies. Do not overfit to one replay or claim knowledge of hidden positions, cooldowns, or gem bags.
- Revisit the model when a patch, map, lineup, or opponent version changes.

## Output

Give evidence and sample size, likely policy, confidence, best response, counter-plan, and the observation that would disconfirm the model. Use a payoff table only when it clarifies real choices and outcomes.
