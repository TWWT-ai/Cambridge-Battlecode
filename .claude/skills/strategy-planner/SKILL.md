---
name: strategy-planner
description: Build and compare practical multi-step CAMBC plans for farming, capturing camps, banking gems, fighting, drafting, and buying items. Use for bot strategy or tactical planning.
---

# Strategy Planner

Turn a confirmed game state into a robust plan for the stated objective.

## Procedure

- Read `GameRules.md`, `BotAPICpp (1).md`, and relevant `sdk/cpp/cambc.h` definitions before relying on mechanics, item recipes, champion values, or action timing.
- Generate at least three materially different candidates when the evidence permits: economy-first, contest/pressure, and a hybrid. For a narrow decision, compare the viable alternatives instead of padding the list.
- Score plans using the match objective: expected gems captured and tributed, time to clear/capture, travel cost, camp respawn value, gold earned/spent, champion survival, carried-gem exposure, altar access, opponent contest risk, and round remaining.
- Account for separate clear and capture phases, the five-round capture timer, divided rewards when allies share a region, camp respawns, tribute channel length, interruption rules, and turn order.
- Compare expected value per turn and the risk-adjusted chance that carried gems reach an altar. Do not maximize damage or camp clears as a substitute for winning score.
- Include map geometry, side, spawn routes, altar distance, camp density/value, chokepoints, and current draft. Adapt the roster and route to team size.
- Provide a primary plan, an alternative, and explicit triggers for switching. State what the team should do after a failed camp clear, enemy sighting, lost carrier, blocked altar, or unexpected opponent response.
- Recommend purchases by timing and marginal value. Account for shard stats, emblem thresholds and passives, duplicate-passive rules, gold-bonus stacking, recall, and Tavi's field-buy/sell exception. Verify any disputed recipe in the SDK before stating it.
- Keep recommendations implementable by the current bot architecture: each champion has its own instance; use the documented shared-memory budget for coordination.

## Output

For each candidate, state expected benefit, cost, main failure mode, and evidence. End with the preferred plan, contingency triggers, and the metric that would falsify it in a league or live match.
