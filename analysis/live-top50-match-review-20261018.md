# Live top-50 unranked evaluation — 18 October 2026

The authenticated `cambc` 2.2.5 CLI now provides the ladder, unranked match-group, summary, and replay commands. The fresh leaderboard at 03:48 UTC listed Intercontinental Fish at rank 1, Nyxius at rank 2, and FRChronic at rank 43. The supplied FRChronic group happened earlier, when its recorded rank was 58.

## Initial group results

The first two groups below followed test submission v35, based on local candidate #189. Match APIs do not return a submission version, so v35 is the likely but unconfirmed build. Later groups and uploads are recorded chronologically at the end of this report. None of these groups tested the production source.

| Opponent | Rank at test | Group | Maps in group order | Result |
|---|---:|---|---|---:|
| Intercontinental Fish | 1 | [`121522cb-6efa-44bd-bb10-09cff99364cc`](https://2026a.battlecode.co.uk/game/match-groups/121522cb-6efa-44bd-bb10-09cff99364cc) | Swirl, Collision, Lanes, Pilgrimage, Contest | 0–5 |
| Nyxius | 2 | [`8e9423ff-cb43-495c-9a35-43b3afd7a74b`](https://2026a.battlecode.co.uk/game/match-groups/8e9423ff-cb43-495c-9a35-43b3afd7a74b) | Swirl, Collision, Pilgrimage, Contest, Stampede | 1–4 |

The rank-2 group’s only win came on Stampede, in the fifth and final match. Because the preceding four games were losses, the current consecutive-win streak remains **0/10**. Across both top-50 groups, Swirl, Collision, Pilgrimage, and Contest all lost. The repeated failures against two different top teams are stronger evidence than the earlier rank-58 FRChronic group.

## Nyxius replay findings

Full summaries and replays are in [`matches/live/8e9423ff-cb43-495c-9a35-43b3afd7a74b/`](../matches/live/8e9423ff-cb43-495c-9a35-43b3afd7a74b/). Every match reported zero bot faults.

| Map | Gems submitted (HC / Nyxius) | HC deaths / kills | Nyxius deaths / kills | Finding |
|---|---:|---:|---:|---|
| Swirl | 0 / 1056 | 26 / 0 | 0 / 19 | First enemy sightings were by round 9; our first death was round 18. No gems were collected or submitted. |
| Collision | 22 / 1030 | 16 / 0 | 0 / 6 | HC collected 210 but banked only 22; the first two HC deaths were at round 36. |
| Pilgrimage | 388 / 1112 | 11 / 0 | 1 / 6 | HC collected and banked 388; Nyxius collected 1,272. Nyxius earned 6,960 gold and dealt 89.6k monster damage versus HC’s 1,040 gold and 28.2k monster damage. |
| Contest | 0 / 1000 | 97 / 7 | 12 / 77 | HC collected no gems and took 80.4k champion damage. This is a sustained combat wipe plus a complete farming failure. |
| Stampede | 1080 / 720 | 7 / 0 | 2 / 3 | HC won the gem race with the Prism lineup; the opposing draft was Ren/Stellar/Cassi & Issac/Ryth/Varg. |

The repeated top-team draft core was Ren, Stellar, Cassi & Issac, Ryth, and Varg. Candidate #189’s Pilgrimage grouping trigger required a different five-pick combination, so it did not activate against Nyxius. That is a concrete follow-up experiment: test extending the grouped-opening condition to the observed Ren/Stellar/Cassi & Issac/Ryth/Varg draft, while measuring regressions across the full Pilgrimage proxy pool. The Swirl/Collision/Contest deaths need separate defensive and combat-response work; changing equipment alone is not supported by these replays.

## Next evaluation steps

1. Keep the production source and `submissions/tungtungsahur.zip` untouched while the streak is 0/10.
2. Test the Pilgrimage meta-draft trigger locally against the same-position candidate plus the existing strong proxy pool, then validate the result in another unranked top-50 group.
3. On Swirl, Collision, and Contest, prioritize keeping the team alive long enough to collect and bank gems; their current failures show that ordinary local win-rate improvements have not transferred to the top-50 fights.
4. Select a fresh top-50 opponent from the current ladder for each live group. Track wins in match order; losses reset the consecutive streak.

## Mite replay findings

Group [`acd48ac2-d256-4149-af46-10f9492efd04`](https://2026a.battlecode.co.uk/game/match-groups/acd48ac2-d256-4149-af46-10f9492efd04) was created against Mite, rank 3 at the 03:48 UTC ladder check. It finished **0–5**. Full summaries and replays are in [`matches/live/acd48ac2-d256-4149-af46-10f9492efd04/`](../matches/live/acd48ac2-d256-4149-af46-10f9492efd04/); every match reported zero bot faults.

| Map | Gems submitted (HC / Mite) | HC deaths / kills | Mite deaths / kills | Finding |
|---|---:|---:|---:|---|
| Interlock | 336 / 1002 | 12 / 1 | 2 / 5 | HC collected 358 and lost 22 on deaths. Mite's first camp clear was round 9; HC's was round 47. |
| Lanes | 568 / 1008 | 2 / 0 | 0 / 0 | Pure farming race: HC collected 634, but Mite dealt 66.1k monster damage versus HC's 40.8k. |
| Elkring | 324 / 1008 | 16 / 0 | 0 / 13 | HC collected 432; the fight and farm both collapsed after the opening. |
| Stampede | 0 / 1080 | 14 / 1 | 2 / 7 | Both teams drafted Prism/Stellar/Cassi & Issac/Ryth/Tavi. Mite's first camp clear was round 32; HC's first was round 329. |
| Expanse | 628 / 1026 | 2 / 0 | 0 / 0 | Another pure economy loss: Mite's first camp clear and tribute were earlier (rounds 11 and 39, versus HC rounds 29 and 51); monster damage was 62.7k versus 40.8k. |

This 0–5 result shows the current candidate is not yet competitive with the top-three bot. Lanes and Expanse lost without champion kills, which points to farm tempo and camp routing. Stampede lost despite the same draft on both sides and a shared-farm rule; first-camp timing is the clearest specific lead. Interlock and Elkring also suffered repeated champion deaths.

## Rejected local follow-ups

- **#190 Pilgrimage draft trigger:** extending the grouped-opening condition to the observed Ren/Stellar/Cassi & Issac/Ryth/Varg core scored 11/12 versus a fresh #189 control at 12/12 on the same six-opponent Pilgrimage screen. Against the matching `cand-ren-meta` proxy, it fell from 2/2 (average 1,072 gems) to 1/2 (756 gems). Reject; do not upload.
- **#191 Swirl counterdraft:** replacing Varg with Ren on Swirl scored 5/10 versus a fresh #189 control at 6/10. Against the exact-draft meta proxy it scored 1/2 versus 2/2 for control, and both variants still lost both Ming and Xuanming games. Reject; do not upload.

These failures keep the current live streak at **0/10**. The three candidate experiments were local and do not count as wins. The active strategy question is now how to increase safe camp-clear tempo while surviving the top teams' early pressure, especially on Stampede, Lanes, Expanse, and the repeated Swirl/Collision/Contest matchups.

## Candidate v36 Mite rematch

After the Mite result, #192 delayed the dangerous Stampede camp for the first 150 rounds while the team cleared side camps. It kept the same 120/136 strong-proxy score across all 17 maps and raised the full Stampede pool from 35/40 to 36/40. The change traded two wins against `my-bot-v2` for two wins against `Faisal-bot`. Its test ZIP was verified and uploaded separately as version 36; the main source and ZIP were untouched.

The fresh Mite group [`a04404dc-de4c-43da-bc99-95ace05a5057`](https://2026a.battlecode.co.uk/game/match-groups/a04404dc-de4c-43da-bc99-95ace05a5057) still finished **0–5**. Its detailed summaries and replays are in [`matches/live/a04404dc-de4c-43da-bc99-95ace05a5057/`](../matches/live/a04404dc-de4c-43da-bc99-95ace05a5057/). The match API does not expose submission versions; v36 was the newest upload and likely ran. On Stampede, the safety rule worked as intended: HC cleared side camps beginning round 35, versus Mite's first side-camp clear at round 32. But HC kept repeating side camps through round 146 and submitted zero gems, while Mite reached the central gem camp at round 124 and submitted 1,080. The change reduced HC's Stampede deaths from 14 to 9 but did not convert the match.

Follow-up #193 tried to force the central gem camp after round 100. It scored 8/10 against five strong Stampede proxies, below #192's 10/10, so reject it. The remaining route problem is the transition from safe side camps to the central gem source, not simply whether to delay the first contest.

## Procless #4 live group (18 Oct 2026)

The authenticated CLI queued group [`1c2711ed-18c0-4eb9-b890-070ca91db7bd`](https://2026a.battlecode.co.uk/game/match-groups/1c2711ed-18c0-4eb9-b890-070ca91db7bd) against Procless, ranked #4 at the current ladder check. It finished **0–5** on Swirl, Collision, Contest, Pilgrimage, and Lanes. The match API does not expose the selected submission version; v36 was the latest test upload before this group and is the likely build. Summaries and downloaded match bundles are in [`matches/live/1c2711ed-18c0-4eb9-b890-070ca91db7bd-matches/`](../matches/live/1c2711ed-18c0-4eb9-b890-070ca91db7bd-matches/). Every match had zero bot faults.

| Map | Gems submitted (HC / Procless) | HC deaths / kills | Procless deaths / kills | Replay finding |
|---|---:|---:|---:|---|
| Swirl | 124 / 1,004 | 17 / 2 | 3 / 12 | HC collected first at r35 and banked at r41, but early deaths began r18; Procless won the sustained fight. |
| Collision | 66 / 1,032 | 18 / 1 | 1 / 7 | First gem collection was r79 for HC versus r21 for Procless; first bank r84 versus r36. |
| Contest | 0 / 1,000 | 58 / 7 | 11 / 45 | HC never collected gems. It dealt 25.5k monster damage versus Procless's 187.3k and received 53.0k champion damage. |
| Pilgrimage | 466 / 1,010 | 12 / 2 | 3 / 7 | Initial collection was close (r55 HC, r57 Procless), but Procless later dealt 79.0k monster damage versus HC's 23.4k. |
| Lanes | 590 / 1,010 | 2 / 0 | 0 / 1 | First collection was r57 HC versus r53 Procless; monster damage was 42.5k versus 70.3k. This was primarily a farm-tempo loss. |

This group confirms three distinct problems: early combat losses on Swirl and Contest, a severe opening delay on Collision, and lower sustained camp damage on Pilgrimage/Lanes. Future map checks should compare camp and tribute event timing as well as final gems.

## Procless #4 re-test with v37-like candidate (#198)

The follow-up group [`4a2bd4ac-4623-4896-8e3f-d8d026845e71`](https://2026a.battlecode.co.uk/game/match-groups/4a2bd4ac-4623-4896-8e3f-d8d026845e71) also finished **0–5** with zero bot faults. v37 was the latest upload at queue time and is the likely build; the public API does not expose version IDs. Match bundles and summaries are in [`matches/live/4a2bd4ac-4623-4896-8e3f-d8d026845e71-matches/`](../matches/live/4a2bd4ac-4623-4896-8e3f-d8d026845e71-matches/).

On Collision, the safety rule fixed the opening delay: HC's first camp clear/collection/bank were r10/r19/r41, compared with Procless r14/r21/r61. The match still ended 22–1,002: HC had 14 deaths, 0 kills, and lost 204 carried gems; Procless had 0 deaths and 10 kills. Monster damage was 18.6k versus 53.0k. The other four maps repeated the previous group’s results (Swirl 124–1,004, Contest 0–1,000, Pilgrimage 466–1,010, Lanes 590–1,010). This shifts the Collision problem from arriving late to surviving the fight after arrival. The top-50 streak remains **0/10**.

## Rank #5 map test and Fragment draft follow-up (18 Oct 2026)

Group [e47c4b9b-0440-4152-bae7-e8912b1de243](https://2026a.battlecode.co.uk/game/match-groups/e47c4b9b-0440-4152-bae7-e8912b1de243) tested the latest upload at queue time, v37, likely, against new team(4), ranked #5. It lost 0–5 with no platform-reported bot faults. Replay logs contained caught failed-action messages: one occupied-destination rejection on Ambush and one cannot-act rejection on each other map. The bot caught those exceptions in its action wrapper and continued.

| Map | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Main cause |
|---|---:|---:|---:|---:|---|
| Ambush | 404 / 1,024 | 0 / 0 | 0 / 0 | 28.4k / 49.5k | Pure farm-economy loss; no champion contact. |
| Corners | 416 / 1,012 | 4 / 1 | 1 / 4 | 31.4k / 64.8k | Both combat and farming gaps. |
| Eight | 99 / 1,019 | 17 / 1 | 1 / 12 | 27.4k / 52.1k | Early combat losses compound the farm deficit. |
| Fragment | 314 / 1,004 | 22 / 4 | 4 / 14 | 20.5k / 74.6k | Severe sustained fight and farm deficit. |
| Rushbait v2 | 168 / 1,006 | 9 / 0 | 0 / 8 | 25.9k / 53.8k | The team farmed and fought less effectively. |

Monster damage was about half the opponent's on four maps and under a third on Fragment. First bank alone did not predict the result: HC banked earlier on Ambush, Fragment, and Rushbait, yet still lost the later gem race.

Local candidate #201 let Varg farm solo camps during the early phase while the rest of the team worked Ryth's camp. It scored 113/136 against the four strong proxies, below the #198 control's 120/135 (one failed control run); Collision fell from 6/8 to 4/8 and Pilgrimage from 8/8 to 5/8. Reject #201.

Candidate #202 changes only Fragment's three-pick draft to Varg / Stellar / Ryth, the compact lineup observed from the rank-5 team. On the same 16-opponent Fragment screen it scored 28/32 twice versus 23/32 twice for the control. Across the 17-map four-strong screen it scored 122/136 with zero failed runs; the control was 120/135 with one failed Elkring run. The only completed-map win-count improvement was Fragment, from 7/8 to 8/8.

Candidate #202 was uploaded separately as test submission v38. The follow-up group [62c8cd21-f213-4d3d-983d-6afc4e1f2a16](https://2026a.battlecode.co.uk/game/match-groups/62c8cd21-f213-4d3d-983d-6afc4e1f2a16) again lost 0–5. Its Fragment replay used the Varg / Stellar / Ryth draft, but finished 215–1,001 with 12 deaths, 0 kills, and 22.9k monster damage versus 0 deaths, 11 kills, and 66.5k monster damage. The draft selector transferred, but the local win-rate gain did not transfer into a live win; the farming gap remains. The other four map selectors were unchanged.

The user-provided [FRChronic group](https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67) is a separate 17 Oct result: 0–5 on Interlock, Stampede, Elkring, Fragment, and Pilgrimage. FRChronic was rank 58 around that match, so it does not count as a top-50 group. The live consecutive-win streak remains **0/10**.

## Rank #6 AlphaSlop live test (18 Oct 2026)

Group [d97d6f55-8e2e-4bde-8b41-87988484d5e1](https://2026a.battlecode.co.uk/game/match-groups/d97d6f55-8e2e-4bde-8b41-87988484d5e1) likely used test v38, the latest upload at queue time. It lost 0–5 on Packs, Monolith, Rows, Ambush, and Fragment.

| Map | Gems submitted HC / AlphaSlop | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---|
| Packs | 188 / 1,028 | 15 / 1 | 1 / 11 | 11.5k / 55.9k | Same four-body roster, but far lower farm output and repeated deaths. |
| Monolith | 534 / 1,026 | 4 / 0 | 0 / 4 | 38.3k / 68.7k | Farming and combat both behind. |
| Rows | 528 / 1,056 | 0 / 0 | 0 / 0 | 39.4k / 68.9k | Pure farm race; no champion contact. |
| Ambush | 404 / 1,024 | 0 / 0 | 0 / 0 | 26.3k / 55.0k | Pure farm race; no champion contact. |
| Fragment | 259 / 1,045 | 14 / 1 | 0 / 14 | 23.9k / 73.0k | The v38 Varg / Stellar / Ryth draft still lost badly to a four-body C&I / Ryth / Stellar core. |

This independent rank-6 group reinforces the repeated sustained farm-damage gap. The new Fragment lineup matched the rank-5 draft but did not counter AlphaSlop's different roster. The top-50 streak remains **0/10**.

## Rank #7 Sneaky Bush Campers live test (18 Oct 2026)

Group [dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d](https://2026a.battlecode.co.uk/game/match-groups/dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d) likely used v38 and lost 0–5 on Stampede, Expanse, Lanes, Interlock, and Elkring.

| Map | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---|
| Stampede | 0 / 1,080 | 23 / 10 | 7 / 12 | 73.2k / 127.4k | We collected 1,080 but banked none; deaths lost the bags. |
| Expanse | 518 / 1,014 | 2 / 0 | 0 / 0 | 33.1k / 62.1k | Pure farm race. |
| Lanes | 524 / 1,002 | 3 / 1 | 0 / 2 | 36.8k / 66.8k | Large sustained farm deficit. |
| Interlock | 364 / 1,032 | 18 / 2 | 1 / 12 | 29.4k / 64.9k | Farming and combat both collapsed. |
| Elkring | 450 / 1,026 | 16 / 3 | 2 / 13 | 45.7k / 82.4k | Farming and combat both behind. |

The output gap persists across more top-10 teams: three maps were mostly economy losses; two added heavy deaths. Stampede again shows that collecting gems does not help unless carriers survive and bank. The live streak remains **0/10**.


## Candidate v39 live retests (18 Oct 2026)

Candidate v39 combines the v38 Fragment draft (Varg / Stellar / Ryth) with an Ambush-only shared opening through round 149, switching to the normal mid-game split at round 150. The CLI submitted it as version 39 immediately before these groups; public match metadata omits submission versions, so v39 is likely, not confirmed. The candidate ZIP is `submissions/tungtungsahur-candidate-v39-ambush150-fragment-meta-unranked-test.zip` (25,735 bytes, SHA-256 `257e4d8266834a401c39e9ed6b7b270306b5ebd21b35612be9d2dd62e1bd21ce`).

The four focused groups against ranks 5, 6, 9, and 10 all lost 0–5, with zero platform-reported bot faults in the downloaded summaries:

| Queue-time rank / group | Map | Gems HC / opponent | Deaths | Kills | Monster damage HC / opponent |
|---|---|---:|---:|---:|---:|
| #5 new team(4), `4cd803e3-96d4-4273-b81f-e14ae750f69f` | Ambush | 596 / 1,012 | 4 / 0 | 0 / 1 | 35.4k / 55.1k |
|  | Corners | 278 / 1,026 | 6 / 1 | 1 / 5 | 23.3k / 62.8k |
|  | Eight | 99 / 1,019 | 17 / 1 | 1 / 12 | 27.4k / 52.1k |
|  | Fragment | 215 / 1,001 | 12 / 0 | 0 / 11 | 22.9k / 66.5k |
|  | Rushbait v2 | 284 / 1,002 | 11 / 0 | 0 / 8 | 28.9k / 55.4k |
| #6 AlphaSlop, `801d7bd3-12fd-4241-84b6-99c508a82261` | Packs | 188 / 1,028 | 15 / 1 | 1 / 11 | 11.5k / 55.9k |
|  | Monolith | 534 / 1,026 | 4 / 0 | 0 / 4 | 38.2k / 68.7k |
|  | Rows | 528 / 1,056 | 0 / 0 | 0 / 0 | 39.4k / 68.8k |
|  | Ambush | 476 / 1,024 | 2 / 0 | 0 / 0 | 31.6k / 55.0k |
|  | Fragment | 259 / 1,045 | 14 / 1 | 0 / 14 | 23.9k / 73.0k |
| #9 Boost, `e77d3f95-04e7-4f6b-b649-b850b1b789e1` | Ambush | 702 / 1,068 | 2 / 0 | 0 / 0 | 46.9k / 63.4k |
|  | Fragment | 132 / 1,026 | 13 / 1 | 0 / 11 | 21.2k / 66.1k |
|  | Stampede | 0 / 1,008 | 9 / 0 | 0 / 4 | 24.8k / 42.2k |
|  | Expanse | 398 / 1,026 | 4 / 1 | 1 / 1 | 29.4k / 64.4k |
|  | Swirl | 0 / 1,068 | 29 / 1 | 1 / 22 | 4.5k / 84.4k |
| #10 Univardisty of Shingtonwash, `5a9d7c5c-4fba-4ec5-a6fa-6c56de1c656b` | Ambush | 462 / 1,062 | 5 / 0 | 0 / 2 | 33.5k / 71.5k |
|  | Fragment | 190 / 1,012 | 17 / 6 | 4 / 16 | 21.9k / 70.7k |
|  | Contest | 0 / 1,000 | 86 / 7 | 5 / 71 | 15.6k / 205.4k |
|  | Pilgrimage | 272 / 1,036 | 18 / 3 | 1 / 12 | 22.9k / 60.6k |
|  | Collision | 44 / 1,000 | 15 / 0 | 0 / 10 | 16.0k / 55.2k |

The Ambush opening banked earlier against rank 5: 72 gems at round 99 versus the opponent's first 106 at round 120. The team reached 178 by round 144, then Cassi and Issac died to camps at round 145. The score stayed at 178 until round 404; Issac later died carrying 106 gems. Across v39 Ambush matches against ranks 5, 6, 9, and 10, banked totals were 596, 476, 702, and 462. Better opening timing did not produce enough sustained farm or kills.

Five more v39 groups against queue-time ranks 11–15 also finished 0–5 each: invisibleAgain (`58adeaed-c8a4-47c8-aad6-5382a3357009`), EMPEROR Tung (`303a1e24-15c6-4579-935d-253bed027393`), VeryGood (`a29c5c00-df0c-44dc-9bcb-e5a542d4c614`), PTN Hyperion (`4f8c181d-cffc-4244-9dbd-21584c402674`), and Let's LARP (`34814bcf-4dfa-434f-8b45-ea57cd3d78f1`). Each group included Ambush and Fragment. Their downloaded Ambush score traces repeat the round-100 72-gem first deposit, followed by opponent catch-up.

At the 55-match checkpoint, groups against queue-time ranks 17 and 18 had also finished 0–5: Shawn (`65b11a0e-7118-41ed-93ee-da58a7da890c`) and Ely2sh (`92156a5d-0de0-40ad-a5f5-5306275bb557`). The groups against ranks 19–29 were still queued or running at that point. The later completion update below supersedes that interim tally.

The corrected local round-150 Ambush test (#209) won 40/40 against the 20-opponent Ambush pool with 6 deaths, versus 37/40 and 28 deaths for a fresh #203 control. The integrated build with the Fragment draft scored 120/136 on the four-strong, 17-map screen; the fresh #202 control scored 122/136. Both scored 8/8 on Ambush in that smaller set. #210 excluded Ambush camps above 100 strength; it fell to 34/40 and 49 deaths versus #209's 40/40 and 6 deaths. Reject #210. Local run IDs and hashes are in `bots/tungtungsahur/PLAN.md`.


## Candidate v39 result update — ranks 19–29 (18 Oct 2026)

All v39 groups through queue-time rank 29 have now finished. There are **110 completed matches and 2 wins**: a Fragment win against Ad Astra (#26) and a Fragment win against 剑桥夜爬者 (#29). The other 108 matches were losses. Completion timestamps show a maximum streak of **one win** and a current streak of **zero**: the #26 win was followed by a loss, the #29 win was preceded by a loss, and the final #29 Expanse match was another loss. The target remains 10 consecutive wins.

Both wins used the v38/v39 Fragment draft Varg / Stellar / Ryth. Against Ad Astra, HC submitted 1,014 gems to the opponent's 276, with 7 deaths to 14, 8 kills to 7, and 53.1k monster damage to 51.2k. Against 剑桥夜爬者, HC submitted 1,006 to 598, with 14 deaths to 23 and 14 kills each; monster damage was 61.1k to 63.4k. Neither match had platform-reported bot faults. These wins support the Fragment draft against these two teams, while the other live Fragment matches remain losses.

Their results were not consecutive. The #26 Fragment win finished at 05:06:20.323 UTC; a rank-27 Ambush loss followed at 05:06:20.599 UTC. A rank-28 Fragment loss finished at 05:06:25.900 UTC before the #29 Fragment win at 05:06:26.768 UTC. The final #29 Expanse loss finished at 05:06:27.422 UTC.

The next groups to test are ranks 30–50. At the last quota check the CLI reported 29/30 used, with reset at 05:20:02 UTC; continue polling existing results and wait for quota reset before creating more groups.

## Current-rank #30 KKB live test (18 Oct 2026)

Group [45c52751-c4fa-4377-8db3-11f8fa2958a0](https://2026a.battlecode.co.uk/game/match-groups/45c52751-c4fa-4377-8db3-11f8fa2958a0) tested the latest upload at queue time (v39 likely; match metadata does not expose submission version) against KKB, rank #30 in the 05:10 UTC ladder snapshot. All five matches finished as losses with zero platform-reported bot faults. On Fragment, our Varg / Stellar / Ryth draft faced Ren / Cassi & Issac / Stellar.

| Map | Gems submitted HC / KKB | Deaths HC / KKB | Kills HC / KKB | Monster damage HC / KKB | Finding |
|---|---:|---:|---:|---:|---|
| Fragment | 483 / 1,013 | 14 / 11 | 6 / 14 | 52.3k / 66.7k | The Fragment draft improved combat relative to many other maps but still lost on kills and gems. |
| Ambush | 702 / 1,058 | 2 / 0 | 0 / 0 | 36.1k / 59.0k | Farming loss without champion contact. |
| Corners | 776 / 1,002 | 8 / 11 | 7 / 6 | 49.5k / 79.2k | We traded kills evenly but fell behind in both damage and gems. |
| Eight | 330 / 1,118 | 14 / 0 | 0 / 7 | 34.2k / 66.9k | Combat collapse compounded the farm gap. |
| Rushbait v2 | 722 / 1,006 | 18 / 4 | 2 / 11 | 45.5k / 72.5k | Excess deaths and lower camp damage erased our collected gems. |

This is a further 0–5 group and does not extend the win streak: campaign total is now 2 wins in 115 matches, maximum streak one, current streak zero. The repeated structural issue is monster damage below the opponent on every map. Match summaries are `match-3d3556a9-8fcf-4d84-a9bc-dd6e540f691b.json`, `match-14ddf754-efea-4ef3-9bc2-5a29a1502c0b.json`, `match-53db3270-2bc9-46cf-bbc2-6fddf505c36e.json`, `match-01d0a362-ea56-4fe0-84a6-9e789344b35a.json`, and `match-c6bb5fe7-0538-421a-a5d0-87cee4c9010e.json`.

## Current-rank #31 umamusume live test (18 Oct 2026)

Group [9cbc69c6-f4e8-4c04-b072-290f6f30c15d](https://2026a.battlecode.co.uk/game/match-groups/9cbc69c6-f4e8-4c04-b072-290f6f30c15d) tested the latest upload at queue time (v39 likely) against umamusume, rank #31 in the 05:20 UTC ladder snapshot. It finished 0–5 with zero platform-reported bot faults.

| Map | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---|
| Fragment | 387 / 1,013 | 20 / 6 | 6 / 19 | 42.2k / 65.7k | Severe combat loss on the compact Varg / Stellar / Ryth draft. |
| Ambush | 702 / 1,024 | 4 / 3 | 0 / 1 | 42.1k / 86.9k | Farm race with no meaningful kills; damage gap is extreme. |
| Packs | 260 / 1,008 | 17 / 5 | 3 / 12 | 15.9k / 54.5k | Farming and survival both collapsed. |
| Monolith | 394 / 1,010 | 8 / 0 | 0 / 8 | 32.6k / 64.3k | Opponent won the wolf farm and fight without deaths. |
| Rows | 594 / 1,056 | 0 / 0 | 0 / 0 | 39.4k / 77.0k | Pure farming loss; no champion contact. |

The campaign total is now 2 wins in 120 completed matches; maximum consecutive streak one, current streak zero. The downloaded summaries are `match-01ec8db3-4196-4919-b93b-2d465276e666.json`, `match-28763d63-0219-407c-afab-b5b1a04133d4.json`, `match-a5f71ad2-8d32-40ec-bfa6-96c0f4c1f4ae.json`, `match-200af05c-703d-4dd8-96ba-915c4af27b22.json`, and `match-7ca24790-d13f-4686-a555-2f4d38bcdebf.json`.

## Queue-time rank #31 Master of Betas live test (18 Oct 2026)

Group [59a3ce77-5499-46cc-92a7-5150bf8aa647](https://2026a.battlecode.co.uk/game/match-groups/59a3ce77-5499-46cc-92a7-5150bf8aa647) tested the latest upload at queue time (v39 likely) against Master of Betas, rank #31 in the 05:23 UTC ladder snapshot. It finished 0–5 with zero platform bot faults.

| Map | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---|
| Fragment | 350 / 1,020 | 21 / 11 | 6 / 20 | 29.1k / 80.8k | Severe fight and farm gap. |
| Ambush | 298 / 1,058 | 5 / 2 | 1 / 2 | 33.3k / 61.7k | Low farm output without decisive combat. |
| Stampede | 0 / 1,080 | 18 / 21 | 11 / 8 | 27.6k / 108.5k | We collected gems, but all were lost before submission. |
| Expanse | 376 / 1,006 | 2 / 0 | 0 / 0 | 29.8k / 61.7k | Pure farming deficit. |
| Swirl | 36 / 1,058 | 29 / 7 | 2 / 20 | 12.3k / 81.2k | Near-total combat collapse. |

After this group the campaign has 2 wins in 125 completed matches; maximum consecutive run is one and current streak remains zero. Match summaries: `match-d52bfa81-e24a-4298-9969-c9083589faa9.json`, `match-32b4dbc5-7d01-4a81-9610-1c5084715d8d.json`, `match-067b8eac-7e94-4390-a56b-80833e2d0e90.json`, `match-a5c921fa-faad-49d3-b348-25a01c1db8a4.json`, and `match-616748ec-d014-42f1-9195-110f76cd7969.json`.

## Queue-time rank #33 Memory? live test (18 Oct 2026)

Group [f2fe8162-ae57-4b93-9a73-738c00502d39](https://2026a.battlecode.co.uk/game/match-groups/f2fe8162-ae57-4b93-9a73-738c00502d39) tested the latest upload at queue time (v39 likely) against Memory?, rank #33 in the 05:24 UTC ladder snapshot. It finished 0–5 with zero platform bot faults.

| Map | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---|
| Fragment | 234 / 1,026 | 14 / 0 | 0 / 14 | 28.5k / 65.9k | Combat loss ended the match before our farm could matter. |
| Ambush | 702 / 1,024 | 2 / 1 | 0 / 0 | 46.9k / 63.4k | Farm race loss despite the improved round-150 opening. |
| Contest | 0 / 0 | 121 / 1 | 1 / 99 | 8.8k / 99.7k | Extreme combat collapse; neither team submitted gems. |
| Pilgrimage | 524 / 1,036 | 7 / 2 | 1 / 4 | 43.3k / 71.2k | Both farm and combat lagged. |
| Collision | 176 / 1,016 | 14 / 1 | 1 / 10 | 21.9k / 54.1k | Severe fight and farm deficit. |

This brings the campaign to 2 wins in 130 completed matches; maximum streak one and current streak zero. Contest ran to round 2,000 with no gems collected or submitted by either team; the standard timer tiebreak was lifetime gold, 11,775 for Memory? versus 575 for HC, followed by kills at 99–1. This was a combat/survival collapse, not a distinct Contest win condition. Raw summaries are `match-73ea0c7f-12dd-48d4-a442-f5c84ae5c4c5.json`, `match-54492159-6d69-4c3f-b69e-c08cb7fac20e.json`, `match-ceb9fa10-c3c6-4ba4-8e29-1c823aa01b75.json`, `match-6ec281d4-812b-4ece-9f52-bf06f19d0c06.json`, and `match-bc54434c-f373-4379-b14a-61371f9fc47f.json`.

## Queue-time rank #26 Cabbage — v40 live test (18 Oct 2026)

Group [8da6a23e-ca78-4e29-bf01-61152c1bd182](https://2026a.battlecode.co.uk/game/match-groups/8da6a23e-ca78-4e29-bf01-61152c1bd182) finished 0–5 against Cabbage, rank #26 at queue time. It was queued immediately after test submission v40; public match data omits submission version, so v40 is likely but cannot be confirmed from the API. All five maps had zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Contest | 200 / 200 | 0 / 200 | 93 / 6 | 4 / 63 | 30.3k / 189.3k | Retreat did not stop the early fight collapse. First team deaths: Issac and Cassi at round 42, both to enemy Cassi. We were at 0 submitted gems when the 2,000-round limit ended. |
| Swirl | 72 / 1,034 | 36 / 1,034 | 31 / 5 | 4 / 23 | 13.9k / 84.5k | Severe combat and farm deficit; only half of our collected gems were banked. |
| Fragment | 124 / 1,020 | 124 / 1,020 | 18 / 2 | 2 / 18 | 14.4k / 76.3k | The Varg / Stellar / Ryth Fragment lineup still lost the fight and farm race. |
| Ambush | 928 / 1,158 | 928 / 1,086 | 2 / 2 | 0 / 0 | 50.4k / 79.5k | No deaths or kills; we banked what we collected but were 230 gems behind. |
| Stampede | 120 / 1,440 | 120 / 1,320 | 19 / 11 | 8 / 9 | 28.5k / 73.9k | Low collection plus a large monster-damage gap; 120 opponent gems were still unbanked. |

The group brings the top-50 live campaign to 2 wins in 135 matches, maximum consecutive streak 1, current streak 0/10. In the Contest replay, our bot saw the enemy group by round 30 and lost two champions by round 42; later enemy kills reached 63 to our 4. Team A's captured stdout contains eight caught `Champion cannot act` errors on Contest (first at round 65), three on Swirl, one on Fragment, and one `Known occupied destination` error on Ambush. Earlier replay forensics classify error 44 as crowd control/stun, so those failed actions reflect enemy control; error 22 indicates a blocked move destination. Platform diagnostics report zero bot faults in every match. The retreat tweak alone is not enough for Contest. Match summaries are `match-a3fa8220-a6ef-45ff-8de6-9398608aaf82.json`, `match-0f4268c1-3bd8-4123-aa44-98de493b2df5.json`, `match-e98f61f3-d57a-4f74-89de-6a0460495b5a.json`, `match-19e783f9-ef27-4422-979d-70d0be7d1481.json`, and `match-d1fe5e42-e3da-494e-900d-2091a2f53555.json`. The replay/debug archive is `matches/live/8da6a23e-ca78-4e29-bf01-61152c1bd182-unpacked/`.

## Queue-time rank #29 Still Testing — v40-likely live test (18 Oct 2026)

Group [bd89f7c3-e3df-4103-97bd-e012f1570c80](https://2026a.battlecode.co.uk/game/match-groups/bd89f7c3-e3df-4103-97bd-e012f1570c80) finished 0–5. It was queued after test submission v40; the public API omits the exact version. There were zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Corners | 218 / 1,028 | 72 / 1,028 | 4 / 0 | 0 / 3 | 18.4k / 71.0k | Lost 146 collected gems before banking; enemy also had much more gold. |
| Eight | 716 / 1,282 | 526 / 1,034 | 12 / 5 | 4 / 5 | 41.5k / 73.4k | Behind in both farm and combat; opponent left 248 gems unbanked. |
| Pilgrimage | 484 / 1,000 | 484 / 1,000 | 15 / 3 | 2 / 10 | 30.7k / 58.1k | Severe combat and farming deficit despite banking every gem we collected. |
| Rows | 528 / 1,122 | 528 / 1,056 | 0 / 0 | 0 / 0 | 38.7k / 71.9k | Pure farm-rate loss, with 66 opponent gems still carried. |
| Rushbait v2 | 554 / 1,058 | 416 / 1,014 | 6 / 3 | 2 / 4 | 34.5k / 64.2k | Lower farm output and 138 of our collected gems lost before submission. |

All five maps had lower monster damage and lower earned gold. This brings the tracked v39/v40 top-50 campaign to 2 wins in 140 games, max streak 1, current streak 0/10. Raw summaries are `match-1042c632-c00c-4aec-9bd3-525b68bdfc40.json`, `match-fa42995c-d287-4c08-912e-b94cf332718b.json`, `match-84cf4340-dc79-404e-9b4c-61ec498845f4.json`, `match-8ffd6515-db0f-4d8f-bd03-2eb9c8ca149d.json`, and `match-d0bbd93d-7e53-41d0-b2df-26e398a8e676.json`.

## Queue-time rank #34 EggsAfter11AM — v40-likely live test (18 Oct 2026)

Group [e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1](https://2026a.battlecode.co.uk/game/match-groups/e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1) finished 0–5 against EggsAfter11AM, rank #34 in the latest ladder read. It was queued after test submission v40; the exact submitted version is not exposed. The group had zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Monolith | 592 / 1,076 | 526 / 1,032 | 6 / 2 | 2 / 2 | 36.0k / 65.4k | Opponent won the farm race with fewer deaths; both teams lost some carried gems. |
| Elkring | 396 / 1,080 | 216 / 1,044 | 18 / 1 | 1 / 13 | 34.0k / 77.9k | Severe survival and combat loss; most of our collected gems were lost before banking. |
| Interlock | 358 / 1,010 | 292 / 1,010 | 17 / 0 | 0 / 11 | 31.0k / 54.5k | Opponent farmed more, banked all gems, and won every champion fight. |
| Lanes | 540 / 1,024 | 474 / 1,002 | 4 / 0 | 0 / 3 | 36.2k / 63.1k | Lower farm output despite low deaths; the opponent still banked nearly all collected gems. |
| Collision | 314 / 1,002 | 102 / 1,002 | 16 / 1 | 1 / 12 | 19.3k / 53.0k | Combat collapse and lost carried gems compounded a large farm deficit. |

The opponent did 2.0–2.8 times our monster damage on each map and earned 1.9–3.8 times our gold. In the Elkring and Collision purchase records, enemy carries and frontline champions commonly completed Power Focus/Strength emblems, then bought Durability Health shards and an emblem; jungle-oriented champions also bought Jungle Health. This is a useful build observation, not proof that Durability caused the outcome. Experiment #137 already changed Issac's second emblem to Durability Health and tied the #133 control at 54/68 strong-proxy games, so do not repeat that global change. A role- and map-specific test would need a fresh local comparison first.

This group brings the live top-50 campaign to 2 wins in 150 matches, maximum consecutive wins 1, current streak 0/10. Raw summaries are `matches/live/match-d9b2e98c-c510-476e-a881-74c9e5452558.json`, `matches/live/match-0ad56a73-4c15-4ecd-8fd6-cccffbf9b368.json`, `matches/live/match-c4e77d65-563f-40c2-ae9d-0db58706d965.json`, `matches/live/match-ab256ff3-4036-4e2b-8f80-2aa621ddbcf2.json`, and `matches/live/match-86106700-f72f-4849-ba5e-b25e09fe133e.json`; the group replay archive is `matches/live/e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1-matches`.

## Queue-time rank #15 Zarzorki — v40-likely live test

Group [deec6df3-1b7f-438d-9221-70e00a5a4591](https://2026a.battlecode.co.uk/game/match-groups/deec6df3-1b7f-438d-9221-70e00a5a4591) finished 0–5 against Zarzorki, rank #15 at queue time and previously untested by team ID in this campaign. It was queued after test submission v40; the API does not expose the exact version. All five matches had zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Fragment | 336 / 1,070 | 204 / 1,048 | 21 / 10 | 10 / 20 | 26.9k / 65.7k | The local Fragment draft transferred no win here; lower farm and combat both contributed. |
| Ambush | 702 / 1,092 | 702 / 1,092 | 2 / 2 | 1 / 0 | 41.9k / 80.6k | Pure farm-rate loss with no deaths advantage; the opponent did almost twice our monster damage. |
| Contest | 0 / 1,000 | 0 / 1,000 | 77 / 5 | 3 / 64 | 3.7k / 187.0k | #216 retreat did not prevent another early fight collapse. Our first five deaths were Ryth r40, Stellar r48, Issac and Cassi r50, and Prism r56. |
| Elkring | 288 / 1,188 | 90 / 1,062 | 23 / 3 | 2 / 16 | 22.2k / 85.3k | Severe combat loss plus 198 of our collected gems lost before banking. |
| Rows | 528 / 1,056 | 528 / 1,056 | 0 / 0 | 0 / 0 | 38.7k / 74.3k | Another pure farm-rate loss with no champion contact. |

This brings the live top-50 campaign to 2 wins in 155 matches; maximum consecutive wins remains 1, current streak 0/10. Contest's 77–5 deaths and 3.7k–187.0k monster damage show that a local full-pool win-rate improvement did not transfer against this top-50 opponent. Rows and Ambush repeat the noncombat farm deficit. Raw summaries are `matches/live/match-880f2a7c-05e1-4eca-9d1d-5b4a625a6089.json`, `matches/live/match-700dab6e-ae81-43a4-a185-a9cdac46c43a.json`, `matches/live/match-66190a8e-61ce-412f-b4d8-48989d96703f.json`, `matches/live/match-53914f3d-4d9f-4f0f-9617-5caab88aadb0.json`, and `matches/live/match-7e07767d-7dbf-4b4f-8e99-8db48d51b6d9.json`.

## Queue-time rank #31 SilverSamurai — v40-likely live test

Group [bfadbe71-52dd-41fc-9d3f-3fda1e00e13d](https://2026a.battlecode.co.uk/game/match-groups/bfadbe71-52dd-41fc-9d3f-3fda1e00e13d) finished 0–5 against SilverSamurai, rank #31 at queue time and previously untested by team ID. It used five maps not in the immediately preceding Zarzorki group. All five matches had zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Expanse | 540 / 1,346 | 518 / 1,106 | 2 / 0 | 0 / 0 | 33.1k / 75.4k | Pure farm-rate loss with low deaths; we lost 22 carried gems before banking. |
| Lanes | 714 / 1,090 | 648 / 1,010 | 3 / 0 | 0 / 3 | 46.0k / 70.2k | Farm gap remained despite modest losses of carried gems. |
| Packs | 420 / 1,032 | 396 / 1,032 | 17 / 7 | 4 / 12 | 22.4k / 57.9k | Both farm and combat fell behind; 24 collected gems were lost before banking. |
| Monolith | 636 / 1,150 | 548 / 1,062 | 6 / 0 | 0 / 5 | 42.9k / 70.1k | No kills and a farm gap; both teams lost 88 carried gems. |
| Swirl | 108 / 1,342 | 72 / 1,078 | 25 / 10 | 2 / 18 | 12.6k / 83.3k | Severe fight and farm collapse; opponent also held 264 gems at the end. |

All five maps again had lower HC monster damage and earned gold. Expanse, Lanes, and Monolith were mostly no-contact farm losses; Packs and Swirl also had substantial combat losses. The live campaign is now 2 wins in 160 matches, maximum consecutive wins 1, current streak 0/10. Raw summaries are `matches/live/match-443f6964-016f-4765-8b70-d71204561e13.json`, `matches/live/match-b4d7a588-3e2b-4473-b410-71be7e1803ff.json`, `matches/live/match-3c085c0a-fdf6-48ea-8793-f8f6282612da.json`, `matches/live/match-4b880501-4b32-4252-87aa-07d1e88f0eee.json`, and `matches/live/match-65ec5e93-1e53-4434-b637-1d46fab4dae0.json`; the group archive is `matches/live/bfadbe71-52dd-41fc-9d3f-3fda1e00e13d-matches`.

## Queue-time rank #35 conqueror_of_openai — v40-likely live test

Group [a40b7063-19c9-47f9-af57-a7420f12bd3f](https://2026a.battlecode.co.uk/game/match-groups/a40b7063-19c9-47f9-af57-a7420f12bd3f) finished 0–5 against conqueror_of_openai, rank #35 at queue time and previously untested by team ID. All five matches had zero platform-reported bot faults.

| Map | Gems collected HC / opponent | Gems submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Corners | 688 / 1,072 | 666 / 1,014 | 5 / 4 | 4 / 4 | 50.9k / 68.9k | Closest race; comparable champion results but lower farm output. |
| Eight | 528 / 1,108 | 528 / 1,036 | 12 / 1 | 1 / 8 | 38.4k / 69.9k | Farm and combat deficits; we banked all gems collected. |
| Pilgrimage | 640 / 1,104 | 640 / 1,036 | 5 / 4 | 3 / 4 | 27.2k / 78.7k | No gem loss, but opponent's monster damage was almost three times higher. |
| Interlock | 380 / 1,054 | 336 / 1,032 | 17 / 0 | 0 / 11 | 31.1k / 61.6k | Severe combat and gem-retention loss. |
| Collision | 582 / 1,254 | 336 / 1,002 | 10 / 1 | 1 / 8 | 32.2k / 64.7k | Combat losses caused a 246-gem gap between collection and deposits. |

This raises the campaign to 2 wins in 165 top-50 matches, maximum consecutive wins 1, current streak 0/10. Monster damage remained below the opponent's on all maps, including Corners where kills and deaths were even. Raw summaries are `matches/live/match-17e6affa-5107-445b-b774-884f31eae85f.json`, `matches/live/match-d43d0cb1-2e5e-4f7d-a092-dac2cacd9f3e.json`, `matches/live/match-56153e48-000d-4983-900a-c8edda0d5645.json`, `matches/live/match-d1053358-efee-4d7f-8734-54407428b171.json`, and `matches/live/match-e5d950b9-fa88-4380-a69e-fa421e1485d6.json`; replay archive: `matches/live/a40b7063-19c9-47f9-af57-a7420f12bd3f-matches`.
 
## Queue-time rank #26 hello — live test (18 Oct 2026)

Group [`f99f5297-0fb7-41b5-a255-c1a523b8875f`](https://2026a.battlecode.co.uk/game/match-groups/f99f5297-0fb7-41b5-a255-c1a523b8875f) finished 0–5. The CLI match-group API exposes result/draft metadata but not champion timeline statistics, so these are the last periodic team-A SCORE lines and counts of captured SCOUT DEATH events from each downloaded match bundle. They are replay indicators, not platform match-summary fields.

| Map | Result | Last logged score HC / opponent | Captured HC death events | Early observation |
|---|---|---:|---:|---|
| Fragment | Loss | 55 / 929 at r560 | 14 | Ryth died r20; Stellar r47. |
| Elkring | Loss | 414 / 972 at r475 | 11 | First logged death Stellar r54; Tavi r222. |
| Monolith | Loss | 424 / 996 at r430 | 8 | Tavi died r133; Issac and Cassi r179. |
| Contest | Loss | 0 / 800 at r2000 | 121 | First deaths Cassi r31, Issac r32, Prism r35; early fight collapse recurred. |
| Eight | Loss | 99 / 947 at r405 | 21 | Ryth died r66; Stellar r82. |

The captured team-A stdout contained no ERROR or EXC lines. The group followed v40's upload, but exact submission version is not reported by the API.

## Queue-time rank #28 Ad Astra — live test (18 Oct 2026)

Group [`6c43fd4a-7925-4eb6-be94-04d82d790b37`](https://2026a.battlecode.co.uk/game/match-groups/6c43fd4a-7925-4eb6-be94-04d82d790b37) finished 1–4. Figures are the last periodic team-A SCORE lines and captured SCOUT DEATH event counts from the replay bundles.

| Map | Result | Last logged score HC / opponent | Captured HC death events | Finding |
|---|---|---:|---:|---|
| Monolith | Loss | 518 / 906 at r505 | 14 | Combat deaths and a large score gap. |
| Lanes | Loss | 620 / 890 at r510 | 9 | Tavi died r93; Issac and Cassi r101. |
| Expanse | Loss | 518 / 988 at r525 | 2 | Almost no logged champion deaths; this is the clearest open-map farm-rate loss. |
| Packs | Loss | 448 / 976 at r495 | 15 | Early deaths began with Issac and Cassi r108. |
| Fragment | Win | 992 / 276 at r800 | 7 | Decisive win in the last logged score snapshot. |

The group followed v40's upload, but exact submission version is not reported by the API.

## Queue-time rank #27 剑桥夜爬者 — live test (18 Oct 2026)

Group [`cf11e290-56c3-43a1-b170-721b79739d79`](https://2026a.battlecode.co.uk/game/match-groups/cf11e290-56c3-43a1-b170-721b79739d79) finished 0–5. Figures below are the last periodic team-A SCORE lines and captured SCOUT DEATH event counts from the replay bundles.

| Map | Result | Last logged score HC / opponent | Captured HC death events | Finding |
|---|---|---:|---:|---|
| Elkring | Loss | 270 / 990 at r540 | 23 | Combat and farm deficits. |
| Rushbait v2 | Loss | 438 / 892 at r755 | 10 | The team fell behind over a long farm window. |
| Contest | Loss | 0 / 800 at r1700 | 67 | Issac and Cassi died r33; another severe early fight collapse. |
| Pilgrimage | Loss | 368 / 980 at r750 | 21 | Combat losses accompanied the farm deficit. |
| Lanes | Loss | 584 / 942 at r420 | 3 | Only three logged deaths; score gap points to route throughput. |

The recorded campaign is now 3 wins in 180 live top-50 games, maximum consecutive streak 1, current streak 0/10. Captured stdout from these latest groups had no ERROR or EXC lines. Exact server submission versions remain unconfirmed. Replay bundles are `matches/live/f99f5297-0fb7-41b5-a255-c1a523b8875f-matches`, `matches/live/6c43fd4a-7925-4eb6-be94-04d82d790b37-matches`, and `matches/live/cf11e290-56c3-43a1-b170-721b79739d79-matches`.

## Candidate #219 — open-map farm split rejected

Candidate #219 enabled the mid-game role split from round 1 on Expanse, Lanes, and Rows. It scored 22/24 against four local opponents; a fresh v40 control scored 23/24 on the identical paired screen. Candidate/control average gems were Expanse 1,014/1,039, Lanes 993/1,011, and Rows 1,013/1,016. Reject it; no live upload or production change.
 
## Queue-time rank #35 Trzy Kwaterki — live test (18 Oct 2026)

Group [`43b3cc32-aefa-4852-938c-1bc1c02e4004`](https://2026a.battlecode.co.uk/game/match-groups/43b3cc32-aefa-4852-938c-1bc1c02e4004) finished 0–5. Figures are last periodic team-A SCORE lines and captured SCOUT DEATH event counts from the downloaded bundles.

| Map | Result | Last logged score HC / opponent | Captured HC death events | Finding |
|---|---|---:|---:|---|
| Elkring | Loss | 378 / 990 at r460 | 16 | Large score gap plus combat losses. |
| Collision | Loss | 584 / 988 at r815 | 18 | Long match with substantial combat losses. |
| Corners | Loss | 526 / 976 at r525 | 7 | Farm gap with limited deaths. |
| Ambush | Loss | 688 / 928 at r685 | 5 | Mostly a farm race. |
| Monolith | Loss | 504 / 946 at r370 | 3 | Mostly a farm race. |

## Queue-time rank #36 glyph-name team — live test (18 Oct 2026)

Group [`dabc9ca4-b6f6-432c-b9da-2ff3782a2311`](https://2026a.battlecode.co.uk/game/match-groups/dabc9ca4-b6f6-432c-b9da-2ff3782a2311) finished 0–5. Figures are last periodic team-A SCORE lines and captured SCOUT DEATH event counts from the downloaded bundles.

| Map | Result | Last logged score HC / opponent | Captured HC death events | Finding |
|---|---|---:|---:|---|
| Monolith | Loss | 548 / 968 at r460 | 7 | Mostly a farm deficit. |
| Elkring | Loss | 252 / 972 at r450 | 18 | Farm and combat collapse. |
| Ambush | Loss | 476 / 914 at r575 | 8 | Farm gap despite limited deaths. |
| Corners | Loss | 402 / 966 at r490 | 7 | Farm gap with limited deaths. |
| Pilgrimage | Loss | 692 / 908 at r815 | 15 | Extended combat and farm deficits. |

These groups followed the v40 upload, but exact server submission versions are not exposed. The tracked campaign is 3 wins in 190 live top-50 games, maximum consecutive streak 1, current streak 0/10. Replay archives: `matches/live/43b3cc32-aefa-4852-938c-1bc1c02e4004-matches` and `matches/live/dabc9ca4-b6f6-432c-b9da-2ff3782a2311-matches`.

## Local follow-up candidates #220–222 — all rejected

#220 (Stellar buys Monster Strength first on Expanse) tied v40 at 8/8 against four proxies but averaged 1,011 vs 1,039 deposited gems. #221 (early role split on Expanse/Lanes/Rows while preserving early combat posture) scored 21/24 vs v40's 23/24 and yielded lower average gems on all three maps. The initial recursive #221 implementation crashed and is excluded; the corrected run is the valid comparison. #222 (Contest retreats when outnumbered by one within eight tiles) scored 39/40 on the full local pool vs fresh v40 at 40/40. None were uploaded.

## Queue-time rank #37 Stubborn Gold Clusters and rank #38 Valenki (18 Oct 2026)

Stubborn Gold Clusters group [`d9280c23-6ca6-4ed4-909b-efffbc129de7`](https://2026a.battlecode.co.uk/game/match-groups/d9280c23-6ca6-4ed4-909b-efffbc129de7) finished 0–5. Captured team-A scoreboard snapshots and death events were: Eight 446–992 at r490 / 17 deaths; Rushbait v2 394–928 at r650 / 9; Corners 394–908 at r430 / 4; Rows 528–990 at r380 / 0; Monolith 564–994 at r500 / 6. Rows is another clean farm-rate loss with no recorded deaths.

The next group, [`e67a83d6-499e-4ab2-bb85-30b776ae3fff`](https://2026a.battlecode.co.uk/game/match-groups/e67a83d6-499e-4ab2-bb85-30b776ae3fff), was queued against Valenki, rank #38 at queue time, and finished 0–5. Match summaries and replay archives are saved under [`matches/live/e67a83d6-499e-4ab2-bb85-30b776ae3fff/`](../matches/live/e67a83d6-499e-4ab2-bb85-30b776ae3fff/). Each pair below is Heavenly Court / Valenki.

| Map | Rounds | Collected gems | Submitted gems | Deaths / kills | Monster damage | Earned gold | Finding |
|---|---:|---:|---:|---:|---:|---:|---|
| Expanse | 571 | 562 / 1,202 | 562 / 1,082 | 2/0 / 0/0 | 36,960 / 72,850 | 1,970 / 4,280 | Farm-rate loss; we banked everything and dealt no champion damage. |
| Lanes | 461 | 634 / 1,060 | 612 / 1,038 | 5/0 / 0/3 | 41,709 / 67,902 | 2,670 / 4,460 | Farm gap plus deaths and no kills; first Cassi/Issac deaths at r155. |
| Rows | 438 | 594 / 1,122 | 594 / 1,056 | 1/0 / 0/1 | 41,388 / 72,900 | 2,535 / 4,640 | Farm-rate loss with almost no combat; all HC-collected gems were banked. |
| Contest | 1,296 | 0 / 1,000 | 0 / 1,000 | 45/19 / 10/33 | 26,620 / 171,881 | 1,270 / 9,170 | Severe early collapse; first Cassi/Issac deaths at r109, then repeated deaths; no gems collected. |
| Fragment | 647 | 482 / 1,070 | 344 / 1,048 | 12/7 / 4/12 | 33,085 / 71,165 | 2,575 / 5,100 | Both farm and combat deficit; HC lost 138 collected gems before banking. |

All five matches reported zero bot faults. The current live submission's drafts were still the older Stellar / Cassi & Issac / Varg lineup; this group did not test the isolated user-roster candidate #223. Exact server submission version remains unavailable in group metadata. After this group the tracked campaign stands at 3 wins in 200 top-50 matches, maximum streak 1, current streak 0/10. The recurring low-death losses on Expanse and Rows confirm a farm-throughput problem independent of combat; Contest remains a separate survival failure.

## Fixed user roster candidate #223 — local screen rejected for live use

Candidate #223 implements the requested fixed picks (Tank / Fighter / Marksman for three-pick maps, adds Support for four, and all five for five-pick maps) with Tavi as the gold carry. It scored 28/40 on a five-map local size screen versus fresh v40 at 39/40, with lower average gems on all five maps: Expanse 984/1,039; Lanes 960/1,011; Rows 928/1,016; Contest 625/950; Fragment 857/1,022. Keep the candidate isolated while improving its economy and accounting for paired picks that field two bodies (Cassi & Issac); it was not uploaded for the Valenki group.

## Queue-time rank #39 EvilMangohh — live test (18 Oct 2026)

Group [`ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b`](https://2026a.battlecode.co.uk/game/match-groups/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b) finished 0–5 against EvilMangohh, rank #39 at queue time. Full summaries and replays are under [`matches/live/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b/`](../matches/live/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b/). Each pair is Heavenly Court / EvilMangohh.

| Map | Rounds | Submitted gems | Deaths / kills | Monster damage | Earned gold | Finding |
|---|---:|---:|---:|---:|---:|---|
| Stampede | 616 | 360 / 1,080 | 6/0 / 0/2 | 34,269 / 81,317 | 1,660 / 5,080 | Farm throughput deficit; HC banked all it collected. |
| Swirl | 771 | 180 / 1,026 | 33/13 / 6/23 | 20,037 / 92,473 | 1,660 / 7,000 | Early collapse began with Ryth r22, Stellar r36, and Cassi/Issac r38. |
| Packs | 556 | 236 / 1,008 | 20/0 / 0/14 | 14,856 / 60,428 | 530 / 3,990 | Combat loss plus very low camp income; 48 collected gems were lost before banking. |
| Ambush | 688 | 284 / 1,000 | 7/1 / 1/4 | 33,622 / 66,074 | 1,010 / 4,770 | Mostly a farm-rate loss despite low HC deaths. |
| Pilgrimage | 668 | 388 / 1,000 | 12/3 / 2/8 | 26,902 / 76,818 | 1,285 / 5,475 | Farm and combat deficits; 92 collected gems were lost before banking. |

All five matches reported zero bot faults. Stampede, Ambush, and Pilgrimage repeat the lower farm-damage pattern; Swirl and Packs add severe combat losses. The Swirl opponent used Cassi & Issac / Stellar / Ryth / Ren, a composition that does not trigger the current narrow Swirl retreat counterdraft. Exact server submission version is not exposed; the group followed the v40-likely submission. The live campaign is now 3 wins in 205 top-50 matches, maximum consecutive streak 1, current streak 0/10.

## Local candidates #224–226 after the rank-39 review

#224 adds Swirl's observed C&I / Stellar / Ryth / Ren lineup to the narrow early-retreat counterdraft. On Swirl against seven local opponents it tied the fresh v40 control at 8/14, with identical per-opponent win counts; against `opp-swirl-meta-core` it averaged 1,024 gems versus 1,058 for control. Reject.

#225 changes the fixed-roster equipment progression to balance Strength and Health. It tied fixed-roster #223 at 28/40 on the four-strong-opponent, five-map screen. Gains were map-specific (Lanes 7/8 vs 5/8); Expanse fell to 4/8 from 6/8, while Rows and Contest remained 4/8 and 7/8 with fewer average gems. Reject as a general item plan.

#226 changes only Vendetta's fighter queue to Monster Strength, Power Strength, Power Health, then Power Strength. It scored 30/40 vs #223 at 28/40 on the same 40-game local screen, including one additional Lanes and Rows win, but averaged 869 gems vs 871 and remained well below the fresh v40 39/40 reference. Keep it isolated; do not upload. Run folders: `matches/league/20261018-072804-cand-swirl-counterdraft-224-src-direct-live-rank39-swirl-response-224`, `matches/league/20261018-072811-cand-contest-parity-retreat-216-src-direct-live-rank39-swirl-response-224-control`, `matches/league/20261018-072913-cand-fixed-roster-225-balanced-items-src-direct-fixed-roster-balanced-items-225-screen`, `matches/league/20261018-072926-cand-fixed-roster-223-src-direct-fixed-roster-balanced-items-225-control`, and `matches/league/20261018-073019-cand-fixed-roster-226-fighter-items-src-direct-fixed-roster-fighter-items-226-screen`.

## Fixed-roster test submission v41 — queue-time rank #46 天使

Group [`112d14b4-4b01-4ef0-b1fd-011dd07c8f6b`](https://2026a.battlecode.co.uk/game/match-groups/112d14b4-4b01-4ef0-b1fd-011dd07c8f6b) finished 0–5 against 天使, rank #46 at queue time. It was created immediately after separate test submission v41 and the drafts match candidate #226's fixed roster; the API does not expose the exact version. Full replays and summaries are under [`matches/live/112d14b4-4b01-4ef0-b1fd-011dd07c8f6b/`](../matches/live/112d14b4-4b01-4ef0-b1fd-011dd07c8f6b/). All metrics below are Heavenly Court / 天使.

| Map | Rounds | Collected gems | Submitted gems | Deaths | Kills | Monster damage | Earned gold | Finding |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Expanse | 631 | 562 / 1,016 | 562 / 1,016 | 3 / 0 | 0 / 0 | 32.5k / 68.0k | 1,970 / 4,290 | Farm-rate loss; first Vendetta death r97. |
| Lanes | 489 | 582 / 1,060 | 582 / 1,038 | 4 / 2 | 0 / 4 | 40.3k / 62.1k | 2,470 / 4,510 | Farm gap plus no kills; Willow died r86, Prism r108. |
| Rows | 404 | 462 / 1,122 | 462 / 1,056 | 0 / 0 | 0 / 0 | 28.6k / 68.9k | 1,890 / 4,590 | Pure farm-rate loss with no deaths. |
| Contest | 1,321 | 0 / 1,000 | 0 / 1,000 | 71 / 3 | 2 / 71 | 5.8k / 190.7k | 205 / 11,700 | Severe opening collapse; first Ryth r44, Prism/Willow r46, Vendetta r48, Tavi r52. |
| Fragment | 629 | 212 / 1,034 | 168 / 1,012 | 11 / 1 | 0 / 10 | 24.2k / 65.7k | 1,125 / 5,375 | Combat and farm deficit; 44 collected gems lost before banking. |

No platform bot faults occurred. 天使 drafted Cassi & Issac on all five maps, giving it one extra champion body against the fixed roster on every map (4 vs 3 bodies on three-pick maps, 5 vs 4 on Rows, and 6 vs 5 on five-pick maps). The farm deficit persisted on Expanse and Rows even without deaths, while Contest had an extreme combat collapse. Campaign: 3 wins in 210 live top-50 matches, max consecutive streak 1, current 0/10.

## Follow-up local item screens #228–229

#228 changed Issac to Power Strength -> Power Health -> Power Strength. It scored 124/136 versus fresh v40 at 125/136 on the 17-map, four-strong-proxy screen; reject. #229 changed Stellar to Power Focus -> Durability Health -> Power Focus and scored 113/136 vs 125/136; reject. Neither was uploaded.

Fixed-roster heal-priority variant #227 tied #226 locally at 30/40 with identical per-opponent outcomes. It was uploaded separately as v42 and tested against OneTap (#47) in group [`83c42928-b082-4ca7-a423-aadb3ce617ae`](https://2026a.battlecode.co.uk/game/match-groups/83c42928-b082-4ca7-a423-aadb3ce617ae); the group finished 0–5. All five matches reported zero platform bot faults.

| Map | Rounds | Gems collected/submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---|
| Expanse | 564 | 526 / 1,010 | 3 / 0 | 0 / 2 | 24.8k / 69.2k | Large farm-rate deficit despite few deaths. |
| Lanes | 482 | 524 / 1,038 | 4 / 1 | 0 / 4 | 36.1k / 71.4k | Roughly half the monster damage and no kills. |
| Rows | 400 | 462 / 1,056 | 0 / 0 | 0 / 0 | 28.4k / 68.9k | Clean farm-rate loss without combat. |
| Contest | 1,072 | 0 / 1,000 | 32 / 5 | 2 / 32 | 18.4k / 145.0k | Severe combat collapse and no deposits. |
| Fragment | 651 | 212 / 1,004 | 14 / 2 | 1 / 13 | 15.6k / 76.3k | Combat loss plus very low farming. |

The OneTap drafts included Cassi & Issac on Expanse, Lanes, Rows, and Contest, giving the opponent an extra body on four maps; Fragment had three bodies per side. The low-death Expanse and Rows results still point to a route/clear-throughput problem independent of combat. Contest and Fragment add a separate fight-survival gap. Across the completed top-50 campaign: 3 wins in 215 matches, maximum consecutive streak 1, current streak 0/10. Summaries and replays are under `matches/live/83c42928-b082-4ca7-a423-aadb3ce617ae/`.

## Rank #47 E=mc²+AI³ — v43-likely group

Group [`cfe10790-872f-4df1-9664-863139501d2d`](https://2026a.battlecode.co.uk/game/match-groups/cfe10790-872f-4df1-9664-863139501d2d) followed the separate v43 candidate upload. The group API omits the exact version, so label it v43-likely. It finished 0–5 with zero platform bot faults.

| Map | Rounds | Collected/submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Gold HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---:|---|
| Contest | 1,282 | 0 / 1,000 | 25 / 16 | 10 / 19 | 50.8k / 121.6k | 2,180 / 6,118 | No gems collected; combat and farming gap. |
| Expanse | 484 | 384 / 1,036 | 2 / 0 | 0 / 0 | 24.2k / 61.1k | 1,400 / 3,810 | Low-death farm-rate loss. |
| Rows | 409 | 462 / 1,056 | 0 / 0 | 0 / 0 | 29.5k / 70.7k | 1,890 / 4,590 | Pure farm-rate loss. |
| Lanes | 455 | 466 / 1,020 | 3 / 1 | 1 / 3 | 36.5k / 64.7k | 2,020 / 4,360 | Banked all gems collected; output lagged. |
| Fragment | 654 | 256 / 1,001 | 14 / 5 | 2 / 13 | 22.1k / 74.0k | 1,100 / 5,775 | Combat, carrying, and farm deficit. |

The Contest replay and `analysis/map-dumps/contest.txt` identify a specific objective-selection failure. On this map only Monolith groups #0 and #1 award gems (200 each); other groups award gold only. The bot repeatedly cleared gold-only groups #3/#4/#2 and never cleared either Monolith. The opponent captured Monolith #0 at about r387 and #1 at about r675, then banked its first 200 gems at r431. Current selection adds 0.25× gold to early Contest camp value, discounts Monolith value by 80%, and marks groups above 100 strength off-limits before late game. This explains why the supposedly safer opening never generated gems. Immediate Monolith access (#234) and a late staged switch (#239) both regressed the local full Contest pool; prioritize a full-team safe objective test rather than another broad aggressive unlock.

Campaign after this group: 3 wins in 220 top-50 matches, max consecutive streak 1, current streak 0/10. The user-supplied FRChronic group [`4cf7ad87-2c52-452e-a9a3-59787c302e67`](https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67) was rechecked; it remains the old 17 Oct 0–5 group against rank-58 FRChronic and does not count.

## Rank #50 WHIM — v44-likely live test

Candidate #245 was uploaded as separate submission v44; the group API does not expose exact versions, so [`a5faf63f-bd4e-400c-8eaa-8da44f2d77c3`](https://2026a.battlecode.co.uk/game/match-groups/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3) is v44-likely. WHIM was rank 50 at queue time. The group lost all five maps with zero platform bot faults.

| Map | Rounds | Collected/submitted HC / WHIM | Deaths HC / WHIM | Kills HC / WHIM | Monster damage HC / WHIM | Gold HC / WHIM |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 1,502 | 0/0 / 1,000/1,000 | 64/6 | 4/58 | 12.4k/230.3k | 445/14,060 |
| Expanse | 694 | 548/406 / 1,092/1,070 | 5/2 | 1/3 | 28.0k/63.8k | 1,860/3,930 |
| Rows | 448 | 528/462 / 1,056/1,023 | 0/0 | 0/0 | 35.5k/74.8k | 2,160/4,740 |
| Lanes | 445 | 336/278 / 1,056/1,012 | 8/0 | 0/7 | 24.8k/62.4k | 1,400/4,560 |
| Fragment | 677 | 212/212 / 1,070/1,026 | 18/7 | 4/18 | 13.9k/79.3k | 1,075/6,025 |

On Contest the first death was Ryth at round 34 to a camp, then Willow at 54, Vendetta at 68, and Prism at 71. The round-450 Monolith switch happened too late to prevent the opening collapse. WHIM drafted Cassi & Issac / Stellar / Ren / Varg / Ryth; it cleared Monoliths while the fixed roster dealt only 12.4k monster damage and collected no gems. Expanse banked 406 from 548 collected (the other 142 gems were lost); Rows was a no-death but pure farm-rate loss; Lanes and Fragment added combat losses. Exact replay artifacts and downloaded summaries are in `matches/live/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3/`.

Candidate #245's local Contest score was 31/40 vs #233 at 33/40; its 820 vs 645 mean gems did not improve wins. On five maps against four proxies it scored 29/40 vs 31/40 and averaged roughly 924 vs 879 deposited gems. Candidate #246 scored 32/40 on Contest but only 28/40 integrated. The current live campaign after WHIM is 3 wins / 225 top-50 matches, max consecutive streak 1, current streak 0/10. Return to the prior meta lineup for the next local experiment; do not promote #245 or #246.


## Rank #47 WHIM — v45-likely group

Submission v45 was the older meta control (#248), selected after it scored 40/40 on local Contest proxies and 197/200 across the five-map proxy screen. The exact submitted version is not exposed in group metadata; this group was queued immediately after upload. WHIM drafted C&I / Stellar / Ren / Varg / Ryth on all five maps. Group [`c559fb26-1c62-44cf-b7ea-32116ca9acdb`](https://2026a.battlecode.co.uk/game/match-groups/c559fb26-1c62-44cf-b7ea-32116ca9acdb) lost 0–5 with zero bot faults.

| Map | Rounds | Collected / banked HC / WHIM | Deaths HC / WHIM | Kills HC / WHIM | Monster damage HC / WHIM | Gold HC / WHIM |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 1,939 | 400 / 0 vs 1,200 / 1,000 | 98 / 28 | 19 / 79 | 12.6k / 256.9k | 2,020 / 16,140 |
| Expanse | 680 | 628 / 508 vs 1,076 / 1,018 | 8 / 1 | 1 / 3 | 38.1k / 65.8k | 2,290 / 3,980 |
| Rows | 466 | 660 / 616 vs 1,122 / 1,056 | 2 / 0 | 0 / 2 | 43.4k / 76.9k | 2,805 / 5,110 |
| Lanes | 498 | 452 / 452 vs 1,044 / 1,000 | 12 / 3 | 0 / 8 | 35.4k / 69.3k | 1,900 / 4,760 |
| Fragment | 700 | 270 / 226 vs 1,136 / 1,034 | 14 / 2 | 2 / 14 | 22.8k / 75.9k | 1,225 / 5,950 |

Our Contest draft was Prism / Stellar / C&I / Ryth / Tavi; WHIM drafted C&I / Stellar / Ren / Varg / Ryth. The scout log records the first death at round 30: our Ryth was killed by WHIM's Stellar in the central fight. Our team eventually collected 400 gems but submitted none, while WHIM banked 1,000. The fight snowballed to 98 deaths vs 28 and 19 kills vs 79; camp damage was 12.6k vs 256.9k. The other maps also show a farm-throughput gap, especially Rows, which lost with only two deaths. Full per-match summaries, scout output, fuel logs, and replay files are under `matches/live/c559fb26-1c62-44cf-b7ea-32116ca9acdb/`.

Local controls do not predict the WHIM matchup: #248 scored 40/40 Contest and 197/200 across five maps, yet lost this live group. Contest draft-only variants were #249 (WHIM lineup, 36/40), #250 (insert Varg, 36/40), and #251 (insert Ren, 37/40). #247 combined the WHIM draft with early Monolith access and scored 21/40. Reject these variants. #252, which changed the Contest retreat threshold to back off when enemies outnumber nearby allies by one, tied #251 at 37/40 and remains rejected.

Campaign after this group: **3 wins in 230 top-50 maps**, maximum consecutive streak 1, current streak **0/10**.


### Follow-up local screens

#252 (WHIM draft plus Contest-only one-enemy retreat) finished 37/40, tying #251 at 37/40 but with different matchup losses. #253 carried the same retreat threshold into the fixed-roster candidate #245 and scored 30/40 vs #245's 31/40. Both are rejected for live promotion.


### Additional local experiments after WHIM

#254 used WHIM's exact map-size draft lineups on all five tested maps, with #248's original bot logic. It scored 188/200 vs the unchanged control at 197/200. #255 changed only Ryth's build to Durability Health -> Jungle Health -> Power Health and scored 29/40 Contest vs #245's 31/40. Both remain isolated and rejected.


## Rank #50 Please — v46 fixed roster and v47 counterdraft

### v46 fixed roster

Candidate #233, uploaded separately as v46 (bundle SHA-256 `C4672FEAD1B7389E2EBA3CE543CEE3300997370274D6FEC44D4BD3437D9E4251`), lost all five maps to Please. Please drafted Cassi & Issac on each map, yielding an extra body compared with the same pick count. No bot faults occurred.

| Map | Rounds | Collected / banked HC / Please | Deaths | Kills | Monster damage HC / Please | Gold HC / Please |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 2,000 | 0 / 0 vs 0 / 0 | 79 / 11 | 8 / 79 | 7.2k / 183.8k | 820 / 16,690 |
| Expanse | 549 | 504 / 504 vs 1,026 / 1,004 | 2 / 0 | 0 / 0 | 28.2k / 62.4k | 1,720 / 4,090 |
| Rows | 390 | 462 / 396 vs 1,122 / 1,056 | 0 / 0 | 0 / 0 | 28.4k / 68.9k | 1,890 / 4,590 |
| Lanes | 498 | 532 / 532 vs 1,046 / 1,002 | 3 / 2 | 2 / 3 | 36.6k / 66.5k | 2,340 / 4,480 |
| Fragment | 1,064 | 886 / 780 vs 1,352 / 1,028 | 20 / 20 | 11 / 19 | 42.7k / 93.2k | 3,425 / 7,242 |

Contest ended at the 2,000-round limit without either team banking gems. Please's extra damage and kills made the difference. Expanse and Rows were no-contact farm-rate losses.

### v47 map-size counterdraft

Candidate #254 copied Please/WHIM's map-size draft pattern: C&I / Stellar / Ren / Varg / Ryth, shortened to match each map's pick limit. Group [`90e4f06e-29ac-4415-99ed-330d0fcc47ba`](https://2026a.battlecode.co.uk/game/match-groups/90e4f06e-29ac-4415-99ed-330d0fcc47ba) ended 1–4 with no bot faults; the only win was Fragment.

| Map | Rounds | Collected / banked HC / Please | Deaths | Kills | Monster damage HC / Please | Gold HC / Please |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 2,000 | 0 / 0 vs 0 / 0 | 107 / 7 | 4 / 71 | 22.0k / 177.5k | 935 / 15,975 |
| Expanse | 549 | 582 / 582 vs 1,026 / 1,004 | 0 / 0 | 0 / 0 | 29.7k / 62.4k | 1,710 / 4,090 |
| Rows | 390 | 726 / 660 vs 1,122 / 1,056 | 2 / 0 | 0 / 0 | 44.6k / 68.9k | 2,970 / 4,590 |
| Lanes | 464 | 846 / 802 vs 1,044 / 1,008 | 0 / 0 | 0 / 0 | 55.4k / 67.3k | 3,550 / 4,360 |
| Fragment | 1,338 | 1,130 / 1,014 vs 926 / 842 | 36 / 41 | 30 / 23 | 74.7k / 63.2k | 6,250 / 5,634 |

On Fragment, the extra C&I body and matching roles improved farming enough to win. The same draft did not solve Contest, where we still suffered a combat collapse; the three other maps remained farm-rate losses. The local five-map proxy score was 188/200 vs #248 at 197/200, so do not generalize this result beyond Fragment yet. The campaign is **4 wins / 240 top-50 maps**, max streak 1, current **1/10**.


### Candidate #256 local follow-up

The exact map-size counterdraft with a Contest-only one-enemy retreat scored 185/200 on the five-map local pool, below #254 at 188/200. Reject the retreat change; retain #254 as the reference while testing item queues.


## v48 itemization test vs Please — 0–5

Candidate #257 retained the v47 counterdraft and changed fighter/farmer/Issac/Varg queues to Power Strength -> Durability Health -> Power Strength. Group [`25164105-a829-499a-9c3a-1c6da287111f`](https://2026a.battlecode.co.uk/game/match-groups/25164105-a829-499a-9c3a-1c6da287111f) lost all five matches with zero bot faults.

| Map | Rounds | Collected / banked HC / Please | Deaths | Kills | Monster damage HC / Please | Gold HC / Please |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 2,000 | 0 / 0 vs 0 / 0 | 115 / 6 | 3 / 93 | 8.5k / 180.0k | 675 / 17,250 |
| Expanse | 549 | 462 / 462 vs 1,026 / 1,004 | 2 / 0 | 0 / 0 | 27.2k / 62.4k | 1,390 / 4,090 |
| Rows | 390 | 660 / 660 vs 1,122 / 1,056 | 2 / 0 | 0 / 0 | 44.3k / 68.9k | 2,700 / 4,590 |
| Lanes | 466 | 662 / 640 vs 1,008 / 1,008 | 1 / 0 | 0 / 1 | 43.7k / 66.1k | 2,810 / 4,250 |
| Fragment | 750 | 284 / 284 vs 1,020 / 1,020 | 28 / 8 | 6 / 20 | 33.3k / 65.0k | 1,675 / 6,289 |

Compared with v47 using Monster Strength before Power Strength, v48 lost the prior Fragment win (1,014 vs 842 banked) and lowered camp damage on every map. The defensive tier after five Power shards appears too costly on our lower income. Campaign: **4 wins / 245 maps**, current streak **0/10**, maximum 1.


## v49 counterdraft vs Memory? — 0–5

The v49 bundle was byte-identical to v47's exact counterdraft (SHA-256 `FFCBEE0EFBFDCA431C8D4F29D4A591E5FC4D5A1321313CAFCF3D5E9265283380`). It lost all five maps to Memory? (rank 47 at queue time) with zero bot faults. Memory used Varg / Stellar / Ren / Ryth / Tavi on Contest and killed 102 of our team while losing 2; neither team banked gems. Three open maps were pure farm-throughput losses and Fragment combined both farm and combat deficits.

| Map | Rounds | Collected / banked HC / Memory? | Deaths | Kills | Monster damage HC / Memory? | Gold HC / Memory? |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 2,000 | 0 / 0 vs 0 / 0 | 123 / 2 | 2 / 102 | 10.8k / 96.1k | 835 / 11,715 |
| Expanse | 582 | 582 / 582 vs 1,018 / 1,018 | 0 / 0 | 0 / 0 | 33.6k / 65.1k | 1,710 / 4,280 |
| Rows | 460 | 858 / 792 vs 1,122 / 1,023 | 2 / 0 | 0 / 0 | 52.7k / 68.9k | 3,510 / 4,590 |
| Lanes | 367 | 524 / 524 vs 1,034 / 1,012 | 0 / 0 | 0 / 0 | 37.4k / 65.7k | 2,220 / 4,230 |
| Fragment | 883 | 513 / 433 vs 1,208 / 1,026 | 24 / 14 | 9 / 16 | 32.1k / 74.2k | 2,075 / 6,175 |

On Contest, #254's linked C&I pair is a possible liability: losing either body loses both, while Memory's five independent champions remained at 2 deaths and secured 102 kills. The next local test #260 removes C&I only from Contest and uses Memory's single-body lineup. Candidate #258's pure Power Strength queue was 182/200 locally vs #254 at 188/200; reject. Campaign: **4 wins / 250 top-50 maps**, max streak 1, current **0/10**.


### Contest draft-only screen

Candidate #260 replaced C&I with Varg and used five independent champions (Varg / Stellar / Ren / Ryth / Tavi) on Contest. It scored 37/40 vs the #249 C&I lineup at 36/40. V50 lost 0–5 to Memory? (rank 43 at queue time) in group [`3cbf32fc-50b9-4021-a59a-f06ed40fdfd9`](https://2026a.battlecode.co.uk/game/match-groups/3cbf32fc-50b9-4021-a59a-f06ed40fdfd9). Contest used the same five-champion draft on both sides; our Ryth died at round 35 with the whole enemy team close, followed by 102 deaths / 6 kills and 5.6k monster damage vs Memory?'s 6 / 102 and 99.4k. Campaign reached 4/255 maps, current streak 0/10.


## Rank-1 and rank-2 follow-up groups

V50 lost all five maps to Intercontinental Fish (rank 1) in [`39ffefa6-4fc3-447f-b6f2-00779d0c1616`](https://2026a.battlecode.co.uk/game/match-groups/39ffefa6-4fc3-447f-b6f2-00779d0c1616). It had no bot faults. Summary totals:

| Map | Rounds | Banked HC / Fish | Deaths | Kills | Monster damage HC / Fish | Camp clears HC / Fish |
|---|---:|---:|---:|---:|---:|---:|
| Contest | 1,154 | 0 / 1,000 | 55 / 3 | 1 / 55 | 8.0k / 194.0k | 8 / 81 |
| Expanse | 579 | 582 / 1,016 | 0 / 0 | 0 / 0 | 33.0k / 74.7k | 7 / 46 |
| Rows | 354 | 572 / 1,056 | 2 / 0 | 0 / 0 | 40.5k / 68.9k | 10 / 17 |
| Lanes | 460 | 758 / 1,014 | 3 / 3 | 0 / 2 | 49.6k / 73.0k | 31 / 46 |
| Fragment | 539 | 88 / 1,004 | 19 / 4 | 2 / 15 | 18.0k / 62.2k | 8 / 23 |

Expanse and Rows are low-death farm losses; Contest and Fragment combine combat and farm failures. In Contest, the opening composition had five single bodies. Our Varg died first at round 85; the team repeatedly lost its gem bag before banking. Fish cleared 81 camps and banked 1,000 gems while our team cleared 8 and banked none.

V51 (#261) held Ryth in place until a teammate was attacked and deferred early spells. It lost 0–5 again. Contest deaths dropped from 55 to 50, but camp clears fell from 8 to 2 and monster damage from 8.0k to 6.3k; the team still banked zero. The other four map results and metrics were unchanged. Reject the stationary opening.

V52 (#264) changed only Expanse's third pick from Ren to Varg, matching Fish's farm specialist. It still lost 0–5, but the Expanse replay improved to 17 camp clears, 35.4k monster damage, 2,060 earned gold, and 584 banked gems (prior v50: 7 clears, 33.0k damage, 1,710 gold, 582 banked); Fish had 46 clears, 74.7k damage, 4,850 gold, and 1,016 banked. This is one replay and needs more validation.

V52 then lost 0–5 to Mite (current rank 2) in [`729a4de9-1426-4694-94c6-d10335409c67`](https://2026a.battlecode.co.uk/game/match-groups/729a4de9-1426-4694-94c6-d10335409c67). On Contest both teams drafted Varg / Stellar / Ren / Ryth / Tavi, but Mite cleared 128 camps to our 1 and dealt 191.2k vs 2.3k monster damage; it killed our roster 116 times without losing a champion and banked no gems, winning on the round-limit tiebreak. The low-contact maps also showed roughly 1.5–2x less camp damage on our side.

Local screens: c261's Contest hold variant scored 36/40 (baseline c249: 36/40); c262's gold-weight change scored 37/40 but produced the same three losses and identical result logs as c260; c263's full Fish-style Contest lineup scored 32/40 and is rejected; c264's Expanse Varg-third draft scored 40/40 against the local proxy set. Active test submission is v52. Campaign is **4/275 top-50 maps**, max streak 1, current streak **0/10**. Production source and ZIP remain unchanged.

## v54–v56 top-50 groups and fuel investigation (18 Oct 2026)

The supplied FRChronic group `4cf7ad87-2c52-452e-a9a3-59787c302e67` is the older 17 Oct 0–5 result, not a new test. After that check, four current top-50 groups were completed; the API does not identify the exact submission build, so versions are labeled by upload timing:

| Likely test build | Opponent (queue-time rank) | Group | Result |
|---|---|---|---:|
| v54 | Mite (#2) | [`4b8234a2-d733-4c51-9afd-36f34083cca9`](https://2026a.battlecode.co.uk/game/match-groups/4b8234a-d733-4c51-9afd-36f34083cca9) | 0–5 |
| v55 | Intercontinental Fish (#1) | [`cec1cd96-aa83-43ca-bd49-44a419934c15`](https://2026a.battlecode.co.uk/game/match-groups/cec1cd96-aa83-43ca-bd49-44a419934c15) | 0–5 |
| v55 | Nyxius (#3) | [`498ef0e4-dd7c-465e-bccc-263ca9c00c08`](https://2026a.battlecode.co.uk/game/match-groups/498ef0e4-dd7c-465e-bccc-263ca9c00c08) | 0–5 |
| v56 | procless (#4) | [`d0be490a-e1f3-4fca-a5ee-7473d29073db`](https://2026a.battlecode.co.uk/game/match-groups/d0be490a-e1f3-4fca-a5ee-7473d29073db) | 0–5 |

The Mite Rows replay banked 594/1,012 gems with 2/0 deaths, 0/0 kills, 40.5k/68.85k monster damage, and 2,430/4,590 gold. Across the four groups the campaign moved from 4/285 to **4 wins / 305 maps**, max streak 1, current streak **0/10**.

| Opponent | Map | Banked gems HC / opponent | Deaths | Kills | Monster damage | Gold |
|---|---|---:|---:|---:|---:|---:|
| Fish | Contest | 0 / 1,000 | 55 / 3 | 1 / 55 | 8.0k / 194.0k | 610 / 11,017 |
| Fish | Expanse | 584 / 1,016 | 4 / 0 | — | 35.4k / 74.7k | 2,060 / 4,850 |
| Fish | Rows | 572 / 1,056 | 2 / 0 | — | 40.5k / 68.9k | 2,430 / 4,590 |
| Fish | Lanes | 378 / 1,008 | 6 / 2 | — | 32.0k / 64.9k | 1,700 / 4,540 |
| Fish | Fragment | 193 / 1,001 | 20 / 4 | 2 / 15 | 19.5k / 66.2k | 1,225 / 5,375 |
| Nyxius | Contest | 0 / 1,000 | 72 / 4 | 1 / 72 | 9.8k / 285.9k | 470 / 21,373 |
| Nyxius | Expanse | 398 / 1,024 | 2 / 0 | — | 30.85k / 65.0k | 1,790 / 4,800 |
| Nyxius | Rows | 682 / 1,056 | 2 / 0 | — | 48.6k / 68.85k | 3,240 / 4,968 |
| Nyxius | Lanes | 452 / 1,002 | 8 / 1 | — | 33.4k / 67.7k | 2,110 / 5,126 |
| Nyxius | Fragment | 179 / 1,012 | 25 / 4 | 2 / 18 | 13.4k / 78.9k | 1,100 / 6,722 |
| procless | Contest | 0 / 1,000 | 49 / 3 | 1 / 49 | 19.26k / 190.24k | 1,065 / 10,565 |
| procless | Expanse | 318 / 1,012 | 2 / 0 | — | 24.2k / 59.36k | 1,130 / 3,520 |
| procless | Rows | 550 / 1,012 | 2 / 0 | — | 40.5k / 67.5k | 2,430 / 4,320 |
| procless | Lanes | 612 / 1,002 | 2 / 0 | — | 41.7k / 65.4k | 2,670 / 4,290 |
| procless | Fragment | 182 / 1,006 | 20 / 0 | 0 / 15 | 16.5k / 77.9k | 875 / 6,000 |

The official replay event stream reports `fuelExhausted` even when the final match summary reports `botFaults: 0`: exhaustion suspends an action instead of registering a crash. An instrumented local build showed camp-group construction costing roughly 69k fuel on Expanse and 95k on Lanes, followed by expensive ranking across 24 and 42 groups respectively. The repeated cost was the pre-late deep-enemy-side check, which recalculated distances to spawn regions for each group. Collecting spawn coordinates from camp objects saved only about 8k on Lanes and did not solve the Expanse cost, so that shortcut was removed from the clean candidate.

Candidate c276 keeps the original spawn bitboard coordinates. It caches exact Chebyshev distances for rectangular spawn regions and evaluates the expensive side check only after a camp's cheap score can beat the current best. It scored 30/30 against local Faisal-bot, opp-fai-mirror, and opp-tts-v5 on Contest, Expanse, Rows, Lanes, and Fragment (10/10 each), but only 5/10 against a c272 mirror. This does not count toward the live target. It was uploaded separately as test version v57 for the user's fresh group. Do not promote it to production without the 10-win live streak. Production source/ZIP hashes remain unchanged.

## Full-map local comparison after v57 upload

Candidate c276's 17-map, three-proxy screen scored **80/102**; the same c272 control scored **82/102**. c276 changed only a few chaotic individual outcomes and did not improve the aggregate. Experimental c277 used the first spawn point as a cheaper representative; it tied c276 at 80/102 and was rejected because it is less faithful without a measurable gain. Keep v57 as an isolated official test only; do not promote it based on local evidence.

## v57-likely pending group — rank 5

An authorized unranked group was queued after uploading v57 against the current rank-5 team, `new team(4)`: [`79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f`](https://2026a.battlecode.co.uk/game/match-groups/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f). Maps: Contest, Expanse, Rows, Lanes, Fragment. At the last status check all five were queued, with no results yet; the group API does not expose the submission version. Do not count it until complete. Current campaign remains 4/305, streak 0/10.


## Completed v57-likely group and draft-only follow-up

This section supersedes the earlier pending status. Group [`79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f`](https://2026a.battlecode.co.uk/game/match-groups/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f) finished 0–5 vs rank-5 `new team(4)`. Attribution is v57-likely because the CLI did not expose the pinned submission version. Replay bundle and summaries are in `matches/live/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f/`.

| Map | Our draft vs opponent | Submitted gems A:B | Deaths A:B | Monster damage A:B | Earned gold A:B |
|---|---|---:|---:|---:|---:|
| Contest | Varg / Stellar / Ren / Ryth / Tavi vs Varg / Cassi&Issac / Ryth / Stellar / Tavi | 0:1,000 | 69:3 | 2.832k:227.668k | 470:13,560 |
| Expanse | Cassi&Issac / Stellar / Varg vs Varg / Cassi&Issac / Stellar | 398:1,014 | 2:0 | 30.850k:62.450k | 1,790:3,870 |
| Rows | Cassi&Issac / Stellar / Varg / Ren vs Varg / Cassi&Issac / Ryth / Stellar | 660:990 | 2:0 | 44.550k:66.924k | 2,970:4,320 |
| Lanes | Varg / Stellar / Cassi&Issac / Ryth / Ren vs Varg / Cassi&Issac / Ryth / Stellar / Tavi | 444:1,002 | 2:0 | 32.663k:63.745k | 1,880:4,200 |
| Fragment | Cassi&Issac / Stellar / Ren vs Varg / Stellar / Ryth | 248:1,004 | 22:1 | 17.273k:74.077k | 1,175:5,800 |

On low-contact Expanse, Rows, and Lanes, our matched-body rosters generated only about half to two-thirds of their monster damage and submitted fewer gems. Contest began down one body (five vs six), then suffered a total combat collapse. Fragment began up one body (four vs three), yet lost 22 champions to one and fell behind on farm. The pair's Expanse monster damage was 6.5k vs 24.8k; on Rows 8.6k vs 13.8k.

Fuel-event review: each side emitted one `fuelExhausted` event per champion on all five maps, including the linked pair as two bodies; this exact roster-sized pattern also appears in v55/v56. All five summaries show `botFaults=0`. This event count alone does not support the theory that c276's ranking change failed to fix a performance-limiting fuel fault.

Draft experiment c279 copies c276 and mirrors the exposed top-5 picks on Contest, Rows, Lanes, and Fragment. It scored 28/30 vs Faisal-bot, opp-fai-mirror, and opp-tts-v5 on the five-map screen, losing twice on Lanes vs opp-fai-mirror. Direct c279 vs c276 scored 6/10, with average submitted gems 849 vs 761. This is mixed local evidence; keep it isolated pending an official group. Production remains unchanged. Campaign is 4/310, max streak 1, current streak 0/10.


## Candidate follow-up after the rank-5 group

c279 mirrors the exposed top-5 drafts on Contest, Rows, Lanes, and Fragment; it was uploaded as test v58. c280 changed Issac's shop build from tank items to monster/power strength on every map. Its five-map result was 28/30 and gem output trailed c279, so reject the global build. It won the direct Rows and Lanes games but lost both Expanse games.

c281 applies that Issac build only on Rows and Lanes. It scored 29/30 vs the three local proxies on the five-map screen and 7/10 directly against c279, with both Rows and both Lanes wins and average submitted gems 884 vs 865. It was uploaded separately as test v59. The full 17-map screen scored 79/102, however, below c276 at 80/102 and c272 at 82/102 on the same proxy pool. Keep v59 experimental and targeted; do not promote it. The user said they would create the next fresh official group, so do not queue another group before they send it.


## v60 targeted Stellar equipment test

Candidate c282 changes only Stellar's build on Expanse, Rows, and Lanes to buy Monster Focus shards first, then Power Focus. The engine SDK says the Monster Focus emblem gives 10% more camp damage. c282 matched c281 at 29/30 on the five-map proxy screen and lowered opponent gem output vs c281. It beat c281 8/10 directly (average submitted gems 878 vs 788), including both side tests on Expanse, Rows, and Lanes. The full 17-map proxy score was 79/102, unchanged from c281 and slightly below c276 (80) / c272 (82). Uploaded separately as **v60**; targeted experiment only, official result pending. No new group queued.


## Item A/B rejects after v60

c283 extended Stellar's Monster Focus-first sequence to Cassi and Tavi on Expanse/Rows/Lanes. It remained 29/30 on the proxy screen but allowed more enemy gems (about 527 vs c282's 505); direct c283 vs c282 was 4/10 with 764 vs 837 average gems. Reject the wider focus-bonus assignment.

c284 changed only Stellar's first focus item on those maps from Monster to Treasure (same Focus growth, +20% gold instead of +10% camp damage). It scored 29/30 vs proxies but allowed about 555 opponent gems and lost 2/10 to c282 directly, 764 vs 837 average gems. Reject the treasure economy build. Retain Stellar-only Monster Focus for v60 official testing.


## c285 Ryth build reject

c285 gave Ryth Monster/Power Strength on Rows and Lanes instead of health. Proxy score fell to 28/30 from c282's 29/30; both losses were Lanes vs opp-fai-mirror. c285 beat c282 6/10 head-to-head, winning both Lanes sides, but lost on Contest A, Expanse A, Rows A, and Fragment A; average gems were 826 vs 853. Reject as insufficiently robust. v60/c282 remains the latest isolated upload pending the user's official group.


## Cassi/Tavi equipment isolates rejected

c286 assigned Monster Focus first to Cassi only on Expanse/Rows/Lanes. Despite 30/30 proxies, it lost 4/10 against c282 and had average gems 813 vs 829. c287 assigned Monster Focus to Tavi on both Lanes sides; it scored 30/30 proxies, then tied c282 5/10 directly with gems 809 vs 825. Reject both. Keep the tested v60 configuration: Monster Focus on Stellar only for these farming maps, current Tavi side-specific build, and current Cassi mage build.


## c288 Ryth Monster Health variant (18 Oct 2026)

c288 replaces Ryth's usual tank health item sequence with Monster Health then Power Health only on Rows and Lanes, keeping health scaling and adding the monster damage emblem. It scored 30/30 on the five-map proxy screen, converting c282's sole loss (Lanes, side A vs opp-fai-mirror). Across all 17 maps, c288 scored 80/102 vs c282's 79/102; the sole map-total change was Lanes, 5/6 to 6/6. c272 scored 82/102. Direct c288 vs c282 was 5–5, but every side-B game won, so the matchup did not resolve which build is stronger. The candidate package is verified and uploaded separately as v61: submissions/tungtungsahur-candidate-v61-unranked-test.zip (SHA-256 B612154823349BBE8601405B736893B7FD0636499D493A4C7B34D1C347B87878). This remains a Lanes-specific local gain, not production or live result. The user has created a v60 group and will send its link; do not queue another group before reviewing it.

c289 (Monster Health + Jungle Health) and c290 (two Monster Health sets) also swept the five-map proxy screen 30/30, but neither beat c288's 30/30 or improved its opponent gem totals. Their opponent gem totals were higher than c288's against all three proxies. Reject these item variants; keep c288 as the local equipment candidate pending v60's official result.


## v60-likely and v62-likely rank-5 groups (18 Oct 2026)

The user supplied group [`dbdcc65c-cb2f-4b28-850b-5fa691da9e34`](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34), created at 09:18 UTC against rank-5 `new team(4)`. It finished 0–5. Since it preceded the c291/v62 upload, it is v60-likely; the group API does not expose a pinned submission version. All five maps were side A for Heavenly Court. Summaries report zero bot faults on both teams.

| Map | Rounds | Banked gems A:B | Monster damage A:B | Camp clears A:B | Deaths A:B |
|---|---:|---:|---:|---:|---:|
| Rushbait v2 | 512 | 212:1,004 | 33.612k:54.762k | 17:35 | 9:0 |
| Rows | 393 | 594:1,056 | 38.854k:66.924k | 9:16 | 0:0 |
| Lanes | 415 | 560:1,038 | 36.673k:68.033k | 20:47 | 3:1 |
| Eight | 410 | 154:1,024 | 26.630k:50.923k | 6:19 | 19:5 |
| Interlock | 671 | 596:1,032 | 37.166k:72.214k | 15:36 | 17:6 |

Rows is the cleanest diagnostic: no champion damage, kills, or deaths occurred. Event inspection corrects the initial “low-value camps” interpretation: both teams captured the same 66-gem wolf groups. Heavenly Court repeatedly cleared only groups 0 and 2 (at x=18 and x=31 on the north side), for 9 total clears; the opponent cleared its nearby groups 1 and 3 and also group 5 (x=7 on the south side), for 16. Some capture events split one 66-gem reward among multiple allies, so the raw number of collection entries is not the number of camp rewards. The loss is a route/clear-throughput gap: 9 vs 16 group clears, 38.854k vs 66.924k monster damage, and 2,430 vs 4,320 earned gold.

The second group [`a96043a5-af65-4a93-a9af-971d34b1a879`](https://2026a.battlecode.co.uk/game/match-groups/a96043a5-af65-4a93-a9af-971d34b1a879) followed the v62 upload and also finished 0–5 against the same opponent. The exposed picks matched the top-5 lineup on all five maps. API metadata still does not prove the pinned submission version.

| Map | Banked gems A:B | Monster damage A:B | Camp clears A:B |
|---|---:|---:|---:|
| Rushbait v2 | 300:1,020 | 33.316k:54.768k | 19:36 |
| Rows | 594:1,056 | 38.854k:66.924k | 9:16 |
| Lanes | 538:1,008 | 35.860k:67.174k | 19:46 |
| Eight | 132:1,008 | 27.481k:53.971k | 7:19 |
| Interlock | 386:1,004 | 30.742k:62.578k | 15:32 |

Mirroring the lineups did not close the farm deficit. Interlock had a better champion-damage/death balance than the first group but less farming and fewer banked gems; Rows was exactly unchanged. The five replay bundles and JSON summaries are under `matches/live/dbdcc65c-cb2f-4b28-850b-5fa691da9e34*` and `matches/live/a96043a5-af65-4a93-a9af-971d34b1a879*`.

### Rows local follow-ups

The c291 farm selector favors targets at gems per estimated turn and gives the current group a 1.3 stick bonus. Varg's solo selector also rejects fighting groups with strength above 20, which excludes the three-wolf 66-gem packs on Rows. Three isolated Rows experiments were screened against c291, Faisal-bot, opp-fai-mirror, and opp-tts-v5:

- c296 gave Cassi Monster Focus then Power Focus on Rows. It won 7/8 total games, with the only loss against c291; it swept the three proxy bots. Its full 17-map screen tied c291 at 82/102. On Rows, however, candidate average banked gems were lower than the c291 control against all three proxies (1,018 vs 1,040; 1,029 vs 1,045; 1,018 vs 1,040). Reject.
- c297 removed the current-target stick bonus on Rows. It also went 7/8, with no proxy wins beyond the control’s 6/6, and had lower banked gems on each proxy. Reject.
- c298 let a healthy Varg begin a Rows wolf pack and continue its current pack under normal retreat checks. It went 7/8 and did not improve the control’s win or gem results. Reject.

These changes remain local and were not uploaded. Continue by instrumenting route choices / camp travel on Rows and by testing a genuine multi-route assignment; equipment-only changes have not moved the live result.

Instrumentation c299 traced Ryth/Varg repeatedly selecting group 4 around rounds 68 onward. Team A produced no group-4 clear event; a sample at round 250 had Ryth stationary at (38,9) while the target was still group 4. c300 extended Ambush's existing 12-turn stalled-target recovery to Rows. Its Rows screen remained 7/8 overall, with 6/6 proxy wins (same as c291) and no gem improvement. Reject; the trace narrows the failure to execution near the target, but does not yet establish whether visibility, camp state, or target access prevents the clear.

c299's later camp-state trace confirmed group 4 was visible with three wolves at round 70; by round 90 two remained, with one still at full health. The bot damaged the pack but never generated a clear event. c301 permanently skipped group 4 and fell to 5/8 (4/6 proxies); reject and retain the route. c302 raised stickiness to 3.0 after a Rows wolf pack was damaged; it tied the control's 6/6 proxy wins and gems, with 1/2 head-to-head. c303 used best-area-tile damage selection on Rows; it fell to 5/8 and lost both head-to-head games. Reject all three. No new candidate was uploaded.

The top-50 campaign is now **4 wins / 320 maps**, with maximum streak 1 and current streak **0/10**. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Rank-1 Intercontinental Fish and Contest counterdraft (18 Oct 2026)

The current ladder lists Intercontinental Fish at rank 1. The fresh group [8a40e9a3-af65-4a93-a9af-971d34b1a879](https://2026a.battlecode.co.uk/game/match-groups/8a40e9a3-af65-4a93-a9af-971d34b1a879) finished 0–5 using the v62-likely upload; exact pinned version is not exposed. All five match summaries show zero bot faults.

| Map | Rounds | Gems A:B | Monster damage A:B | Camp clears A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|---:|
| Ambush | 534 | 582:1,024 | 32.514k:59.350k | 6:12 | 0:0 | 0:0 |
| Contest | 1,165 | 0:1,000 | 6.3k:200.7k | 2:95 | 76:2 | 0:62 |
| Corners | 425 | 374:1,002 | 34.272k:76.375k | 13:41 | 5:0 | 0:4 |
| Expanse | 579 | 584:1,016 | 35.510k:74.700k | 17:46 | 4:0 | 0:0 |
| Fragment | 526 | 102:1,020 | 21.638k:64.062k | 10:24 | 14:1 | 0:14 |

Contest was the priority failure. Our draft was Varg / Cassi & Issac / Ryth / Stellar / Tavi; Fish used Stellar / Tavi / Prism / Cassi & Issac / Ren. Our first death was Cassi at round 41, followed by Issac 42, Ryth 45, Tavi 46, Stellar 50, and Varg 54. The scout log shows a central enemy cluster before that sequence. Fish earned 12,271 gold and later bought many Focus emblems; our deaths prevented shopping and the resulting item gap widened the loss. Ambush, Corners, and Expanse were mainly farm-rate losses; Fragment combined lower farming with 14 deaths.

Local follow-ups based on Fish's exposed lineup:
- c304 mirrored Fish's Contest draft exactly. It scored 4/8 on the one-map screen, losing both games to c291; reject as a draft-only mirror.
- c305 kept C&I and Ryth, added Willow, and dropped Varg. It swept the three proxies but lost both sides to c291 (6/8 total); reject.
- c306 used Varg / Ryth / Stellar / Tavi / Willow, removing the linked pair for five independent bodies. It scored 8/8 on the Contest screen, including both sides against c291, and tied c291 at 82/102 on the full 17-map proxy pool. This is a targeted live test candidate, not a general upgrade.

c306 was uploaded separately as test version 63. A five-map group against Fish on Ambush, Contest, Corners, Expanse, and Fragment is queued as [350cf6e4-a539-4b50-b612-63f2086b91d9](https://2026a.battlecode.co.uk/game/match-groups/350cf6e4-a539-4b50-b612-63f2086b91d9); the group API currently reports queued and omits the pinned version. Do not count its results until finished.

Campaign after the v62-likely Fish group: **4 wins / 325 completed top-50 maps**, maximum streak 1, current streak **0/10**. Production source and ZIP are unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. The final production build/ZIP gate remains 10 consecutive wins.


## Rank-1 v63–v65 follow-up (18 Oct 2026)

Three successive five-map groups against Intercontinental Fish finished 0–5 with no bot faults: v63-likely group https://2026a.battlecode.co.uk/game/match-groups/350cf6e4-a539-4b50-b612-63f2086b91d9, v64-likely group https://2026a.battlecode.co.uk/game/match-groups/b3d6be46-136a-4b63-8158-8cda6e2e0443, and v65-likely group https://2026a.battlecode.co.uk/game/match-groups/981927d5-6aae-4256-935d-3ae0202a36cc. The CLI does not expose pinned submission versions; labels follow upload-before-queue timing.

The v63-likely Contest draft used Varg / Ryth / Stellar / Tavi / Willow (five bodies against Fish's six). It reduced deaths relative to v62's collapse, but still banked no gems. The v64-likely change relaxed Contest's special retreat check; live numbers barely moved. v65-likely added a three-tile opening response range and secured two kills, but still lost the farm race.

| Map (v65-likely) | Banked gems A:B | Camp-clear entries A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| Ambush | 582:1,024 | 6:12 | 32.514k:59.350k | 0:0 | 0:0 |
| Contest | 0:1,000 | 4:78 | 8.696k:188.144k | 59:6 | 2:59 |
| Corners | 374:1,002 | 13:41 | 34.272k:76.375k | 5:0 | 0:4 |
| Expanse | 584:1,016 | 17:46 | 35.510k:74.700k | 4:0 | 0:0 |
| Fragment | 102:1,020 | 10:24 | 21.638k:64.062k | 14:1 | 0:14 |

Contest evidence: v63-likely dealt 8.639k champion damage, cleared 2 camp entries, and recorded 60 deaths / 0 kills against Fish's 56.299k / 84 / 5 / 60. v64-likely moved to 9.095k / 3 / 57 / 0 against 55.252k / 76 / 0 / 57. v65-likely rose to 9.802k / 4 / 59 / 2 against 58.779k / 78 / 6 / 59. The three-tile response got the first two champion kills, but did not create a gem-farming window.

Local Contest trials: c307's six-body C&I lineup without Willow scored 6/8 and lost both c291 games; reject. c308's general retreat threshold kept 8/8 on Contest and tied c306 at 82/102 full-map, but did not improve the live result; reject. c309's five-tile opening leash scored 7/8; reject. c310's three-tile opening response scored 8/8 and 82/102, tying c306 while reaching 1,000 gems in all eight Contest proxy games; uploaded as test v65. c311's four-tile response scored 7/8 and lowered Contest proxy gems; reject.

The next priority is map economy and routes. Expanse is a clean comparison: identical four-body drafts, no champion damage, but our first camp clear was round 28 versus Fish at round 15 and total clears were 17:46. Contest also remains a farm failure despite the small v65 combat gain (0:1,000 gems). Keep c306/c310 only as test candidates pending stronger evidence; do not promote a local tie.

Campaign after v65-likely: **4 wins / 340 completed top-50 maps**, maximum streak 1, current streak **0/10**. Production source and ZIP remain unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.

## Rank-5 custom-map retest and campaign status (18 Oct 2026)

The user-created v60-likely group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) was 0-5 against rank-5 new team (4) on rushbait_v2, rows, lanes, eight, and interlock. The current v65-likely submission was then tested on the same five maps in group [67012c50-6dcd-4e12-9e4a-9043c8a3a7cb](https://2026a.battlecode.co.uk/game/match-groups/67012c50-6dcd-4e12-9e4a-9043c8a3a7cb); it also finished 0-5. Match-group data omits pinned submission versions, so labels follow queue timing. No platform bot faults were reported.

| Map | Banked gems A:B | Camp-clear entries A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 300:1,020 | 19:36 | 33.316k:54.768k | 3:0 | 0:2 |
| rows | 594:1,056 | 9:16 | 38.854k:66.924k | 0:0 | 0:0 |
| lanes | 538:1,008 | 19:46 | 35.860k:67.174k | 3:0 | 0:2 |
| eight | 132:1,008 | 7:19 | 27.481k:53.971k | 19:2 | 2:11 |
| interlock | 386:1,004 | 15:32 | 30.742k:62.578k | 13:4 | 3:9 |

The v65 counterdraft mirrors the opponent's Varg / Cassi & Issac / Ryth / Stellar core on rushbait_v2 and adds Tavi on eight. Rushbait improved over v60-likely (212 to 300 banked gems; 9 to 3 deaths), but remained a large farming deficit. In rows, our side cleared camp groups 0 and 2 (9 entries) while the opponent cleared mirrored groups 1, 3, and 5 (16 entries). Neither side dealt champion damage or lost a champion. Team gold was 2,430 versus 4,320, matching the camp-clear gap; route throughput is the likely cause of the item gap.

Captured team-A stdout has two caught Champion cannot act errors on rushbait_v2 and one on interlock; the API reports zero bot faults. Local c316 early split-route scored 4/8 on Rows, including 0/2 against c310 and 0/2 against c291; reject it. Logging-only c317 shows c310 routes all five champions through Ryth's objective and locally rotates groups 0, 2, then 4. That alone does not explain why the live top-5 Rows game cleared only groups 0 and 2; investigate arrival, camp readiness, and path completion before changing item builds.

The v65-likely groups against rank-50 WHIM (f3c0018c-fa0e-4cfd-9aef-b80b8aca1c24) and rank-40 Super Intelligence (50ee54e6-246d-4382-94e8-7d45c78ccab9) also finished 0-5. Contest against Super Intelligence banked 0 gems, with 78 deaths and 11 kills; other maps were chiefly farm-rate deficits. Campaign: 4 wins / 360 completed top-50 maps, maximum streak 1, current streak 0/10. Production source and ZIP remain unchanged at their recorded hashes; do not promote local variants.

## v66 Rows commitment test (18 Oct 2026)

Version 66-likely, which triples the value of a damaged Rows wolf group, was tested against rank-5 new team (4) on the same maps in group [05465728-a486-48f7-8439-41b56bc27724](https://2026a.battlecode.co.uk/game/match-groups/05465728-a486-48f7-8439-41b56bc27724). It finished 0-5. The per-map scores and camp clears were identical to v65-likely: rushbait_v2 300:1,020 and 19:36; rows 594:1,056 and 9:16; lanes 538:1,008 and 19:46; eight 132:1,008 and 7:19; interlock 386:1,004 and 15:32. Rows therefore did not respond to the soft target bonus. Reject c318/v66; it remains test-only. Campaign is now 4 wins / 365 completed top-50 maps, max streak 1, current 0/10. Production source and ZIP remain unchanged.

## v67 damaged-pack lock test (18 Oct 2026)

The stricter Rows rule in c320 was uploaded as version 67 and queued against rank-5 new team (4) in [group 955faf23-97fb-4f5f-b405-8944957190c7](https://2026a.battlecode.co.uk/game/match-groups/955faf23-97fb-4f5f-b405-8944957190c7). It finished 0-5 with no platform bot faults. Match groups do not report pinned submission versions; v67 attribution follows upload-before-queue timing.

| Map | Banked gems A:B | Camp-clear entries A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 300:1,020 | 19:36 | 33.316k:54.768k | 3:0 | 0:2 |
| rows | 528:1,056 | 9:16 | 37.846k:66.924k | 0:0 | 0:0 |
| lanes | 538:1,008 | 19:46 | 35.860k:67.174k | 3:0 | 0:2 |
| eight | 132:1,008 | 7:19 | 27.481k:53.971k | 19:2 | 2:11 |
| interlock | 386:1,004 | 15:32 | 30.742k:62.578k | 13:4 | 3:9 |

On Rows, c320 cleared 9 camp entries and no champions died, but banked 528 gems versus 1,056. The v65, v66, and v67 replays use the same map seed and draft. c320's route cleared groups 0, 2, and 4; v65/v66 cleared groups 0 and 2 for 594 gems. The paired replay isolates a 66-gem reduction after the route change. Reject c320/v67. Its local Rows screen was 6/8 (1/2 each vs c310 and c291, 2/2 against each weak proxy) and averaged 1,006 gems. A follow-up c321 that removed early gold weighting on Rows also scored 6/8 and averaged 974 gems; reject it too.

Campaign: **4 wins / 370 completed top-50 maps**, maximum streak 1, current streak **0/10**. Keep c320 and c321 test-only. The production bot and ZIP remain unchanged; continue investigating route throughput before promoting any change.

## v68–v71 farming and survival follow-ups (18 Oct 2026)

Four more groups against rank-5 new team (4) all finished 0-5 with zero platform bot faults: [v68 group](https://2026a.battlecode.co.uk/game/match-groups/1f420eff-95d4-47cf-adf2-1181a8dfc274), [v69 group](https://2026a.battlecode.co.uk/game/match-groups/b9ee15a5-adc4-41a8-8912-9e82789b30d4), [v70 group](https://2026a.battlecode.co.uk/game/match-groups/0c22b4fb-111d-407d-bb96-e84a2f9bc336), and [v71 group](https://2026a.battlecode.co.uk/game/match-groups/47ff93c4-2182-4c8d-9b2a-61961476fd63). The same maps, drafts, and seeds were used throughout.

v68 added a 30% health retreat trigger. It made no measurable difference: the eight replay stayed at 132:1,008 gems and 19:2 deaths, with the same Team-A deaths at rounds 80–105; all five map metrics matched v65. Reject c323/v68. v69 gave Cassi Monster Focus before Power Focus on the camp-heavy maps. On Rows it raised our monster damage from 38.854k to 44.550k and camp-clear entries from 9 to 11, while submitted gems stayed 594:1,056 and the group still went 0-5. The two extra clear events occurred at rounds 382 and 385, after the opponent's route had effectively won the race. This is a real late farm gain but not a match improvement.

v70 kept Cassi's Monster Focus change on Rows and gave Ryth Monster Strength instead of Health. Rows remained exactly at v69's 594:1,056 gems, 11:16 clears, and 44.550k:66.924k monster damage; the extra Ryth item change did not add throughput. v71 reduced Rows' current-target bonus from 1.3 to 1.0, but its Rows metrics returned to the v65 baseline (594:1,056 gems, 9:16 clears, 38.854k:66.924k damage). Reject c326/v70 and c327/v71. Both local and live results show the extra target looseness did not help.

Additional local-only screens: c322's move-after-shot Tavi change scored 3/8 on eight; c323's low-health rule tied c310 on every successful paired game; broad-map c324/c325 gear screens scored 13/24 on Rows, Lanes, and Expanse; c326's Rows-only gear screen was 15/23 with one failed run, versus the c310 control's 15/24; c328's Varg solo-safe-camp Rows variant tied the baseline at 6/8 and 974 average gems. Keep these experiments separate. Campaign: **4 wins / 390 completed top-50 maps**, maximum streak 1, current 0/10. No production source or bundle changes.

## Latest current-rank-5 group: Sneaky Bush Campers (18 Oct 2026)

Group [2c01edc0-7f92-468f-9838-0337a2d12c8f](https://2026a.battlecode.co.uk/game/match-groups/2c01edc0-7f92-468f-9838-0337a2d12c8f) finished 0-5. It is v71-likely by upload/queue timing; the public group record omits pinned versions. No platform faults occurred. This is distinct from the older supplied group `dbdcc65c-...`, which was the v60-likely match already documented above.

| Map | Gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 488:1,022 | 17:46 | 34.150k:68.284k | 14:9 | 6:12 |
| rows | 792:1,023 | 13:19 | 52.958k:74.400k | 0:0 | 0:0 |
| lanes | 546:1,016 | 24:44 | 38.922k:69.965k | 5:1 | 0:4 |
| eight | 366:1,032 | 9:18 | 29.632k:64.428k | 17:2 | 1:12 |
| interlock | 464:1,020 | 17:32 | 37.092k:63.788k | 19:0 | 0:13 |

Rows is the cleanest route benchmark: no champion combat, but our team cleared 13 camps to the opponent's 19. The opponent banked at least 1,016 gems on all maps. Eight and Interlock combine a farm deficit with a severe combat gap (36:2 deaths and 1:25 kills together). Campaign: **4 wins / 395 completed top-50 maps**, maximum streak 1, current 0/10. Production source and ZIP remain unchanged.


## Rank-5 follow-up: v71 baseline, v72 regroup test, and v73 draft test (18 Oct 2026)

The supplied group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) is the already-reviewed v60-likely 0–5 set. It is distinct from the later groups below.

An additional baseline group, [712f56bb-9f90-4e85-ace1-be9942c88fe8](https://2026a.battlecode.co.uk/game/match-groups/712f56bb-9f90-4e85-ace1-be9942c88fe8), was queued against #5 before the v72 upload and finished 0–5; it is v71-likely by timing. Candidate c330 was uploaded as v72. Its group, [77aeac8f-fed2-4eca-bf60-3ac9a5817353](https://2026a.battlecode.co.uk/game/match-groups/77aeac8f-fed2-4eca-bf60-3ac9a5817353), also finished 0–5. Paired map seeds/drafts show the contact-regroup change hurt Interlock and left the other maps unchanged:

| Interlock comparison | Submitted gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| v71-likely control | 464:1,020 | 17:32 | 37.092k:63.788k | 19:0 | 0:13 |
| v72-likely c330 | 298:1,010 | 13:27 | 27.826k:59.624k | 18:0 | 0:13 |

Reject c330. Local c331's help-call variant tied c327 at 16/24, so it was not uploaded.

Candidate c332 changed only Interlock's draft to lead with Tavi. Its local screen was 22/28 versus 16/24 for the control set, including 3/4 head-to-head games. It was uploaded separately as test v73 and queued immediately before group [b4117649-1de1-4564-b0c4-4f633cb53371](https://2026a.battlecode.co.uk/game/match-groups/b4117649-1de1-4564-b0c4-4f633cb53371). The group finished 0–5 against current #5 Sneaky Bush Campers. Exact versions are omitted from the group API, so v73 attribution follows upload/queue timing. There were no platform-reported bot faults.

| Map | Banked gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B | First camp clear A:B |
|---|---:|---:|---:|---:|---:|---:|
| Interlock | 536:1,004 | 13:33 | 27.429k:76.532k | 18:2 | 2:15 | 44:9 |
| Eight | 366:1,032 | 9:18 | 29.632k:64.429k | 17:2 | 1:12 | 42:13 |
| Rows | 792:1,023 | 13:19 | 52.958k:74.400k | 0:0 | 0:0 | 25:28 |
| Lanes | 546:1,016 | 24:44 | 38.922k:69.965k | 5:1 | 0:4 | 46:43 |
| Rushbait v2 | 488:1,022 | 17:46 | 34.150k:68.284k | 14:9 | 6:12 | 25:20 |

Interlock's draft selector did transfer: Team A selected Tavi / Cassi & Issac / Ryth / Stellar against the opponent's Stellar / Ren / Tavi / Prism. The opponent cleared camps at rounds 9, 24, and 38 before our first at round 44. Its Stellar earned 11 kills; our team had 18 deaths and 2 kills. Eight also had an early death at round 79 and a 17:2 death gap. Rows remains an uncontested economy deficit: no champion damage or deaths, but 13 versus 19 camp clears. Lanes and Rushbait show both fewer clears and lower monster damage. The Interlock replay stdout has two caught “Champion cannot act” errors, Eight has two, and Rushbait has one; the server reported no bot faults.

A separate local test followed the requested fixed roster: 3 picks Ryth / Vendetta / Tavi, 4 add Willow, 5 add Prism. Candidate c333 scored 3/30 on Interlock, Eight, and Rows versus c327's 23/30. Across all 17 maps against opp-fai-mirror and Faisal-bot, c333 scored 31/68 versus c327's 57/68. Candidate c334 kept the same roster and let Vendetta clear a separate safe wolf camp in the early phase; it scored 7/30 on the targeted screen and 34/68 on the full pool. These variants are rejected as broad candidates and were not uploaded.

Campaign: **4 wins / 410 completed top-50 maps**, maximum streak 1, current streak **0/10**. The test artifacts and match summaries are under matches/live/b4117649-1de1-4564-b0c4-4f633cb53371/. Production source and ZIP remain unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.


## Local follow-up after v73: fixed roster, wolf farming, and support tests

c335 changed only Interlock to Varg / Ryth / Tavi / Willow; it scored 3/10 versus c327's 6/10 on the same five proxy opponents. c336 tried Tavi / Cassi & Issac / Ryth / Willow and also scored 3/10 on that screen. Reject both counterdrafts.

c338 kept c333's fixed roster and relaxed Vendetta's separate-wolf filter from a fixed strength cutoff to an estimated-health safety check. It scored 8/30 against opp-tts-v9, opp-fai-mirror, ming_bot, xuanming, and Faisal-bot on Interlock / Eight / Rows; c327 scored 23/30 on its matching screen. Reject c338 as a broad candidate. These tests were local only; none were uploaded.

A new unranked group was queued against queue-time rank-50 Martin Shkreli's Defense Team: [9de98fb4-1737-4b66-b7b4-0859bfc0096d](https://2026a.battlecode.co.uk/game/match-groups/9de98fb4-1737-4b66-b7b4-0859bfc0096d). It tested the latest uploaded v73-likely c332 on Interlock, Eight, Rows, Lanes, and Rushbait v2; results are in the section below.

## v73-likely rank-50 result (18 Oct 2026)

The group finished 0–5 with no platform bot faults. The queue-time opponent was Martin Shkreli's Defense Team (team ID `e116c0be-ed7a-4fe8-b713-d611b8bd09d2`, rank 50 then). Submission versions are not pinned in the group API, so v73 attribution follows upload/queue timing.

| Map | Banked gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B | First clear A:B |
|---|---:|---:|---:|---:|---:|---:|
| Interlock | 254:1,052 | 7:16 | 26.410k:61.460k | 15:7 | 5:10 | 44:44 |
| Eight | 496:1,118 | 7:16 | 32.559k:76.992k | 20:10 | 8:11 | 42:44 |
| Rows | 528:1,056 | 9:17 | 38.654k:70.200k | 0:0 | 0:0 | 25:26 |
| Lanes | 488:1,006 | 18:44 | 34.355k:68.381k | 7:3 | 2:5 | 46:39 |
| Rushbait v2 | 444:1,034 | 21:44 | 38.677k:72.669k | 6:6 | 3:4 | 19:14 |

The team often reached its first clear at roughly the same time as the opponent, but the opponent cleared substantially more camps afterward. Rows isolates the farm deficit without combat: 9:17 camp clears, zero deaths, and 528:1,056 banked gems. Interlock and Eight added a large death / damage gap. Fresh summaries are saved under `matches/live/9de98fb4-1737-4b66-b7b4-0859bfc0096d-*-fresh.json`; replay bundles are under `matches/live/9de98fb4-1737-4b66-b7b4-0859bfc0096d/`.

## Rows own-side route experiments (18 Oct 2026)

The user re-sent [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34). The CLI confirms it is the already-recorded v60-likely group from 09:18 UTC, a 0–5 result against `new team(4)` (rank 5 at queue time; rank 6 on the current ladder). Its freshly fetched summaries match the v60 figures in the earlier table; this link does not add another five matches to the campaign.

Local route isolates against the same five proxy bots on Rows, both sides (10 games each), used c327 as control:

- c339's side-camp selector found no eligible target (route sentinel 9) and matched the control at 10/10 with unchanged gem results. Reject; no route change was exercised.
- c340 removed the safety / deep-camp exclusions globally. It selected enemy-side group 1 from round 1 and scored 5/10; reject.
- c341 restricted the route to groups nearer our spawn and selected our side's group 4 from round 2. It scored 8/10 versus c327's 10/10; reject.
- c342 delayed the same route until round 60 but kept the early-phase gate. It emitted no route-selection logs and matched c327 at 10/10, so the experiment was inactive; reject.
- c343 allowed the route after round 60 during midgame, targeting own-side groups 4 / 5. It scored 6/10 versus c327's 10/10, including farm losses to opp-tts-v9 (792 vs 990 gems) and Faisal-bot (891 vs 990) from side A; reject.

All five candidates remain local and unuploaded. The current Rows evidence does not support a Varg solo side-route; group 4's wolf pack and early separation cost more than the additional route earns. Continue with route timing / group-clear execution analysis instead of reusing these selectors.

### Rows squad-spacing hypothesis

c344's local camp scoring trace showed that group 4 was eligible but usually scored below the closer/current camps, so the standard squad rotation was not being blocked by safety filtering. c345 tested a different coordination idea: on Rows, the Fighter squad avoids camps within 5 tiles of Ryth's current anchor, while the Tank continues excluding the Fighter's selected camp. The candidate built and scored 10/10 against the same five local proxies on Rows, matching c327's 10/10. It was slower (mean win round 627.5 vs 614.4) and let opponents bank more gems on average (768.9 vs 732.6), so reject c345 and keep it local. Artifacts: `matches/league/20261018-125734-c345/` and baseline `matches/league/20261018-125742-c327/`.

Campaign after the rank-50 group: **4 wins / 415 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Production source and ZIP remain unchanged. The supplied v60 group is a re-sent link and is not counted a second time.

### Rows camp coverage and no-Tank draft (18 Oct 2026)

The rank-50 Rows replay in group `9de98fb4-1737-4b66-b7b4-0859bfc0096d` shows our side cleared camp group 0 (18,3) five times and group 2 (31,3) four times, never group 4 (42,3). The opponent cleared group 1 (31,46) seven times, group 3 (18,46) five times, and group 5 (7,46) five times. The first clears were nearly tied at rounds 25 and 26; the winner's repeated coverage of all three groups explains the later 528:1,056 gem gap.

c346 tested matching the opponent's Rows draft (Varg, Cassi & Issac, Tavi, Stellar) without Ryth. Stellar led squad A and Issac led squad B. After fixing Issac's early leader handoff, c346 scored 4/10 against c327's 10/10 on the same five proxies. Reject it; it remains local in `bots/c346`, with final artifacts under `matches/league/20261018-130520-c346/`.

c347 kept the standard lineup but made Varg follow Ryth's camp route after midgame instead of helping Issac's squad when no safe solo camp existed. It scored 5/10 on the five-proxy Rows screen against c327's 10/10; reject the regrouping. c348 changed only Ryth's Rows build from Monster/Power Health to Monster/Power Strength. It scored 10/10 versus proxies, as did c327; c348 banked 983.4 gems on average versus 990.0 and won at round 616.4 on average versus 614.4. In the direct c348-vs-c327 Rows comparison it split 5–5: c348 won all five side-A games and lost all five side-B games. One completed side-B game printed c327's win but failed to save its replay due to a duplicate bundle name. The strength build is therefore side-dependent and unpromoted. Artifacts: `matches/league/20261018-130908-c348/` and `matches/league/20261018-130938-c348-direct-rows-ryth-strength-vs-base/`.

## Fresh queue-time rank-1 group (18 Oct 2026)

Group [794748d5-1c1f-42c5-a937-9f82e1a5fb75](https://2026a.battlecode.co.uk/game/match-groups/794748d5-1c1f-42c5-a937-9f82e1a5fb75) finished 0–5 against queue-time #1 Intercontinental Fish. The likely submitted version was v73/c332 by upload and queue timing; the match-group API does not expose the pinned version. The separate user-supplied [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) remains the earlier 09:18 UTC v60-likely 0–5 against new team (4), already counted once.

| Map | Submitted gems A:B | Camp-clear entries A:B | Monster damage A:B | Deaths A:B | Kills A:B | First clear A:B |
|---|---:|---:|---:|---:|---:|---:|
| Interlock | 110:1,010 | 9:29 | 20.927k:59.443k | 15:0 | 0:12 | 44:9 |
| Eight | 176:1,078 | 8:17 | 32.450k:62.598k | 14:2 | 1:8 | 42:27 |
| Rows | 528:1,056 | 9:17 | 38.654k:68.850k | 0:0 | 0:0 | 25:21 |
| Lanes | 510:1,014 | 23:41 | 38.734k:65.711k | 4:0 | 0:3 | 46:38 |
| Rushbait v2 | 278:1,000 | 15:42 | 24.835k:62.886k | 14:0 | 0:10 | 19:21 |

There were no API-reported bot faults. The captured Team-A stdout contains caught `Champion cannot act` action errors on Interlock and Eight (two on Interlock, four on Eight), which did not register as platform faults and should be traced separately. Combat losses are severe on Interlock, Eight, and Rushbait; Lanes and especially Rows isolate the economy problem. Interlock's first clear was 35 rounds later than Fish's. On Rows there was no champion damage or deaths: Team A repeatedly cleared only its north-side groups at (18,3), (18,5), and (31,3), while Fish cleared the three south-side groups at (7,46), (18,46), and (31,46). First clears were close, but Fish completed 17 clear entries to our 9 and banked twice as many gems. The opponent therefore wins both through an earlier opening on Interlock and through broader repeat coverage after the opening on Rows.

This adds five completed top-50 maps to the campaign: **4 wins / 420 maps**, maximum streak 1, current streak **0/10**. Fresh summaries are `matches/live/794748d5-1c1f-42c5-a937-9f82e1a5fb75-*-fresh.json`; raw downloaded replay archive is `matches/live/794748d5-1c1f-42c5-a937-9f82e1a5fb75`.

## v74-likely Interlock Ren draft retest (18 Oct 2026)

Candidate c350 changed only the Interlock draft to take Ren in place of Tavi, matching the opposing Ren / Stellar / C&I / Ryth lineup. Its local screen tied c332 at 9/10 against the same five Interlock proxy bots; direct c350-vs-c332 was 1–1. It was uploaded as test v74 and queued against Fish in [group 9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3](https://2026a.battlecode.co.uk/game/match-groups/9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3). Both teams drafted Ren, so the pick did not deny Fish its champion. The group lost 0–5 and had no API-reported bot faults.

The paired Interlock replay improved submitted gems from 110 to 182 and first clear from round 44 to 43, but clear entries fell from 9 to 7, our deaths rose from 15 to 18, and kills remained 0 while Fish rose from 12 to 14. Fish still banked 1,010 and cleared 30 entries. Eight, Rows, Lanes, and Rushbait exactly repeated the prior group's baseline metrics. Reject c350/v74 as a broad improvement; the matchup-only Interlock gain is too small and came with worse survival and throughput.

Additional local candidates, all unuploaded except c350/v74:
- c349 moved the Varg farmer's turn priority ahead of the back line; it scored 4/10 against c332 on five maps and lost both Rows games. Reject.
- c351 raised retreat health thresholds to 50% for the Tank / 55% for others on Interlock, Eight, and Rushbait; it scored 1/6 against c332 and banked 680 vs 869 average gems. Reject.
- c352 mirrored Fish's Rows no-Tank lineup (Ren / C&I / Varg / Stellar). It scored 6/10 on the local Rows proxies but lost 0/2 against c332 and banked 891 vs 990. Reject.
- c353 moved Varg's Rows build to Power Strength before Monster Strength. It tied c332 at 10/10 against proxies and 1/2 head-to-head, but averaged 639 vs 614 win rounds and let the Faisal-family proxies bank 726 vs 710 gems. Reject.
- c355 lowered the outmatched threshold to 1.05 on Interlock, Eight, and Rushbait; it tied c332 at 3/6 and banked 775 vs 928. Reject.

Campaign after v74-likely: **4 wins / 425 completed top-50 maps**, maximum streak 1, current streak **0/10**. Keep production source and bundle unchanged. Latest test upload is v74/c350; its exact pin is inferred from upload-before-queue timing.

The next Rows-only timing isolate, c356, forced the split at round 35 instead of waiting for a five-shard purchase. It scored 9/10 against the five local Rows proxies but lost 0/2 head-to-head against c332; Faisal-family proxies banked 759 gems on average versus c332's 710, and candidate wins averaged round 629 versus 614. Reject c356: the earlier split did not improve the control and made local farm outcomes slower/worse.

## Fresh top-1 groups: v74 baseline and v75 Ambush timing (18 Oct 2026)

The old user-supplied group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) is the already-reviewed 09:18 UTC 0–5 against `new team(4)`; it is not a new test. I queued fresh unranked groups against current #1 Intercontinental Fish using the authenticated CLI. Group [e6b3ee2b-077f-4d25-91b7-f2f5c71fce91](https://2026a.battlecode.co.uk/game/match-groups/e6b3ee2b-077f-4d25-91b7-f2f5c71fce91) is v74-likely and finished 0–5 across five previously untested maps:

| Map | Gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| Ambush | 582:1,024 | 6:12 | 32.514k:59.350k | 0:0 | 0:0 |
| Expanse | 584:1,016 | 17:46 | 35.510k:74.700k | 4:0 | 0:0 |
| Packs | 140:1,004 | 3:21 | 8.770k:55.310k | 19:0 | 0:14 |
| Fragment | 102:1,020 | 10:24 | 21.638k:64.062k | 14:1 | 0:14 |
| Collision | 146:1,008 | 13:44 | 19.965k:59.790k | 15:0 | 0:11 |

There were zero API-reported faults on all five maps. Ambush and Expanse are clean camp-throughput losses; Packs, Fragment, and Collision combine farm losses with severe combat deaths. On Packs, opposing Issac bought Power Strength at round 24, while ours first bought Jungle Health at round 47. c358 tested giving Issac the offensive build on Packs/Collision: 11/20 proxy wins versus c332's 12/20, so reject the change.

c359 moved Ambush's mid-game split from round 150 to the five-shard trigger or round 100. It tied c332's 10/10 Ambush proxy screen, with mean wins 941 vs 993 rounds and mean opponent gems 278 vs 330. It was uploaded as separate test v75, then tested in [group 7250aac0-ed63-4984-bed9-7a9fb1d685a1](https://2026a.battlecode.co.uk/game/match-groups/7250aac0-ed63-4984-bed9-7a9fb1d685a1). This v75-likely group lost 0–5 to Fish. Only Ambush changed: submitted gems worsened from 582 to 404, deaths rose from 0 to 2, and camp clears rose by just one (6 to 7). Expanse, Packs, Fragment, and Collision exactly matched the prior group. Reject the early split; keep v75 test-only.

c357's delayed Rows Varg side route lost 0/2 direct games against c332 (792:990 gems). The newer telemetry keeps the Rows finding unchanged: broadening route coverage must increase clears and banked gems without pulling Varg away from a productive squad route. These two top-1 groups add 10 completed maps; campaign is **4 wins / 435 maps**, max streak 1, current **0/10**. Production source and bundle remain unchanged.

### Expanse local follow-ups

The top-1 Expanse replay showed Issac buying Monster Strength at r64 while our Issac bought Jungle Health at r173. c360 tested the offensive build only on Expanse: it tied c332 at 10/10 proxy wins but was slower (855 vs 836 average win rounds), yielded more opponent gems (656 vs 640), and lost both direct games (967:952 total gems). c361 forced the mid-game split at r35 after the first clear; it tied proxies, but averaged 857-round wins and 954 own gems versus c332's 836 and 976, and lost one of two direct games. Reject both. Keep looking at camp target timing and travel rather than changing build or phase without a transfer signal.
## Current top-2 Mite sample and Packs follow-ups (18 Oct 2026)

The repeated user URL dbdcc65c-cb2f-4b28-850b-5fa691da9e34 is the old 09:18 UTC 0–5 against new team (4), already reviewed. The latest uploaded test was v77/c363. Fresh unranked group [e29257b6-18d9-49aa-b952-43a426e1ab2d](https://2026a.battlecode.co.uk/game/match-groups/e29257b6-18d9-49aa-b952-43a426e1ab2d) against queue-time rank #2 Mite lost all five maps with zero platform bot faults.

| Map | Gems A:B | Camp clears A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| Ambush | 356:1,024 | 7:11 | 33.6k:55.7k | 3:2 | 1:2 |
| Expanse | 540:1,116 | 16:32 | 33.5k:65.2k | 2:0 | 0:0 |
| Packs | 208:1,014 | 7:19 | 18.5k:48.5k | 13:0 | 0:10 |
| Fragment | 300:1,048 | 15:27 | 29.2k:73.2k | 14:6 | 4:13 |
| Collision | 154:1,002 | 19:36 | 26.3k:51.8k | 13:0 | 0:9 |

Ambush and Expanse remain mostly farm-rate losses, with no kills on Expanse and only two deaths combined. Packs, Fragment, and Collision lose both camp throughput and champion fights. On Packs, both teams drafted Cassi & Issac / Stellar / Ren. Mite Stellar scored 7 kills, zero deaths, and 5.9k champion damage. Our Stellar had 3 deaths and 2.1k champion damage; Cassi and Issac died at rounds 52–53. Our Ren had four deaths, 35 earned gold, no purchased items, and no kills. Mite Issac used Strength items. This replay points to early C&I survival and focused response to Stellar, rather than merely adding late-game Tank durability.

The v76/v77 Fish comparisons show a partial map-specific gain: the Ren role fix raised Packs from 140 to 252 gems and reduced deaths from 19 to 14; the follow-up Ren tank build raised it to 344 gems and four additional clear entries, but still produced no kills. The same v77 build scored only 208 gems and 13 deaths against Mite, so that gain did not transfer across top teams.

Local c364b (Issac Monster Strength first), c365 (Packs combat leash until round 600), and c366 (Issac Power Strength first) all failed to improve the same five-proxy Packs screen over c363's 6/10. Their direct c363 comparisons were 0/2, 1/2, and 0/2 respectively. Reject and do not upload. Current campaign: **4 wins / 450 top-50 maps**, maximum streak 1, current **0/10**. Raw summaries and the replay archive are matches/live/e29257b6-18d9-49aa-b952-43a426e1ab2d-*-summary.json and matches/live/e29257b6-18d9-49aa-b952-43a426e1ab2d.zip.
## v78–v80 Mite/Fish top-50 tests (18 Oct 2026)

The repeated user link dbdcc65c-cb2f-4b28-850b-5fa691da9e34 is the stale 09:18 group against new team (4). Three new candidate versions were tested against #2 Mite; v79 was also tested against #1 Intercontinental Fish. All four groups lost 0–5 with no API bot faults.

| Test | Opponent/group | Packs gems | Clears | Monster damage | Deaths | Kills |
|---|---|---:|---:|---:|---:|---:|
| v78/c367 | Mite, 295d27b1-85a1-44ed-a423-77ae854b5f54 | 184:1,038 | 5:21 | 17.1k:53.4k | 12:0 | 0:9 |
| v79/c368 | Mite, 3b66586a-63ba-4a4f-bff3-7030e5dec3bb | 232:1,020 | 6:20 | 17.8k:53.1k | 12:0 | 0:9 |
| v79/c368 | Fish, 1980b74e-6197-4f43-8c6d-0a2a169edefe | 256:1,008 | 10:18 | 21.8k:54.3k | 14:0 | 0:10 |
| v80/c369 | Mite, 5e02cb8a-e151-427c-91e9-f98102325456 | 140:1,040 | 5:20 | 15.2k:52.3k | 13:0 | 0:10 |

c367 mimicked Mite's Issac Strength equipment. Its Packs output was below the prior v77 Mite sample: 184 vs 208 gems and 5 vs 7 clears, despite one fewer death. c368 made Packs retreat whenever enemy strength reached parity. Against Mite it raised gems 208→232 and reduced deaths 13→12 and kills conceded 10→9, but reduced clears 7→6 and monster damage 18.5k→17.8k. Against Fish, Packs gems were 256 versus v77's 344 with the same 14 deaths; the local survival gain did not transfer. c369 changed Packs target priority to highest raw enemy damage. It lost to Mite with 140 gems, 5 clears, and 13 deaths, below v77's 208, 7, and 13.

On Ambush, Expanse, Fragment, and Collision, the v78/v79/v80 Mite samples replayed the prior v77 map statistics. The root gap remains opponent-independent camp throughput plus severe fight losses on Packs/Fragment/Collision; no candidate has produced a live win. Local Packs screens: c367 6/10 vs c363 6/10, direct 1/2; c368 7/10 vs a fresh c363 control 6/10, direct 1/2; c369 7/10 vs c363 6/10, direct 1/2. c367 and c369 are rejected; c368 is not promoted after the Fish regression.

Latest uploaded test v80/c369. Campaign: **4 wins / 470 completed top-50 maps**, maximum streak 1, current **0/10**. Replay summaries for the Mite v78–v80 groups are under matches/live/295d27b1-85a1-44ed-a423-77ae854b5f54-*-summary.json, matches/live/3b66586a-63ba-4a4f-bff3-7030e5dec3bb-*-summary.json, and matches/live/5e02cb8a-e151-427c-91e9-f98102325456-*-summary.json. Fish v79 summaries are under matches/live/1980b74e-6197-4f43-8c6d-0a2a169edefe-*.

## v81 Expanse opening split — two top-team groups

v81/c373 changes only Expanse routing: it starts in the mid-game path at round 1, puts Stellar with the Cassi/Issac trio, sends Varg solo to a separate safe camp, and gives the team leader a 0.75 gold weight. Both unranked groups finished 0–5 with no bot faults.

| Opponent | Expanse gems | Clears | First clear | Deaths | Other maps (gems) |
|---|---:|---:|---:|---:|---|
| #2 Mite | 636:1,116 | 20:32 | 14:11 | 0:0 | Ambush 356:1,024; Packs 140:1,040; Fragment 300:1,048; Collision 154:1,002 |
| #1 Intercontinental Fish | 778:1,016 | 22:46 | 14:15 | 0:0 | Ambush 582:1,024; Packs 92:1,012; Fragment 102:1,020; Collision 146:1,008 |

Against the v77 samples, Expanse deposits improved 540→636 against Mite and 584→778 against Fish; first clear advanced from round 28 to round 14 in both groups. The route now starts on the home wolf camp, then spreads across the home loop. It still produces fewer than half of the top opponents' clear entries, so the remaining Expanse problem is repeat-clear rate after the opening. v81 did not materially alter the other four maps.

Local screening was mixed: an Expanse-only zero-gold weight lost 0/10 and averaged 838 gems; a Varg-only early solo route lost 0/10 and averaged 907; a 0.75 weight without the role split averaged 773. The full 3+1 split was closest to control (948 vs 952, 0/10), then transferred as a clear live gain against both opponents. Keep v81 test-only. Current campaign is **4 wins / 480 completed maps**, best streak 1, current 0/10. Latest upload v81/c373; production source and ZIP remain unchanged.

## v82–v83 Expanse follow-up

v82/c375 replaced Varg with Ren. It lost 0–5 to Mite and Fish with no bot faults. Expanse dropped from v81's 636 to 470 gems against Mite and from 778 to 506 against Fish; each game had two deaths. Reject the draft replacement.

v83/c376 split Expanse into a Cassi/Issac pair plus solo Stellar and Varg, with Cassi publishing her solo target so Varg can avoid both camps. It also lost 0–5 to each top team, with no faults:

| Opponent | Expanse gems | Clears | First clear | Deaths | Other maps |
|---|---:|---:|---:|---:|---|
| #2 Mite | 738:1,116 | 24:32 | 14:11 | 0:0 | Same as v81 |
| #1 Intercontinental Fish | 796:1,016 | 28:46 | 14:15 | 0:0 | Same as v81 |

Compared with v81, the new split adds 102 gems/four clears against Mite and 18 gems/six clears against Fish. Local screening went 16/16 across eight controls. The two solo routes now separate cleanly; Issac is the main remaining underperformer against the top teams. Campaign: **4 wins / 500 maps**, max streak 1, current 0/10. Latest upload v83/c376, still test-only.

## User-created v60 group vs ladder #5 (18 Oct 2026)

Group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) completed all five maps against ladder #5, new team(4). The user created this group with v60; the match JSON does not expose the submission version. Heavenly Court lost all five. Diagnostics show zero bot faults on both sides.

| Map | Submitted gems (Heavenly Court:#5) | Camp clears | Deaths | Kills |
|---|---:|---:|---:|---:|
| rushbait_v2 | 212:1,004 | 17:35 | 9:0 | 0:7 |
| rows | 594:1,056 | 9:16 | 0:0 | 0:0 |
| lanes | 560:1,038 | 20:47 | 3:1 | 1:2 |
| eight | 154:1,024 | 6:19 | 19:5 | 3:9 |
| interlock | 596:1,032 | 15:36 | 17:6 | 3:11 |
| **Total** | **2,116:5,154** | **67:153** | **48:12** | **7:29** |

The loss combines an economy gap (our team banked 41% of the opponent's gems and 44% of its camp clears) with a fight-survival gap. Rows lost despite zero deaths, so route value and clear cadence need work even without combat losses. Eight and Interlock are the urgent survival maps: they account for 36 of our 48 deaths. Rushbait_v2 also has both a low deposit and nine deaths. No faults occurred, so these are strategy/pathing outcomes, not runtime failures.

This group expands live top-50 map coverage beyond Ambush, Expanse, Packs, Fragment, and Collision to Rows, Lanes, Eight, Interlock, and Rushbait_v2. Seven published maps still have no top-50 live result: Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, and Swirl. A direct v83 comparison against #5 on the same five maps has been queued as group bd1c7f28-ab38-464c-aa27-74c0325737d6; results pending.

Campaign tally before the pending v83 group: **4 wins / 505 completed top-50 maps**, best streak 1, current streak **0/10**. Production files remain untouched.

## Latest-upload comparison vs #5 on the same five maps (18 Oct 2026)

After the v60 group above, a second unranked group was queued against #5 immediately after uploading v83/c376: [bd1c7f28-ab38-464c-aa27-74c0325737d6](https://2026a.battlecode.co.uk/game/match-groups/bd1c7f28-ab38-464c-aa27-74c0325737d6). It also lost 0–5 with no bot faults. The platform summary does not state the submission number, but this was the latest-upload test group.

| Map | Gems (v83-target:#5) | Clears | Deaths | Kills |
|---|---:|---:|---:|---:|
| rushbait_v2 | 300:1,020 | 19:36 | 3:0 | 0:2 |
| rows | 594:1,056 | 9:16 | 0:0 | 0:0 |
| lanes | 538:1,008 | 19:46 | 3:0 | 0:2 |
| eight | 132:1,008 | 7:19 | 19:2 | 2:11 |
| interlock | 182:1,054 | 10:30 | 15:0 | 0:11 |
| **Total** | **1,746:5,146** | **64:147** | **40:2** | **2:26** |

Relative to the earlier v60 group, only Rushbait_v2 improved clearly (212→300 gems; deaths 9→3). Rows was identical; Lanes and Eight were similar; Interlock fell from 596 to 182 gems. These are separate matches with different drafts/seeds, so they are not paired evidence that v83 caused the regressions. The durable finding is the same: Rows is a no-death farming race, while Eight and Interlock need safer combat behavior; the v83 group had 34 of 40 deaths on those two maps. The actual candidate change was Expanse-specific, so these maps remain unsolved.

The two completed groups add ten top-50 map matches: campaign is **4 wins / 510 completed maps**, max streak 1, current streak **0/10**. Latest upload is v83/c376; production remains unchanged. Seven published maps still have no top-50 live result: Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, and Swirl.
# v88–v91 Fish rematches and repeated user link (18 Oct 2026)

The user re-sent [group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34`](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34). The CLI confirms it was created at 09:18 UTC against `new team(4)` and completed 0–5; it is the same earlier group, so count it once.

Four later test uploads were run against current #1 Intercontinental Fish. All four groups lost 0–5, with zero API-reported bot faults. Values below are our banked gems / camp-clear entries / deaths.

| Map | v88 / c388 | v89 / c390 | v90 / c391 | v91 / c392 |
|---|---:|---:|---:|---:|
| Rushbait | 284 / 15 / 7 | 190 / 17 / 12 | 284 / 15 / 7 | 190 / 17 / 12 |
| Rows | 462 / 10 / 0 | 462 / 10 / 0 | 462 / 10 / 0 | 462 / 8 / 0 |
| Lanes | 518 / 24 / 3 | 584 / 26 / 4 | 518 / 24 / 3 | 584 / 26 / 4 |
| Eight | 168 / 5 / 16 | 132 / 4 / 17 | 168 / 5 / 16 | 132 / 4 / 17 |
| Interlock | 88 / 8 / 16 | 88 / 8 / 16 | 204 / 9 / 13 | 88 / 10 / 16 |
| **Total** | **1,520 / 62 / 42** | **1,456 / 65 / 49** | **1,636 / 63 / 39** | **1,456 / 65 / 49** |

Groups: [v88](https://2026a.battlecode.co.uk/game/match-groups/0c7b5719-919b-4699-8ff8-fd2c042da3e3), [v89](https://2026a.battlecode.co.uk/game/match-groups/bc7fd0c4-c8cf-49f3-bd59-6cecbce92aa2), [v90](https://2026a.battlecode.co.uk/game/match-groups/6ea755d1-d3b1-4dfe-a03f-4f3895c25282), [v91](https://2026a.battlecode.co.uk/game/match-groups/1575825c-6b57-4943-9d60-3bb4d1ca76eb). Fish banked roughly 1,000 gems per map in all four groups. v88/c388 scored 24/30 in the local multi-bot screen; v89/c390 scored 22/30. v90/c391 also scored 24/30 overall and improved Interlock's split opening locally; v91/c392 scored 5/6 on Interlock locally but regressed in the live game. This shows the mirror draft does not reliably transfer. Keep both changes test-only.

v89 and v91 each logged one caught stdout action error on Lanes (`Unit is not in vision`), despite zero platform API faults. Investigate that action path separately. The repeated group link contributes no new match. These four groups add 20 completed maps, bringing the campaign to **4 wins / 565 top-50 maps**, maximum streak 1, current **0/10**. Production bot and ZIP hashes remain unchanged.

## v92 Mite/Fish coverage and v93 Contest counterdraft (18 Oct 2026)

The resent user link [`dbdcc65c-cb2f-4b28-850b-5fa691da9e34`](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) is still the old 09:18 UTC 0–5 group against `new team(4)`; it adds no matches. Test candidate c395 was uploaded as v92 and evaluated across three fresh groups. All 15 games lost; these groups extend top-50 live map coverage to **17/17**.

| Opponent / group | Map | Gems HC:opp | Deaths | Kills | Monster damage HC:opp |
|---|---|---:|---:|---:|---:|
| #1 Fish / [bfd8fc8b-fbd1-4a36-8605-3ca3a614150d](https://2026a.battlecode.co.uk/game/match-groups/bfd8fc8b-fbd1-4a36-8605-3ca3a614150d) | Rushbait_v2 | 284:1,060 | 7:0 | 0:6 | 28.320k:64.097k |
| | Rows | 462:1,056 | 0:0 | 0:0 | 36.850k:68.850k |
| | Lanes | 518:1,000 | 3:2 | 0:2 | 41.148k:64.875k |
| | Eight | 168:1,006 | 16:0 | 0:11 | 24.925k:60.335k |
| | Interlock | 276:1,026 | 14:0 | 0:8 | 25.354k:65.338k |
| #2 Mite / [9c5b4cf5-f6e4-4a90-b05a-a9e03ffb38bd](https://2026a.battlecode.co.uk/game/match-groups/9c5b4cf5-f6e4-4a90-b05a-a9e03ffb38bd) | Contest | 0:0 | 94:0 | 0:94 | 1.500k:190.500k |
| | Corners | 294:1,000 | 6:0 | 0:5 | 29.150k:58.050k |
| | Elkring | 486:1,026 | 17:1 | 1:13 | 41.924k:85.396k |
| | Monolith | 614:1,002 | 1:0 | 0:1 | 44.500k:66.264k |
| | Pilgrimage | 570:1,010 | 14:5 | 3:10 | 29.163k:83.241k |
| #2 Mite / [4985936d-db5b-4a7a-9058-f1be73a50bfd](https://2026a.battlecode.co.uk/game/match-groups/4985936d-db5b-4a7a-9058-f1be73a50bfd) | Stampede | 0:1,008 | 8:0 | 0:4 | 17.866k:59.756k |
| | Swirl | 0:1,020 | 27:1 | 1:21 | 7.370k:88.980k |
| | Interlock | 480:1,034 | 11:7 | 3:6 | 34.220k:67.268k |
| | Rows | 528:1,012 | 0:0 | 0:0 | 37.668k:64.800k |
| | Eight | 198:1,008 | 10:2 | 1:7 | 31.894k:54.390k |

Across v92, the recurring gaps remain both combat survival and farming. Rows again lost without deaths, while Swirl had 27 deaths and only 7.37k monster damage. Contest was a complete collapse: no gems, 94 Team-A death events, and 94 kills conceded. The detailed summaries are under `matches/live/bfd8fc8b-summary-*.json`, `matches/live/9c5b4cf5-summary-*.json`, and `matches/live/4985936d-summary-*.json`.

Contest purchase events also show why changing item order is unlikely to close this gap by itself. The v92 Team-A roster earned only 105 gold total; Varg bought three Monster Strength shards at round 69, and the other four champions bought nothing. Mite earned 21,406 and spent 19,720 gold across six champions; its first purchases were Treasure Focus/Strength shards from rounds 50–136, followed by many more items. Earlier local test #138 put Stellar on Treasure Focus first and lost four wins versus the control. Treat Mite's purchases as evidence of its earlier income snowball, not evidence that Treasure-first should be copied without a new farm-economy test.

### v93 adaptive six-body Contest draft

Candidate c397 changed only Contest draft selection: when the enemy revealed C&I plus Ryth or Tavi, it selected Varg / C&I / Ryth / Stellar / Tavi to reach six physical bodies. It passed the three-proxy Contest screen 6/6 and split a two-game Contest direct screen 1–1 against c391. Bundle `submissions/tungtungsahur-candidate-v93-c397-adaptive-contest-six-body.zip` SHA-256: `031C65B56E2DBB46378A1FF37CE5402FFB66636C4E9C37ACE15F4E08990AB6B5`. Uploaded as test v93.

The fresh #2 Mite group [eba1da49-7ea6-4711-ac74-11972535abd3](https://2026a.battlecode.co.uk/game/match-groups/eba1da49-7ea6-4711-ac74-11972535abd3) finished 0–5. It was queued immediately after the v93 upload, but group metadata does not expose the pinned submission; treat this as v93-likely. On Contest, the replay shows c397's six-body mirror against Mite's Prism / C&I / Ryth / Stellar / Tavi draft, but the match reached round 2,000 with 0:0 gems and 140 Team-A death events. The first six deaths were Cassi r37, Issac r38, Tavi r41, Ryth r47, Stellar r50, and Varg r57. Team-A stdout logged 12 `Champion cannot act` errors; previous forensics tie this message to crowd control, so it indicates time lost to stuns and is not by itself proof of a bot fault. Final score snapshots on the other maps were Swirl 0:976, Interlock 132:988, Rows 528:990, and Eight 198:876 gems. The downloaded archive is `matches/live/eba1da49-7ea6-4711-ac74-11972535abd3.zip`.

Matching the opponent's body count did not fix Contest; this sample had more Team-A death events than v92's Mite Contest sample (140 vs 94) and still banked no gems. The next Contest investigation should focus on opening engagement, damage uptime, and reaching the two 200-gem Monolith camps rather than another lineup mirror. Local follow-up c398 (same draft rule with c395's Interlock safety change) scored 12/12 against three proxies but only 2/4 versus c395, with equal 720:720 aggregate gems. c399 kept Willow while adding C&I and dropping Varg; it scored 5/6 against proxies and 1/2 versus c395. Neither showed a local advantage, but c399 was sent to one targeted Mite test to measure the healer-plus-six-body hypothesis.

Two more local experiments were rejected. c400 moved the existing burst call before Contest survival; it exactly matched c395's 6/6 proxy results and score/win rounds, then went 5/10 head-to-head with c395, winning every side-A game and losing every side-B game at the same 500:400 score split. Since retreat starts at 30–35% health while burst requires 60%, the reordering did not enable a useful cast during retreat. c401 prioritized the highest raw-damage target in Contest burst ties; it scored 10/12 across Contest and Interlock proxies versus c395's 12/12, and its Ming results fell to 2/4 (591:564 gems) from c395's 4/4 (791:314). Reject both.

Candidate c399 was uploaded as test v94 (`submissions/tungtungsahur-candidate-v94-c399-contest-six-body-with-willow.zip`, SHA-256 `2B33AEEC34F2B16B9D37895572AB5D83CB9B75119881038E92A095FC9FE1328D`) and queued against #2 Mite in [group 528af232-c8fa-42e7-9375-240ff909d1a9](https://2026a.battlecode.co.uk/game/match-groups/528af232-c8fa-42e7-9375-240ff909d1a9). The group finished 0–5; exact pinned version is not in metadata, so call it v94-likely. On Contest, the C&I / Ryth / Stellar / Tavi / Willow draft matched six bodies and banked 0:0 gems, but logged 132 Team-A death events; Cassi and Issac died at r29, then Tavi r41 and Ryth r46. Six `Champion cannot act` errors were logged. This is a small reduction from v93's 140 death events, but still worse than v92's 94, and the seeds differ, so it is not evidence of an improvement. Other final score snapshots were Swirl 0:976, Interlock 480:998, Rows 528:990, and Eight 198:876. Interlock retained c395's higher 480-gem result; the other maps were effectively unchanged.

The 15 v92, five v93, and five v94 matches leave the campaign at **4 wins / 590 completed top-50 maps**, maximum streak 1, current streak **0/10**. All 17 official maps now have live results. Latest upload is v94/c399, rejected for production. Production hashes remain unchanged: source `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; ZIP `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## v95 Contest Prism mirror vs #2 Mite (18 Oct 2026)

The user-supplied `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` link is the previously reviewed 09:18 UTC 0–5 group against `new team(4)` and adds no results. Local v94 follow-ups screened three hypotheses: c402's 50% Contest heal threshold tied c399 at 7/8 and 3,200 total gems across four strong proxies; c403's back-line farm rule scored 4/8. Both are rejected. c404 changed only Contest's lineup to Prism / Stellar / Cassi & Issac / Ryth / Tavi. It tied c399 at 38/40 on the full 20-opponent Contest pool while adding 200 aggregate gems (36,000 vs 35,800); a side-swapped two-game head-to-head split 1–1, so c404 was tested only as a Mite-specific draft mirror.

Bundle SHA-256: `70A98FAA3FC6663AA43CED2F6A2F82B1B1230C76C2E63B706FEAFB2A8FDAA3AA`. Uploaded as test v95. The fresh [group](https://2026a.battlecode.co.uk/game/match-groups/dbffabee-68c9-4ddd-a9eb-5e59b423e846) against current #2 Mite finished 0–5. The platform confirms that our Contest draft exactly mirrored Mite's Prism / Stellar / C&I / Ryth / Tavi lineup; other maps used their existing drafts. Per-map Team A:Team B:

| Map | Gems | Camp-clear entries | Monster damage | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Contest | 0:0 | 2:128 | 3.625k:191.376k | 141:0 | 0:117 |
| Swirl | 0:1,020 | 1:17 | 7.370k:88.980k | 27:1 | 1:21 |
| Interlock | 480:1,034 | 18:32 | 34.221k:67.268k | 11:7 | 3:6 |
| Rows | 528:1,012 | 9:16 | 37.668k:64.800k | 0:0 | 0:0 |
| Eight | 198:1,008 | 6:17 | 31.894k:54.390k | 10:2 | 1:7 |

No platform bot faults occurred. Contest stdout contained five caught `Champion cannot act` errors. The first enemy sightings came at rounds 20–21 and our first death was Ryth at r28. The team earned 210 gold and spent 190; Mite earned 22,626 and spent 20,900. The matchup mirror did not slow the wipe or create farm income. Reject v95 for general play.

The follow-up five-map group against current rank-50 Bamboo Teahouse, [51e941e4-5904-4c2d-bd75-87d761c2b0c3](https://2026a.battlecode.co.uk/game/match-groups/51e941e4-5904-4c2d-bd75-87d761c2b0c3), also finished 0–5, with zero platform bot faults:

| Map | Gems HC:Bamboo | Camp-clear entries | Monster damage HC:Bamboo | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Contest | 0:800 | 6:116 | 20.213k:236.557k | 123:3 | 1:94 |
| Swirl | 0:1,020 | 2:23 | 10.616k:79.781k | 37:6 | 4:28 |
| Interlock | 546:1,054 | 22:33 | 50.865k:57.515k | 15:0 | 0:11 |
| Rows | 660:1,056 | 11:17 | 45.544k:68.850k | 0:0 | 0:0 |
| Eight | 36:1,038 | 5:21 | 31.525k:55.255k | 20:4 | 2:14 |

Interlock produced 546 gems and 50.865k monster damage, but conceded 15 deaths and no kills; Rows lost as a clean farm race; Contest, Swirl, and Eight combined major combat and income gaps. The campaign is now **4 wins / 600 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. All 17 official maps have live coverage. Production source and ZIP were not modified. Replay archive and match summaries are in `matches/live/51e941e4-5904-4c2d-bd75-87d761c2b0c3.zip` and `matches/live/v95-bamboo-*-summary.json`.


## Rows route diagnostics after the repeated user link

The user supplied `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` again. It is the previously reviewed 09:18 UTC group versus `new team(4)`, already counted as 0-5; campaign totals do not change.

For the fresh Bamboo Rows replay, capture events show Team A clearing groups 0/2/4 ten times in total and Bamboo clearing groups 1/3/5 sixteen times. Team A's group 4 was first captured at r175; Bamboo first captured group 5 at r105. Team A Varg repeatedly shared group rewards for 22 gems per capture; Bamboo Varg earned 66 per capture. This supports a route-coverage and solo-target issue, not a fight or equipment issue.

Local route tests:

- c405 published the tank target before the fighter chose a distinct target: 4/14 wins.
- c406 added 1.3 target stickiness to c405: 5/14 wins.
- c407 prevented Varg from joining captures on Rows: 12/14, but split 1-1 against c404 with no gem advantage.
- c408/c410 logged route targets. Varg's regular solo target was empty; he fell back to Issac's objective. c409 allowed Varg to solo wolf packs up to three wolves with a 75% starting-health gate; it scored 9/14 (7/7 side A, 2/7 side B) after selecting a far camp at (42,5). c411 added an allied-half restriction and scored 12/14 (7/7 side A, 5/7 side B), but still split 1-1 against c404.

All are local-only and none has a reliable edge over baseline. No candidate was uploaded. Campaign stays at **4 wins / 600 completed top-50 maps**, best streak 1, current **0/10**; production remains unchanged.


## v96-likely result vs current rank-50 umamusume (18 Oct 2026)

The authenticated CLI confirmed the repeated user URL `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is still the older 09:18 UTC group versus `new team(4)`. After installing CAMBC 2.2.5 in an isolated temporary environment, c411 was uploaded as test v96 and queued in fresh group [819e5b24-2227-4065-9eda-d49419a8568f](https://2026a.battlecode.co.uk/game/match-groups/819e5b24-2227-4065-9eda-d49419a8568f) versus queue-time rank-50 umamusume. The group finished 0-5. Match metadata omits the pinned submission version, so attribution is v96-likely. No platform `botFault` events occurred.

| Map | Submitted gems HC:opponent | Camp-clear entries | Monster damage (k) | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Rows | 528:1,056 | 11:17 | 42.740:68.850 | 2:0 | 0:0 |
| Lanes | 590:1,016 | 24:46 | 40.304:69.365 | 1:0 | 0:1 |
| Eight | 264:1,036 | 5:26 | 26.985:62.213 | 24:6 | 1:12 |
| Interlock | 292:1,006 | 15:21 | 32.442:57.703 | 15:1 | 1:10 |
| Contest | 0:200 | 3:129 | 28.790:187.793 | 98:7 | 7:72 |

The candidate did not close the Rows route gap. Lanes has a similar damage/clear deficit; Eight and Interlock combine the economy gap with frequent deaths. Contest reached round 2,000: Team A collected 200 gems but banked none; the opponent banked 200 at r1868. Team A's Cassi and Issac both died to the opponent's Ren at r45. The replay has ten Team-A fuel-exhaustion events on Contest, including six at r35-r39; there were also four Team-A events on Lanes and three on Eight. Per the local rules, exhaustion suspends a turn and resumes it next round without counting as a bot fault; investigate these concentrated spikes, while treating this single seed as a lead rather than proof of cause. The v95-likely Mite Contest summary had three Team-A exhaustion events on a different draft/seed.

A local phase audit also found c413's attempted early Rows route was unreachable: Rows is already `Phase::mid` from round 1, so c413 replayed c411 unchanged and matched its score results. Do not upload c413. c411 was submitted separately as test v96 (bundle SHA-256 `13BE6FF1AEE3D1FC6E2905C252A8FFDB13466D036BFF8344BD5A886A947C8BF8`); reject it for production. Replay archive: `matches/live/819e5b24-2227-4065-9eda-d49419a8568f.zip`. Match summaries and group metadata: `matches/live/819e5b24-2227-4065-9eda-d49419a8568f/`.

Campaign is **4 wins / 605 completed top-50 maps**, maximum streak 1, current **0/10**. All 17 official maps have live coverage. Production hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` (source) and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` (ZIP).

## v97-likely vs rank-50 Live Love Larp and Contest carrier diagnosis (18 Oct 2026)

Group [bab275a5-8821-4586-81e2-23b16e626e90](https://2026a.battlecode.co.uk/game/match-groups/bab275a5-8821-4586-81e2-23b16e626e90) finished 0-5. The group metadata does not pin the submission, so attribute v97-likely. There were no platform bot faults.

| Map | Gems HC:opponent | Camp-clear entries | Monster damage (k) | Deaths | Kills | Fuel exhaustion A:B | Gold earned |
|---|---:|---:|---:|---:|---:|---:|---:|
| Contest | 0:1,000 | 8:119 | 33.4:206.5 | 77:23 | 12:43 | 0:0 | 1,635:12,135 |
| Lanes | 648:1,018 | 25:46 | 42.5:65.9 | 0:0 | 0:0 | 5:4 | 2,740:4,190 |
| Eight | 672:1,024 | 12:23 | 52.6:64.3 | 16:9 | 4:8 | 0:0 | 3,015:4,705 |
| Interlock | 656:1,014 | 23:38 | 38.4:68.1 | 7:2 | 1:4 | 0:0 | 2,580:4,770 |
| Rows | 528:1,056 | 11:17 | 46.5:68.8 | 3:0 | 0:0 | 0:0 | 2,700:4,590 |

Contest is the largest collapse. In its replay, Issac collected 200 gems from the Contest Monolith group at r1006 near (24,35). At r1014 he still carried the gems while enemy Tavi was at (24,29) and enemy Stellar at (29,29). No teammate was close enough to escort him. Enemy Stellar killed Issac at r1018 and took the 200 gems, later banking them. This is direct evidence for a carrier-awareness/escort test; c420 added a shared carrier marker and escort behavior but scored 6/8 on the four-proxy screen versus c417's 7/8. It won the side-B but lost the side-A games against both c417 and c404, with no direct gem edge, so do not upload it.

Fuel traces on isolated c414/c415 builds found costly visibility reads (about 9–15k fuel per list) and pathfinding stages (about 20–30k combined); some role actions began with under 5k fuel left. This explains a mechanism for occasional suspended turns but does not establish fuel as the main Contest cause. c416's enemy-visible deferral tied c411 at 7/8 Contest wins with lower average gems; c418's keep-Tavi counterdraft scored 7/8 without a direct edge; c419's nearest-35-gold-camp opening scored 5/8. Reject these local variants.

Campaign after the five-map group: **4 wins / 610 top-50 maps**, maximum streak 1, current **0/10**. Production source and ZIP remain unchanged. Full local replays, logs, and summaries are under `matches/league/20261018-165217-c420-direct-contest-carrier-escort/`; live summaries are under `matches/live/bab275a5-8821-4586-81e2-23b16e626e90/`.

## v98-likely vs rank-49 Please: carrier escort did not transfer (18 Oct 2026)

Candidate c421 was uploaded as test v98 after an 8/8 local Contest screen versus c417, c404, opp-fai-mirror, and opp-tts-v5; a fresh c417 control scored 5/8. c421 only published the carrier marker while an enemy was within 8 tiles and sent one frontline ally to escort. The fresh [five-map group](https://2026a.battlecode.co.uk/game/match-groups/8a9a1654-7673-4da3-bbae-daaa2f5cc715) against queue-time rank-49 Please finished 0-5. Submission pin is not present in group metadata; attribute v98-likely. All five maps had zero platform bot faults.

| Map | Gems HC:Please | Camp clears | Monster damage (k) | Deaths | Kills | Fuel exhaustion A:B | Gold earned (k) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Contest | 0:200 | 9:132 | 48.1:170.8 | 85:23 | 15:51 | 0:0 | 1.9:14.2 |
| Lanes | 750:1,000 | 30:43 | 49.6:65.7 | 0:0 | 0:0 | 2:0 | 3.2:4.3 |
| Eight | 683:1,029 | 8:20 | 34.7:83.4 | 30:9 | 7:16 | 0:0 | 2.1:6.3 |
| Interlock | 204:1,004 | 10:35 | 21.6:63.4 | 23:2 | 2:14 | 0:0 | 1.2:5.0 |
| Rows | 528:1,056 | 11:17 | 40.7:68.9 | 2:0 | 0:0 | 0:0 | 2.4:4.6 |

Contest replay events show Prism collected 200 gems at r1027 at (17,31). Please's Ryth took the 200 from Prism at r1063 near (25,22), then submitted them at r1109. The escort change did not prevent the theft, and the map still had 85:23 deaths, 15:51 kills, and 9:132 camp-clear entries. The 8/8 local screen did not transfer; reject c421 for general use. A separate c422 Contest-only change that waits to fight until the tank is hit scored 1/8 against the same four local proxies versus c417's fresh 5/8; reject c422, unuploaded.

Campaign after this group is **4 wins / 615 top-50 maps**, maximum streak 1, current **0/10**. Latest test upload is v98, not validated for production. Production source and ZIP remain unchanged. Raw summaries, stdout/fuel logs, and replays are under `matches/live/8a9a1654-7673-4da3-bbae-daaa2f5cc715/`; the group archive is `matches/live/8a9a1654-7673-4da3-bbae-daaa2f5cc715.zip`.


## v99 versus rank-45 Please: paired Contest counterdraft (18 Oct 2026)

The fresh [v99 group](https://2026a.battlecode.co.uk/game/match-groups/e0cdf2be-2e78-4e8c-b4ed-9ca36db12ada) lost 0-5. c418 kept Tavi rather than counterdrafting Ren after Please revealed Ren. Its Contest match used the exact same seed (`11295110919520135683`) as v98/c421 against the same opponent roster, making that one-map comparison paired:

| Contest measure | v98/c421, our Ren draft | v99/c418, our Tavi draft |
|---|---:|---:|
| Submitted gems, us:Please | 0:200 | 0:0 |
| Camp-clear entries, us:Please | 9:132 | 2:144 |
| Monster damage (k), us:Please | 48.1:170.8 | 16.8:177.9 |
| Deaths, us:Please | 85:23 | 94:11 |
| Kills, us:Please | 15:51 | 7:65 |
| Our first camp clear | r48 | r83 |

With Tavi, Team A got an early kill on enemy Varg at r43, but Tavi also died in that fight; the team never recovered its camp tempo. On v98, our Prism collected 200 gems at r1027, but Please's Ryth took them at r1063 and deposited them at r1109. The four other maps in v98 and v99 had matching seeds and identical results: Lanes 750:1,000, Eight 683:1,029, Interlock 204:1,004, Rows 528:1,056. v99 had three caught `Champion cannot act` messages on Contest and zero platform `botFault` events; that small count does not account for the result gap. Reject c418/v99; keep the Ren counterdraft, but do not treat c421's escort behavior as validated.

c423's local Contest “farm window” also failed its screen: 5/8 wins, equal to a fresh c417 control, with 4,600 versus 6,200 aggregate gems. It was not uploaded. Campaign after v99: **4 wins / 620 top-50 maps**, maximum streak 1, current **0/10**. The user's repeated [group dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) is the old 0-5 group against `new team(4)` and adds no results. Production source and ZIP remain unchanged.


## v100 candidate: Contest opening split (live result pending)

c425 starts Contest's existing tank-led and fighter-led farming squads from the opening; its early combat reach stays unchanged through round 149. The focused four-proxy screen was 8/8 and 7,200 aggregate gems versus c417's 5/8 and 6,200. On the broader 20-opponent Contest pool, both candidates scored 38/40; c425 earned 36,600 gems versus c417's 37,200 and lost to different matchups. This does not establish a broad local improvement, but the focused result justified one separate test upload, v100. Its bundle is `submissions/tungtungsahur-candidate-c425-contest-opening-split.zip` (SHA-256 `6D66DEC80AADAEB1197DE633473E640FC5867324DD834E405C56F8B055D4936D`). A fresh live group has not yet been run. The user's repeated `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` group is old and cannot test v100. Campaign remains **4 wins / 620 maps**, current streak **0/10**; production files remain unchanged.


## Offline replay deep dive: rank-49 Please on Contest (19 Oct 2026)

I inspected the existing v98/c421 Contest replay from group `8a9a1654-7673-4da3-bbae-daaa2f5cc715`, match `6197b74b-e853-406c-86d6-36e3721b5907`. The high-level farm and combat gap starts early:

- Please's Ryth cleared the first camp at round 27; our first clear was round 48, by Stellar.
- Please's Stellar bought Focus shards at round 37. Our Stellar's first recorded Focus purchases were at round 79.
- Our team killed Please's Varg at round 35, Cassi and Issac at round 43, and Ren at round 85. Please's Stellar then started killing our champions at round 101; it recorded 20 kills overall.
- Team totals were 132:9 camp-clear entries, 170.8k:48.1k monster damage, 23:85 deaths, and 14.2k:1.9k earned gold for Please:us. We collected a 200-gem reward at round 1027, lost it to Please's Ryth at round 1063, and it was submitted at round 1109. There were no platform bot faults or fuel exhaustion events.

The replay therefore shows an early farming lead, followed by a lethal Stellar power spike and repeated deaths that prevent our team from converting camps into gold. The later 200-gem carrier loss is real, but it occurs after the farm and combat deficit is already established. These figures are direct replay statistics; the conclusion that early economy compounds into the later wipe is an inference from their timing. The archived replay directory is `matches/live/8a9a1654-7673-4da3-bbae-daaa2f5cc715/6197b74b-e853-406c-86d6-36e3721b5907/`.

No new strategy has been validated against Please. Live unranked matches and uploads remain paused; local proxies cannot establish a top-50 result.


## Please draft-order counter experiment (19 Oct 2026)

The archived rank-49 Please Contest record has draft picks `[9,3,4,8,0]`, which map through the SDK enum to Varg / Cassi & Issac / Stellar / Ren / Ryth. A local synthetic proxy uses this exact order and an atlas planner, so it can test the draft profile and macro response but is not Please's bot.

Candidate c644 applies a two-tile enemy leash for the first 75 rounds on our Team A side and permits a shop recall past visible enemies farther than five tiles on Team B, only when the opponent uses that exact pick order. It won both sides twice against the proxy, but matched the current bot exactly on the 12-game strong Contest pool and 40-game broad Contest pool. The previous membership-only gate lost one `opp-swirl-meta-core` side because it shares the same picks in a different order. c644 remains a local-only candidate; the paused live queue has not validated it.


## c644 proxy side-by-side qualification (19 Oct 2026)

Both synthetic Please-proxy games ended at round 2000. In the current-source control, Team A scored 200:400 with kills 48:32, deaths 51:57, and earned gold 4,770:13,255; Team B scored 200:200 with kills 25:30, deaths 51:37, and gold 4,545:13,435. c644 scored 800:400 on Team A (kills 60:16, deaths 31:74, gold 7,320:9,130) and 200:0 on Team B (kills 22:52, deaths 73:31, gold 3,395:15,585). The Team A record is a positive combat signal against the proxy. Team B's timeout win comes despite a severe death and gold deficit, so it does not establish a robust map or farming advantage. This synthetic proxy is not the ranked Please executable; c644 remains unpromoted while live testing is paused.


## Offline Please counter combination c646 (19 Oct 2026)

c646 combines the exact-order Contest counter in c644 with c570's Lanes Ryth equipment queue for the Varg/C&I/Stellar/Tavi/Willow opponent draft. It scored 2/2 against each matching local synthetic proxy. Across the 20 local default opponents on Contest and Lanes it scored 79/80 (40/40 Contest, 39/40 Lanes), equal to current-source win counts with no winner flips. On six strong proxies across all 17 maps it scored 182/204 and exactly matched current c553 on all winners, scores, and rounds. The two matching bots are synthetic planners, not the ranked Please executable. c646 remains a local candidate; no official match or upload occurred.


## Correction: Please's recorded Lanes roster (19 Oct 2026)

The archived match-group JSON resolves the draft codes: Please's Contest picks `[9,3,4,8,0]` are Varg/Cassi & Issac/Stellar/Ren/Ryth; its Lanes picks `[9,3,4,8,10]` are Varg/Cassi & Issac/Stellar/Ren/Tavi. c644's exact-order Contest gate matches the first roster. c646's Lanes Team-A gear branch requires Willow, so it does not match the recorded Lanes draft. c646's Lanes proxy result uses a different synthetic Willow roster. The recorded Please Lanes loss was our Team A against Please Team B.

The follow-up Team-A Lanes Ryth queues against the matching synthetic Ren/Tavi roster did not establish a win gain: c647 (Monster Strength first) stayed 2/2 and 39/40 on the broad local Lanes pool, with no winner changes, while reducing both our own gold and gems in its Team-A target game; the target-side outcome repeated exactly. c648 (Power Strength first) fell to 1/2. The earlier Tavi-for-Ryth roster swap c569 was 0/2 against the Ren/Tavi proxy. Keep these local results separate from actual top-50 validation; live unranked testing is paused.

## c649–c654 Contest proxy follow-up (19 Oct 2026)

Against the local synthetic Please Contest proxy, c652's 2-tile leash through r99 repeated twice at 2/2 and reached 1,000:400 on Team A at r1998. c649, c650, and c653 each scored 1/2; c651 and c654's 2/2 results were weaker. c652 matched c646 on the broad 40-game and strong 12-game Contest sets, with no score or round changes outside the target proxy. These results do not count as top-50 wins; official unranked matches remain paused and production remains c553. Exact hashes and replay paths are in `bots/tungtungsahur/PLAN.md`.
A local cutoff bracket around c652 found that stopping at round 90 matched c652 exactly, while extending the narrow leash to include round 100 changed the Team-A proxy result from 1,000:400 to 200:400. Cutoffs at 105 and 110 also lost Team A. This suggests the safe local setting is to stop before round 100, but it is only one synthetic proxy and has not been tested against ranked Please. No official games were run; production remains c553.
The Contest equipment follow-up tested Monster Focus on Stellar because the rank-49 replay showed Please buying Focus early. c659 lost Team A to a 600:600 gem tie and gold tiebreak (8,070:10,205); the c652 Power Focus control scored 1,000:400. Though c659 died less, its economy and target result were worse. Keep Power Focus for this matchup; this local synthetic test does not validate against ranked Please.
The archived Lanes replay's event timestamps show Please cleared with Ren at r35 and Varg at r41, followed by Stellar at r48. Our Issac's first clear was r47, Ryth's r63, and Varg's r146. Please bought Power Focus on Stellar at r67 and Power Strength plus Durability Health on Ren at r68; our Stellar's Monster Focus purchases began at r73. The match had no deaths and ended 750:1,000 gems with 30:43 camp clears, identifying route throughput as the main Lanes gap. A turn-one split and an exact-draft round-45 split each scored 1/2 against the local synthetic proxy, repeating a 904:1,012 Team-A loss; keep the round-50 opening. This does not validate the route change against Please's executable.
Follow-up tests targeted the r41-vs-r146 Varg first-clear gap on Lanes. Removing Varg from early capture duty was an exact no-op against the synthetic proxy and across the full 40-game Lanes pool. A separate passive-camp route scored 1/2 (984:1,012 on Team A); a separate safe active-camp route also scored 1/2 (962:1,012). Keep the grouped opening pending real-match validation; the local proxy does not establish a Please counter.

Delayed versions of the separate passive route (c665 starts at r35, c666 at r40) each scored 1/2 against the synthetic Please-layout proxy, below c646's 2/2 control. Team A lost 882:1,012 at r585 with c665 and 868:1,012 at r517 with c666; both Team-B games repeated the 1,020:990 control. Reject these cutoffs. The actual Please replay remains evidence of a route-tempo deficit, but these local tests have not found a safe route adjustment and do not validate a top-50 counter.

A local Rows draft replay matched the archived rank-49 Please roster: the proxy drafted Varg/Cassi & Issac/Stellar/Ren and c593 drafted Varg/Cassi & Issac/Ryth/Ren. c593 beat it 2/2, but current production c553 repeated exactly the same drafts, scores (1,056:660 and 1,023:660), kills, deaths, and rounds. This isolates the result as a proxy weakness, not a c593 improvement. c593's full-map head-to-head against c553 was 16/34, with side-dependent outcomes and both Pilgrimage games lost; do not promote it based on the 630/680 and 187/204 pool metrics alone.

The archived rank-49 Please Rows replay shows the opener was almost tied (our first clear r29; Please r25), but clears ended 11:17. Our Cassi cleared no camps, Issac one, Varg three, Ryth three, Ren four; Please's Varg cleared four, Ren five, Stellar three, and both C&I champions added five more. A local draft-only test c667 prioritized Stellar after enemy Varg/C&I, but its 24-opponent Rows score fell to 46/48 from fresh production's 47/48, with no gains and one extra `ming_bot` loss. Please's local draft proxy also produced the same 2/2 result and exact scores for production, confirming no measured transfer from the draft change. Investigate sustained camp cadence instead of promoting c667.

The broader c667 Rows screen confirms the draft swap is not a reliable fix: 46/48 over 24 local opponents versus 47/48 for fresh production, no wins gained, and one extra loss to `ming_bot` on side B. Against c553 directly it split by side, losing 792:1,001 on side A and winning 1,023:924 on side B. Both builds still beat the exact-draft synthetic proxy 2/2. Keep c667 rejected; the live replay's sustained camp-clear difference remains unexplained by the near-tied opener.

The rank-49 Please Rows replay records its Cassi buying five Power Focus and four Durability Focus shards at r32; our Cassi's first purchases were at r201 (Power Focus) and r280 (Durability Health). Please's Cassi dealt 14.6k monster damage to our 4.1k. c668 swapped our second queue to Durability Focus but scored 46/48 across 24 local Rows opponents versus fresh c553's 47/48. c669 lowered Cassi's safe shop-trip threshold to 75 gold and lost both direct c553 games (990 gems on both sides, versus 1,012/1,056 for c553); both still beat the weak draft-only proxy, so that proxy does not validate the timing change. Reject both candidates. These purchases may reflect the income/clear gap rather than explain it.

A Rows-only objective test made Ren follow Issac's shared camp while retaining Ren's fighter role. c670 matched fresh production's 47/48 across 24 opponents, with the same sole meta-core side-A loss and no win changes. The exact-draft proxy stayed 2/2 but c670 banked fewer gems. This does not explain the official 11:17 clear gap; reject the objective change.


### Rows replay route follow-ups c671–c672 (19 Oct 2026)

The Please replay's side-A Ryth cleared gold-only wolf group 8 twice (r190 and r264) before his first gem-camp clear at r331. c671's separate passive route for Cassi failed to improve the focused local screen (4/6; losses on side B to c553 and the synthetic Please-layout proxy). c672 changed Rows Ryth's first emblem to Monster Strength while retaining Power Health; the 24-opponent screen was 47/48, identical to fresh production on every winner, with slightly lower own gems and a 1.8-round average finish improvement. These local tests do not explain the replay's 11:17 camp-clear deficit and are rejected as win-rate upgrades.


A Rows-only route test c673 told Ryth to skip gold-only camps. It lost both direct games to fresh c553, 990 gems each versus c553's 1,012 and 1,056. The two wins against the synthetic Please-layout proxy were not diagnostic because production also goes 2/2 against it. The attempt to remove the r190/r264 gold-only cycles therefore failed; they may fund purchases while nearby gem camps respawn.


### Rows Ren routing follow-up c674 (19 Oct 2026)

c674 routes Ren to a safe separate gem camp on Rows while preserving his fighter role and falling back to Issac's objective when no target is safe. It scored 11/12 versus 11/12 for fresh c553 on six strong local opponents, lowering average opponent gems by 38.5 and finishing roughly 20 rounds sooner; the 24-opponent pool had the same 47/48 wins and identical winners. Its exact-draft synthetic Please proxy remained 2/2 for both, and it did not remove the meta-core side-A loss. This is a local pace lead only, not a validated top-50 improvement.


### c675 integrated local comparison (19 Oct 2026)

c675 combines the Rows Ren separate gem route with c604's existing map-gated profiles. Against the same six strong opponents on all 17 maps, it tied c604 at 187/204 with identical winners; changes were confined to Rows. On the default 20-opponent pool, the recovered result was 631/680, again matching c604 with no winner flips. The single failed replay write reran in a unique directory as a clean 1,008–490 win at r708. This preserves a local candidate but does not constitute a top-50 win or improve the measured win count.


## c686 Stampede candidate uploaded as v101 (19 Oct 2026)

After local screening, c686 was uploaded through the authenticated CLI as test version 101. Its
separate bundle is `submissions/tungtungsahur-test-c686-stampede.zip` (32,490 bytes; SHA-256
`B2920032530E5AA9D2124D5296C2D6C967B6ADEF03BF2EC783BBD8D3D0BD252A`). c686 scored 633/680 on
the local 17-map, 20-opponent pool and 39/40 on Stampede in two runs. Production `tungtungsahur`
and `submissions/tungtungsahur.zip` were not changed, and the test candidate has not been submitted
as the production build.

The supplied `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` group is the old v60 group versus then-rank-5
new team(4), not a v101 test. A fresh unranked group is required. TinyFish reports installed/enabled,
but its browser controls are not exposed in this session; the desktop command guard also rejected
opening the match-group page. No v101 game has run, so the official streak remains 0/10.
