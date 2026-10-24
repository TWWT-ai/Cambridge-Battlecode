# Top-50 and unranked evaluation — 17 October 2026

## Scope and limits

The original public ladder response is saved in [`top50-20261017.json`](top50-20261017.json); a fresher snapshot is [`top50-20261017-1442.json`](top50-20261017-1442.json), with ladder data updated at 14:41:59 UTC. The API did not return a stable snapshot ID. `cambc login` reports a valid seven-day CLI session, but the challenge endpoint still returns `SIGN_IN_REQUIRED` with that CLI token. No unranked match was created. Local league results are proxy tests, not wins against current top-50 teams, so the requested 10-win streak remains at 0/10.

The latest ladder's `mostPickedChampions` entries, summed across these 50 team records, report Cassi & Issac 2,192 picks, Stellar 2,045, Ren 968, Varg 821, Ryth 393, Tavi 248, Vendetta 93, and Willow 33; Prism is absent. These are each team's reported top-three fields, not a complete match-by-match draft history.

The following is the initial live challenge queue, in current ladder order. The reported picks are each team's top-three fields, not its full draft history.

| Rank | Team | Rating | Reported top picks |
|---:|---|---:|---|
| 1 | Intercontinental Fish | 2058.2 | C&I 50, Stellar 50, Ren 46 |
| 2 | Mite | 2017.1 | C&I 50, Stellar 45, Ryth 39 |
| 3 | Sneaky Bush Campers | 1982.1 | Stellar 49, C&I 39, Ren 33 |
| 4 | Nyxius | 1981.7 | C&I 50, Stellar 45, Ren 43 |
| 5 | procless | 1958.6 | C&I 50, Stellar 50, Ryth 39 |
| 6 | Univardisty of Shingtonwash | 1916.5 | C&I 50, Stellar 50, Tavi 49 |
| 7 | Nyx | 1893.3 | Stellar 50, C&I 49, Ren 40 |
| 8 | new team(4) | 1881.9 | C&I 50, Stellar 50, Varg 50 |
| 9 | AlphaSlop | 1877.4 | C&I 50, Stellar 50, Ren 27 |
| 10 | Boost | 1845.4 | Stellar 50, Tavi 46, Ren 34 |

The five leading teams all report C&I and Stellar in their top three; Ren appears in three of those five, and Ryth in two. Public `/api/v1/teams/{id}/performance` data exposes rating history but no map split, so map-specific conclusions need match groups. The public `GET /api/v1/match-groups/{id}` endpoint returns each map result and replay URL once a group exists; a public Fish–Mite match group was inspected. The ladder alone does not reveal full map-specific strategies.

## Candidate results

The baseline reference is `u4`: 432/480 in the 24-opponent local league and 55/60 against `ming_bot`, `xuanming`, and `faisal-orig`.

| Candidate | Full local league | Strong local proxies | Race vs idle | Decision |
|---|---:|---:|---:|---|
| User lineup: Ryth, Vendetta, Tavi, Willow, Prism | 111/480 | 7/60 | not run | Reject as a drop-in draft |
| User lineup with phase advancement on any champion's emblem | 296/480 | 35/60 | not run | Better than the unmodified user lineup, still far below baseline |
| Top-pick draft: Cassi & Issac, Stellar, Ren, Varg, Ryth | 414/480 | 53/60 | not run | Keep the current draft |
| Early Varg solo on every map | 418/480 | 51/60 | 10,129 rounds | Reject as an all-map change |
| Early Varg solo on Collect, Corners, Monolith, and Rows | 425/480 | 52/60 | 10,023 rounds | Keep as a research candidate; does not beat baseline |
| Varg-first top-meta draft on every map | not run | 71/80 | - | Reject: 2 fewer wins than main on the same four sources |
| Varg replaces Ryth only on 80×80 Expanse | 434/480 | 76/80 | - | No promotion: exact same-session main scored 432/480, so the +2 difference is within noise |
| On Expanse, switch to C&I/Varg/Stellar only after enemy Varg appears | 435/480 | 77/80 | - | Best tested Expanse response; +3 vs main is still inside noise, so no promotion |
| Prism / Stellar / C&I / Ryth / Tavi draft on Contest and Stampede | 108/136 current pool (main 104/136) | 15/16 in each of two candidate runs; main 11/16 in two matched baselines | - | Best current-pool candidate; +4 wins all come from these two maps; retain in candidate pending top-50 validation |
| Contest defensive emblems first | 5/8 Contest (candidate 7/8) | - | - | Reject; more deaths and no win gain |
| Contest team-gather then Monolith rush | 6/8 Contest | - | - | Reject; deaths fell to 43.1/game, but win count fell by one |
| Contest Monster damage emblem first | 6/8 Contest | - | - | Reject; below the current candidate |
| Contest Ryth escort for a 100+ gem carrier | 6/8 Contest | - | - | Reject as general behavior; fixes Ming side B but adds Xuanming and Faisal losses |

League summaries and replays are in `matches/league/20261017-143045-cand-user-roster`, `20261017-144456-cand-user-phase`, `20261017-144111-cand-ren-meta`, `20261017-143648-cand-early-varg`, `20261017-144922-cand-varg-gated`, `20261017-145904-cand-varg-meta`, `20261017-150005-tungtungsahur`, `20261017-150356-cand-expanse-varg`, `20261017-150702-tungtungsahur`, and `20261017-151324-cand-expanse-counter`. Strong-proxy summaries are in the adjacent runs tagged `varg-meta-strong-sources`, `main-meta-strong-sources`, `expanse-varg-strong-sources`, and `expanse-varg-counter-strong`.

The unmodified user lineup has no Stellar or Varg, but the existing phase controller waits for one of those champions to complete an emblem before entering mid game (with a round-600 fallback). In an Expanse loss against Ming, it had 58 gems to Ming's 144 at round 100 and 356 to 978 at round 510, with no deaths. That replay points to a farming-pace loss. Advancing phases on any champion improved the user lineup's league score to 296/480, but it still recorded 2,225 deaths across 480 games and lost to the baseline by 136 wins.

On the current 17-map pool, main scored 104/136. Candidate #78 uses Mite's observed Prism / Stellar / C&I / Ryth / Tavi draft only on Contest and Stampede, the two maps with contested camp altars. It scored 108/136; the only per-map changes were Contest 5/8→7/8 and Stampede 6/8→8/8. Repeated targeted runs gave 15/16 to the candidate twice and 11/16 to main twice. Contest deaths fell from 56.9 to 48.8 per game, but the candidate's Ming side-B loss still ended 200–200: after banking 200 by r1100, Stellar died carrying another 200 at r1911, following an enemy altar lock at (25,24) at r985. Four follow-up variants (#79–82: defensive items, earlier Monolith, camp damage, and tank escort) scored only 5–6/8, so none replaces candidate 78. This is local evidence, not progress on the requested live streak.

The follow-up run folders are `matches/league/20261017-155738-cand-contest-iron-test`,
`20261017-155745-cand-contest-rush-test`, `20261017-155843-cand-contest-monster-test`, and
`20261017-160055-cand-contest-escort-test`.

The all-map early Varg test sped the idle race by only 182 rounds over the original main idle run, while reducing the league score to 418. Gating the change to Collect, Corners, Monolith, and Rows improved race speed more clearly (10,023 rounds versus 10,311 on the original main idle run), but scored 425/480. The project treats about ±8 league wins as noise and only promotes candidates that beat the current main, so this change stays in its candidate folder.

The top-pick Ren draft is not a drop-in improvement either: 414/480. Ren currently falls through to the generic Fighter role, so a dedicated Ren plan may be worth a separate, matchup-driven experiment after live logs are available.

The consistent current-main loss against the four strong local sources is Expanse side B. The replay against the Ming-style Varg/Stellar draft starts with us ahead, then falls behind by round 200 and continues losing the score race without deaths. On the archived Ming and Xuanming variants, the two deaths at r484 also drop a 48-gem bag. Replacing Ryth with Varg only on 80×80 Expanse changes those two matchups from 19/20 to 20/20 in the strong-source set. An opponent-aware version keeps the main draft order until an enemy Varg pick is visible, then completes C&I/Varg/Stellar. That variant scored 435/480 overall and 77/80 on the four sources, the best tested Expanse response so far; the +3 full-league gain is still within the ±8 noise band, so it remains unpromoted.

## Current practical strategy

- Keep the current Stellar / Cassi & Issac / Ryth / Varg / Tavi draft and role item builds. The available tests do not support replacing them with the user lineup or a direct Ren swap.
- Preserve fight-oriented equipment. Earlier farm-damage equipment variants gained little race speed and lost local league wins; the Home shard variation tied the baseline.
- Map-specific early solo farming is a promising test direction, but the Varg-only candidate has not passed the full league gate. Avoid enabling solo wolves everywhere; previous tests lost fights on Collision and Interlock.
- The existing [`maps.md`](maps.md) analysis contains map routes, altar locations, camp yields, and the per-map banking / defense recommendations.

## Next step for live validation

The CLI login flow is approved and `cambc` is signed in, but that credential does not establish the browser session required by `/api/v1/challenges`. TinyFish is available, but remains uninstalled and unconnected in this session. Once a game-site browser session can be used to create an unranked group, compare tribute pace, enemy captures, deaths, and altar-lock behavior on every map. Do not describe local proxy results as the requested 10 consecutive top-50 wins.

## Current 17-map pool tests (17 October 2026)

The refreshed map pool is listed in `analysis/map-pool-20261017.json`. Main's local baseline scored
**104/136** over all 17 current maps, 8 games per map against `ming_bot`, `xuanming`, `faisal-orig`,
and `opp-racer`. These four are local proxies; this is not a top-50 win count. Map refreshes changed
some same-named layouts, so this score is not comparable to the earlier 432/480 result on the old pool.

| Map | Wins / 8 | Average submitted gems (our bot / opponent) |
|---|---:|---:|
| ambush | 6/8 | 408 / 316 |
| collision | 4/8 | 650 / 703 |
| contest | 5/8 | 425 / 200 |
| corners | 8/8 | 970 / 507 |
| eight | 7/8 | 945 / 330 |
| elkring | 7/8 | 965 / 619 |
| expanse | 5/8 | 907 / 869 |
| fragment | 7/8 | 944 / 534 |
| interlock | 8/8 | 990 / 572 |
| lanes | 4/8 | 923 / 934 |
| monolith | 7/8 | 972 / 678 |
| packs | 8/8 | 974 / 368 |
| pilgrimage | 5/8 | 868 / 756 |
| rows | 8/8 | 978 / 747 |
| rushbait_v2 | 5/8 | 916 / 892 |
| stampede | 6/8 | 712 / 285 |
| swirl | 4/8 | 769 / 680 |

The clearest structural issue is Lanes: the bot lost all four side-B games but won all four side-A
games. Against an idle bot, its times to 998 were r623 on A and r635 on B, so its base route is nearly
mirror-balanced; against stronger bots it loses the central economy race as second mover. Swirl is a
fight problem: the bot lost both sides against Ming and Xuanming, with sampled matches showing 47–70
deaths and 132–198 gems lost. Collision losses against Ming showed 15–16 deaths and repeated locks at
the only walkable altar, (27,20).

Swirl experiments did not produce a promotion: replacing Varg with Vendetta scored 0/4 against Ming
and Xuanming; replacing Ryth with Vendetta while retaining Varg also scored 0/4. Keeping the whole team
grouped through round 600 scored 4/8 across all four local sources, equal to main, and only 1/4 against
Ming and Xuanming. All candidates remain isolated; `bots/tungtungsahur/src` and
`submissions/tungtungsahur.zip` are unchanged.

An idle control on Lanes, Swirl, Contest, Stampede, and Pilgrimage went 10/10, but reached only 800/400
gems by r2000 on Contest, 720 on Stampede, and 972 on Pilgrimage. This supports the current map report's
finding that Contest and Stampede are controlled by scarce, difficult camp sources rather than ordinary
solo farm loops. See `analysis/maps.md` for the refreshed model and provisional map-specific strategies.

A Lanes-only candidate letting Varg solo farm from round 1 scored 2/8 against the four local proxies,
down from main's 4/8. The Lanes idle control is nearly side-balanced (r623 A, r635 B), so the main's
four side-B proxy losses reflect the contested opening against faster opponents, not a broken route.

Experiment 78 uses `bots/cand-contest-prism`: on Contest and Stampede only, it drafts Prism, Stellar,
Cassi & Issac, Ryth, Tavi; all other maps retain the current main lineup. Full-pool candidate run
`matches/league/20261017-154817-cand-contest-prism` scored 108/136 against main's 104/136; the 15
other map scores are identical. Candidate targeted run `20261017-154718-cand-contest-prism` scored
15/16, and the full-pool run also scored 15/16 over the same two maps. Main scored 11/16 in the full
pool and repeated that result in `20261017-154932-tungtungsahur`. Keep the candidate isolated pending
live validation; the main source and `submissions/tungtungsahur.zip` are unchanged.

Public top-1-vs-top-2 group `dbad7f6f-421b-42a4-91e2-46b125d6e582` was Mite 3–2 over Intercontinental
Fish across Packs, Rows, Rushbait v2, Stampede, and Contest. Mite won Rows and Stampede; Fish won Packs
and Rushbait. The API records Mite as the Contest winner after 2,000 rounds, but both teams scored 0,
so do not treat that as evidence of map dominance. Mite drafted Prism / Stellar / Cassi & Issac / Ryth /
Tavi on Contest and Stampede; those map-specific drafts motivated candidate 78.

The user selected “Enable TinyFish” and its connection prompt was surfaced, but its latest confirmed
state is still `installed: false`. The live challenge API still requires a game-site browser session,
so the unranked top-50 streak remains **0/10**. Do not count these local tests toward it.

### Follow-up experiments (17 Oct, later session)

Collision teleport banking did not improve the local result: the 100+ gem version scored 4/8 (same
number of wins as main), and using it for any positive bag scored 2/8. The route did activate in
replays, but did not solve the contested altar/economy problem. These are experiments 83-84 in
`bots/tungtungsahur/PLAN.md`.

Experiment 85 replaces Ryth with Varg only on Collision and retains experiment 78's Prism draft on
Contest and Stampede. Its full 17-map pool scored **109/136**, against **108/136** for experiment 78
and **104/136** for main. The only changed map score versus experiment 78 is Collision, 4/8 -> 5/8;
Contest is 7/8 and Stampede is 8/8. Collision Varg won one Xuanming game but still lost both games
against Ming. This remains an isolated local candidate, not a verified top-50 strategy. Main source
and submission ZIP remain unchanged. The live top-50 unranked streak is still **0/10**.

### Collision and Swirl follow-ups (17 Oct, later session)

Experiments 86-87 did not improve Collision: Varg taking Jungle Health first and a
Cassi & Issac / Ryth / Varg draft both scored 4/8, below experiment 85's 5/8. Both lost all four
games against Ming and Xuanming. Experiment 88 gave Varg and the mage Jungle Health first on Swirl;
it reduced sampled deaths but scored 3/8 versus 4/8 for the current candidate and remained 0/4
against those two strong proxies. The lower damage build reduced gem throughput enough to erase its
survival gain. Replay and run evidence is summarized in bots/tungtungsahur/PLAN.md and
analysis/maps.md.

The best full-pool local candidate remains experiment 85 at 109/136. No new live matches were
created: TinyFish remains installed: false, so the unranked top-50 streak remains **0/10**.

Experiments 89-90 kept the Swirl result at 4/8 with Varg assigned to a three-body squad, then
dropped it to 2/8 when banking was delayed to 150 gems unless an enemy was visible. The delayed
bank variant lost 1,802 carried gems in deaths across its four Ming/Xuanming games (647 for the
matched experiment 85 games). Immediate banking remains the stronger tested choice under combat
pressure. The per-map no-contact simulator is useful for forming hypotheses, but it did not predict
these local-proxy outcomes.

Experiment 91 adds the Expanse C&I / Varg / Stellar draft order to candidate 85. The combined
candidate scored 112/136 across the full 17-map, four-proxy league, against 109/136 for candidate 85
and 104/136 for a same-session main recheck. Its only new map improvement is Expanse, from 5/8 to
8/8; Collision, Contest, and Stampede retain their earlier gains, and the other thirteen maps match
main. It gained three wins against Ming, four against Xuanming, none against Faisal, and one against
opp-racer. This is the best local candidate, but it is still not live top-50 validation; the live
unranked streak remains 0/10.

### Pilgrimage and Lanes follow-ups (17 Oct, later session)

Experiments 92-94 failed to improve Pilgrimage's 5/8 result: lowering the bank trigger to 100 scored
4/8; splitting from round 1 remained 5/8 but traded two wins over Ming for a loss to Xuanming on
both sides; replacing Ryth with Vendetta scored 3/8 and lost all four games to Ming/Xuanming.
Experiments 95-97 also failed to improve Lanes against the strongest local proxies. A round-200
split fell to 3/8. Replacing Ryth with Ren stayed at 4/8 and went 0/4 against Ming/Xuanming;
replacing Tavi with Ren rose to 5/8 overall but reduced Ming/Xuanming wins from 2/4 to 1/4. Keep
experiment 91's drafts, opening, bank logic, and equipment in the isolated best candidate.

Runs: `matches/league/20261017-163317-cand-pilgrimage-bank100`,
`20261017-163437-cand-pilgrimage-mid-open`, `20261017-163547-cand-pilgrimage-vendetta`,
`20261017-163709-cand-lanes-mid200`, `20261017-163746-cand-lanes-ren`, and
`20261017-163824-cand-lanes-ren-tank`. The current best full-pool local candidate is still
experiment 91 at 112/136. No live unranked game was created, so the current top-50 streak stays
0/10; the TinyFish browser connector is not yet installed/connected. Main source and submission
ZIP remain unchanged.


### Rushbait opening and movement follow-up (17 Oct 2026)

Experiment 99 starts the mid-game squad phase immediately on Rushbait v2 (30x80), regardless of side. Two targeted repetitions scored 7/8. Integrated with the current map-specific candidate, it scored 113/136 across 17 maps and four strong local proxies (previous candidate #91: 112/136; same-session main: 104/136). Rushbait improved 5/8 to 7/8; Stampede declined 8/8 to 7/8, for a net one-win gain. The expanded 680-game pool scored 592/680, versus 587/680 for #91 and 577/680 for main. Most broad-pool gains came from Rushbait (35/40 to 39/40) and Swirl (34/40 to 35/40). The candidate remains a local proxy result, not top-50 match evidence.

Experiment 98's blocked-move fallback was rejected: it held 112/136 on the strong set but fell to 586/680 in the broad set after one Ambush side-B loss to the Bruiser proxy. The side-specific Rushbait branch runs scored 3/8 and 4/8 but logs show the early condition never triggered, so they are invalid tests of the proposed behavior.

The isolated best is now bots/cand-best-expanse-meta, with its Rushbait opening update. Runs: matches/league/20261017-171120-cand-best-expanse-meta (strong) and 20261017-171232-cand-best-expanse-meta (broad); movement fallback broad run 20261017-165306-cand-move-fallback. The live unranked top-50 streak remains 0/10. Main source and submission ZIP remain unchanged.


### Lanes side-B equipment follow-up (17 Oct 2026)

The Lanes side-B losses are still the clearest economy weakness. A side-B-only opening split did not add wins. Tavi's Monster Strength first build on both sides stayed 4/8 and fell to 1/4 against Ming/Xuanming, so it was rejected. Restricting the same item sequence to side B scored 5/8 in two targeted repeats and improved Lanes from 4/8 to 5/8 in the full strong-proxy set. This raised the full result from experiment 99's 113/136 to 114/136, with no other strong-set map regressions; broad results rose from 592/680 to 593/680. The broad paired comparison changed three side-B outcomes: two losses became wins and one win became a loss. The result is a small local improvement, not live top-50 evidence.

Current isolated local best: bots/cand-lanes-sideb-tavi-monster. Strong run: matches/league/20261017-172556-cand-lanes-sideb-tavi-monster; broad run: 20261017-172648-cand-lanes-sideb-tavi-monster. The requested live streak remains 0/10. TinyFish is still not installed, and main source plus submission ZIP remain unchanged.


### Fresh-build controls and match analysis (17 Oct 2026)

The valid v104 build scored 117/136 against the four strong local proxies, versus 104/136 for a fresh main-source build under the same candidate name. Fourteen main losses became wins and one Rushbait win regressed. In the broad pool, v104 scored 610/680 versus 593/680 for the freshly rebuilt no-recovery source; Ambush rose 21/40 to 40/40. A second, narrowed lookup variant scored 611/680 broad but 116/136 strong, so v104 remains the leading local candidate for the top-team target.

Earlier “identical source-swap” results are invalid: the copied source files retained older timestamps, so the incremental build reused v104's WASM. The corrected comparisons refreshed timestamps, explicitly rebuilt, and verified distinct WASM hashes. Run IDs and map-level outcomes are in `bots/tungtungsahur/PLAN.md`.

The v104 losses to `ming_bot` cluster around central-altars, farming pace, and deaths: Collision lost 416–968 and 254–924 with 22/14 deaths; Swirl lost 352–990 and 476–980 with 55/47 deaths; Pilgrimage lost 596–924 and 692–980. Contest and Stampede also reached tied scores at the 2000-round cap. These are proxy findings, not live top-50 evidence.

No live unranked top-50 match has been created; the requested streak remains 0/10. TinyFish remains uninstalled, so the challenge API's browser session is unavailable. Main source and submission ZIP remain unchanged.

### Corrected broad control and Swirl follow-up (17 Oct 2026)

With fresh builds and different verified WASM hashes, v104 scored 610/680 in the broad local league versus 577/680 for a freshly rebuilt main source (`20261017-192402-cand-ambush-stall-recovery`). Map deltas were Ambush +19, Expanse +6, Stampede +4, Rushbait v2 +3, Contest +2, Lanes +1, Swirl +1, Collision -2, and Pilgrimage -1; all other map totals matched. V104 scored 117/136 in the strong local-proxy league versus main's 104/136.

The follow-up Swirl-only late-retreat rule was a no-op in observed play: it stayed 0/4 against Ming/Xuanming, and all four replay ZIP hashes matched the v104 controls exactly. TinyFish has been surfaced for connection, but its latest confirmed state is still installed=false. No live matches were created; the live streak remains 0/10, and the main source and upload ZIP are unchanged.

Swirl's health-based recall threshold was tested at 50% and 40%. The 50% variant scored 3/8 on the targeted set versus v104's 4/8. The 40% variant tied at 4/8 and reached 118/136 strong, but its broad score was 607/680 versus 610/680 for v104; broad Swirl declined from 35/40 to 32/40. Reject both thresholds and retain v104's defaults. Its source was restored with the original v104 source hash and rebuilt WASM hash.

On Pilgrimage, Tavi buying Monster Strength before Power Focus scored 5/8 in the targeted set versus 6/8 for v104 (`20261017-194005-cand-ambush-stall-recovery` vs `20261017-175715-cand-ambush-stall-recovery`). This experiment was rejected without a full-pool run; the v104 source and build are restored.

Proactively attacking a visible home altar lock while empty also scored 5/8 in two repeat Pilgrimage runs, versus v104's 6/8. It won one Ming side but lost both Xuanming sides. Reject the change; v104 has been restored.

On Collision, clearing the single central altar lock while empty scored 4/8 versus v104's 5/8, and still lost all four Ming/Xuanming games (`20261017-194508-cand-ambush-stall-recovery`). Reject the change. The v104 source and WASM were restored after the test.

Replacing Collision's Varg pick with Tavi tied v104 at 5/8 and remained 0/2 against Ming (`20261017-194617-cand-ambush-stall-recovery`). Reject the draft and restore Varg.

On Swirl, moving Varg to Ryth's camp improved the average gem score against Ming, but the variant stayed 0/4 against Ming/Xuanming and fell to 34/40 across the 20-opponent Swirl pool versus v104's 35/40 (`20261017-194840-cand-ambush-stall-recovery`). Reject it; v104's solo Varg behavior is restored.

## Latest isolated local candidate: experiment #115

On Lanes side B, increasing the gold threshold for a shopping recall from 150 to 250 produced 6/8 in two targeted strong-proxy repeats. A fresh v104 control scored 5/8. Integrated results were 118/136 strong versus 117/136 and 611/680 broad versus 610/680; only the Lanes map total improved. The active candidate is `bots/cand-ambush-stall-recovery/src/bot.cpp`, with snapshot `candidate-source-v115-lanes-shoptrip250.cpp`. It remains isolated from main and the submission ZIP.

TinyFish now reports `installed: true`, but its browser actions are not exposed in this session. No browser-backed challenge or live win has been recorded; the live streak remains **0/10**. Main source and submission ZIP hashes remain unchanged.

Follow-up threshold sweep: 200 gold scored 5/8 in two identical Lanes strong-proxy runs (`20261017-195844` and `20261017-195930`); 300 gold scored 3/8 (`20261017-195907`) and lost both Faisal games. Reject both values. The side-B 250-gold rule remains the local leader at 6/8 targeted, 118/136 strong, and 611/680 broad.

## Swirl and Collision draft follow-ups

Swirl's Willow-for-Varg support draft tied the baseline at 4/8, but lost all four Ming/Xuanming games and finished at much lower average gem totals (195 and 427); reject it (`20261017-223244`). On Collision, Ryth/Vendetta/Tavi scored 2/8, Ryth/C&I/Tavi scored 1/8, and replacing only Varg with Ryth scored 4/8 versus 5/8 for the current lineup. All variants lost every Ming/Xuanming game (`20261017-223334`, `20261017-223401`, `20261017-223428`). Keep the standard Swirl and Stellar/C&I/Varg Collision drafts. These remain local proxy results; the live streak is still 0/10 because TinyFish browser actions are not available in this session.

## Live unranked group supplied by the user

Group `4cf7ad87-2c52-452e-a9a3-59787c302e67` finished 0–5 for Heavenly Court against FRChronic. The five maps were Interlock (750–1004), Stampede (0–1080), Elkring (432–1008), Fragment (286–1018), and Pilgrimage (596–1027); all ended by gems with no bot errors reported. FRChronic's performance endpoint placed it at rank 58 around the match, outside the top 50, so the requested top-50 streak stays 0/10. It drafted C&I and Stellar in all five matches and Varg in four. Heavenly Court's draft matches the current main draft order, but the group response has no submission/version ID. The data points to a substantial gem-income gap, especially Stampede's zero, but replay-level causes remain unverified because this runtime cannot access the signed-in replay bundles. See [`platform-match-review-4cf7ad87.md`](platform-match-review-4cf7ad87.md).

The Stampede follow-up freshly paired main against the isolated v115 candidate on both sides versus Ming, Xuanming, Faisal, and opp-racer. Main scored 6/8; v115 scored 7/8 by converting the Xuanming side-A loss. The candidate's Prism/Stellar/C&I/Ryth/Tavi draft is the same five-champion composition as FRChronic used in the live Stampede game; main used Stellar/C&I/Ryth/Varg/Tavi. Monster Strength-first builds for Tavi, Prism, or both scored 7/8, 6/8, and 5/8, so none improved on v115's existing 7/8. Keep the current equipment and candidate draft isolated pending a top-50 live test. The 40-match screen, manifest, and replay bundles are under `matches/league/20261017-2301-stampede-monster-screen/`; local results do not count toward the live streak.

A fresh full-ladder read at `/api/v1/teams/leaderboard?limit=50` returned `401 SIGN_IN_REQUIRED` from this runtime. Until browser-backed access is exposed, use the saved 14:41 UTC top-50 snapshot as historical context only; it does not establish the current complete top 50. FRChronic's team performance history did establish rank 58 around the user-supplied group's match time.

## Stampede shared-team follow-up (17 Oct 2026)

The isolated #126 branch delays Stampede's mid-game split until Stellar's late-game flag. It scored
8/8 against Ming, Xuanming, Faisal, and opp-racer on both sides; a fresh v115 control scored 7/8.
Against the 22 local opponents on Stampede, it scored 41/44 versus 36/44 for v115. Six losses became
wins and one win became a loss; the change reduced deaths and gems lost in the Ming side-A replay and
turned its 900–900 round-cap loss into a 900–180 win at r1695. The complete run IDs and candidate
hashes are in `bots/tungtungsahur/PLAN.md`. This remains local-proxy evidence and contributes no live
top-50 wins.

Timing sweeps that held the shared phase through round 900 or 600 scored 7/8 and were rejected. A
round-900 check after the late-game flag was an exact no-op (identical Ming replay ZIP hash). Keep #126
isolated at `bots/cand-stampede-team/src/bot.cpp`; #115 remains the all-map tested candidate pending a
full pool comparison.

Access recheck after the supplied group link: the public group endpoint is readable, while the 50-team
leaderboard, the match summary, and the replay bundle return HTTP 401. TinyFish is installed and
enabled, but no TinyFish browser-action tools are exposed in this session. The top-50 win streak is
still **0/10**; FRChronic's rank 58 around the supplied group remains outside the target.
# Latest local candidate and live-match status (17 Oct 2026)

The current isolated local candidate is experiment #131, based on the Stampede shared-farm phase from #126. It scored 119/136 against the four strong local proxies (same outcomes as #126) and 614/680 in two identical broad 17-map runs; #126 scored 612/680 broad. The gains over #126 came from Stampede and Pilgrimage, with one Lanes loss. These are local proxy games, not current top-50 games.

The user-supplied unranked match group 4cf7ad87-2c52-452e-a9a3-59787c302e67 finished 0–5 against FRChronic, ranked 58 around the match. Heavenly Court scored 750, 0, 432, 286, and 596 on Interlock, Stampede, Elkring, Fragment, and Pilgrimage; FRChronic scored 1004, 1080, 1008, 1018, and 1027. The group reports no bot errors, but the replay and per-match summary endpoints still require the signed-in browser session. The top-50 consecutive-win streak remains 0/10. Main source and ZIP remain unchanged.
# Local candidate update (18 Oct 2026)

Experiment #133 is the current isolated candidate. It changes only Elkring's five-pick order to put Varg before Ryth and preserves the existing Fragment three-pick lineup. Against four strong local proxies it scored 120/136 twice (exact same outcomes); in the 20-opponent broad pool it scored 618/680 twice (exact same outcomes), versus #131's 119/136 and 614/680. The broad gains were four Elkring wins, with no other map total changes. These local proxies are not the requested current top-50 unranked matches.

The live group 4cf7ad87-2c52-452e-a9a3-59787c302e67 remains a 0–5 loss to FRChronic, rank 58 around the match; the top-50 streak remains 0/10. The group record exposes scores and drafts, but this runtime has no browser action to retrieve the authenticated replay bundles. Main source and submission ZIP are unchanged.
# Pilgrimage follow-up (18 Oct 2026)

Starting from #133, Varg-before-Ryth on Pilgrimage and Ren-for-Tavi each scored 5/8 in the targeted strong-proxy set, below the baseline's 6/8. The Varg order raised gem totals against Ming but did not win; Ren converted one Ming side but lost both Xuanming games. Keep #133's existing Pilgrimage draft. These results do not count as live top-50 wins.
# Public rank refresh (18 Oct 2026)

The leaderboard endpoint still returns HTTP 401. FRChronic's public performance endpoint is readable; its latest published history point is rank 67 at 2026-10-17 23:00:35 UTC, while it was rank 58 around the supplied unranked group. This latest point remains outside the top 50 but does not verify the live ranking on 18 Oct.
# Candidate test package (18 Oct 2026)

The #133 candidate is packaged at submissions/tungtungsahur-candidate-v133-unranked-test.zip for an unranked platform test. Its source files match the tested candidate directory. It has not been uploaded; the main submission ZIP remains unchanged.
# Swirl follow-up (18 Oct 2026)

The Varg-before-Ryth order change scored 3/8 against the four strong local proxies versus #133's 4/8 control. It did not improve results against Ming or Xuanming and lost an additional opp-racer side. Reject it; the top-50 live streak remains 0/10.

### Equipment experiments after #136

Against Ming and Xuanming on all maps and both sides, Issac's five Jungle Health then Durability Health sequence tied the #133 baseline at 54/68 (#137); Stellar's Treasure Focus-first build fell to 50/68 (#138). Both changes are rejected, and #133 is restored. No live top-50 progress is counted.

## Latest isolated candidate and live status (18 Oct)

#141 caches the Swirl map check during initialization and retreats at strength parity only on Swirl. It scores 121/136 against four strong local proxies (one above #133) and 613/680 in two broad repeats (five below #133, with the difference confined to Swirl). Its test ZIP is `submissions/tungtungsahur-candidate-v141-unranked-test.zip` and remains local; its source was uploaded as distinct candidate submission version 25. #133 remains the broad-pool control. The live top-50 streak is still 0/10 because browser-action tools are not exposed to this runtime even though TinyFish is installed/enabled. Main source and submission ZIP hashes remain unchanged.

## Current candidate #143 (18 Oct)

Enemy-draft analysis showed that Ming and Xuanming both used Cassi & Issac / Varg / Stellar / Vendetta on Swirl. #143 uses the parity-retreat threshold only for that lineup on Swirl. It scored 1/4 in the targeted Ming/Xuanming Swirl screen versus #133's 0/4, 121/136 strong proxies twice versus 120/136, and 618/680 broad games twice. Broad map totals exactly match #133; the strong gain is one extra Swirl win. The separate test source was uploaded as candidate submission version 26; the verified ZIP is `submissions/tungtungsahur-candidate-v143-unranked-test.zip`. No live top-50 games count yet; streak remains 0/10. Main source and ZIP are unchanged.

## Collision mirror follow-up (#144, 18 Oct 2026)

The #143 control scored 1/4 against Ming and Xuanming on Collision with a mirrored Cassi & Issac / Varg / Stellar core. Raising the retreat threshold to 1.5x scored 0/4; reject #144 and restore #143. Runs: `20261018-004844-cand-stampede-broad-pair` (control) and `20261018-004856-cand-stampede-broad-pair` (#144).

The supplied match-group URL is still the 17 Oct group, finished 0-5 to FRChronic with submission versions unavailable (`null`); it does not contain candidate v26 results. Live top-50 streak remains 0/10.

## Candidate #145: Pilgrimage banking route (18 Oct 2026)

The #143 Pilgrimage side-B loss to Faisal-bot carried Tavi's 144-gem bag into the west side of the map; the enemy recovered it, and death losses totaled 236 gems. #145 prefers allied-half altars for bags of 100+ gems only on Pilgrimage. It scored 31/40 twice against the 20-opponent local pool, versus a fresh direct-runner #143 control at 29/40. Gains were isolated to one Faisal-bot and one opp-tts-aggro side. The four-proxy screen stayed 6/8. This improves the local map result but is not a current top-50 win. Candidate source was uploaded as separate submission version 27; main source and ZIP are unchanged.

The supplied match-group URL still resolves to the finished 17 Oct 0-5 FRChronic group; it predates v26/v27 and exposes no submission versions. The current leaderboard endpoint returns `401 SIGN_IN_REQUIRED`. Live top-50 streak remains 0/10.

## Candidate v27 full-map recheck (18 Oct 2026)

The #145 source uploaded as candidate submission v27 completed a direct-runner 17-map, 20-opponent local pool at 620/680, two wins above the fresh #143 same-runner control at 618/680. Only Pilgrimage changed (29/40 to 31/40); the other 16 map totals were identical. Its 17-map screen against four strong local proxies scored 121/136, exactly matching #143's per-map totals. Ming remains 26/34 with losses concentrated on Collision, Pilgrimage, and Swirl. This is local proxy evidence and does not count toward the live top-50 streak.

Collision experiments aimed at the Ming/Xuanming mirror did not improve the 5/8 map baseline: #146's full-team shared-farm phase scored 4/8, and #147's Varg Power Strength-first build stayed 5/8 while lowering gems against Ming. Both are rejected. The supplied group URL is still the old FRChronic 0–5 group with null submission versions. Live consecutive wins remain 0/10; main source and ZIP remain unchanged.

### Swirl empty-lock follow-up and link recheck (18 Oct)

#148 attacked a nearby enemy altar lock while unloaded on Swirl when no enemy was visible. It scored 4/8 against four strong local proxies, below #145's 5/8 control, and lost both sides to Ming and Xuanming. Reject it. The user supplied `4cf7ad87-2c52-452e-a9a3-59787c302e67` again; the public record is unchanged: created 17 Oct, finished 0–5 to FRChronic, and both submission versions are null. It predates candidate v27, so it does not validate the current candidate. Live top-50 streak remains 0/10.

#149–152 did not improve the strong local-proxy results. On Swirl, Tavi for Ryth tied 5/8 but reduced Ming-game gem totals; a counterdraft-only 40% heal trip fell to 4/8. On Collision, a Varg solo opening and a two-pair camp split each scored 4/8 against v27's fresh 5/8 control. The pair split submitted only 66/132 gems in its two Ming games versus v27's 416/254. Keep v27. These runs are local proxies and do not count toward the live top-50 streak.

## Latest status and live access check (18 Oct 2026)

The latest saved ladder snapshot is still from 17 Oct 14:41 UTC; it does not establish today's complete top 50. A fresh GET to `/api/v1/teams/leaderboard?limit=50` and to `/api/v1/challenges` returned HTTP 401 `SIGN_IN_REQUIRED`. The public match-group GET returned HTTP 200 and confirmed that the supplied group `4cf7ad87-2c52-452e-a9a3-59787c302e67` is the finished unranked 0–5 Heavenly Court loss to FRChronic from 17 Oct 21:50 UTC, with five matches, null submission IDs/versions, and `myTeamId: null`. It predates test submission version 33 and contributes no top-50 wins.

TinyFish is enabled and installed, but `nodeRepl.rpc('browser')` fails because the browser service module is missing; local Chrome debugging ports are closed. The `cambc` CLI lists local run/build/bundle/login/submit commands, with no match-group creation command. A fresh live group and the current ladder therefore remain inaccessible from this runtime.

Candidate #184 is the strongest measured local all-map build: Packs 38/40 twice versus a fresh version 31 control at 34/40, and 632/680 versus 628/680 across 17 maps, with the all-map gain confined to Packs. Its verified candidate ZIP was uploaded separately as test submission version 33. Follow-up #185 kept the split but shortened the early combat leash; it tied #184 at 38/40 on the full Packs pool in two runs, shifting rather than reducing the two losses, so it remains unuploaded. Live top-50 streak remains **0/10**. The production source and ZIP remain unchanged.

## Pilgrimage candidate #186 (18 Oct 2026)

#186 targets the round-700 farming deficit against opp-tts-v3 by starting Pilgrimage's role split at round 1, balancing the team into 3+3 squads, and limiting early engagement until round 600. It scored 34/40 twice on the full Pilgrimage pool versus a fresh #184 control at 29/40. Its strong four-proxy screen was 4/8 versus #184's 6/8: both v3 games improved, but both Xuanming games regressed. Two unseeded all-map runs repeated at 636/680, versus 632/680 for a fresh #184 all-map control; Pilgrimage improved 29/40→34/40, Lanes moved 40/40→39/40, and the other 15 maps matched. This is local proxy evidence, not a top-50 live win. The bundle has been uploaded as test submission version 34; #184 remains version 33.

The verified #186 bundle was uploaded separately through the CLI as test submission version 34 (bundle SHA-256 `45A8118EACE011FCD67622BF5263E1172B0D622804B48A82A0CE858510DC2677`). The supplied group URL `4cf7ad87-2c52-452e-a9a3-59787c302e67` is the finished 17 Oct group with null submission versions and cannot validate #186. The browser bridge still fails because its service module is missing, so no fresh group has been created or inspected. Live streak remains 0/10. The production source and ZIP remain unchanged. Full run IDs and source/WASM hashes are in `bots/tungtungsahur/PLAN.md`.

## 18 Oct current rank-5 results and farm diagnostic

The user's supplied group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is a fresh five-map unranked group against rank-5 `new team(4)`; it finished 0–5 and is v60-likely. A later v62-likely group `a96043a5-af65-4a93-a9af-971d34b1a879` also finished 0–5 with mirrored exposed drafts. The CLI does not expose pinned submission versions, so these attributions are based on upload/queue timing.

Rows was a no-contact loss with 9 vs 16 camp clears and 38.854k vs 66.924k monster damage. Both sides farmed 66-gem packs; our side repeated two nearby groups, while the opponent also cleared a third route. c296–c298 local Rows route/equipment experiments did not beat c291: no increase over the control's 6/6 proxy wins, and gem output did not improve. Full local score for c296 remained 82/102, tied with c291.

The top-50 campaign now stands at **4 wins / 320 maps**, maximum consecutive streak 1, current streak **0/10**. Production source and ZIP remain unchanged; no local candidate is uploaded after v62.

Instrumented local Rows candidate c299 repeatedly selected group 4 without a recorded clear; one Ryth sample was stationary at (38,9). c300 extended the Ambush stalled-target recovery to Rows but did not improve the proxy results or gems. This points to camp execution/visibility state as the next diagnostic, while leaving the exact cause open.

Further replay instrumentation showed group 4 was visible and partially damaged, but never fully cleared. c301 skipping it regressed to 5/8, c302 stronger target commitment tied the control, and c303 area-target optimization fell to 5/8 and lost both direct c291 games. Reject these local-only candidates; no upload followed v62.

## Current #1 Fish result and v63 test candidate (18 Oct 2026)

Group 8a40e9a3-af65-4a93-a9af-971d34b1a879 against Intercontinental Fish finished 0–5 without bot faults. Contest's first six deaths occurred between rounds 41 and 54, ending 0 gems / 76 deaths / 0 kills against 1,000 / 2 / 62. Ambush, Corners, and Expanse were low-death farm-rate losses; Fragment combined combat and farm deficits.

A direct Contest lineup mirror did not pass local controls (c304 4/8 and 0/2 vs c291). c306 removes the linked C&I pick, retains Varg / Ryth / Stellar / Tavi, and adds Willow. It scored 8/8 on the Contest screen and tied c291 at 82/102 on the full local pool. Uploaded separately as test v63; group 350cf6e4-a539-4b50-b612-63f2086b91d9 against Fish is queued. Do not count it until the group is complete. Campaign: 4 wins / 325 top-50 maps, current streak 0/10. Production bundle remains unchanged.


## 18 Oct continuation: rank-1 Fish v63–v65

Three five-map unranked groups against Intercontinental Fish completed 0–5, with no bot faults. v63's Contest Willow draft, v64's relaxed retreat threshold, and v65's three-tile opening response all failed the match. v65 achieved 2 kills and 6 enemy deaths on Contest but still ended 0 gems vs 1,000 and 59 deaths vs 6. The other four maps matched prior results: Ambush 582:1,024, Corners 374:1,002, Expanse 584:1,016, Fragment 102:1,020.

c310 (v65) tied c306 at 82/102 on the full local proxy pool and won 8/8 Contest proxy games; c307, c309, and c311 regressed their local screens. Treat c310 as a narrow test, not a promotion. Expanse appears to be a camp-route issue: same four-body draft, no champion damage, first clear round 28 vs Fish round 15, 17 vs 46 camp-clear entries.

The top-50 campaign is **4 wins / 340 completed maps**, max streak 1, current streak **0/10**. Production source and ZIP remain at their recorded unchanged hashes. Full metrics and replay paths are in analysis/live-top50-match-review-20261018.md.

## Rank-5 v65 retest and latest campaign (18 Oct 2026)

The user-created v60-likely group dbdcc65c-cb2f-4b28-850b-5fa691da9e34 lost 0-5 to current rank-5 new team (4) on rushbait_v2, rows, lanes, eight, and interlock. After the v65 counterdraft was active, the same five maps were queued again in group 67012c50-6dcd-4e12-9e4a-9043c8a3a7cb; it also lost 0-5. Labels follow queue timing because the group API omits pinned submission versions.

The v65 draft fixed visible matchup choices from the v60 group: it took Ryth on rushbait_v2 and Tavi on eight, matching the rank-5 lineup. Rushbait improved (212 to 300 gems, 9 to 3 deaths), but remained out-farmed 300:1,020. Rows remained 594:1,056, with zero champion damage and 9:16 camp-clear entries. Team A cleared groups 0 and 2; the opponent cleared mirrored groups 1, 3, and 5. The 2,430:4,320 gold totals track those nine versus sixteen clears. On eight, adding Tavi did not prevent 19 deaths to 2 or the 132:1,008 banked-gem result.

Local c316 route-split scored 4/8 on Rows, losing both head-to-heads with c310 and both with c291; reject it. Logging-only c317 confirms c310's early plan sends the whole team through Ryth's objective. Its local route moves between groups 0, 2, and 4; the top-5 live Rows replay cleared only groups 0 and 2, so investigate whether it reaches and completes the third route before target selection pulls it back.

The v65-likely groups against rank-50 WHIM and rank-40 Super Intelligence also finished 0-5. Current campaign: 4 wins / 360 completed maps, maximum streak 1, current streak 0/10. Production source and ZIP remain unchanged; c316 and c317 are local-only diagnostics.

## v66-likely rank-5 result

Group 05465728-a486-48f7-8439-41b56bc27724 tested c318/v66 against rank-5 new team (4) on rushbait_v2, rows, lanes, eight, and interlock. It finished 0-5. All five submitted-gem and camp-clear metrics matched v65 exactly; Rows remained 594:1,056 gems and 9:16 clears. The damaged-pack target multiplier did not alter the live result. Reject c318/v66; it is test-only.

Current campaign: 4 wins / 365 completed top-50 maps, max consecutive streak 1, current 0/10. Production source and ZIP are unchanged.

## v68–v71 follow-up results (18 Oct 2026)

Four further groups against rank-5 new team (4) completed 0-5 with no bot faults: [v68](https://2026a.battlecode.co.uk/game/match-groups/1f420eff-95d4-47cf-adf2-1181a8dfc274), [v69](https://2026a.battlecode.co.uk/game/match-groups/b9ee15a5-adc4-41a8-8912-9e82789b30d4), [v70](https://2026a.battlecode.co.uk/game/match-groups/0c22b4fb-111d-407d-bb96-e84a2f9bc336), and [v71](https://2026a.battlecode.co.uk/game/match-groups/47ff93c4-2182-4c8d-9b2a-61961476fd63). Drafts and seeds were held constant.

v68's low-health retreat made no difference to the eight loss (19:2 deaths, 132:1,008 gems). v69's Cassi Monster Focus order increased Rows damage and clear entries (38.854k/9 to 44.550k/11), but banked gems stayed 594:1,056; the extra clears were too late. v70's Rows Ryth Strength change added nothing. v71's lower target stickiness matched the old Rows result. c328's solo Varg route tied baseline at 6/8 locally. Reject the survival and route candidates; keep only Cassi's Rows build as a test-only lead while seeking earlier throughput. Local c322 scored 3/8 on eight; c324/c325 were 13/24 on Rows/Lanes/Expanse; c326 was 15/23 with one failed run versus c310's 15/24. Campaign: **4 wins / 390 completed top-50 maps**, max streak 1, current 0/10. Production remains unchanged.

## v67 Rows lock retest (18 Oct 2026)

The c320 damaged-pack hard lock was uploaded as version 67 and tested against rank-5 new team (4) in group [955faf23-97fb-4f5f-b405-8944957190c7](https://2026a.battlecode.co.uk/game/match-groups/955faf23-97fb-4f5f-b405-8944957190c7). It finished 0-5 without platform bot faults. Four maps matched v65/v66. Rows dropped from 594 to 528 banked gems while clear entries remained 9:16; team A cleared groups 0, 2, and 4, and had no deaths. Reject c320/v67: the local 6/8 screen (1/2 versus c310, 1/2 versus c291) did not predict its top-5 result.

c321 removed early gold weighting on Rows; it also scored 6/8 locally with 974 average gems, so reject. Current campaign: **4 wins / 370 completed top-50 maps**, max streak 1, current 0/10. Production source and ZIP remain unchanged; continue the route-throughput investigation.

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


## Current 18 Oct campaign snapshot after rank-5 v73-likely test

The user-supplied dbdcc65c-cb2f-4b28-850b-5fa691da9e34 group was the earlier v60-likely 0–5 set. Later tests include the v71-likely baseline, v72-likely contact-regroup test, and v73-likely Interlock Tavi-first draft against current rank-5 Sneaky Bush Campers; all finished 0–5. The v73 group is b4117649-1de1-4564-b0c4-4f633cb53371.

The latest five-map data confirms two distinct problems: Rows is still a no-combat farm-rate loss (13:19 camp clears, 792:1,023 gems); Interlock and Eight combine farm and survival gaps (18:2 and 17:2 deaths, respectively). v73's Interlock draft did apply, so its failure is not a selector-transfer issue. Local fixed roster candidates c333/c334 scored 31/68 and 34/68 versus c327's 57/68 and remain unuploaded.

Campaign total: **4 top-50 map wins / 410 completed maps**, maximum streak 1, current streak **0/10**. Production source and ZIP remain at the recorded hashes.


## Pending top-50 follow-up: rank-50 group

Group 9de98fb4-1737-4b66-b7b4-0859bfc0096d is queued against current rank-50 Martin Shkreli's Defense Team on five maps. It is v73-likely because the API omits pinned versions and c332 was the latest upload. The outcome is not yet counted.

The local fixed roster and Vendetta wolf-farming variants c333–c338 did not beat the c327 proxy control and remain unuploaded. Campaign stays 4 wins / 410 completed maps, max streak 1, current 0/10 pending completion.
