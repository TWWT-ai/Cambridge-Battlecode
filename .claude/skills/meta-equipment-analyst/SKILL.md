---
name: meta-equipment-analyst
description: Analyze CAMBC map/meta statistics, team compositions, item builds, shard growth, emblem passives, and gold efficiency. Use when selecting equipment or comparing patch-era strategies.
---

# Meta and Equipment Analyst

Ground build recommendations in current item rules, champion growth, maps, and match results.

## Procedure

- Verify every current mechanic and enum against `GameRules.md`, `BotAPICpp (1).md`, and `sdk/cpp/cambc.h`. When exports disagree, expose the conflict and use executable SDK/source evidence as the tie-breaker.
- Build a per-champion item comparison from base stats, growth per shard, passive, role, expected attack/cast uptime, survival needs, and likely opponent threats.
- Compute shard cost and marginal stat gain; distinguish raw stats from completed-emblem passives. Account for duplicate-family passive non-stacking, any stacking gold bonuses, and Tavi's special shopping rules.
- Treat an emblem recipe or passive as unverified until it is consistent across the handbook and SDK. Do not hide contradictions in a recommendation.
- Compare builds by relevant outcome metrics across maps and sides: tributed gems, time to first capture/tribute, survival/deaths, gold, objective completion, and fight conversion. Damage and clears are explanatory measures, not the win condition.
- Segment results by map, side, team size, lineup, opponent strength, and patch/version. Report sample size and uncertainty; avoid inferring a meta from one match.
- Recommend a default purchase order plus conditions for switching (early contest, high camp damage, fragile gem carrier, low gold, late game, or opponent composition).

## Output

Give a concise build table with purchase order, expected gains, tradeoffs, evidence, and confidence. Flag missing or contradictory data before recommending a supposedly optimal build.
