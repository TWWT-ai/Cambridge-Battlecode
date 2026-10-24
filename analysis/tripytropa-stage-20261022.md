# Tripytropa stage report — 22 October 2026

## Current best

Production remains `bots/tripytropa`. Its corrected map-hybrid build completed 7,710 local matches against 771 runnable bot folders: **1,739 wins (22.55%)**, with **22/771** opponents at 8/10 or better. The requested 8/10 against every opponent is not met. The results use the installed local runner and its older maps/rules, not the uploaded 21 October rules or a live match.

## Follow-up experiments

| Candidate change | Local evidence | Decision |
|---|---|---|
| Tavi follows Ryth on Fragment | 80/100 on a ten-bot Fragment screen, same as production; on the difficult five-map screen, candidate 48/100 vs production 54/100 | Reject |
| Safer Fragment opening; retreat on a one-unit local disadvantage | 80/100 on the same Fragment screen, with no aggregate gain | Reject |
| Tavi Monster Focus on Fragment | 75/100 vs production's 80/100 on the ten-bot Fragment screen | Reject |
| Ryth Jungle Health then Monster Health/Power Strength | 80/100 on the ten-bot screen; 25/100 vs production's 30/100 on the difficult five-map screen; direct Fragment result 5/10 with wins only on one side | Reject |
| Fragment bank threshold 25 | Lost 0/10 direct matches to production | Reject |
| Vendetta Jungle Health on Fragment/Monolith | 10/20 direct matches, with all wins on one side | No demonstrated gain |
| Fragment mid-game at round 150 | 5/10 direct matches, with wins only on one side | No demonstrated gain |
| Monolith earlier retreat threshold | 0/100 against ten difficult local Monolith variants | Reject |
| Force Monolith objective after round 250, solo or full roster | 0/10 direct matches for each variant; full-roster candidate averaged 613 gems against production's 961 | Reject |
| Pick Prism first on five-pick maps | 10/30 direct matches across Contest, Lanes, and Monolith; lost all ten Monolith games | Reject |

The weak ten-bot Fragment screen was not representative of the full pool; many older local candidates beat the fixed roster decisively. No screened variant was promoted and no follow-up full sweep was run. Candidate sources and replay bundles are under `matches/candidates/` and `matches/league/`.

## Diagnosis

Fragment losses are driven by a sustained farm gap and the three-pick roster's limited bodies. On Monolith, sampled losses began near an even early gem race, then the opposing six-body lineup repeatedly killed our five champions and finished near 980–994 gems while we banked roughly 500–700. The fixed requested roster remains unchanged in production. The next useful experiment needs a measurable gain against these harder local proxies before a full folder sweep.
