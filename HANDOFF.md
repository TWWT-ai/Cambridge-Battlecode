# Handoff: tungtungsahur (Cambridge Battlecode 2026a)

Everything an agent needs to continue this project. Read this first, then `CLAUDE.md` (commands,
architecture, gotchas) and `bots/tungtungsahur/PLAN.md` (numbered experiment log through #185, with
later c553–c676 follow-ups appended below it).

## 1. Goal and deadlines

- Competition: Cambridge Battlecode 2026a (CAMBC), a turn-based bot game written in C++ and compiled
  to WASM by `cambc.exe`. First team to tribute 1000 gems wins; otherwise most gems at round 2000.
- The user's bot: **`bots/tungtungsahur`**. Current live objective: reach **10 consecutive wins** in
  unranked match groups against top-50 teams. Local proxy matches do not count.
- Season schedule (from the site): Sprint 1 submissions lock **Sun 18 Oct 23:59 BST**, Sprint 2 lock
  Sat 24 Oct, Sprint 3 lock Sat 31 Oct; international qualifiers 4 Nov, UK qualifiers 11 Nov, finals
  18 Nov.
- Production upload: keep `submissions/tungtungsahur.zip` matched to `bots/tungtungsahur/src`, and do
  not change either production artifact before the 10-win streak. The user authorized authenticated
  unranked testing and separate experimental submissions; those use isolated `bots/c###` folders.

## 2. Ground rules from the user

- Keep production isolated while testing. Never modify opponent bots (`Faisal-bot`, `ming_bot`,
  `xuanming`, `opp-*`, `my-bot*`, `tralalerotrarala`, ...). Experiments go in new folders such as
  `bots/c###`.
- Do not promote a local result to production on proxy performance alone. Update the production source
  and ZIP only after the agreed 10 consecutive top-50 live wins, then record the change in `PLAN.md`.
- The user designs strategy and wants it tested honestly; when their idea tests worse, show the numbers,
  offer a variant, and let them choose. They write in English and Chinese.
- Don't enter or expose credentials. The authenticated CAMBC 2.2.5 CLI can read the ladder and queue,
  inspect, and download authorized unranked match groups.

## Current platform status (19 Oct 2026)

- Target: **10 consecutive wins** in fresh unranked groups against top-50 teams. The archived live
  campaign stands at **4 wins / 620 completed maps**, best streak 1, current streak **0/10**; all 17
  maps have historical live coverage. No local proxy win counts toward this target.
- The latest completed top-50 result in the live report is v99/c418 against rank-45 Please, a 0–5
  loss. The separate test upload v100/c425 splits Contest's opening farm routes; it scored 8/8
  against four strong local proxies and tied c417 at 38/40 in the broader 20-opponent pool, with 600
  fewer banked gems. It has no fresh live group. The user's supplied link
  (`dbdcc65c-cb2f-4b28-850b-5fa691da9e34`) is the previously counted 0–5 group against `new team(4)`.
  The user paused live group creation and uploads; do not start new ones while paused.
- Local work continued on 19 Oct while official unranked matches remain paused. c563 combines
  map-gated Pilgrimage survival rules and scored 184/204 over the six-strong, 17-map proxy set
  versus c553's 182/204; the 680-game default pool stayed 626/680. c563 is an isolated matchup
  candidate, not a validated production replacement. c565's Ryth squad reassignment had no effect.
  The c566-trace diagnostic logger changed replay behavior, so its movement counts are invalid. A
  Lanes-only bank-at-48 rule in c567 scored 7/12 versus c563 control's 12/12; reject it. c568/c569
  Willow draft experiments were late or harmful. c570 keeps the Lanes lineup and equips Ryth with
  Monster Strength then Power Strength only on side A against the exact Willow lineup from the
  official Please loss. It scored 4/4 across two runs against a matching local proxy, while c553
  scored 2/4; the six-strong Lanes screen was 12/12 and the full 20-opponent Lanes pool 39/40, the
  same win count and lone loss as c553. c571 combines c570 with c563 and scored 184/204 and
  626/680; normalized per-opponent outcomes matched c563 exactly, so the combined build showed no
  wider-pool gain. These remain local candidates, not live results.
  Details are in `bots/tungtungsahur/PLAN.md`. The c586 combined local candidate later reached
  630/680 on the default pool and 186/204 on the six-strong all-map screen. A Swirl follow-up
  matching part of Mite's Ryth/C&I/Stellar core (c588) rose from 32/40 to 33/40 on the default
  Swirl pool, but fell from 11/12 to 10/12 on the six-strong Swirl screen. Its earlier-trigger
  variant c589 fell to 4/8 against four strong Swirl proxies. Both remain isolated. No canonical
  source/ZIP update or live match/upload was made.
  A same-pool planner benchmark scored `ming_bot` 110/170 versus c586's 155/170 across five strong
  local proxies and 17 maps; it was better only on Eight and much weaker on Ambush, Corners,
  Monolith, and Rows. Do not replace c586 wholesale with that bot. The workspace CLI is 2.1.6 and
  lacks a ladder command; an isolated CAMBC 2.2.5 CLI refreshed the ladder read-only on 19 Oct (see
  `analysis/top50-evaluation-20261019.md`). A c590 Eight counter-draft based on Ming's
  lineup arrived too late, replaced Tavi with Vendetta, and scored 8/10 versus c586's 9/10 on the
  same five-proxy map screen; reject it. c591 fixed that lineup from the first pick and fell to
  7/10 on the same screen; reject it too. c592's Rows Varg capture change tied c586 on the strong
  Rows screen and standard Rows pool. c593 keeps the Varg/C&I/Ryth/Stellar Rows lineup when enemy
  Ren is visible; it converted the meta-core Rows side-A loss on two focused runs and scored 187/204
  versus c586's 186/204 on the six-strong, 17-map screen. The full default pool stayed 630/680 with
  identical outcomes. c594 kept Tavi/C&I/Ryth/Stellar on Interlock and raised the meta-core side-A
  score 270→780 while reducing deaths 29→20, but it remained a loss and did not raise the strong or
  standard-pool win count. c595's Ren-first Interlock draft fell to 37/44 versus c594's 43/44; c596's
  Varg-first Stampede draft fell to 9/12 versus c593's 11/12. c597's Stampede Ryth strength queue
  matched c593's 11/12 exactly and raised deaths 14→17 in the meta-core loss. Reject these variants.
  Ambush movement telemetry showed far more travel toward captures than live camps. Removing
  non-carry roles from all nearby captures (c601) reduced travel but fell to 41/44 versus c593's
  43/44 on 22 opponents; reject it. A side-A-only clean version, c604, scored 44/44 on that pool,
  tied c593 at 187/204 on the six-strong all-map screen, and scored 631/680 versus c593's 630/680.
  It changed 19 records, all Ambush side A, and converted only the `my-bot` side-A loss to a win;
  no losses were added. Keep c604 as an isolated local candidate, not live top-50 validation. The
  production source/ZIP remain c553 and unranked testing/uploads remain paused.
- Historical Contest carrier evidence from v98: Prism collected 200 gems at r1027; Please's Ryth took
  them at r1063 and deposited at r1109. Local escort and tank-hit variants did not improve the tested
  results.
- The canonical workspace source and ZIP are currently c553, with SHA-256
  `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and
  `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. These workspace hashes do
  not identify which version a past live group used; group metadata omits pinned submissions.

## Fresh ranked data and local follow-up (19 Oct 2026)

- Latest read-only ladder snapshot: `analysis/top50-20261019-latest.json` (50 of 689). Current top
  three are Intercontinental Fish, Mite, and Sneaky Bush Campers. Their latest 25 ranked map results
  were 22/25, 12/25, and 16/25 respectively. Drafts and roster movement are in
  `analysis/top50-evaluation-20261019.md`.
- Fish beat current #5 Univardisty 4–1 in group `9bc92ff8-1a26-4676-9f08-060868eadd0e`, but lost
  Stampede 0–1,080 after its first clear at r106 and eight deaths; Univardisty cleared at r19, made
  17 clears, and died twice. In the newest Mite–Sneaky Bush Campers group
  `f84aa4ce-84e6-46c1-954c-27d66d67f4b2`, SBC won 3–2. Corners and Collision show deposit/retention
  failures despite Mite clearing first or clearing more camps. All ten converted summaries are saved
  under `analysis/match-summary-<match-id>.json`.
- c676 tried Fish's Expanse Monster-first gear order for Cassi & Issac. It tied c553 at 10/10 on five
  local opponents, with lower own gems, more opponent gems, and a slower finish. Reject it.
- c677 copied Univardisty's exact Stampede lineup and fell to 7/12 versus a fresh c675 control at
  11/12. c678 replaced only Prism with Varg while keeping the tank and marksman; it scored 10/12 and
  added a loss. Reject both drafts. Current best local base remains c675/c604 at 631/680 on its
  default proxy pool; neither Stampede candidate has passed the targeted strong screen.
- Production remains c553 at the hashes above. The official match/upload pause remains in force;
  current top-50 streak is still 0/10. Local proxy runs do not count toward that goal.

## 3. Main strategy architecture (experiment 63 baseline; current canonical source c553)

Draft (`draft.cpp`, first `team_size()` picks): **Stellar, Cassi & Issac, Ryth, Varg, Tavi**
(3 picks: Stellar, Cassi & Issac, Ryth = 4 bodies; 4 picks: + Varg; 5 picks: + Tavi).

Phases (`game_phase()`, flags in shared-memory bytes 6/7 top bits):
- **Early** (until Stellar or Varg completes an emblem = 5 matching shards, or round 600): the whole
  team works Ryth's camp (Issac leads while Ryth is dead); followers stand behind the leader until the
  camp is awake. Only Stellar and Varg capture cleared camps (rewards split among allies standing on the
  group, so the gold goes to them; Varg leaves a capture to a free Stellar) while the team moves on.
  Camp choice counts gold double (`early_gold_weight = 2`). Everyone banks every capture immediately
  (holding a 60-gem bag lost lanes openings, exp. 63).
- **Mid**: squads A (Ryth leads, Stellar, Tavi) and B (Issac leads, Cassi); Varg solo-farms gem
  clusters and lone wolves, or helps squad B when nothing is soloable. Back-liners solo nearby gem
  clusters (radius 16) and lone wolves near their leader. Engage only enemies within 5 tiles and not
  deep in the enemy half; stay out of camps deep in the enemy half; retreat when enemies outnumber us
  by 2+ within 6 tiles or are 1.3x stronger.
- **Late** (Stellar owns 3 emblems): fight any enemy in sight unless outmatched (1.3x).

Every turn (`Bot::play_turn`): SCORE/SCOUT logging, shop, survive (retreat at 30% Ryth / 35% others,
recall), update respawn ledger, choose objective, `burst` (cast the best ready spell on enemies, ported
from ming_bot), bank, shopping trip (recall at 150+ gold when safe), peel (stun enemy tributes), place
altar lock, then the role turn.

Item builds (each line = 5 shards = one emblem, then the next):
| Champion | Build |
|---|---|
| Stellar | Power Focus (repeat) |
| Varg | Monster Strength, then Power Strength |
| Ryth, Issac | Jungle Health, then Power Health |
| Tavi | Power Focus |
| Cassi | Power Focus, Durability Health, Power Focus |
Everyone keeps one altar lock (10 gold).

Key constants (top of `bot.cpp`): `shop_trip_gold 150`, `retreat_tank 0.3`, `retreat_other 0.35`,
`stick_bonus 1.3`, `solo_cluster_radius 16`, `join_capture_range 6`, `outmatched_ratio 1.3`,
`mid_game_by 600`, `mid_leash 5`, `deep_margin 4`, `outnumbered_by 2`, `stellar_join_range 8`,
`capture_range 10`, `early_gold_weight 2.0`.

Logging (keep the formats, tools parse them): `SCORE round ours theirs` every 5 rounds; `SCOUT DRAFT`,
`SCOUT SEE` (enemies in sight), `SCOUT DEATH` (our deaths, bag, enemies near), `SCOUT LOCK`,
`SCOUT PHASE` (mid/late start).

## 4. Current performance

| Test | Result |
|---|---|
| Standard league `tools/opps22b.txt` + xuanming + faisal-orig (480 games) | **432 / 480** |
| ming_bot | 16–18 / 20 |
| xuanming (user-added, strong) | 19 / 20 |
| Original Faisal-bot (`bots/faisal-orig`) | 19–20 / 20; 7 Faisal draft variants 139–140 / 140 |
| Every bot in `bots/` (137 opponents, 2740 games, logging copy `tts-moves`) | 2116 / 2740 (77%); other bots 371/380; our old versions 164/220 |
| No opponent: average round to reach 1000 gems (`--opps zz-idle`) | ~516 |

Weak spots: near-mirror games against our own older versions (11–16/20), collision side B and lanes
side A against ming_bot. Platform results with the current version are not known yet.

## 5. How to evaluate (important)

- The engine is deterministic but chaotic: any change, even logging or extra fuel use, reshuffles
  single games. About ±8 wins on the 480-game league or ±30 rounds on one map is noise.
- Standard check for a candidate: `python tools/league.py <bot> --opps $(cat tools/opps22b.txt),xuanming,faisal-orig --jobs 18 --tag note`
  (about 2–3 min), plus the race test `python tools/league.py <bot> --opps zz-idle` and
  `python tools/race.py <dir> <dir>` for per-map rounds.
- Other tools: `tools/scout.py` (one match's SCOUT summary, also works on platform log zips),
  `tools/deaths.py` (deaths per opponent), `tools/moves.py` (walking breakdown, needs the logging copy
  `bots/tts-moves` or `bots/tts-trips`), `analysis/shard_value.py` (camp damage per item build).
- Never run several `cambc run` at once; `league.py` pre-builds bots because `run-batch` compiles
  unreliably on this machine. Python on Windows: write files as bytes (CRLF breaks `patch`).

## 6. What we learned (with evidence)

**Top platform players.** The ladder (public, 539 teams) is led by Intercontinental Fish (2035) and
Mite (2011). From platform logs (`ZIPs/*-logs.zip`, `diagnosis/*.zip`, extracted under
`matches/platform-logs` and `matches/diagnosis`; analyses in `analysis/forensics.md`):
- They are economy machines: tribute after almost every capture (~48 gems), 2.2–3.9 gems/round, reach
  1000 by round 335–475, take the contested central camps (corners centre pairs, packs centre).
- Mite / the `us_against` opponent drafts Ren + Stellar + Cassi & Issac (+ Varg, Ryth): 4–5 stunners.
  Against them our old version spent 30–53% of champion time dead (Cassi & Issac half of the deaths).
  Retreating earlier did not reduce deaths (exp. 62); the cause is probably stun-lock burst, unproven.
- Pure speed losses happened on rows and expanse with no contact (they reached 990 by r390–405).
- Replay files (`replay.repl26a`, magic `a62per`, embeds the map file) have no documented format; we can
  only identify the map. `cambc.exe view <file>` shows them in the visualiser.

**Economy.** Clearing camps is only ~17% of champion turns; walking is ~34% (to camps and altars).
Champions walk 280–360 tiles per game; pathing is already within 4–9% of the shortest terrain path
(BFS distance fields, equivalent to A*), so pathfinding is not a lever. The costly parts are altar
trips on elkring/monolith/rows (580–640 team tiles per game) and followers trailing a leader.

**Equipment.** Best camp damage per gold: Monster in the damage stat first, then Power (Strength for
Tavi, Ryth, Varg, Issac; Focus for Stellar, Cassi). But farming builds made the bot weaker overall
(exp. 64: 415–422 vs 432) and only ~1% faster; fight items (Ryth health, Tavi spell focus, Cassi
durability) matter more. Home emblem for Ryth and Stellar ties the main version (exp. 65, `bots/u4`).

**Bugs fixed along the way** (all in main): altar double-lock freeze (`enemy_lock_at`), respawn-squat
deadlock (ready = round + max(timer,1)), engaging enemies standing on their spawn, capture move-on,
followers walling the leader in (`behind()`), treating an out-of-sight group as cleared.

## 7. Experiment history (details in PLAN.md)

| # | Change | Result |
|---|---|---|
| 1–46 | Overnight 14–15 Oct: bank fix, fuel caching, safe unit reads, solo cluster farming, gold sharing, focus fire, locks, Stellar before Tavi | league 102/162 → 160/162 on the original set |
| 47–48 | 4 bug fixes + ming_bot burst | kept |
| 50 | back-liners solo lone wolves | kept |
| 52 | Varg solo farmer instead of Prism on maps with soloable camps | kept |
| 56 | SCOUT telemetry | kept |
| 57–59 | user's "feed Stellar" plan (draft Stellar first, phases, gold priority) + Varg helps squad B | kept (392 vs 380) |
| 60–61 | user's "whole team farms together" plan: all game 328 (no); early game only | kept (388, ming 18/20) |
| 63 | carries bank every capture in the early game (collision/lanes fix) | kept (394/440; xuanming 19/20) |
| 49, 51, 53–55, 62, 64, 65 | bigger bags, squad carry, cautious Varg, draft-based fight ratios, comeback mode, earlier retreats, farming builds, far-altar carry, next-camp altar, sticky camps | rejected (noise or worse) |

## 8. Open problems and next steps

1. **Get platform logs of the current version** against Intercontinental Fish, Mite, xuanming-like
   teams; run `tools/scout.py` / `tools/deaths.py` on them. Local opponents don't reproduce the top
   teams' fights, so platform logs are the main source of truth.
2. **Deaths against stun-heavy drafts** (Ren/Stellar/Cassi/Ryth): find the cause from SCOUT DEATH lines
   (stun-lock? fighting near their altar? Cassi/Issac pair?) before changing retreat logic.
3. **Collision** (single walkable altar, contested): still loses side B to ming_bot; ideas never tested:
   lock-proof banking at the sealed altar (39,20) with a teleport crystal, or holding the altar area.
4. **Rows and expanse speed** (pure races): the top players are ~1.5x faster there.
5. Small, unproven: Home emblem for Ryth/Stellar (`bots/u4`, tie), map-gated bag carrying only on
   monolith/rows.

## 9. Where things are

- `bots/tungtungsahur/src`: main bot (`bot.cpp` ~2165 lines, `bot.h`, `draft.cpp`, `team.h`, `main.cpp`).
- `bots/opp-tts-v2` … `v9`: older mains (v9 = previous main before exp. 63). `bots/faisal-orig`: original
  Faisal-bot (`bots/Faisal-bot` now holds a copy of our v8 code). `bots/cand-*`, `exp-*`, `u*`, `build-*`,
  `feed-*`: experiment copies, safe to delete.
- `tools/`: league, race, scout, deaths, moves, errors scripts; opponent lists `opps22b.txt`, `opps-all.txt`.
- `analysis/`: analyst reports (`forensics.md`, `ming-study.md`, `mechanics.md`, `maps.md`,
  `econ-profile.md`), map dumps, simulators, `shard_value.py`.
- `matches/league/`: every league run (`summary.json` per run, `history.csv`); `all-bots*.txt` full runs.
- Rules: `GameRules.md`, API: `BotAPICpp.md`, enum values: `sdk/cpp/cambc.h`. Handbook online at
  https://2026a.battlecode.co.uk/game/docs (renders client-side; no real balance patches yet).



## Latest top-50 study (17 Oct 2026)

The public top-50 ladder snapshot is now `analysis/top50-20261017-1442.json`; pick-frequency findings and candidate results are documented in `analysis/top50-evaluation-20261017.md`. The old 432/480 result belongs to the previous map pool. On the refreshed 17-map pool, main scored 104/136 and isolated experiment 78 scored 108/136. Earlier user-lineup and Varg experiments were not promoted.

The following 17 Oct notes are historical. On 18 Oct the authenticated CAMBC 2.2.5 CLI was used for
unranked groups; this supersedes the earlier TinyFish/browser-session blocker described in the old
notes. The live campaign and current candidate are summarized at the end of this file. Local proxy
games still do not count toward the requested 10 consecutive top-50 wins.

Latest same-session comparator (17 Oct 2026): main 432/480; Expanse-only Varg draft 434/480. Against the four stronger local sources, main scored 73/80 and the candidate 76/80. The candidate is experiment 72 in `bots/tungtungsahur/PLAN.md`; it remains unpromoted because the full-league gain is within noise. `bots/cand-expanse-varg` contains the isolated draft variant.

The follow-up opponent-aware Expanse draft is experiment 73: it switches to C&I/Varg/Stellar after seeing an enemy Varg pick, and otherwise keeps the current order. It scored 435/480 and 77/80 on the same four strong sources, versus main 432/480 and 73/80. The +3 full-league result is within the measured noise band, so it remains a candidate in `bots/cand-expanse-counter`.

The latest top-50 snapshot (`analysis/top50-20261017-1442.json`) was generated at 14:45 UTC from ladder data updated at 14:41 UTC. Across the top 50 teams' reported top-pick fields, C&I leads with 2,192, followed by Stellar (2,045), Ren (968), and Varg (821); this is not a complete draft history. The first ten challenge targets, in ladder order with rating and reported picks, are listed in `analysis/top50-evaluation-20261017.md`. Public match-group IDs can be inspected for per-map results and replay URLs once a challenge is created.

The requested 10 consecutive unranked wins against top-50 teams remain at 0/10. No live match has been created. The user selected “Enable TinyFish” and its connection prompt was surfaced, but the latest confirmed state is still `installed: false`. Local proxy games do not count toward the streak.

## Current map-pool status (17 Oct 2026)

The official pool has 17 maps. `tools/league.py` now resolves their downloaded filenames, and the map
analysis lives in `analysis/maps.md`, `analysis/map-layout-20261017.txt`, and
`analysis/maps-extra-20261017.txt`. The current main code was tested unchanged against four strong local
proxies on every map: **104/136** (8 games per map). This is a new-pool result and is not comparable to
the old 432/480 score. Collision, Lanes, and Swirl scored 4/8 each. Lanes lost all four side-B proxy
games but was only 12 rounds slower from B versus idle; Swirl losses to Ming/Xuanming had 47–70 deaths;
Collision against Ming had 15–16 deaths and repeated locks at the only walkable altar.

Three Swirl candidates failed the promotion gate: Varg→Vendetta 0/4 against Ming/Xuanming; Ryth→Vendetta
0/4; grouped opening through round 600 4/8 across four proxies, equal to main's 4/8. Main source and
submission bundle remain unchanged. `tools/scout.py` was corrected to read its SCORE trace as the bot's
own perspective for both team sides.

A Lanes-only Varg solo opening scored 2/8 against the four local proxies, below main's 4/8, so it also
remains rejected in `bots/cand-lanes-varg-solo`.

Experiment 78 uses `bots/cand-contest-prism`: on Contest and Stampede only, it drafts Prism, Stellar,
Cassi & Issac, Ryth, Tavi; all other maps retain the current main lineup. Full-pool candidate run
`matches/league/20261017-154817-cand-contest-prism` scored 108/136 against main's 104/136; the 15
other map scores are identical. Candidate targeted run `20261017-154718-cand-contest-prism` scored
15/16, and the full-pool run also scored 15/16 over the same two maps. Main scored 11/16 in the full
pool and repeated that result in `20261017-154932-tungtungsahur`. Keep the candidate isolated pending
live validation; the main source and `submissions/tungtungsahur.zip` are unchanged.

Contest follow-ups #79–82 tried defensive-first items, a team-gathered Monolith rush, camp-damage
emblems, and Ryth escorting a nearby 100+ gem carrier. They scored 5/8 to 6/8 against candidate 78's
7/8, so keep the original candidate loadout. Its Contest loss to Ming on side B tied 200–200 after
Stellar died carrying a second 200-gem bag at r1911; the enemy locked (25,24) at r985. The current
Mite–Fish public group also shows a 0–0 Contest result at r2000 despite Mite using this draft. This
objective remains unproven against top teams.
Follow-up replay folders: `matches/league/20261017-155738-cand-contest-iron-test`,
`20261017-155745-cand-contest-rush-test`, `20261017-155843-cand-contest-monster-test`, and
`20261017-160055-cand-contest-escort-test`.

## Latest continuation update (17 Oct 2026, later session)

Experiments 83-85 and their results are in `bots/tungtungsahur/PLAN.md`. Collision teleport banking
scored 4/8 for bags of 100+ and 2/8 when triggered for any positive bag; neither variant improves
the contested-map result. A Collision-only Stellar / C&I / Varg draft scored 5/8 twice versus main's
4/8, but still lost both games to Ming and won only one side against Xuanming. Combined with
experiment 78's Contest/Stampede draft, the isolated candidate scored **109/136** across the 17-map
pool (experiment 78: 108/136; main: 104/136). Only Collision improved over experiment 78, from 4/8
to 5/8. Candidate folder: `bots/cand-contest-prism-collision-varg-test`; full run:
`matches/league/20261017-160824-cand-contest-prism-collision-varg-test`.

This is a local-proxy lead, not a proven live strategy. Main source and submission ZIP remain at the
previous version. The live unranked top-50 streak remains 0/10. TinyFish was selected for enabling,
but search still reports `installed: false`, and this runtime exposes no plugin install/connect
action or TinyFish browser tools. Continue local strategy work while waiting for the connector to
become available; never count proxy results toward the 10 live wins.

## New collision / Swirl evidence (17 Oct 2026, later session)

Experiments 86-88 are documented in bots/tungtungsahur/PLAN.md. Two Collision changes both scored
4/8 against the four local proxies (experiment 85 scored 5/8): Varg Jungle Health first, and a
Cassi & Issac / Ryth / Varg lineup that drops Stellar. Both still lost all games against Ming and
Xuanming. On Swirl, Jungle Health first for Varg and the mage lowered deaths by 2-23 per sampled
strong-proxy match but dropped the score from 4/8 to 3/8 due to lost gem throughput. The current
evidence favors studying camp assignment / 3+2 body allocation on Swirl over adding more defense.

Experiment 85 scored 109/136 before the Expanse follow-up; main source and ZIP are unchanged.
The live top-50 unranked streak is still 0/10, and TinyFish remains uninstalled.

Experiments 89-90 tested Swirl grouping and bank timing. Varg joining Issac's squad after the
opening held at 4/8 but did not win against Ming or Xuanming. Delaying banking to 150 gems when no
enemy was visible fell to 2/8 and lost 1,802 carried gems in the four strong-proxy games, versus
647 for experiment 85. Immediate banking remains preferable under current combat pressure. See
bots/tungtungsahur/PLAN.md and analysis/maps.md for the detailed runs.

Experiment 91 is the new best local candidate: add the Expanse C&I / Varg / Stellar draft order to
experiment 85's Contest / Stampede / Collision picks. It scored 112/136, against 109/136 for
experiment 85 and 104/136 for a same-session main recheck. Map gains are Collision 4->5/8, Contest
5->7/8, Expanse 5->8/8, and Stampede 6->8/8; the other thirteen maps are unchanged. Candidate is
bots/cand-best-expanse-meta; full run is
matches/league/20261017-162931-cand-best-expanse-meta. Main source and ZIP remain unchanged, and the
live unranked top-50 streak remains 0/10.

## Pilgrimage / Lanes continuation (17 Oct 2026)

Experiments 92-97 did not beat the current candidate. Pilgrimage T=100 banking scored 4/8; a
round-1 split tied at 5/8 but traded the Ming matchup for Xuanming losses; a Vendetta-for-Ryth draft
scored 3/8. On Lanes, switching to split squads at r200 scored 3/8. Ren for Ryth stayed 4/8 and lost
both sides to Ming/Xuanming; Ren for Tavi scored 5/8 overall but reduced wins against those two
from 2/4 to 1/4. Detailed results and paths are in `bots/tungtungsahur/PLAN.md` and
`analysis/top50-evaluation-20261017.md`.

The current isolated best remains experiment 91 at 112/136 across the 17-map local pool. The main
source and submission ZIP remain unchanged. Live unranked top-50 streak is 0/10. TinyFish was
surfaced again after the user's explicit request to enable it, but its latest confirmed state is
still not installed or connected; the browser session needed to create platform matches is still
unavailable. Continue local research while waiting for the connection, and do not count proxy games
toward the live streak.


## Rushbait / movement continuation (17 Oct 2026)

Experiment 99 is now the strongest local candidate: on Rushbait v2 (30x80), force the mid-game squad phase from the opening on either side. Its targeted result was 7/8 in two repeats. Integrated in bots/cand-best-expanse-meta, it scored 113/136 across the 17-map, four-strong-proxy league (previous candidate #91: 112/136; main: 104/136) and 592/680 in the broad local pool (#91: 587/680; main: 577/680). Rushbait improved from 5/8 to 7/8 in the strong set and 35/40 to 39/40 in the broad set; Swirl also gained one broad-pool win, while Stampede lost one strong-proxy win. See bots/tungtungsahur/PLAN.md, analysis/maps.md, and analysis/top50-evaluation-20261017.md.

Experiment 98's movement fallback is rejected: broad score fell to 586/680 and a Bruiser Ambush side-B win became a severe loss. Side-specific Rushbait trials scored 3/8 and 4/8 because the intended early branch did not activate; treat them as invalid. The all-side opening is the tested rule.

Keep bots/tungtungsahur/src and submissions/tungtungsahur.zip untouched. Live unranked top-50 progress is still 0/10; local results are not live evidence. TinyFish is available but remains uninstalled and unconnected, so the game-site browser session is not available to create platform matches.


## Lanes equipment continuation (17 Oct 2026)

The new strongest local candidate is bots/cand-lanes-sideb-tavi-monster: only on Lanes side B, Tavi buys Monster Strength first and then Power Focus. It scored 5/8 in two targeted repetitions, 114/136 in the four-strong-proxy full league, and 593/680 in the 20-opponent broad pool. The previous candidate scored 4/8, 113/136, and 592/680; broad Lanes rose 36/40 to 37/40. All strong-set map totals outside Lanes are unchanged. The improvement is small and remains local evidence only.

Rejected tests: Ryth Monster Strength first on Swirl (3/8); mid-game opening on Lanes side B (4/8, zero side-B wins); and Tavi Monster Strength on both Lanes sides (4/8, weaker against Ming/Xuanming). Runs and rationale are in bots/tungtungsahur/PLAN.md and analysis/maps.md.

Do not update main source or ZIP yet. Live unranked top-50 streak remains 0/10. TinyFish reports installed=false, so the game-site browser session is unavailable.


## Corrected fresh-build results (17 Oct 2026)

The earlier same-name swaps were stale-build comparisons: copied files kept timestamps older than the compiled objects, and the incremental build reused v104. Discard the apparent identical outcomes. After refreshing timestamps and verifying distinct WASM hashes, the recovery version scored 610/680 broad versus 593/680 without recovery; Ambush improved 21/40 to 40/40. The targeted strong-proxy Ambush result was 8/8 versus 6/8. A fresh main-source build under the same name scored 104/136 strong versus v104's 117/136.

The narrowed v105 source scored 611/680 broad and 116/136 strong. Keep v104 in `bots/cand-ambush-stall-recovery/src/bot.cpp` as the leading candidate for the strong-proxy objective; v105 is saved alongside it. Detailed run IDs and source/build hashes are in `bots/tungtungsahur/PLAN.md`.

Replay analysis points to central-altar control and repeated deaths on Collision/Swirl, plus farming pace on Pilgrimage. Contest and Stampede ended tied at the 2000-round cap. Continue testing map-specific survival and bank timing. Live unranked top-50 progress remains 0/10; TinyFish is still uninstalled. Main source and `submissions/tungtungsahur.zip` remain unchanged.

Latest corrected broad control: v104 recovery scored 610/680 vs a freshly rebuilt main source at 577/680 (`20261017-192402-cand-ambush-stall-recovery`). Map deltas: Ambush +19, Expanse +6, Stampede +4, Rushbait v2 +3, Contest +2, Lanes +1, Swirl +1, Collision -2, Pilgrimage -1; all other maps matched. Strong set: 117/136 vs 104/136. The Swirl late-retreat follow-up was a no-op (0/4 vs Ming/Xuanming; all four replay ZIP hashes matched v104). TinyFish was surfaced for connection, but remains confirmed uninstalled; live streak 0/10. Main source and upload ZIP are unchanged.

Swirl-only recall at 50% health scored 3/8 targeted despite reducing deaths. At 40%, it tied v104's targeted 4/8 and scored 118/136 strong, but broad fell to 607/680 from 610/680; Swirl fell from 35/40 to 32/40. Reject both. The v104 candidate source was restored and rebuilt to the original source/WASM hashes. Main source and submission ZIP are still unchanged.

Pilgrimage follow-up: giving Tavi Monster Strength before Power Focus scored 5/8 versus v104's 6/8 against Ming, Xuanming, `faisal-orig`, and `opp-racer` (`20261017-194005-cand-ambush-stall-recovery`). Reject; v104 was restored and rebuilt again. Main source and ZIP remain unchanged.

Another Pilgrimage trial attacked a visible home altar lock even with an empty bag. It scored 5/8 in two identical runs (`20261017-194247` and `20261017-194304`), below v104's 6/8. It won one Ming side but lost both Xuanming sides. Reject; v104 remains restored.

Collision follow-up: attacking the central altar lock with no gems scored 4/8 versus v104's 5/8 and still lost all four Ming/Xuanming games (`20261017-194508-cand-ambush-stall-recovery`). Reject; v104's source and WASM were restored. Main source and ZIP remain unchanged.

Collision draft follow-up: swapping Varg for Tavi while keeping Stellar and C&I tied v104 at 5/8 and remained 0/2 vs Ming (`20261017-194617-cand-ambush-stall-recovery`). Reject; v104's draft and WASM are restored.

Swirl follow-up: moving Varg from solo farming to Ryth's camp increased the two Ming loss scores to 631 average gems from v104's 414, but stayed 0/4 vs Ming/Xuanming and scored 34/40 across the broad Swirl set versus v104's 35/40 (`20261017-194840-cand-ambush-stall-recovery`). Reject; v104 was restored and rebuilt.

## Current status after experiment #115 (17 Oct 2026)

The isolated local leader is now `bots/cand-ambush-stall-recovery/src/bot.cpp`, snapshot
`candidate-source-v115-lanes-shoptrip250.cpp`. It changes the Lanes side-B shopping recall threshold
from 150 to 250 gold. Two targeted runs scored 6/8; the fresh v104 control scored 5/8. The full
strong-proxy set scored 118/136 vs 117/136, and the broad local pool scored 611/680 vs 610/680. Lanes
alone improved: 6/8 vs 5/8 strong and 38/40 vs 37/40 broad. Full run IDs and exact hashes are in
`bots/tungtungsahur/PLAN.md` and `bots/tungtungsahur/REPORT.md`.

The requested live unranked target is still 10 consecutive wins; progress remains 0/10 because no
challenge has been created. TinyFish now reports `installed: true`, but its browser actions are not
exposed in this session. Continue local work, but do not count proxy games toward the live streak and
do not copy the candidate into main source or `submissions/tungtungsahur.zip` until the live target is
met. Main source and upload ZIP hashes remain
`188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and
`06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

Threshold follow-up: 200 gold scored 5/8 in two identical Lanes strong-proxy runs
(`20261017-195844` and `20261017-195930`); 300 gold scored 3/8 (`20261017-195907`) and lost both
Faisal games. Reject #116 and #117; 250 gold remains the best tested side-B shopping threshold.
Their snapshots are in `bots/cand-lanes-shoptrip-threshold/`. The active experiment file there is
200 gold, separate from the isolated #115 leader.

Swirl/Collision follow-up experiments #118–121: Willow replacing Varg on Swirl tied at 4/8 but lost
all four Ming/Xuanming games with very low gem totals (`20261017-223244`). Collision Ryth/Vendetta/Tavi
scored 2/8 (`20261017-223334`); Ryth/C&I/Tavi scored 1/8 (`20261017-223401`); Stellar/C&I/Ryth scored
4/8 (`20261017-223428`), below the current Stellar/C&I/Varg lineup's 5/8. All three Collision variants
lost both sides to Ming and Xuanming. Reject them; keep the current drafts.

TinyFish is installed now, but its browser actions are not exposed in this session. The user supplied
unranked group `4cf7ad87-2c52-452e-a9a3-59787c302e67`: Heavenly Court lost 0–5 to FRChronic on
Interlock, Stampede, Elkring, Fragment, and Pilgrimage. FRChronic was rank 58 around the match, so the
top-50 streak remains 0/10. The group draft and score review is in
`analysis/platform-match-review-4cf7ad87.md`; replay downloads still require a browser session this
runtime cannot access. Main source and submission ZIP remain unchanged.

Fresh Stampede follow-up: `matches/league/20261017-2301-stampede-live-followup` compared main (6/8)
with the isolated v115 candidate (7/8) against Ming, Xuanming, Faisal, and opp-racer on both sides.
v115 uses Prism/Stellar/C&I/Ryth/Tavi, matching the live opponent's Stampede composition; the live
main draft omitted Prism. Equipment variants buying Monster Strength first on Tavi, Prism, or both
scored 7/8, 6/8, and 5/8, so reject them and keep current equipment. See
`matches/league/20261017-2301-stampede-monster-screen/summary.json`. These are local results, not
top-50 wins. Main source and ZIP hashes remain unchanged.

New Stampede experiment #126: `bots/cand-stampede-team/src/bot.cpp` delays the mid-game squad split
until Stellar's late-game flag. It scored 8/8 vs v115's 7/8 on the four strong local proxies and 41/44
vs 36/44 across the 22-opponent Stampede pool. Longer holds to round 900 and round 600 both scored
7/8; reject. The late-check ordering variation was an exact no-op, proven by the identical Ming replay
ZIP hash. Details, run IDs, and hashes are in `bots/tungtungsahur/PLAN.md`; the candidate snapshot is
`bots/cand-stampede-team/candidate-source-v126-stampede-phase.cpp`.

Main source and submission ZIP remain unchanged. The all-map tested local candidate is still #115;
#126 is Stampede-only pending a full-pool and live top-50 comparison. The latest leaderboard request
returned 401, as did the match-summary and replay endpoints. TinyFish reports installed and enabled,
but browser-action tools are not exposed in this session. The live top-50 streak remains 0/10.
# Current handoff status — 17 Oct 2026

The user supplied group 4cf7ad87-2c52-452e-a9a3-59787c302e67, an unranked 0–5 loss to FRChronic (rank 58 around the match). Map scores, drafts, and the missing replay access are documented in analysis/platform-match-review-4cf7ad87.md. No live top-50 wins count toward the 10-win streak; it remains 0/10.

Current best isolated local source: bots/cand-stampede-broad-pair/src/bot.cpp, experiment #131. Same-name fresh runs scored 119/136 strong-proxy wins and 614/680 broad wins in two exact repeats; #126 scored 119/136 and 612/680. The broad #131-vs-#126 deltas were Stampede +1, Pilgrimage +2, Lanes -1. Run IDs and SHA-256 hashes are in bots/tungtungsahur/PLAN.md. TinyFish is installed/enabled, but this session has no browser-action tools; the signed-in replay bundle cannot be read here.

Do not copy this candidate into the main source or rebuild the submission ZIP until the live top-50 streak condition is achieved. Current main source hash: 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5. Current ZIP hash: 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.
# Current handoff status — 18 Oct 2026

Current best isolated candidate is #133 in bots/cand-stampede-broad-pair. It applies Varg-before-Ryth only on Elkring (30x30 with altars at 26,3 and 3,26), keeping the standard Fragment lineup. It scored 120/136 against four strong local proxies in two exact repeats and 618/680 in the broad pool in two exact repeats; #131 scored 119/136 and 614/680. All four broad gains were Elkring games. #132 applied the change to both 30x30 maps and was rejected because its Fragment total fell by three wins.

See bots/tungtungsahur/PLAN.md for the run IDs and hashes. Main source hash remains 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5; ZIP hash remains 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. The live group remains 0–5 against rank-58 FRChronic; top-50 streak 0/10. TinyFish is installed and enabled, but no browser-action tools are exposed in this runtime, so replay-level causes remain unverified. Do not update main source or ZIP until the 10-win live top-50 streak is verified.
Pilgrimage follow-up: #134 (Varg before Ryth) and #135 (Ren for Tavi) each scored 5/8 versus #133's 6/8 on the targeted four-proxy set. Reject both; restore #133. Full-map and repeat results for #133 remain 120/136 strong and 618/680 broad, repeated exactly. The source and ZIP are still unchanged.
Rank refresh: FRChronic's latest readable public performance-history point is rank 67 at 2026-10-17 23:00:35 UTC; the 50-team leaderboard still returns HTTP 401, so current live top-50 membership is unverified.
The tested #133 source is packaged at submissions/tungtungsahur-candidate-v133-unranked-test.zip (SHA-256 558C3D1FD41B759FA5E9558F4AE361F67212BD08C374CB1BE85CDFC6124094EB). Its source files were checked against the candidate directory. The package is local and has not been uploaded; the main submission ZIP is unchanged.
Swirl follow-up: #136 (Varg before Ryth) scored 3/8 versus #133's 4/8; reject and restore #133. The candidate test ZIP remains byte-verified at submissions/tungtungsahur-candidate-v133-unranked-test.zip.

Latest equipment screens #137–138 were rejected. Issac's Durability Health follow-up tied the #133 baseline at 54/68 against Ming/Xuanming; Stellar's Treasure Focus-first build scored 50/68. The #133 candidate source and WASM are restored. Local proxy results do not count toward the live top-50 streak, which remains 0/10. Main source and `submissions/tungtungsahur.zip` remain unchanged.

Latest continuation: #139 global parity retreat was rejected at 44/68 strong proxies. #141 caches a parity retreat rule for Swirl only, scoring 121/136 strong and 613/680 broad in two identical broad runs; the broad result is five below #133, with all five losses on Swirl. #142's 1.1× variant failed the targeted screen. Keep #133 as the broad-pool control and #141 as the top-proxy candidate. The #141 test ZIP is local at `submissions/tungtungsahur-candidate-v141-unranked-test.zip`; its source was uploaded as distinct candidate submission version 25. Live top-50 streak remains 0/10; the browser-action connector is not exposed here. Main source and `submissions/tungtungsahur.zip` remain unchanged.

## Current continuation — #143

#143 applies the parity-retreat rule only on Swirl when the opponent drafts Cassi & Issac, Varg, Stellar, and Vendetta. It scored 121/136 against four strong local proxies in two runs and 618/680 in two exact broad-pool repeats; broad per-map totals match #133, with one additional strong-set Swirl win. The test ZIP is verified locally and the source is uploaded as separate candidate submission version 26. It has not been tested in a new live match group. Live top-50 streak remains 0/10; the main `tungtungsahur` source and ZIP remain unchanged.

## Current continuation — #144 and supplied link (18 Oct 2026)

#144 raised the retreat threshold to 1.5x against a mirrored Collision draft with Cassi & Issac, Varg, and Stellar. It scored 0/4 against Ming/Xuanming versus #143's 1/4 control; reject #144 and restore #143. Runs: `matches/league/20261018-004844-cand-stampede-broad-pair` and `matches/league/20261018-004856-cand-stampede-broad-pair`.

The match-group link supplied again is the same unranked group created 17 Oct at 21:50 UTC: Heavenly Court lost 0-5 to FRChronic. The public API shows `submissionId: null` and `version: null` for both teams, so it cannot verify which candidate played; the group also predates candidate v26. A fresh top-50 match group is still needed. Live streak: 0/10. #143 remains the best isolated local candidate; candidate submission v26 is uploaded. Main source and `submissions/tungtungsahur.zip` are unchanged (hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`).

## Current continuation — #145 (18 Oct 2026)

#145 adds Pilgrimage-only allied-half altar preference for carriers with at least 100 gems. Its direct 40-game local Pilgrimage screen repeated at 31/40; same-runner #143 control was 29/40. The two per-opponent gains were one side against Faisal-bot and one against opp-tts-aggro. A replay-backed Faisal-bot side-B loss flipped from 676-988 with 236 death-bag gems lost to a 1004-820 win with zero gems lost on deaths. The exact four-strong-proxy Pilgrimage screen tied #133 at 6/8. Replay folders and summaries are under `matches/league/145-direct-broad-pilgrimage-20261018`, its repeat, and `matches/league/143-direct-broad-pilgrimage-control-20261018`.

The candidate is packaged at `submissions/tungtungsahur-candidate-v145-unranked-test.zip` (24,829 bytes, SHA-256 `B311BBD9172CCB1B94447A2A0C9C220A8EFE331CF1C3126A225668BA8438F404`) and was uploaded as separate submission version 27. Candidate source/WASM hashes are `82BD25CB989585392CD627085947DDD48E6051352E0B363097C8142A1EFD1D84` and `44FF0132155193697094CBEAA6AEC1D2E0AF3009DB8D9D6B2FA481D49D0D0881`. Main source/ZIP remain unchanged at `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

Live top-50 streak remains 0/10. The supplied link is the old 17 Oct group, and the current leaderboard API returns 401 without the site browser session. This runtime still has no browser-action tool to create a new group. A fresh unranked group using v27 against a current top-50 team is the next live-validation input.

## Current continuation — full v27 local evaluation (18 Oct 2026)

The direct-runner broad pass completed 680/680 matches at 620 wins. Against the fresh same-runner #143 control (618/680), only Pilgrimage changed: 29/40 to 31/40; every other map total matched. The strong four-proxy full-map screen completed 136/136 at 121 wins, with exact per-map parity against #143. All replay bundles and summaries are under `matches/league/20261018-010922-cand-stampede-broad-pair-direct-v145-full-pool-20261018` and `matches/league/20261018-011341-cand-stampede-broad-pair-direct-v145-strong-all-maps-20261018`.

Ming remains 26/34 and is the clearest local weakness. On Collision, both sides lost (416–1012 and 254–1012); enemy tributes clustered near (26,19), repeated altar locks appeared at (27,20), and our deaths dropped 110/66 gems. On Swirl, both sides lost with 47/34 deaths and 98/242 gems lost on deaths. Pilgrimage losses were 596–1016 and 692–1072; only side A lost gems to deaths. The data points to central altar control on Collision and survival/income on Swirl; the Pilgrimage route improvement does not yet beat Ming.

Reject #146 (keep the team grouped on Collision: 4/8 vs the #145 5/8 baseline, losing both Ming and Xuanming games) and #147 (Varg Power Strength first: 5/8, unchanged wins and lower Ming-game gems). Keep #145 as the current isolated candidate, uploaded separately as v27. The direct-runner helper is `tools/direct_league.py`; the batch wrapper remains broken by a Windows CMake path error.

Verified hashes remain: #145 source `82BD25CB989585392CD627085947DDD48E6051352E0B363097C8142A1EFD1D84`, WASM `44FF0132155193697094CBEAA6AEC1D2E0AF3009DB8D9D6B2FA481D49D0D0881`, test ZIP `B311BBD9172CCB1B94447A2A0C9C220A8EFE331CF1C3126A225668BA8438F404`; main source `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and main ZIP `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` remain unchanged. All six candidate ZIP source entries match.

Live top-50 streak remains 0/10. The provided URL still points to the finished 17 Oct 0–5 FRChronic group; its public API shows null submission versions. A fresh group using v27 against a current top-50 team is still needed. The signed-in browser cannot be controlled in this runtime.

Swirl follow-up #148 tried breaking an enemy altar lock while unloaded if no enemy was visible. The 8-game screen scored 4/8, below #145's 5/8, losing both Ming and both Xuanming games; reject it and preserve candidate v27. The latest user-provided URL is still the same 17 Oct 0–5 FRChronic group with null submission versions, so live top-50 streak remains 0/10.

Experiments #149–152 were screened and rejected. Swirl Tavi-for-Ryth tied v27 at 5/8 but cut Ming-game gems; the counterdraft-only 40% recall threshold fell to 4/8. Collision Varg-solo and 2+2 paired farm each scored 4/8 versus a fresh v27 control at 5/8; paired farm scored only 66 and 132 in the Ming games versus v27's 416 and 254. Candidate v27/#145 remains the best tested local variant. TinyFish is installed and enabled, but its browser actions are not exposed to this runtime. Live top-50 streak remains 0/10; main source and submission ZIP are unchanged.

## Current continuation — #153 Collision camp avoidance (18 Oct 2026)

Replay diagnostics found all four champions repeatedly targeting the same enemy-side group of three elks (108 gems, 180 damage/turn). #153 starts from v27/#145 and skips groups above 100 damage/turn only on Collision, identified by 41×41 dimensions and the altar at (27,20). Against Ming, Xuanming, Faisal-bot, and opp-racer it scored 6/8 versus v27's fresh 5/8 control; against the full local 20-opponent Collision pool it tied 37/40. Keep it as a Collision-specific local candidate, not a replacement for v27's verified full-map baseline.

Source/WASM hashes: `0AB17AE08EA254173FD8633F25F95B0F2746AEC98BBAB5B785FFE718B0000575` / `5442D39B50092DA187917F2DEE9EFA0B94D169540D1654A2DE9567B0EFC2DF9B`. Package `submissions/tungtungsahur-candidate-v153-unranked-test.zip` is 24,956 bytes, SHA-256 `C0519B27C99CC4BE90D89A8F590C76D8045921D38A8B8B8A7DCFE64EA74015A5`; all six source entries were byte-verified. The candidate was uploaded as test submission version 28 using `cambc submit cand-collision-no-elite-camp`. The 8-game Swirl out-of-map check matched v27 exactly. Run folders, matchup changes, and details are in `bots/tungtungsahur/PLAN.md` and `analysis/maps.md`.

The user supplied the same group URL again: it remains the 17 Oct group where Heavenly Court lost 0–5 to FRChronic; all five games finished and both teams have null submission versions. The 10-win top-50 streak is still 0/10. TinyFish is installed/enabled, but this runtime has no browser-action tool to use the user's signed-in site session or create a new group. Main source/ZIP hashes remain unchanged (`188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` / `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`).

The exact v28/#153 all-map strong screen finished 121/136, tying the fresh v27 control at 121/136. Collision improved by one map win, while Lanes dropped by one; treat #153 as a test candidate, not a full-map improvement. Pilgrimage #154 (3/3 split from round 1) and #155 (regroup during fight alarms) each scored 5/8 versus v27's fresh 6/8, with losses shifted away from Ming but toward Xuanming. Preserve v27's Pilgrimage setup. Full summaries and run IDs are in `bots/tungtungsahur/PLAN.md`.

## Current continuation — #156–158 (18 Oct 2026)

Five-pick mage-first #156 scored 117/136 strong proxies versus v27's fresh 121/136. Pilgrimage-only #157 tied the strong set at 121/136 but lost the broad Pilgrimage pool, 29/40 vs 31/40. Combat-alarm-only #158 scored 5/8 on Pilgrimage vs v27's 6/8. Reject all three; retain v27/#145 as the best full-map local baseline. No candidates #156–158 were uploaded.

The latest user link remains group `4cf7ad87-2c52-452e-a9a3-59787c302e67`, created 17 Oct, finished 0–5 on five maps, with null submission versions. The leaderboard API returns 401. TinyFish is enabled but browser actions still are not exposed to this runtime, so no new live group can be created here. Live top-50 streak remains 0/10. Candidate v28 remains separately uploaded; main source and ZIP hashes are unchanged: `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

### Supplied match group data and replay access

The public metadata for group `4cf7ad87-2c52-452e-a9a3-59787c302e67` shows five finished losses: Interlock 750–1004 (683 rounds), Stampede 0–1080 (637), Elkring 432–1008 (505), Fragment 286–1018 (636), and Pilgrimage 596–1027 (930). Both sides have null submission IDs and versions, so these games cannot identify the bot build. The replay bundle endpoint responds `Sign in to watch or download replays`; the signed-in website session is not available to this runtime. No replay files were retained.

The requested fixed Ryth/Vendetta/Tavi/Willow/Prism roster was already screened as #66 (111/480) and with the phase trigger corrected as #67 (296/480); both were far below the map-adaptive v27 baseline and were rejected. Keep the optimized draft unless new live evidence justifies another evaluation.

## Latest v28 broad check (18 Oct 2026)

v28/#153 scored 622/680 in a full local broad run versus a fresh v27 control at 620/680. The apparent +2 is inconclusive: Collision had two wins flip each way (net zero), and Lanes improved 38/40→40/40 even though v28 only changes Collision. `cambc run --help` has no seed control. The v27 experimental source and WASM were restored and verified at SHA-256 `82BD25CB989585392CD627085947DDD48E6051352E0B363097C8142A1EFD1D84` and `44FF0132155193697094CBEAA6AEC1D2E0AF3009DB8D9D6B2FA481D49D0D0881`. Main source and ZIP remain untouched. Live top-50 streak remains 0/10.

The same-name v28 run (`20261018-021303`) reproduced 622/680, but still differed from v27 on Lanes, so naming the candidate like v27 did not produce a seed-paired comparison. The runner has no seed flag; preserve the result as inconclusive. I also checked `nodeRepl.rpc('browser', ...)`: the browser service module is missing. Opening the supplied page with `Start-Process` was rejected by runtime policy, so no browser window opened. Do not retry by bypassing that policy; wait for a new group link or an exposed browser action tool.

## Current continuation — #160 Collision threshold (18 Oct 2026)

The 150-DPS Collision exclusion tied the original v28 rule at 37/40 on the full Collision proxy pool and tied v27 at 121/136 on all maps. Reject #160 and retain v27 as the local baseline; v28 remains uploaded but unvalidated live. The CLI help has no challenge/match-group command. Leaderboard API is still 401, browser actions are absent, `nodeRepl.rpc('browser')` reports a missing service module, and opening the URL was blocked by runtime policy. The supplied group remains 0–5 with null versions; live streak 0/10. Main source and ZIP are unchanged.

## Current continuation — #161 Contest draft screen (18 Oct 2026)

The Contest-only Willow-for-Ryth counter-draft was rejected. It tied v27 at 7/12 on the selected six-opponent screen, improving only against the caster/locker proxies while falling from 7/8 to 4/8 against the four strong proxies. Across the full 20-opponent Contest pool it scored 21/40; fresh v27 control scored 32/40, matching its prior result. Keep v27 as the local baseline. Run IDs and hashes are in bots/tungtungsahur/PLAN.md; the candidate was neither packaged nor uploaded.

The latest supplied URL is again group 4cf7ad87-2c52-452e-a9a3-59787c302e67, the completed 17 Oct 0–5 FRChronic group with null submission versions. It cannot validate the uploaded v28 or any newer candidate. Live top-50 win streak remains 0/10. This runtime still has no browser-action connector or CLI match-group creation command, and the leaderboard endpoint returns 401. The separately uploaded v28 remains unvalidated live. Do not update the main source or ZIP until the user-authorized 10-win live streak is verified. Main source and ZIP hashes remain 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.

## Current continuation — Contest candidate v29 (18 Oct 2026)

Best current isolated local candidate: Contest-only early gold weight 0.25, with v27's normal phase split. #165 scored 8/8 on the selected strong Contest screen (v27 7/8), 33/40 twice against the full local Contest pool (v27 32/40), and 122/136 across all 17 maps against four strong local proxies (v27 121/136). The measured wins were Ming on Contest side B and opp-fai-casters on Contest side A; other strong-set outcomes matched. The no-gold and full-team-lock variations were rejected. Full run IDs, source/WASM hashes, and replay details are in bots/tungtungsahur/PLAN.md.

Candidate ZIP submissions/tungtungsahur-candidate-v165-unranked-test.zip was verified (25,457 bytes; SHA-256 ea5dd394822f95ac691bf6adc2cc4910bcfb25ec3ab7da0cee2a4d4a9b65e505) and uploaded as separate submission version 29. It needs a new unranked match group against current top-50 opponents. The latest supplied link is still the completed 17 Oct 0–5 FRChronic group, with null submission IDs and versions; it predates v29. Live top-50 streak remains 0/10. This runtime has no browser-action connector or match-group creation command, and the leaderboard API returns 401, so I cannot create or verify that group here. Please create a new group using candidate v29 and send its URL. Do not update the main source or ZIP until the 10-win live streak is verified. Main hashes remain 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.

### v29 full broad-pool cross-check (18 Oct 2026)

The full 20-opponent, 17-map run scored 619/680 for v29 and 620/680 for fresh v27. Per-map totals matched except Contest (33/40 vs 32/40) and Pilgrimage (29/40 vs 31/40); the code change is gated to Contest. Mark the all-map aggregate inconclusive without seed pairing. The repeated Contest results still make v29 worth live testing, but do not treat it as a broad-pool improvement. Candidate v29 is uploaded; live top-50 streak remains 0/10 pending a new match-group link.

### Pilgrimage banking screens (#166–167)

Two new Pilgrimage tweaks were rejected. Lowering the 100-gem allied-half bank threshold to 68 tied the broad pool at 31/40 but fell to 5/8 strong; its target opp-tts-v3 Ryth death replay was byte-identical because survive() returns before bank(). Trying bank() before retreat only for low-health carriers with at least 68 gems tied the strong set at 6/8 but scored 30/40 broad against v27's 31/40. Keep v27's existing Pilgrimage behavior. Replays, run IDs, and hashes are in bots/tungtungsahur/PLAN.md; neither candidate was uploaded.

### Pilgrimage follow-up (#168–169)

The locked-altar surcharge (#168) tied v27 at 6/8 strong and 31/40 broad and did not fix the 92-gem carrier deaths. Banking before burst (#169) also tied the strong screen, with byte-identical action logs, and scored 28/40 in its unpaired full-pool run versus v27's recent 31/40. Reject both and retain v27. Details and hashes are in bots/tungtungsahur/PLAN.md.

The user supplied group `4cf7ad87-2c52-452e-a9a3-59787c302e67` again. It is the same completed 17 Oct 0–5 FRChronic group with null submission versions; it does not validate v29 or add to the live streak (0/10). The unauthenticated page request returns only the SPA shell, the browser-control service is missing, and opening the URL was blocked by runtime policy. A new unranked group using candidate v29 against current top-50 opponents is still needed. Main source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

### Pilgrimage high-bag retreat screen (#170)

A Pilgrimage-only 55% retreat threshold for carriers with at least 68 gems tied the strong screen at 6/8 and lost both games against opp-tts-v3; Ryth still died carrying 92 gems. Reject and preserve v27's current retreat threshold. Run details and hashes are in bots/tungtungsahur/PLAN.md. Main source and submission ZIP remain unchanged.

### Contest gold-weight refinement (#171–172)

Early gold weights 0.5 and 0.1 each scored 7/8 against the four strong local Contest proxies, below v29's 8/8 at 0.25. Retain v29's 0.25 setting as the strongest tested Contest-specific candidate; the other values were not run through the full pool. TinyFish is installed and enabled, but its browser-action tools are not exposed to this session, so live standings and match groups remain inaccessible here.

### Contest altar-lock response (#173)

The Tank's nearby gem-carrier lock-clearing rule tied a fresh v29 control at 3/8 against targeted Contest proxies and recorded the same 267 team deaths. Reject it. Main source and ZIP remain untouched; live top-50 streak is 0/10.

## Current continuation — #174–175 map-specific candidates (18 Oct 2026)

The Corners opening split (#174) scored 36/40 in two full Corners-pool runs versus v27's 34/40. The six-opponent screen was 9/12 versus a fresh v27 6/12. Across 680 games, #174 tied v27 at 620/680; Corners gained two wins while Pilgrimage lost two in an unseeded run, so the all-map score is inconclusive. Combining this with v29's Contest 0.25 early-gold weight (#175) scored 69/80 twice across the full Contest and Corners pools (33/40 and 36/40), versus v27's 66/80 (32/40 and 34/40). Source/WASM hashes and run paths are in `bots/tungtungsahur/PLAN.md`.

#175 was uploaded separately as test submission version 30. The supplied match-group URL still points to the completed 17 Oct FRChronic 0–5 group, where both submission versions are null; it cannot validate v30. Live top-50 win streak remains 0/10. The CLI upload succeeded, but the signed-in browser session is not controllable from this runtime because the browser service module is missing. A fresh unranked group must select version 30 to start live validation.

Main source and ZIP were rechecked and remain unchanged: `bots/tungtungsahur/src/bot.cpp` SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; `submissions/tungtungsahur.zip` SHA-256 `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Current continuation — #176 Contest safe farming (18 Oct 2026)

#176 extends test version 30 with a Contest-only rule to avoid camp groups above 100 damage per turn before late game. It repeated 39/40 on the full Contest pool versus version 30's 33/40; in replay comparisons, deaths dropped sharply while gem tributes increased. The full 17-map pool was 628/680 against a fresh version 30 control at 621/680. Contest changed 33/40→39/40, Corners stayed 36/40, and the other map totals matched except Lanes (+2) and Stampede (-1). The 600–600 Contest tie against opp-fai-ranged was lost on lifetime gold, 7,795 vs 8,962.

Two attempts to raise mid/late Contest gold priority were rejected: weight 0.25 scored 38/40, losing both my-bot-v2 sides with zero gems; weight 0.05 scored 37/40. Keep #176's Contest safe-farming rule and the early 0.25 gold weight only.

The #176 source/WASM hashes are `7A7CC9F51129C4F3B27B56928EB08651EE06AD7C7AE9809CE7AD427886CD6B73` / `E306C68671B55E7A5DBA53221A7DFFDE69CC1B37EA866D1D7976ECF6C0CED1A5`. It is uploaded as test submission version 31; an identical retry created version 32. These are separate test submissions; the main source and ZIP remain untouched. Live top-50 streak is still 0/10. The supplied old match group has null submission versions and cannot validate either candidate. A fresh unranked group using version 31 or 32 is needed.

Main hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` for `bots/tungtungsahur/src/bot.cpp` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` for `submissions/tungtungsahur.zip`.

### Remaining map-loss leads from v31's 680-game run

The weakest local opponents were opp-tts-v5 (25/34), opp-tts-v3 (28/34), and opp-tts-v4 (28/34). Against v5, both Collision losses involved repeated locks at the central altar (27,20); its Swirl loss finished 498–1086 after 66 deaths and 1,050 gems lost. Against v3, both Pilgrimage sides lost (136–1004 and 884–1036); side B lost 92 gems on deaths, and both games show altar locks at (14,3)/(35,3). Both v4 and v5 also beat the bot on both Packs sides (792–1000 and 388–1056). These remain local proxy results; prioritize altar access and bag preservation on those maps, then validate against fresh live opponents.

## Swirl follow-ups (#179–180, 18 Oct 2026)

Extending Contest's >100 damage/turn camp avoidance to Swirl scored 34/40 against #176's fresh 35/40 control. Broadening the Swirl retreat trigger to a Ryth/Cassi & Issac/Stellar/Tavi opponent draft scored 30/40; opp-tts-v5 improved to 2/2, but locker and other matchups regressed. Both experiments were rejected and were not uploaded. Retain #176 as the best local candidate; its test submissions are versions 31 and 32.

The link supplied again, `https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67`, still identifies the completed 17 Oct 0–5 FRChronic group with null submission versions. It cannot validate versions 31/32 and does not change the live top-50 streak (0/10). I rechecked the signed-in browser bridge; its browser service module is missing, and the CLI only exposes local run/build/submit commands, so this runtime still cannot create or inspect a fresh live group. Main source SHA-256 remains `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; production ZIP remains `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Do not promote the candidate until the 10-win live streak is verified.

## Current continuation — #181–184 (18 Oct 2026)

Swirl tests #181–183 did not beat the fresh #176 baseline: the partial-core Tavi draft guess fell to 32/40, the exact final-pick condition was a no-op under simultaneous drafting, and the 150-DPS camp threshold tied at 35/40 with fewer deaths. Reject those variants. Packs candidate #184 starts its existing role-specific farm split from round 1; it scored 38/40 twice versus a fresh version 31 control at 34/40, converting both opp-tts-v4 and opp-tts-v5 losses on both sides. The complete 17-map run scored 632/680 against version 31's 628/680; only Packs improved. One replay-collision recovery run completed the affected matches successfully. Run IDs and source/WASM hashes are in `bots/tungtungsahur/PLAN.md`.

Candidate ZIP `submissions/tungtungsahur-candidate-v37-unranked-test.zip` (SHA-256 `A0431087FCF07B283432DC5476A1AE3396CB667C62DE1EF7F51D3167BDADAFE5`) was verified and uploaded separately as test submission version 33. The latest supplied URL remains the completed 17 Oct FRChronic 0–5 group with null submission versions; it does not validate v33. The page shell is reachable, but the signed-in browser action bridge still fails because its service module is missing. Live top-50 streak remains 0/10; a fresh unranked group selecting v33 is required. Do not promote this local candidate into the production source or ZIP until the live ten-win streak is verified.


## Latest follow-up — #185 and live endpoint check (18 Oct 2026)

#185 keeps #184's Packs split-farming opening but restores the early attack-range leash until round 600. It won 4/4 selected games against Faisal-bot and opp-tts-locker versus a fresh #184 control's 2/4, but two full Packs pools were 38/40, tied with #184's fresh 38/40 control. The wins and losses shifted between matchups; #184 remains the best measured all-map candidate. #185 was not uploaded. Runs and hashes are in `bots/tungtungsahur/PLAN.md`.

The live API recheck confirmed the supplied group is finished unranked 0–5, Heavenly Court vs FRChronic, created 17 Oct 21:50 UTC, with five matches, null submission IDs/versions, and `myTeamId: null`. GET leaderboard and challenges both returned `401 SIGN_IN_REQUIRED`; the signed-in browser bridge remains unavailable and Chrome debugging ports are closed. The saved ladder snapshot is from 17 Oct, not current. Live top-50 streak remains 0/10.

Test submission version 33 contains the verified #184 candidate ZIP. Main source and production ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Latest follow-up — #186 Pilgrimage and all-map repeat (18 Oct 2026)

#186 starts the role-objective split from round 1 on Pilgrimage, balances the team 3+3, and keeps early combat at the attack-range leash until round 600. It scored 34/40 twice on Pilgrimage versus fresh #184's 29/40. Two complete 17-map candidate pools repeated at 636/680; a fresh #184 control scored 632/680. The map delta was Pilgrimage +5 (29/40→34/40), Lanes -1 (40/40→39/40), all other maps tied. The targeted four-strong-proxy screen regressed from 6/8 to 4/8: both v3 games improved but both Xuanming games were lost. This is promising unseeded local evidence, not live validation. The six-file source-matched bundle was uploaded separately as test submission version 34 (SHA-256 `45A8118EACE011FCD67622BF5263E1172B0D622804B48A82A0CE858510DC2677`); #184 remains test version 33.

The supplied match-group URL `4cf7ad87-2c52-452e-a9a3-59787c302e67` still points to the completed 17 Oct unranked 0–5 group with null submission versions, so it tests neither version 33 nor 34. The browser bridge still fails because its service module is missing; no fresh group has been created or inspected. Live streak remains 0/10. Production source and ZIP remain unchanged.

## Latest live evaluation (18 Oct 2026)

The official `cambc` 2.2.5 CLI used the confirmed sign-in to create and inspect unranked groups and download summaries/replays. This supersedes older handoff statements that browser actions were required. The current leaderboard snapshot (03:48 UTC) ranked Intercontinental Fish #1, Nyxius #2, Mite #3, and FRChronic #43.

Candidate test submission v35 (based on local #189) was likely used, but the public match API omits submission versions. It lost 0–5 to #1, went 1–4 against #2 (winning Stampede last), and lost 0–5 to #3. Streak: **0/10**. The supplied FRChronic group is a separate older 0–5 result and its replay files have now been downloaded.

The #1 and #2 groups repeatedly lost Swirl, Collision, Pilgrimage, and Contest. The #2 Swirl game submitted 0 gems after 26 deaths; Contest submitted 0 after 97 deaths; Pilgrimage submitted 388 versus 1,112. Against #3, Lanes and Expanse were farming losses with almost no combat; Stampede submitted 0 despite both teams drafting Prism/Stellar/C&I/Ryth/Tavi, and our first camp clear was at round 329 versus Mite's round 32. No match reported bot faults. Detailed tables and replay links are in `analysis/live-top50-match-review-20261018.md`.

Local #190 (broadened Pilgrimage meta trigger) and #191 (Swirl Ren counterdraft) both regressed against fresh controls; neither was uploaded. Main source and production ZIP are unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. The requested 10-win streak is not achieved; focus the next experiment on survival and early camp-clear tempo.

## Current continuation — Procless #4 and follow-up tests (18 Oct 2026)

The supplied URL is the completed 17 Oct FRChronic group. A fresh group against Procless, rank 4 at queue time, was created with the authenticated official CLI: [`1c2711ed-18c0-4eb9-b890-070ca91db7bd`](https://2026a.battlecode.co.uk/game/match-groups/1c2711ed-18c0-4eb9-b890-070ca91db7bd). It finished 0–5 on Swirl, Collision, Contest, Pilgrimage, and Lanes with zero bot faults. The match API omits submission versions; v36 was the latest test upload before the group and likely ran. Replay evidence is in `matches/live/1c2711ed-18c0-4eb9-b890-070ca91db7bd-matches/` and the map-by-map review is in `analysis/live-top50-match-review-20261018.md`.

Key findings: Collision first collection/bank was r79/r84 for us versus r21/r36 for Procless. Lanes and Pilgrimage began collecting at nearly the same time, but Procless dealt 70.3k/79.0k monster damage versus our 42.5k/23.4k. Swirl finished 124–1,004 after 17 deaths to 3; Contest finished 0–1,000 after 58 deaths to 11. This candidate is not live-competitive yet.

Local Stampede #194/#195/#196 scored 8/10, 7/10, and 9/10 versus a fresh #192 control at 10/10. Low-health burst #197 scored 17/30 on Swirl/Collision/Contest versus #192's fresh 20/30 control. Reject and do not upload those variants. Live streak is still 0/10. Production source/ZIP hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` / `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`; the requested 10-win streak is not achieved.

## Latest candidate — Collision camp-safety rule (#198, v37)

#198 adds the tested >100 damage-per-turn camp exclusion on Collision only, based on the replay where two champions died to camps before our first collection at r79 (Procless collected at r21). It scored 7/10 twice on the five-opponent Collision proxy screen versus fresh #192 at 5/10 twice, 142/170 versus 140/170 across the five strong proxies and 17 maps, and 637/680 versus 636/680 across the broad local pool. The broad map change was +1 Pilgrimage rather than Collision, so rely most on the repeated targeted and strong Collision evidence and keep this provisional.

The verified 25,395-byte six-source bundle is `submissions/tungtungsahur-candidate-v44-unranked-test.zip` (SHA-256 `ECA9239FC02FB397CA1E844A9C9A3EEB6B3CC8BD3FD46D8879559ABC01E53500`); it was uploaded separately as test version 37. The same-map-set Procless re-test at [`4a2bd4ac-4623-4896-8e3f-d8d026845e71`](https://2026a.battlecode.co.uk/game/match-groups/4a2bd4ac-4623-4896-8e3f-d8d026845e71) finished 0–5. Collision’s opening improved to first clear/collection/bank r10/r19/r41, but HC still lost 22–1,002 with 14 deaths and 204 gems lost; the opponent had 0 deaths and 10 kills. This fixes route timing, not survival or gem retention. Collision-only earlier retreat thresholds in #199 (parity, 5/10) and #200 (1.15×, 6/10) both regressed versus #198’s 7/10 local screen; reject them. Main source and production ZIP remain at hashes `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` / `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`; live streak remains 0/10.

## Latest continuation — rank #5 and Fragment draft (18 Oct 2026)

The user-provided URL, group 4cf7ad87-2c52-452e-a9a3-59787c302e67, is the old FRChronic 0–5 group on Interlock, Stampede, Elkring, Fragment, and Pilgrimage. FRChronic was rank 58 at the time, so it does not count toward the top-50 streak.

The fresh rank-5 opponent new team(4) was tested twice on Ambush, Corners, Eight, Fragment, and Rushbait v2. The first group e47c4b9b-0440-4152-bae7-e8912b1de243 likely used v37 and lost 0–5. Our monster damage was around half of the opponent's on four maps and 20.5k versus 74.6k on Fragment. Ambush was an uncontested farm loss: 404 submitted against 1,024, with no deaths on either side. Eight and Fragment suffered heavy combat losses.

Local #201's early solo-Varg farm split regressed (113/136 versus the #198 control at 120/135, with one failed control run); reject it.

Local #202 uses Varg / Stellar / Ryth only on Fragment. It scored 28/32 twice on a 16-opponent Fragment screen versus the control's 23/32 twice, and 122/136 on the 17-map strong set versus the control's 120/135 with one failed run. The source-matched bundle was uploaded separately as test v38; it did not alter the production source or ZIP. Fresh group 62c8cd21-f213-4d3d-983d-6afc4e1f2a16 likely used v38 and again lost 0–5. Its Fragment roster confirms the draft selector ran, but the game ended 215–1,001 with 12 deaths, 0 kills, and 22.9k monster damage versus 0 deaths, 11 kills, and 66.5k. Local draft improvement did not transfer to a live win.

The live streak remains 0/10. Production hashes are unchanged: source 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5; ZIP 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. Detailed summaries and run paths are in analysis/live-top50-match-review-20261018.md and bots/tungtungsahur/PLAN.md.

## Latest continuation — AlphaSlop rank 6 and rank-7 queue (18 Oct 2026)

After the v38 Fragment draft test, a fresh group against AlphaSlop (rank 6 at queue time), d97d6f55-8e2e-4bde-8b41-87988484d5e1, lost 0–5 on Packs, Monolith, Rows, Ambush, and Fragment. We remained below the opponent's monster damage on every map: Rows 39.4k vs 68.9k and Ambush 26.3k vs 55.0k were pure farm races with no deaths; Packs and Fragment added large combat deficits. The v38 Fragment roster faced a four-body C&I / Ryth / Stellar lineup and lost 259–1,045.

Ambush follow-ups #203–206 all failed to improve on the same local screen: early squad split 30/32, Prism-for-Tavi draft 30/32, camp-focused equipment 30/32, and draft-plus-equipment 31/32 versus control 31/32 (with lower average gems). None was uploaded.

A group against current rank 7 Sneaky Bush Campers was queued as dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d on Stampede, Expanse, Lanes, Interlock, and Elkring. All matches were still queued at the time of this update. Continue polling that group ID; do not duplicate it.

The requested live streak remains 0/10. Test v38 is separate; production source and ZIP hashes are unchanged at 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D.

## Rank-7 completion — Sneaky Bush Campers (18 Oct 2026)

The previously queued group dc9f582e-6fb1-46af-ae61-3f5cf02e9b4d against rank-7 Sneaky Bush Campers has finished 0–5 on Stampede, Expanse, Lanes, Interlock, and Elkring. Stampede collected 1,080 gems but lost all submissions after 23 deaths; the opponent submitted 1,080 with 10 deaths. Expanse/Lanes were farming losses; Interlock/Elkring combined lower farming with repeated deaths. See analysis/live-top50-match-review-20261018.md and bots/tungtungsahur/PLAN.md.

Production remains unchanged; test streak is 0/10. The next meaningful work is a measured improvement to sustainable camp damage, safe gem returns, and fight survival. Top-50 groups are still losses, so do not promote v38 or rejected #203–206.


## Latest status — candidate v39

The user-provided FRChronic group `4cf7ad87-2c52-452e-a9a3-59787c302e67` is the old 0–5 group against a team ranked 58 at the time. The authenticated CLI is signed in and usable for submissions and unranked groups.

Test v39 combines the Fragment Varg / Stellar / Ryth draft with an Ambush shared opening through round 149 and a mid-game split from round 150. The six-source bundle `submissions/tungtungsahur-candidate-v39-ambush150-fragment-meta-unranked-test.zip` is 25,735 bytes, SHA-256 `257e4d8266834a401c39e9ed6b7b270306b5ebd21b35612be9d2dd62e1bd21ce`, and was uploaded separately as version 39. Production `bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged.

The corrected round-150 variant scored 40/40 with 6 deaths on the local 20-opponent Ambush pool versus a fresh control at 37/40 with 28 deaths. A combined 17-map strong-proxy screen scored 120/136 versus a fresh Fragment-candidate control at 122/136; the all-map result is not a gain. The >100-strength Ambush camp exclusion scored 34/40 with 49 deaths; reject it.

Live v39 groups against queue-time ranks #5, #6, #9, and #10 all lost 0–5. Five more groups against ranks #11–15 also lost 0–5 each. Groups against #17 Shawn and #18 Ely2sh are complete at 0–5. v39 has 0 wins in its first 55 live matches; the target remains 10 consecutive wins and the streak is 0/10. Groups against ranks #19–29 are queued/running:

- #19 NotSoLonely — `91557762-ae80-4526-9b26-5379c8ed8997`
- #20 print dont int — `99a3dca7-2e58-419d-adf8-692bb2129408`
- #21 KratosMessi — `37f7bd89-59c6-4ea9-9b1d-6f40dd679f40`
- #22 ❤️Quantom❤️ — `8d437cb4-9b43-4a6b-9c0a-ed664858e346`
- #23 meow — `2b33d39c-37b6-4661-9902-f7403a2c1412`
- #24 Cabbage — `1d9b4d93-4c43-4666-8260-489529d5d04d`
- #25 geese geese go — `3285e2e6-2f22-4df0-bf3c-df2e7479502f`
- #26 Ad Astra — `6fd1505a-de9a-4ded-aae3-a41359bcc6a9`
- #27 hello — `4533eb58-6d91-40b3-ad36-a46b31e9ef75`
- #28 Still Testing — `a0adb4b4-f0fd-47ff-abd1-6a42544982a9`
- #29 剑桥夜爬者 — `16bc4778-36b6-404c-933e-628b228ab67b`

The rank-5 Ambush replay shows the opening's limit: HC banked 72 at round 99, reached 178 by round 144, then Cassi and Issac died to camps at round 145. The score stayed at 178 until round 404, and Issac later died carrying 106 gems. Future work needs sustained farming, safe gem returns, and combat survival. Poll the existing groups before creating duplicates. Do not promote v39 or update production until the ten-win live streak is verified. Production hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` / `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.


## v39 group completion correction — through rank 29

The rank #19–29 groups have all finished. In total, v39 recorded 2 wins out of 110 completed matches. Both were on Fragment with Varg / Stellar / Ryth: Ad Astra (#26) 1,014–276 and 剑桥夜爬者 (#29) 1,006–598. The other 108 matches were losses. The wins were separated by losses; maximum consecutive run is one, current streak zero of the requested ten. Both winning summaries report zero platform faults. See the live review for damage, kill, and death metrics.

The v39 campaigns' best confirmed transfer is the Fragment draft. It has two live wins, but the surrounding matches remain mostly severe farming/combat losses. The Ambush round-150 behavior is still local-only evidence; the >100-strength filter and the round-120 timing both regressed locally. Round 120 repeated 39/40 with 34 deaths; round 150 repeated 40/40 with 6 deaths.

All groups through rank 29 are finished. CLI quota was 29/30 at the last check and resets at 05:20:02 UTC. Continue with rank 30 onward after reset, then inspect each group before creating more. Do not upload another test candidate until these v39 results are fully reviewed. Production files remain untouched and the 10-win streak is not achieved.

### Rank #30 KKB group finished

Created [45c52751-c4fa-4377-8db3-11f8fa2958a0](https://2026a.battlecode.co.uk/game/match-groups/45c52751-c4fa-4377-8db3-11f8fa2958a0) using the remaining quota before reset; it finished 0–5. Queue-time rank was #30. The Fragment lineup Varg / Stellar / Ryth lost 483–1,013; every map had lower HC monster damage. The 115-match campaign total is 2 wins, 113 losses, maximum consecutive streak 1, current streak 0/10. The first #30 group's match summaries are saved at the workspace root; see `analysis/live-top50-match-review-20261018.md` for map-by-map findings.

The KKB (#30) group is fully reviewed. A follow-up local Fragment draft adding Cassi & Issac to Varg / Stellar scored 26/32 versus a fresh 28/32 Varg / Stellar / Ryth control; reject it and keep v39 as the latest live submission. Production remains untouched. Wait for the 05:20:02 UTC quota reset before creating the next top-50 group.

### Rank #31 umamusume group finished

Group [`9cbc69c6-f4e8-4c04-b072-290f6f30c15d`](https://2026a.battlecode.co.uk/game/match-groups/9cbc69c6-f4e8-4c04-b072-290f6f30c15d), queue-time rank #31, finished 0–5 with no platform bot faults. Monster damage was lower on all maps: Fragment, Ambush, Packs, Monolith, Rows. Campaign total is 2/120 live wins, max streak 1, current 0/10. Full stats are in `analysis/live-top50-match-review-20261018.md`; next target is #32 Master of Betas after the rolling quota frees a slot.

### Master of Betas group finished

Group [`59a3ce77-5499-46cc-92a7-5150bf8aa647`](https://2026a.battlecode.co.uk/game/match-groups/59a3ce77-5499-46cc-92a7-5150bf8aa647), queue-time rank #31, finished 0–5. Zero platform faults. The 125-match campaign has 2 wins and a 0/10 current streak. Swirl finished 36–1,058 with 29 deaths; Stampede collected but submitted 0. Review the full map table before choosing the next map-specific change. The group was queued when current rank #31 was Master of Betas; ranks have shifted since the earlier #30/#31 groups.

### Memory? group finished

Queue-time rank #33, group [`f2fe8162-ae57-4b93-9a73-738c00502d39`](https://2026a.battlecode.co.uk/game/match-groups/f2fe8162-ae57-4b93-9a73-738c00502d39), finished 0–5 with zero platform faults. Campaign is 2/130 live wins, current streak 0/10. Contest ran to round 2,000 with no gems; Memory? won the normal gold tiebreak 11,775–575 after 121 HC deaths to 1 and 99 kills to 1. This is a combat/survival failure. Raw summaries and exact stats are in the live review.

## Current continuation — Contest candidate v40

Candidate #216 was uploaded separately as test submission version 40 after local Contest testing showed 40/40 versus a fresh v39 control at 39/40, plus 400 more Contest gems on a four-strong-proxy screen. The 17-map integrated screen tied v39 at 125/136 wins; all per-map win counts matched. This is a limited live-test candidate, not a production promotion. The live v39 baseline remains 2 wins in 130 top-50 matches, maximum consecutive streak 1, current streak 0/10. Production source and ZIP hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

The next v40-likely live group against Cabbage (queue-time rank #26) finished 0–5: [`8da6a23e-ca78-4e29-bf01-61152c1bd182`](https://2026a.battlecode.co.uk/game/match-groups/8da6a23e-ca78-4e29-bf01-61152c1bd182). Contest ended 0 submitted gems with 93 deaths to 6; first deaths were our Cassi and Issac at round 42. Swirl and Stampede also had severe collection/survival gaps; Ambush submitted 928 vs Cabbage's 1,086. Zero platform faults. Captured stdout had eight `Champion cannot act` errors in Contest (crowd control/stun per `analysis/forensics.md`), three in Swirl, one in Fragment, and a blocked-destination error in Ambush. The API omits exact submission version, so v40 is probable from timing, not confirmed. Campaign: 2/135 live wins, maximum streak 1, current streak 0/10. Full metrics and replays are in `analysis/live-top50-match-review-20261018.md` and `matches/live/8da6a23e-ca78-4e29-bf01-61152c1bd182-unpacked/`. v40 remains a test-only build. Production hashes are unchanged.

The next v40-likely group against Still Testing, rank #29 at queue time, finished 0–5: [`bd89f7c3-e3df-4103-97bd-e012f1570c80`](https://2026a.battlecode.co.uk/game/match-groups/bd89f7c3-e3df-4103-97bd-e012f1570c80). Monster damage was lower on all five maps. The clearest map split: Corners 72/1,028 gems, 4/0 deaths, 18.4k/71.0k monster damage; Rows 528/1,056 with no deaths or kills, 38.7k/71.9k damage; Pilgrimage 484/1,000 with 15/3 deaths. Zero platform faults. Campaign: 2/140 wins, current streak 0/10. Exact map stats and summaries are in the live review. A new group against previously untested EggsAfter11AM (rank #32 snapshot) is running on Monolith, Elkring, Interlock, Lanes, and Collision.

### Current update — EggsAfter11AM complete; Zarzorki queued

The EggsAfter11AM group [`e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1`](https://2026a.battlecode.co.uk/game/match-groups/e40bd79d-4833-4f38-8ea8-fd0b28b3d3d1) completed 0–5 with zero platform faults. The detailed map table and raw summaries are in `analysis/live-top50-match-review-20261018.md`. In brief, we did 2.0–2.8 times less monster damage on each map, with the largest fight collapses on Elkring, Interlock, and Collision. EggsAfter11AM repeatedly bought a damage emblem followed by Durability Health on carries/frontliners; some champions also bought Jungle Health. Experiment #137 already tried one Issac Durability second-emblem build and tied the local control, so don't repeat it as a general change. Current campaign: 2 wins/150 top-50 live matches, max consecutive streak 1, current streak 0/10.

Group [`deec6df3-1b7f-438d-9221-70e00a5a4591`](https://2026a.battlecode.co.uk/game/match-groups/deec6df3-1b7f-438d-9221-70e00a5a4591) is now queued against Zarzorki (rank #15 and not previously tested by team ID), on Fragment, Ambush, Contest, Elkring, and Rows. Poll/review this group before queuing another. The CLI showed quota 29/30 before queue; the next reset is 05:55:39 UTC. Test submission v40 remains separate from production; production source and ZIP hashes are unchanged.

Zarzorki has now finished 0–5 with no platform faults. Contest parity retreat still lost 77–5 deaths and 3.7k–187.0k monster damage; Ambush and Rows were no-contact farming losses; Elkring lost 198 collected gems before banking; Fragment's specialized draft lost 204–1,048. The campaign is 2 wins/155 matches, maximum streak 1, current streak 0/10. Review the full table and raw summaries in `analysis/live-top50-match-review-20261018.md`. No production changes: source SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; ZIP SHA-256 `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

The next group [`bfadbe71-52dd-41fc-9d3f-3fda1e00e13d`](https://2026a.battlecode.co.uk/game/match-groups/bfadbe71-52dd-41fc-9d3f-3fda1e00e13d) against SilverSamurai (queue-time rank #31, previously untested) also finished 0–5. Expanse, Lanes, and Monolith were largely no-contact farm losses; Packs and Swirl included severe combat losses. All maps had lower monster damage and earned gold, with zero platform faults. The campaign is now 2 wins/160 matches, maximum streak 1, current streak 0/10. Raw data and exact metrics are in the live review. Continue top-50 tests after checking quota and current ladder; no production source or ZIP changes.

The rank-35 group [`a40b7063-19c9-47f9-af57-a7420f12bd3f`](https://2026a.battlecode.co.uk/game/match-groups/a40b7063-19c9-47f9-af57-a7420f12bd3f) against conqueror_of_openai also finished 0–5 with zero platform faults. Monster damage was lower across all five maps. Corners was the closest result: 666/1,014 gems, 5/4 deaths, and 4/4 kills; Pilgrimage banked every gem collected but had 27.2k/78.7k monster damage. The campaign is 2 wins/165 matches, max streak 1, current streak 0/10. Full table and raw summaries are in the live review.
 
### Current continuation — three more top-50 groups reviewed

The user is signed in and authorized live unranked testing. The supplied old group link resolves to the 17 Oct FRChronic set and remains 0–5. Current test build is v40-likely; exact server version is omitted from match metadata.

New groups: hello (#26), https://2026a.battlecode.co.uk/game/match-groups/f99f5297-0fb7-41b5-a255-c1a523b8875f, 0–5; Ad Astra (#28), https://2026a.battlecode.co.uk/game/match-groups/6c43fd4a-7925-4eb6-be94-04d82d790b37, 1–4; 剑桥夜爬者 (#27), https://2026a.battlecode.co.uk/game/match-groups/cf11e290-56c3-43a1-b170-721b79739d79, 0–5. Total campaign is 3/180 live top-50 maps, max consecutive streak 1, current streak 0/10. Latest scores, observed deaths, and replay archives are documented in analysis/live-top50-match-review-20261018.md.

Local candidate #219 forced a generic early farm split on Expanse/Lanes/Rows; it scored 22/24 versus fresh v40 at 23/24 and had slightly lower average gems per map, so it is rejected and was never uploaded. New live evidence separates the problems: Contest is an early survival collapse (67–121 observed deaths, first deaths r31–35); Expanse/Lanes can lose on farm pace with only 2–3 observed deaths. Production bots/tungtungsahur/src/bot.cpp and submissions/tungtungsahur.zip remain unchanged (previous hashes: source 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5, ZIP 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D).

The quota query most recently reported 14/30 used and reset at 06:11:31 UTC. Check quota and ladder before the next live group. Keep building isolated candidates, compare them against a fresh v40 control, and do not update production until the agreed 10 consecutive top-50 live wins are achieved.
 
### Latest update — rank-35 and rank-36 completed

Rank-35 Trzy Kwaterki group 43b3cc32-aefa-4852-938c-1bc1c02e4004 finished 0–5. Rank-36 glyph-name team group dabc9ca4-b6f6-432c-b9da-2ff3782a2311 also finished 0–5. Captured replay score/death evidence is in analysis/live-top50-match-review-20261018.md and the bundles are under matches/live/. Current cumulative campaign: 3/190 top-50 live maps, max consecutive streak 1, current streak 0/10. Exact server versions are not exposed, but both groups followed the v40 upload.

Local candidates #220 (Monster Strength before Focus for Stellar on Expanse), #221 (safe early farm split), and #222 (stronger Contest retreat) all lost their paired comparison to v40; keep them unuploaded. #221's first recursive helper run is invalid and excluded; the corrected run is 21/24 vs 23/24. Candidate #219 is also rejected. Production source/ZIP remain unchanged with prior hashes documented above.

New evidence keeps showing farm-score gaps on low-death maps, plus a distinct early combat collapse on Contest. One strategic mismatch needs attention before more promotion attempts: the current draft lineup still includes Stellar, Cassi & Issac, and Varg, while the user's fixed test roster is Ryth, Vendetta, Tavi, Willow, Prism (3 picks Tank/Fighter/Marksman; add Support for 4; all five for 5). Evaluate a candidate lineup and update the carry/phase assumptions in an isolated test source before any production update. The next tests must remain paired against a fresh v40 control. Check ladder and quota before creating another live group.

### Follow-up — rank #37/#38 and user-roster candidate

The Stubborn Gold Clusters rank-37 group [`d9280c23-6ca6-4ed4-909b-efffbc129de7`](https://2026a.battlecode.co.uk/game/match-groups/d9280c23-6ca6-4ed4-909b-efffbc129de7) finished 0–5. The user-supplied group [`4cf7ad87-2c52-452e-a9a3-59787c302e67`](https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67) is the older 17 Oct FRChronic 0–5 set; its replay review and five downloaded bundles are in `analysis/platform-match-review-4cf7ad87.md` and `matches/live/4cf7ad87-2c52-452e-a9a3-59787c302e67/`.

After the user confirmed sign-in, the 2.2.5 CLI successfully read the ladder and created a fresh unranked group against Valenki (#38), [`e67a83d6-499e-4ab2-bb85-30b776ae3fff`](https://2026a.battlecode.co.uk/game/match-groups/e67a83d6-499e-4ab2-bb85-30b776ae3fff). It finished 0–5 with zero bot faults. Expanse and Rows were clean farm-rate losses (36.96k/72.85k and 41.39k/72.90k monster damage despite 2 and 1 HC deaths); Lanes and Fragment added combat and gem-loss deficits; Contest collected 0, died 45 times, and dealt 26.62k/171.88k monster damage. Full metrics and replay artifacts are in `analysis/live-top50-match-review-20261018.md` and `matches/live/e67a83d6-499e-4ab2-bb85-30b776ae3fff/`.

Candidate #223 implements the user's fixed roster but scored 28/40 locally against v40's 39/40, and produced fewer gems on every screened map. It remains isolated and was not used in the Valenki live group. The live current-submission draft still uses the old character set. Campaign total is now 3 wins/200 top-50 matches, max consecutive streak 1, current 0/10. Current source/ZIP hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Quota after the Valenki group: 16/30 used; reset at 06:23:42 UTC. Continue with an untested top-50 team and inspect each group before queuing another.

The next live group against queue-time rank-39 EvilMangohh, [`ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b`](https://2026a.battlecode.co.uk/game/match-groups/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b), also finished 0–5 with no bot faults. Stampede, Ambush, and Pilgrimage were low-farm-output losses despite limited deaths; Swirl and Packs had large combat collapses. Swirl's first deaths were Ryth r22, Stellar r36, and Cassi/Issac r38, against an enemy Cassi & Issac / Stellar / Ryth / Ren composition that bypasses the current narrow Swirl counterdraft. Exact map table and replays are in `analysis/live-top50-match-review-20261018.md` and `matches/live/ac0d61a8-8f84-4ecd-bbbe-88cd8e61319b/`. Campaign: 3/205 top-50 maps, max streak 1, current 0/10. Quota is 15/30, ready; reset at 06:36:15 UTC. Next make a local Swirl counterdraft test for that observed composition and continue reviewing against fresh top-50 teams.

### Local follow-ups #224–226

The Swirl counterdraft extension #224 tied v40 at 8/14 and reduced gems against `opp-swirl-meta-core`; reject. Fixed-roster equipment #225 tied #223 at 28/40. #226 (Vendetta buys Monster Strength, Power Strength, Power Health, then Power Strength) reached 30/40 vs #223's 28/40 on the 40-game fixed-roster screen, with one more Lanes and Rows win but slightly lower average gems (869 vs 871). It remains well below v40's 39/40 and is not uploaded. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain untouched. Detailed run IDs and results are in `bots/tungtungsahur/PLAN.md` and `analysis/live-top50-match-review-20261018.md`.

### Fixed-roster live validation — v41 and v42

The fixed-roster candidate was uploaded separately as test submission v41 and tested against queue-time rank-46 天使: group [`112d14b4-4b01-4ef0-b1fd-011dd07c8f6b`](https://2026a.battlecode.co.uk/game/match-groups/112d14b4-4b01-4ef0-b1fd-011dd07c8f6b), 0–5. Drafts matched Ryth / Vendetta / Tavi, adding Willow on four-pick maps and Prism for five-pick maps. 天使 drafted Cassi & Issac every time, creating a one-body deficit on all five maps. Expanse and Rows were low-death farm losses; Contest had 71 deaths to 3 and 0 submitted gems; Fragment had 11 deaths, 0 kills, and only 168 deposited. Full data and replay files: `analysis/live-top50-match-review-20261018.md`, `matches/live/112d14b4-4b01-4ef0-b1fd-011dd07c8f6b/`.

Candidate #227 adds urgent Willow heal priority and tied #226's 30/40 local screen. It was uploaded separately as v42. Its OneTap (#47) group [`83c42928-b082-4ca7-a423-aadb3ce617ae`](https://2026a.battlecode.co.uk/game/match-groups/83c42928-b082-4ca7-a423-aadb3ce617ae) finished 0–5 with no bot faults. Expanse and Rows were low-death farm-rate losses (24.8k/69.2k and 28.4k/68.9k monster damage); Contest and Fragment had severe combat gaps. The top-50 campaign is now 3/215, maximum streak 1, current streak 0/10. Full stats and replays are documented in `analysis/live-top50-match-review-20261018.md` and `matches/live/83c42928-b082-4ca7-a423-aadb3ce617ae/`. #228 (Issac mixed Strength/Health queue, 124/136) and #229 (Stellar Durability Health second, 113/136) both lost to fresh v40 at 125/136; reject. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged.

## Latest continuation — Contest review and next candidate (18 Oct 2026)

The user re-sent [FRChronic group 4cf7ad87-2c52-452e-a9a3-59787c302e67](https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67). The authenticated CLI confirms it is the same five-map 0–5 result from 17 Oct against FRChronic (rank 58 at the time); it does not add a top-50 match.

The latest top-50 group is [cfe10790-872f-4df1-9664-863139501d2d](https://2026a.battlecode.co.uk/game/match-groups/cfe10790-872f-4df1-9664-863139501d2d) against queue-time rank-47 E=mc²+AI³, following the separate v43 test upload. It finished 0–5 with zero platform faults. Map stats and replay evidence are in `analysis/live-top50-match-review-20261018.md` and `matches/live/cfe10790-872f-4df1-9664-863139501d2d/`. Contest had no gems collected or submitted (25 deaths, 10 kills, 50.8k monster damage); Expanse, Rows, and Fragment were low-farm losses with few or no kills, while Lanes banked all 466 collected gems but still lost on output. The tracked top-50 campaign is now **3 wins in 220 maps**, maximum consecutive streak 1, current streak **0/10**.

Contest's map dump shows only Monolith camps yield gems: two 200-gem groups; every other camp is gold-only. In the v43 Contest replay we repeatedly cleared gold-only groups #3/#4/#2 and never cleared either Monolith. The current Contest heuristic adds gold value to camp selection, discounts Monolith value to 20%, and blocks camps stronger than 100 until late; the opponent cleared Monolith #0 at round 387 and #1 at round 675, then banked its first 200 at round 431. This is the concrete objective-selection failure. Aggressive candidate #234 (unban strong camps and remove the discount) and staged #239 both regressed local Contest results; do not reuse those builds. Candidate work should keep the full team together for a safer Monolith attempt rather than split the fighter onto a gold-only camp.

Candidates #230–239 were local-only; none should be promoted. #230 (Tavi Monster Strength first) scored 28/40 vs #227 at 30/40; #231 (allow safe Tavi shopping trips) tied at 30/40; #232 (Vendetta wolf farm on every map) scored 28/40 vs 30/40; #233 (Contest-only Vendetta split) scored 31/40 vs 30/40 on the short screen and 33/40 vs 32/40 on the full Contest pool, but failed live 0–5; #234 immediate Contest Monolith priority scored 18/40; #235 late-only Monolith value change tied at 32/40 with no opponent flips; #236/#237 Contest draft substitutions scored 29/40 and 28/40 vs 32/40; #238 broad C&I draft scored 26/40 vs 30/40; #239 staged late Contest objective scored 22/40. All remain isolated.

Production source and submission ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## v44-likely test — WHIM, queue-time rank 50 (18 Oct 2026)

Candidate #245 was uploaded separately as test submission v44. Group [`a5faf63f-bd4e-400c-8eaa-8da44f2d77c3`](https://2026a.battlecode.co.uk/game/match-groups/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3) against WHIM (rank 50 at queue time) finished 0–5. The API omits exact submission versions, but it was queued immediately after the v44 upload; call it v44-likely. All five matches reported zero bot faults. Replays and raw summaries are under `matches/live/a5faf63f-bd4e-400c-8eaa-8da44f2d77c3/`.

| Map | Rounds | Collected/submitted HC / opponent | Deaths HC / opponent | Kills HC / opponent | Monster damage HC / opponent | Gold HC / opponent | Finding |
|---|---:|---:|---:|---:|---:|---:|---|
| Contest | 1,502 | 0/0 / 1,000/1,000 | 64/6 | 4/58 | 12.4k/230.3k | 445/14,060 | Immediate camp attrition; opponent owned both Monolith routes. |
| Expanse | 694 | 548/406 / 1,092/1,070 | 5/2 | 1/3 | 28.0k/63.8k | 1,860/3,930 | Banked all but 142 collected gems; farm and fight deficit. |
| Rows | 448 | 528/462 / 1,056/1,023 | 0/0 | 0/0 | 35.5k/74.8k | 2,160/4,740 | Pure farm-rate loss. |
| Lanes | 445 | 336/278 / 1,056/1,012 | 8/0 | 0/7 | 24.8k/62.4k | 1,400/4,560 | Fight loss and low farm output. |
| Fragment | 677 | 212/212 / 1,070/1,026 | 18/7 | 4/18 | 13.9k/79.3k | 1,075/6,025 | Major combat and farm gap. |

Contest replay: our first death was Ryth at r34 to a camp; Willow died at r54, Vendetta at r68, and Prism at r71. The team had not reached the round-450 switch, so staging the Monolith attempt did not protect the opening. WHIM drafted Cassi & Issac / Stellar / Ren / Varg / Ryth; its multi-body composition repeatedly cleared Monoliths, while we produced no gems. Overall this candidate did not transfer its local result to a top-50 opponent.

Local comparison: #245 scored 31/40 on the full Contest proxy pool vs #233 at 33/40; average submitted gems rose from 645 to 820. On the four-proxy five-map screen #245 scored 29/40 vs #233 at 31/40 and averaged about 924 vs 879 gems. Candidate #246 reached 32/40 on Contest but 28/40 on the integrated screen. Neither is a live-win improvement. #240/#241 scored 10/40, #242 19/40, #243 25/40, and #244 27/40 on the Contest pool. Reject all for further live promotion.

The live campaign is now **3 wins in 225 top-50 maps**, maximum streak 1, current streak **0/10**. The gem gain from the later Monolith switch did not transfer against WHIM. Next work should return to the stronger meta draft and isolate Contest opening survival and sustained camp damage. Production source and ZIP remain unchanged.


## v45-likely live test — WHIM (rank 47, 18 Oct 2026)

Candidate #248 re-used the older meta bot as a control. It won 40/40 local Contest proxy games and 197/200 across Contest, Expanse, Rows, Lanes, and Fragment, but that strength did not transfer to WHIM: submission v45-likely group [`c559fb26-1c62-44cf-b7ea-32116ca9acdb`](https://2026a.battlecode.co.uk/game/match-groups/c559fb26-1c62-44cf-b7ea-32116ca9acdb) finished 0–5. The API omits exact source versions; the match group was queued immediately after v45 upload. No bot faults occurred. WHIM drafted C&I / Stellar / Ren / Varg / Ryth on every map. Full summaries, scout logs, and replays: `matches/live/c559fb26-1c62-44cf-b7ea-32116ca9acdb/`.

| Map | Collected / banked HC–WHIM | Deaths | Kills | Monster damage HC–WHIM | Gold HC–WHIM |
|---|---:|---:|---:|---:|---:|
| Contest | 400 / 0 vs 1,200 / 1,000 | 98–28 | 19–79 | 12.6k–256.9k | 2,020–16,140 |
| Expanse | 628 / 508 vs 1,076 / 1,018 | 8–1 | 1–3 | 38.1k–65.8k | 2,290–3,980 |
| Rows | 660 / 616 vs 1,122 / 1,056 | 2–0 | 0–2 | 43.4k–76.9k | 2,805–5,110 |
| Lanes | 452 / 452 vs 1,044 / 1,000 | 12–3 | 0–8 | 35.4k–69.3k | 1,900–4,760 |
| Fragment | 270 / 226 vs 1,136 / 1,034 | 14–2 | 2–14 | 22.8k–75.9k | 1,225–5,950 |

Contest replay evidence: Ryth died first at round 30 to Stellar in the central skirmish. Our team later collected 400 gems but lost all before banking; early fighting snowballed into 98 deaths and far less camp damage. Across all maps, camp damage and earned gold were about half of WHIM's. Isolated draft-only local tests of the WHIM lineup scored 36/40 (#249), adding only Varg scored 36/40 (#250), and adding only Ren scored 37/40 (#251), each below the unchanged #248 control at 40/40 on Contest. Combined with immediate Monolith access (#247, 21/40), these are rejected for promotion. The isolated Contest one-enemy retreat test #252 finished at 37/40 and did not beat its control.

The campaign is now **3 top-50 map wins / 230 maps**, maximum win streak 1, current streak **0/10**. The earlier user-sent FRChronic link is still the already-reviewed 17 Oct rank-58 set, not a new top-50 result. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged.


### Additional local retreat tests after v45

#252 applied the one-enemy retreat margin to the off-roster Ren draft and finished 37/40 on Contest, tying #251 at 37/40 with a different set of losses; it did not establish an improvement. #253 applied the same Contest-only retreat margin to the user's fixed-roster v44-derived bot and scored 30/40, below its #245 control at 31/40. Reject both. The WHIM result remains the only new live group this continuation; campaign stays at 3/230, current streak 0/10.


### Further local screens

#254 applied WHIM's map-size draft order across Contest/Expanse/Rows/Lanes/Fragment without its aggressive objective changes and scored 188/200 vs #248's 197/200; reject. #255 moved Ryth to Durability Health before Jungle Health and Power Health, scoring 29/40 Contest vs #245's 31/40; reject. Submission v46 (#233) lost 0–5 to then-rank-50 Please in group `908bea80-655f-45f9-938f-305b924d97df`.


## v46 fixed-roster and v47 counterdraft tests — Please (rank 50)

The current fixed roster (#233, uploaded as v46; bundle SHA-256 `C4672FEAD1B7389E2EBA3CE543CEE3300997370274D6FEC44D4BD3437D9E4251`) lost 0–5 against Please in group [`908bea80-655f-45f9-938f-305b924d97df`](https://2026a.battlecode.co.uk/game/match-groups/908bea80-655f-45f9-938f-305b924d97df). Please drafted C&I on every map, adding a second body; no bot faults occurred. Contest reached 2,000 rounds with no gems banked by either side; HC had 79 deaths / 8 kills / 7.2k monster damage vs Please's 11 / 79 / 183.8k. Expanse and Rows were clean but low-damage farming losses.

The map-size counterdraft (#254, uploaded as v47; bundle SHA-256 `FFCBEE0EFBFDCA431C8D4F29D4A591E5FC4D5A1321313CAFCF3D5E9265283380`) copied Please/WHIM's C&I / Stellar / Ren / Varg / Ryth draft ordering. It scored **1–4**, winning Fragment, in group [`90e4f06e-29ac-4415-99ed-330d0fcc47ba`](https://2026a.battlecode.co.uk/game/match-groups/90e4f06e-29ac-4415-99ed-330d0fcc47ba), with zero bot faults. On Fragment we banked 1,014 vs 842 gems, dealt 74.7k vs 63.2k monster damage, and killed 30 vs 23. Contest still collapsed (107 deaths, 4 kills, 22.0k monster damage vs 7 / 71 / 177.5k); Expanse, Rows, and Lanes lost to farm throughput.

Local full proxy screen for #254 was 188/200 vs unchanged #248 at 197/200; its first live win is isolated to this matchup/map result. Candidate #256 added a Contest-only one-enemy retreat to #254 and scored 185/200 vs #254 at 188/200; reject. The top-50 campaign stands at **4 wins / 240 maps**, max streak 1, current streak **1/10**. Full replay and scout folders: `matches/live/908bea80-655f-45f9-938f-305b924d97df/` and `matches/live/90e4f06e-29ac-4415-99ed-330d0fcc47ba/`.


### Candidate #256 local follow-up

The exact map-size counterdraft with a Contest-only one-enemy retreat scored 185/200 on the five-map local pool, below #254 at 188/200. Reject the retreat change; retain #254 as the reference while testing item queues.


## v48 itemization follow-up — Please (rank 50)

Candidate #257 retained v47's counterdraft and changed fighter/farmer/Issac/Varg queues to Power Strength, then Durability Health, then Power Strength; it lost 0–5 in group [`25164105-a829-499a-9c3a-1c6da287111f`](https://2026a.battlecode.co.uk/game/match-groups/25164105-a829-499a-9c3a-1c6da287111f), with zero bot faults. It also lost Fragment, reversing v47's one win: 284 gems banked to Please's 1,020, 28 deaths to 8, and 6 kills to 20. Contest damage dropped from 22.0k (v47) to 8.5k; Lanes fell from 55.4k to 43.7k. The defensive second tier delays too much useful damage on our slower economy. Campaign returns to **4 wins / 245 maps**, current streak **0/10**, max streak 1. Next isolate pure Power Strength without the secondary Durability tier. Replay data: `matches/live/25164105-a829-499a-9c3a-1c6da287111f/`.


## v49 counterdraft vs Memory? (rank 47)

v49 re-uploaded the exact v47 source/bundle (same SHA-256 `FFCBEE0EFBFDCA431C8D4F29D4A591E5FC4D5A1321313CAFCF3D5E9265283380`) and lost 0–5 to Memory? in group [`0ab66a47-d3d9-4f88-92ad-5854b979e29e`](https://2026a.battlecode.co.uk/game/match-groups/0ab66a47-d3d9-4f88-92ad-5854b979e29e), with zero bot faults. Memory's Contest draft used Varg / Stellar / Ren / Ryth / Tavi, no linked C&I pair; it killed 102 of our units while losing 2. We banked no gems on Contest. Expanse, Rows, and Lanes were no-contact or low-death farm-rate losses; Fragment banked 433 vs 1,026 gems. Full replay and summary files: `matches/live/0ab66a47-d3d9-4f88-92ad-5854b979e29e/`.

Candidate #258's pure Power Strength queue scored 182/200 locally, below #254 at 188/200; reject. Campaign remains **4 wins / 250 maps**, maximum streak 1, current streak **0/10**. A Contest-only five-single-body draft test (#260) is running locally to isolate the linked-C&I matchup.


### Candidate #260 local result

The single-body Contest draft (Varg / Stellar / Ren / Ryth / Tavi) scored 37/40, one win better than the C&I / Stellar / Ren / Varg / Ryth Contest draft at 36/40. It was uploaded as v50 and lost 0–5 to Memory? in group `3cbf32fc-50b9-4021-a59a-f06ed40fdfd9`. In Contest, both sides drafted the same five champions; HC suffered 102 deaths / 6 kills and 5.6k monster damage vs Memory?'s 6 / 102 and 99.4k. Campaign at v50 completion: 4 wins / 255 maps.


## Top-50 continuation: rank 1 and rank 2

Candidate v50 lost 0–5 to current rank 1 Intercontinental Fish in group [`39ffefa6-4fc3-447f-b6f2-00779d0c1616`](https://2026a.battlecode.co.uk/game/match-groups/39ffefa6-4fc3-447f-b6f2-00779d0c1616). Main issue: farming throughput. On low-contact Expanse, HC banked 582 vs 1,016 gems with zero deaths but cleared 7 camps / dealt 33.0k monster damage / earned 1,710 gold, versus Fish's 46 / 74.7k / 4,850. Contest was a combat collapse: 0 gems banked, 55 deaths / 1 kill, and 8 camps cleared vs Fish's 3 / 55 and 81 camps.

V51 (#261) tried withholding early attacks and holding Ryth still on Contest. It also lost 0–5 to Intercontinental Fish in group [`dc38a306-c22c-416f-899a-a6d1eaabc880`](https://2026a.battlecode.co.uk/game/match-groups/dc38a306-c22c-416f-899a-a6d1eaabc880). The Contest opening fell from 8 to 2 camp clears and damage fell from 8.0k to 6.3k; deaths fell slightly from 55 to 50, but Fish still killed every unit and banked 1,000. Reject the stationary tank opening.

V52 (#264) changed only Expanse's third draft pick from Ren to the farm specialist Varg. The live group [`d38357a2-8edb-4aa4-b6bf-5450b985c1cb`](https://2026a.battlecode.co.uk/game/match-groups/d38357a2-8edb-4aa4-b6bf-5450b985c1cb) still lost 0–5. On Expanse, the one replay improved from 7 to 17 camp clears, 33.0k to 35.4k monster damage and 1,710 to 2,060 gold, while banking 584 vs 1,016; Fish still had 46 camp clears and 74.7k damage. Treat this as a promising isolated draft adjustment, not a demonstrated win.

V52 also lost 0–5 to current rank 2 Mite, group [`729a4de9-1426-4694-94c6-d10335409c67`](https://2026a.battlecode.co.uk/game/match-groups/729a4de9-1426-4694-94c6-d10335409c67). Mite mirrored our Contest lineup, then won through much higher camp output: 128 clears, 191.2k monster damage and 22,723 gold vs HC's 1, 2.3k and 105; HC died 116 times and scored no kills. Across the campaign there are now **4 wins / 275 top-50 maps**, maximum streak 1, current streak **0/10**. Production source and ZIP remain unchanged. Raw summaries and replay bundles are in the corresponding `matches/live/<group-id>/` folders.

## Current continuation — fuel diagnosis and test submission v57 (18 Oct 2026)

Since the previous note, three further top-50 groups were completed, all 0–5:

- Mite, rank 2, v54-likely: [`4b8234a2-d733-4c51-9afd-36f34083cca9`](https://2026a.battlecode.co.uk/game/match-groups/4b8234a2-d733-4c51-9afd-36f34083cca9).
- Intercontinental Fish, rank 1, v55-likely: [`cec1cd96-aa83-43ca-bd49-44a419934c15`](https://2026a.battlecode.co.uk/game/match-groups/cec1cd96-aa83-43ca-bd49-44a419934c15).
- Nyxius, rank 3, v55-likely: [`498ef0e4-dd7c-465e-bccc-263ca9c00c08`](https://2026a.battlecode.co.uk/game/match-groups/498ef0e4-dd7c-465e-bccc-263ca9c00c08).
- procless, rank 4, v56-likely: [`d0be490a-e1f3-4fca-a5ee-7473d29073db`](https://2026a.battlecode.co.uk/game/match-groups/d0be490a-e1f3-4fca-a5ee-7473d29073db).

The top-50 campaign is **4 wins / 305 maps**, maximum streak 1, current streak **0/10**. Match detail is in `analysis/live-top50-match-review-20261018.md`; replay data is under the matching `matches/live/<group-id>/` folders. The persistent low-contact farm gap remains: open-map monster damage was generally around half the leading opponents' output, while Contest and Fragment also showed combat collapses.

Official replay events exposed `fuelExhausted` on the bot despite `botFaults: 0`. A local c275 trace showed the camp-ranking path as the opening-turn hotspot: maps contained 24 camp groups on Expanse and 42 on Lanes, and each group was repeatedly checked for whether it was deep in enemy territory. A candidate cached exact Chebyshev distances for rectangular spawn regions and moved that expensive check after cheap camp scoring. Replays and notes are in `analysis/live-top50-match-review-20261018.md` and `analysis/maps.md`.

Candidate c276 retains the original spawn bitboard coordinates. It scored **30/30** across five maps against the local Faisal-bot, opp-fai-mirror, and opp-tts-v5 proxies (10/10 each); it scored 5/10 against a same-source c272 mirror. It is a test candidate, not a measured top-50 improvement. The authenticated CLI uploaded it as separate **test submission v57**. The user is creating a fresh unranked group; use v57 if available and add that group link before queuing further matches. The quota query showed 10/30 used after reset.

Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged; hashes are `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

### Full-map local comparison after v57 upload

The v57 candidate c276 scored 80/102 on all 17 official maps against Faisal-bot, opp-fai-mirror, and opp-tts-v5. The c272 control scored 82/102 on the same pool. c276 improved one game against Faisal-bot and one against opp-fai-mirror, but lost two additional games against opp-tts-v5; this is not a broad local improvement. Experimental c277 replaced the exact nearest-spawn calculation with a representative spawn and also scored 80/102; reject c277 as less faithful with no gain. Keep v57 only for the user's pending official evaluation. Production remains unchanged.

### v57-likely group queued against rank 5

After local screening, an additional authorized unranked group was queued using the latest upload, likely v57, against current rank-5 `new team(4)`. Group [`79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f`](https://2026a.battlecode.co.uk/game/match-groups/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f) covers Contest, Expanse, Rows, Lanes, and Fragment. All five matches were queued at the last check; no results are counted yet. Campaign remains 4/305 completed maps, current streak 0/10. Download/review as soon as `match-groups show` reports completion, then add the outcome before queueing another group.


## Latest continuation — v57-likely result, c279 screen (18 Oct 2026)

This section supersedes the earlier note that group `79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f` was still queued. It finished 0–5 vs rank-5 `new team(4)`. Since it was queued immediately after uploading v57, the source attribution is v57-likely; the group API did not expose the pinned version. Replays and summaries are under `matches/live/79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f/`.

The central losses on Expanse, Rows, and Lanes were farming/economy output despite matched body counts: monster damage was 30.850k/44.550k/32.663k vs 62.450k/66.924k/63.745k, submitted gems 398/660/444 vs 1,014/990/1,002. Contest had five of our bodies vs six opponents, 69 deaths, one kill, and 2.832k monster damage vs 227.668k. Fragment had four bodies vs three but still 22 deaths / one kill and 248 vs 1,004 submitted gems.

The raw `fuelExhausted` count equaled the champion roster size on both sides, every map, across the v55, v56, and v57-likely groups; `botFaults` was zero. It is not a c276-specific signal and is no longer the working cause of the losses.

Candidate c279 is a draft-only copy of c276. It mirrors the opponent's exposed picks on Contest, Rows, Lanes, and Fragment. Local results: 28/30 vs Faisal-bot, opp-fai-mirror, and opp-tts-v5 on those five maps (the two losses were Lanes vs opp-fai-mirror); c279 beat c276 6/10 in a direct head-to-head on the same maps, with average submitted gems 849 vs 761. Mixed proxy results; keep c279 isolated until an official group provides evidence. No new group was queued after v57; the user said they would create one.

Campaign: **4 wins / 310 top-50 maps**, max streak 1, current streak **0/10**. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.


## Test versions v58/v59 and wider screen (18 Oct 2026)

The user authorized separate test uploads and said they would create the next fresh group; no group was queued after `79b3d5c5-6fe4-4264-a8ec-ca8f3dc9776f`.

- c279, draft-only mirror of the rank-5 lineup on Contest / Rows / Lanes / Fragment, uploaded as **v58**. It scored 28/30 vs three local proxies on the five-map screen and beat c276 6/10 directly (849 vs 761 average submitted gems).
- c280 changed Issac to a fighter/damage build on all maps. It scored 28/30, but reduced average gems vs the c279 proxy screen; direct c280 vs c279 won 6/10, chiefly on Rows and Lanes but losing both Expanse tests. Reject globally.
- c281 keeps c279's drafts and uses the Issac fighter build only on Rows and Lanes. It scored 29/30 on the five-map proxy screen and beat c279 7/10 directly (884 vs 865 average submitted gems), with both Rows and both Lanes head-to-head tests won. It was uploaded separately as **v59**.
- Wider 17-map proxy screen: c281 79/102, vs c276 80/102 and c272 82/102 on their identical pool. No general improvement. Keep v59 as targeted experimental evidence only; ask the user to select v59 for the fresh official group if they have not created it yet.

No candidate has been promoted. The requested top-50 campaign remains 4 wins / 310 maps, max streak 1, current 0/10. Production source and bundle hashes remain unchanged.


## v60 equipment experiment (18 Oct 2026)

Current latest test upload is **v60**, built from c281/c279 draft changes. c282 changes only Stellar's purchase order on Expanse, Rows, and Lanes: Monster Focus shards first to complete the 10%-camp-damage emblem, then Power Focus. The SDK documents the camp damage bonus.

On the five-map screen c282 scored 29/30 (same as c281), and lowered each proxy opponent's average gems compared with c281. Direct c282 vs c281 won 8/10 with average submitted gems 878 vs 788; both Expanse, Rows, and Lanes side-specific games went to c282. The full 17-map screen stayed at 79/102, same as c281; c276 is 80/102 and c272 is 82/102. Treat v60 as targeted for the farm maps, not a general improvement. It has not yet been tested in an official group. The user said they would create the next group; do not queue another.

Campaign remains 4 wins / 310 maps, max streak 1, current streak 0/10. Production source and ZIP unchanged.


## Rejected item extensions (18 Oct 2026)

- c283 spread Monster Focus (same 10% camp emblem) from Stellar to Cassi and Tavi on Expanse/Rows/Lanes. It stayed 29/30 vs the proxy trio, but average opponent gems rose from about 505 with c282 to 527; direct c283 vs c282 was 4/10 (764 vs 837 average gems). Reject. Keep the Monster Focus build on Stellar only.
- c284 replaced Stellar's Monster Focus emblem with Treasure Focus (+20% gold instead of +10% camp damage, same Focus growth). It was 29/30 vs proxies but allowed about 555 average opponent gems; direct c284 vs c282 was 2/10 (764 vs 837 average gems). Reject the econ item for these maps.

v60/c282 remains the current test candidate. No top-50 result yet; user is creating the next group.


## Ryth strength-build screen rejected (18 Oct 2026)

c285 changed Ryth from health to monster/power strength on Rows and Lanes, based on the rank-5 Lanes replay. It scored 28/30 vs proxies (c282 29/30); both losses were Lanes vs opp-fai-mirror. Directly vs c282 it scored 6/10 and averaged 826 vs 853 gems; it won both Lanes games but lost once each on Contest, Expanse, Rows, and Fragment. This was not robust and is rejected. Keep v60/c282 as the latest test upload. No new unranked group was queued; the user said they would create one.


## Isolated Cassi/Tavi Monster Focus checks rejected (18 Oct 2026)

To explain c283's combined regression, c286 gave Cassi Monster Focus first (Stellar unchanged). It scored 30/30 vs the three proxies, but direct c286 vs c282 scored 4/10 and averaged 813 vs 829 gems; reject. c287 gave Tavi Monster Focus on both sides of Lanes, replacing the previous side-B strength build. It also scored 30/30 vs proxies, but direct c287 vs c282 was 5/10 and averaged 809 vs 825 gems; reject. Keep c282's Stellar-only Monster Focus order for v60.

The latest rank-5 ladder remains Intercontinental Fish, Mite, Nyxius, procless, and new team(4). The fresh official group link has not been provided yet; no extra group was queued.


## c288 Ryth monster-health equipment screen (18 Oct 2026)

c288 changes only Ryth's Rows/Lanes build from the normal tank health items to Monster Health followed by Power Health, retaining health growth while adding the monster damage emblem. It scored 30/30 against Faisal-bot, opp-fai-mirror, and opp-tts-v5 on Contest / Expanse / Rows / Lanes / Fragment; c282 scored 29/30 on the same screen, with c288 converting the Lanes side-A loss against opp-fai-mirror. On the full 17-map screen c288 scored 80/102 versus c282's 79/102; the only per-map difference was Lanes, which rose from 5/6 to 6/6. c272 remains at 82/102. A direct 10-game c288-vs-c282 comparison split 5–5, with all five side-B games won, so it does not establish a head-to-head advantage. c288's verified candidate ZIP is submissions/tungtungsahur-candidate-v61-unranked-test.zip (SHA-256 B612154823349BBE8601405B736893B7FD0636499D493A4C7B34D1C347B87878) and it was uploaded separately as v61. Keep it isolated while the user's fresh v60 group is pending the link. Main source and ZIP remain unchanged at the recorded hashes.

c289 replaced Ryth's Power Health second set with Jungle Health; c290 instead bought Monster Health twice. Both again scored 30/30 on the five-map proxy screen, but neither improved on c288's wins, and both allowed more opponent gems on each opponent aggregate. Keep c288's Monster Health + Power Health combination as the Rows/Lanes tank candidate; reject c289/c290.


## Latest top-50 review: rank 5 and Rows route finding (18 Oct 2026)

The user-supplied group [`dbdcc65c-cb2f-4b28-850b-5fa691da9e34`](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) finished 0–5 against rank-5 `new team(4)`. It was created before v62, so is v60-likely; exact pinned version is not shown. Rushbait, Rows, Lanes, Eight, and Interlock all lost. No bot faults.

The subsequent v62-likely group [`a96043a5-af65-4a93-a9af-971d34b1a879`](https://2026a.battlecode.co.uk/game/match-groups/a96043a5-af65-4a93-a9af-971d34b1a879) also lost 0–5. It mirrored the opponent's exposed lineup on all five maps, with zero platform faults. Full metrics and replay paths are in `analysis/live-top50-match-review-20261018.md`.

Rows isolates the farming weakness: no deaths or champion damage, but the team cleared 9 camps and dealt 38.854k monster damage vs 16 and 66.924k. Event data confirms both sides collected 66-gem wolf groups. Our team kept repeating groups 0 and 2; the opponent also farmed group 5. Split collection entries were multiple allies sharing a single 66-gem capture, not low-value camps. The main next experiment is multi-route assignment / route-choice instrumentation, not more global item changes.

Local Rows candidates c296 (Cassi Monster Focus), c297 (no current-target stick bonus), and c298 (allow healthy Varg to solo a wolf pack) were rejected. Each scored 7/8 in a screen including a c291 head-to-head and three local proxies; c291 itself swept all six proxy games. c296 tied c291's full-pool 82/102 and lowered average Rows gems against each proxy. None was uploaded.

Instrumented c299 confirms Ryth/Varg repeatedly select Rows group 4 but do not clear it; a round-250 sample showed Ryth stationary at (38,9). c300 extended the 12-turn target-stall recovery already used on Ambush, but it did not change gem output or improve the 7/8 Rows screen. The trace shows where to investigate, but not yet why the camp is not cleared. Local-only; not uploaded.

Additional isolates: c299 observed three visible group-4 wolves at r70 and two by r90, but no group clear. c301 skipping group4 regressed to 5/8 (4/6 proxies), so do not disable the route. c302's stronger damaged-pack stickiness tied c291's 6/6 proxy wins and gem output. c303's Rows area-target optimization fell to 5/8 and lost both c291 head-to-head games. All are rejected and remain unuploaded. Next diagnose why the pack is only partly damaged and left.

Campaign: **4 wins / 320 top-50 maps**, max streak 1, current streak **0/10**. Current test upload remains v62; local c296–c298 are not uploaded. Production source SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; production ZIP SHA-256 `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Keep production untouched until 10 consecutive top-50 wins.

## Current rank-1 findings and v63 live test (18 Oct 2026)

The current ladder lists Intercontinental Fish at #1. Group 8a40e9a3-af65-4a93-a9af-971d34b1a879 finished 0–5 using v62-likely; zero bot faults. Contest collapsed: 76 deaths / 0 kills / 6.3k monster damage and 0 banked gems versus Fish's 2 deaths / 62 kills / 200.7k monster damage / 1,000 gems. Our first death was Cassi at round 41 and the rest of our six bodies fell by round 54. Ambush, Corners, and Expanse were farm-rate deficits; Fragment added combat losses. Full table and scout trace are in analysis/live-top50-match-review-20261018.md.

Fish drafted Stellar / Tavi / Prism / Cassi & Issac / Ren on Contest and bought a large Focus-heavy build after our side died and fell behind on gold. A pure lineup mirror c304 went 4/8 locally and lost both c291 head-to-head games. c305 (C&I / Ryth / Stellar / Tavi / Willow) went 6/8, sweeping proxies but losing both c291 games. c306 (Varg / Ryth / Stellar / Tavi / Willow) removed the linked pair and scored 8/8 on Contest, including both c291 games; the full 17-map screen tied c291 at 82/102. Treat it as a Contest-specific live test.

c306 was uploaded separately as v63. Group 350cf6e4-a539-4b50-b612-63f2086b91d9 against Fish on Ambush, Contest, Corners, Expanse, and Fragment is queued. Poll it to completion and analyze before another submission. Current record is **4 wins / 325 top-50 maps**, max streak 1, current 0/10. Production source/ZIP remain unchanged and must stay untouched until the 10-win streak.


## Current rank-1 campaign status (18 Oct 2026, after v65)

Three groups against Intercontinental Fish have now completed 0–5, each with zero bot faults: v63-likely 350cf6e4-a539-4b50-b612-63f2086b91d9, v64-likely b3d6be46-136a-4b63-8158-8cda6e2e0443, and v65-likely 981927d5-6aae-4256-935d-3ae0202a36cc. Version attribution is based on upload timing because match-groups show omits pinned versions.

v65's Contest 3-tile opening response achieved 2 kills and 6 enemy deaths, versus 0 kills and 0 enemy deaths in v64. It still had 59 deaths, 0 banked gems, and 4 camp-clear entries versus Fish's 6 deaths, 1,000 gems, and 78 entries. Ambush / Corners / Expanse / Fragment metrics matched the prior c306 groups exactly. Full per-map metrics and replay summaries are in analysis/live-top50-match-review-20261018.md.

Local Contest candidates: c307 six-body C&I lineup 6/8, reject; c308 standard retreat threshold 8/8 Contest and 82/102 full maps, no live improvement, reject; c309 five-tile response 7/8, reject; c310 three-tile opening response 8/8 Contest and 82/102 full maps, test v65; c311 four-tile response 7/8, reject. c310's live result shows a small combat improvement but no farm win. Next inspect Expanse route selection, opening clear timing, and gold/item snowball.

Campaign is **4 wins / 340 completed top-50 maps**, max streak 1, current streak **0/10**. Main source / production ZIP remain unchanged at the recorded hashes. Continue isolated test candidates; the production source and ZIP gate remains 10 consecutive wins.

## Top-50 retest: rank-5 maps and route diagnostics (18 Oct 2026)

The user-created v60-likely group dbdcc65c-cb2f-4b28-850b-5fa691da9e34 lost 0-5 to rank-5 new team (4). The current v65-likely submission repeated the same maps in group 67012c50-6dcd-4e12-9e4a-9043c8a3a7cb and also lost 0-5. Version labels follow queue timing because group results omit pinned versions.

| Map | Banked gems A:B | Clear entries A:B | Monster damage A:B | Deaths A:B | Kills A:B |
|---|---:|---:|---:|---:|---:|
| rushbait_v2 | 300:1,020 | 19:36 | 33.316k:54.768k | 3:0 | 0:2 |
| rows | 594:1,056 | 9:16 | 38.854k:66.924k | 0:0 | 0:0 |
| lanes | 538:1,008 | 19:46 | 35.860k:67.174k | 3:0 | 0:2 |
| eight | 132:1,008 | 7:19 | 27.481k:53.971k | 19:2 | 2:11 |
| interlock | 386:1,004 | 15:32 | 30.742k:62.578k | 13:4 | 3:9 |

Rows was a pure economy loss: no champion damage, 9 versus 16 camp clears, and 2,430 versus 4,320 gold. Our side cleared groups 0 and 2; the opponent cleared mirrored groups 1, 3, and 5. The gold and gear gap follows camp throughput. On eight, the current draft still ended 19 deaths to 2 and 132:1,008 gems. Rushbait improved from the v60-likely result (212 to 300 gems and 9 to 3 deaths), but still lost decisively.

Reject local c316: 4/8 on Rows, with both games lost to c310 and both lost to c291. Logging-only c317 confirms c310 keeps the opening around Ryth's objective. Next instrument group arrival/readiness/path completion on Rows, and separately test safer engagement on eight. Keep c316/c317 local.

Rank-50 WHIM and rank-40 Super Intelligence were also 0-5 with v65-likely. Campaign: 4 wins / 360 top-50 maps, maximum streak 1, current 0/10. Production source and ZIP remain unchanged; the 10-win streak gate is unmet.

## v66-likely result

Group 05465728-a486-48f7-8439-41b56bc27724 against rank-5 new team (4) finished 0-5. The c318 Rows-only damaged-pack multiplier made no difference: all five map outcomes, submitted-gem totals, and camp-clear counts matched v65 exactly, including Rows at 594:1,056 gems and 9:16 clears. Reject c318/v66; do not promote it. Campaign: 4 wins / 365 completed top-50 maps, max streak 1, current 0/10. Production source and ZIP remain unchanged.

## v67 / c320 Rows lock retest

Group [955faf23-97fb-4f5f-b405-8944957190c7](https://2026a.battlecode.co.uk/game/match-groups/955faf23-97fb-4f5f-b405-8944957190c7) tested c320 after its v67 upload against rank-5 new team (4). It lost 0-5 with no bot faults. The Rows-only map dropped to 528:1,056 gems (9:16 camp-clear entries, 37.846k:66.924k monster damage, no deaths); c320's event log shows groups 0, 2, and 4 cleared. The v65/v66/v67 replays share the same seed and draft; v65/v66 cleared groups 0 and 2 and banked 594:1,056. Reject c320 despite a local 6/8 screen and 1,006 average gems; the paired server replay regressed.

c321 set Rows early gold weight to zero. It tied at 6/8 locally and averaged 974 gems, so reject. The other four maps in the c320 group matched v65/v66 results. Campaign: **4 wins / 370 completed top-50 maps**, maximum streak 1, current 0/10. Production remains unchanged; next work should isolate route arrival, camp readiness, and group-completion timing rather than alter item builds.

## v68–v71 follow-up groups

Groups [v68](https://2026a.battlecode.co.uk/game/match-groups/1f420eff-95d4-47cf-adf2-1181a8dfc274), [v69](https://2026a.battlecode.co.uk/game/match-groups/b9ee15a5-adc4-41a8-8912-9e82789b30d4), [v70](https://2026a.battlecode.co.uk/game/match-groups/0c22b4fb-111d-407d-bb96-e84a2f9bc336), and [v71](https://2026a.battlecode.co.uk/game/match-groups/47ff93c4-2182-4c8d-9b2a-61961476fd63) all lost 0-5 to rank-5 new team (4), with no bot faults. They share the same maps, drafts, and seeds.

The v68 low-health retreat rule did not change the eight result: 132:1,008 gems and 19:2 deaths, with the same early death events. Reject c323. v69's Cassi Monster Focus build raised Rows camp damage to 44.550k and clear entries to 11, from 38.854k and 9, but still banked 594:1,056. The extra clears happened at rounds 382 and 385, too late to turn into submitted gems. v70 changed Ryth's Rows build to Monster Strength and did not improve on v69. v71 reduced target stickiness and returned to the v65 Rows result: 594:1,056 gems and 9:16 clears. Keep the Cassi build as a Rows-only test lead, but do not promote it; reject c326/c327.

Local-only checks: c322 scored 3/8 on eight; c323 matched its control; c324/c325 scored 13/24 across Rows, Lanes, and Expanse; c326 scored 15/23 on the same maps with one failed run against c310's 15/24; c328's Varg solo-safe-camp Rows route tied the baseline at 6/8 and 974 average gems. Campaign: **4 wins / 390 completed top-50 maps**, maximum streak 1, current 0/10. Production source and ZIP are unchanged.

## Latest current-rank-5 group

The group [2c01edc0-7f92-468f-9838-0337a2d12c8f](https://2026a.battlecode.co.uk/game/match-groups/2c01edc0-7f92-468f-9838-0337a2d12c8f) against #5 Sneaky Bush Campers is 0-5, likely v71 by upload/queue timing, with no platform faults. Gems by map were 488:1,022 (rushbait_v2), 792:1,023 (rows), 546:1,016 (lanes), 366:1,032 (eight), and 464:1,020 (interlock). Rows had 13:19 camp clears with no champion combat. Eight and Interlock together had 36:2 deaths and 1:25 kills. This is distinct from the older link `dbdcc65c-...` already covered as a v60-likely loss. Campaign: **4 wins / 395 top-50 maps**, max streak 1, current 0/10. Production source and ZIP unchanged.


## Continuation state — rank-5 testing after v73 (18 Oct 2026)

The user-supplied group dbdcc65c-cb2f-4b28-850b-5fa691da9e34 is the v60-likely set already recorded above (0–5). The latest rank-5 group is b4117649-1de1-4564-b0c4-4f633cb53371, queued immediately after uploading c332 as test v73; it finished 0–5. The API does not expose pinned versions.

v73's Interlock Tavi-first draft transferred, but the team still banked 536:1,004 gems, cleared 13:33 camps, and had 18:2 deaths / 2:15 kills. Sneaky Bush Campers first cleared camps at rounds 9, 24, and 38; our first clear was round 44. Its Stellar recorded 11 kills. Rows was again a no-combat route deficit (792:1,023 gems, 13:19 clears, 0 deaths); Eight had 17:2 deaths / 1:12 kills. Full per-map telemetry and replay artifacts are in analysis/live-top50-match-review-20261018.md and matches/live/b4117649-1de1-4564-b0c4-4f633cb53371/.

c333 implemented the requested fixed three-to-five champion roster; it scored 3/30 targeted and 31/68 on the full local pool, while c327 scored 23/30 and 57/68. c334 added Vendetta's separate safe-wolf farm during the early phase; it scored 7/30 and 34/68. Both are rejected and remain local-only.

Campaign: **4 wins / 410 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Production source and submission ZIP were rehashed and remain unchanged: 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. Continue with isolated local improvements and current top-50 unranked groups; do not promote a candidate without evidence and keep the production bundle untouched until 10 consecutive wins.


## Local screens before the rank-50 result (18 Oct 2026)

Group 9de98fb4-1737-4b66-b7b4-0859bfc0096d against queue-time rank-50 Martin Shkreli's Defense Team is complete: 0–5, with no platform faults. It followed v73; c333–c338 were local-only and not uploaded.

Local rejections since c334:
- c335 Interlock Varg / Ryth / Tavi / Willow: 3/10; c327 control: 6/10.
- c336 Interlock Tavi / Cassi & Issac / Ryth / Willow: 3/10.
- c338 early Vendetta wolf camps with a health-based safety check: 8/30 across Interlock / Eight / Rows; c327: 23/30.

At this snapshot, campaign progress was 4 wins / 410 completed top-50 maps, max streak 1, current streak 0/10. The completed group brings the current count to 415 maps; production files remain untouched at the recorded hashes.

## Latest continuation state (18 Oct 2026)

The queued group [9de98fb4-1737-4b66-b7b4-0859bfc0096d](https://2026a.battlecode.co.uk/game/match-groups/9de98fb4-1737-4b66-b7b4-0859bfc0096d) is complete: v73-likely c332 lost 0-5 to queue-time rank-50 Martin Shkreli's Defense Team, with zero platform faults. Submitted gems were 254:1,052 (Interlock), 496:1,118 (Eight), 528:1,056 (Rows), 488:1,006 (Lanes), and 444:1,034 (Rushbait v2). Full telemetry is in `analysis/live-top50-match-review-20261018.md`; fresh JSON summaries are under `matches/live/9de98fb4-1737-4b66-b7b4-0859bfc0096d-*-fresh.json`.

The user re-sent the earlier group [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34). Fresh CLI metadata confirms it is the already-documented v60-likely 0-5 against `new team(4)` (rank 5 when queued; rank 6 on the current ladder). Its match summaries agree with the existing v60 table, so it adds no new maps.

Rows route experiments: c339 selected no target and matched c327; c340 selected enemy-side group 1 and scored 5/10; c341 selected own-side group 4 from round 2 and scored 8/10; c342's round-60 early-phase gate never activated; c343's midgame route scored 6/10. c327 scored 10/10 on every matching Rows proxy screen. Reject c339-c343 and keep them unuploaded. These results point away from forcing Varg onto another solo side route.

Campaign remains **4 wins / 415 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Production source and ZIP hashes remain unchanged; continue isolated local screens and unranked groups against top-50 teams. Keep production untouched until the 10-win streak is achieved.

### Rows anchor-spacing follow-up (18 Oct 2026)

c345 made the Fighter squad avoid Rows camps within 5 tiles of Ryth's current anchor. It built successfully and scored 10/10 on the five-proxy Rows screen, the same as c327. However, c345 averaged 768.9 opponent-banked gems and a 627.5-round win, versus c327's 732.6 and 614.4 rounds. Reject c345; it remains local and was not uploaded. Replay summaries are `matches/league/20261018-125734-c345/summary.json` and `matches/league/20261018-125742-c327/summary.json`. The supplied `dbdcc65c-...` link is still the previously reviewed v60-likely 0–5 group, so it does not change campaign progress: **4 wins / 415 top-50 maps**, max streak 1, current streak **0/10**. Production files and hashes remain unchanged.

### Rows camp rotation and no-Tank draft (18 Oct 2026)

The rank-50 Rows replay shows our side cleared groups 0/2 five/four times and never group 4. The opponent cleared mirrored groups 1/3/5 seven/five/five times. First clear timing was close (round 25 vs 26); sustained route coverage is the gap. c346 matched the opponent's Varg / Cassi & Issac / Tavi / Stellar draft, with Stellar leading squad A. After fixing the early Issac leader handoff, c346 scored 4/10 against c327's 10/10 Rows screen. Reject it; keep it local and do not upload. Final artifacts: `matches/league/20261018-130520-c346/`; evidence is in `analysis/live-top50-match-review-20261018.md` and `analysis/maps.md`.

Campaign remains **4 wins / 415 completed top-50 maps**, max streak 1, current streak **0/10**. The supplied `dbdcc65c-...` link is the earlier v60-likely 0–5 group. Production source and ZIP remain unchanged.

Rows follow-ups: c347 moved Varg onto Ryth's camp route after midgame and scored 5/10 vs c327's 10/10 on the same five proxies; reject. c348 replaced Ryth's Health shards with Strength shards on Rows; it tied c327 at 10/10 vs proxies but had slightly fewer gems and later wins. Direct Rows head-to-head was 5–5, with c348 winning all five side-A games and losing all five side-B games, so reject as side-dependent. One completed match's result printed, but duplicate replay-bundle naming prevented saving that replay. The health build remains in production. Details and artifact paths are in `analysis/live-top50-match-review-20261018.md` and `analysis/maps.md`.

### Latest live group: #1 Intercontinental Fish (18 Oct 2026)

Group [794748d5-1c1f-42c5-a937-9f82e1a5fb75](https://2026a.battlecode.co.uk/game/match-groups/794748d5-1c1f-42c5-a937-9f82e1a5fb75) finished 0–5, likely with v73/c332 by upload timing (the group API does not reveal pinned versions). Per-map banked gems were 110 / 176 / 528 / 510 / 278 versus Fish's 1,010 / 1,078 / 1,056 / 1,014 / 1,000 on Interlock / Eight / Rows / Lanes / Rushbait v2. Interlock first clear was round 44 vs 9; Rows had no deaths or champion damage, but only 9 vs 17 camp-clear entries. Lanes was also a clean farm deficit (23 vs 41 entries). The opponent won with both much earlier Interlock pressure and broader sustained camp coverage. Full telemetry and replay archive are under `analysis/live-top50-match-review-20261018.md` and `matches/live/794748d5-1c1f-42c5-a937-9f82e1a5fb75*`.

There were no API-reported bot faults, but captured Team-A stdout logged caught `Champion cannot act` errors twice on Interlock and four times on Eight. Keep this as an instrumentation/debug lead; it does not account for the no-combat Rows/Lanes economy gap. The user's supplied `dbdcc65c-...` URL is the older 09:18 group against new team (4), already reviewed; do not count it again.

Campaign now stands at **4 wins / 420 completed top-50 maps**, maximum streak 1, current streak **0/10**. Continue isolated candidates and authorized unranked testing. Production source and submission ZIP remain unchanged; do not promote until the live streak reaches 10 wins.

### Test v74: Fish Interlock Ren-first and follow-up isolates (18 Oct 2026)

c350 changed only Interlock's first pick to Ren and was submitted as test v74. The five-map group [9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3](https://2026a.battlecode.co.uk/game/match-groups/9ba714e8-b4e1-4480-8f8d-b4d7f4a389c3) against current #1 Intercontinental Fish finished 0–5 with no platform bot faults. Both sides picked Ren, so it did not deny Fish its pick. On Interlock, our gems improved 110→182 and first camp clear 44→43, but clear entries declined 9→7 and deaths increased 15→18; the opponent scored 1,010 gems and 14 kills. The other maps repeated the previous group exactly. Treat v74 as an unpromoted matchup experiment.

Rejected local candidates: c349 farmer turn priority 54 (4/10 vs c332, both Rows games lost); c351 50%/55% retreat thresholds on combat maps (1/6 and 680:869 gems); c352 Fish-mirror Rows draft with Ren instead of Ryth (6/10 proxies, 0/2 vs c332); c353 Rows Varg Power Strength before Monster Strength (10/10 proxy tie, slower wins and more opponent gems); c355 1.05 outmatched ratio on Interlock/Eight/Rushbait (3/6, 775:928 gems). None is promoted or uploaded. Current focus remains camp coverage/repeated clears and combat disengage instrumentation.

Campaign is **4 wins / 425 completed top-50 maps**, max streak 1, current streak **0/10**. Production source and ZIP hashes remain unchanged. Test v74 is separate from the production bundle; do not promote until the 10-win live streak is reached.

Rows follow-up c356 forced the mid-game farm split at round 35, based on Fish Varg's early item buys. It scored 9/10 against local Rows proxies but lost 0/2 head-to-head against c332, with slower wins (629 vs 614 rounds) and higher Faisal-family opponent gems (759 vs 710). Reject it; the existing shard-triggered timing remains the better local result. Latest uploaded test is v74/c350; production source and ZIP remain unchanged. Campaign remains **4 wins / 425 top-50 maps**, current streak **0/10**.

### Latest continuation: user link, fresh top-1 groups, and rejected candidates (18 Oct 2026)

The user-supplied [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34) is the old 09:18 UTC group against `new team(4)`, already counted and reviewed; do not count it again. The authenticated CLI can now queue groups directly. Fresh group [e6b3ee2b-077f-4d25-91b7-f2f5c71fce91](https://2026a.battlecode.co.uk/game/match-groups/e6b3ee2b-077f-4d25-91b7-f2f5c71fce91) used current test v74 (inferred from upload/queue timing) against current #1 Intercontinental Fish and lost 0–5 on Ambush, Expanse, Packs, Fragment, and Collision. Its replay data is in `matches/live/e6b3ee2b-077f-4d25-91b7-f2f5c71fce91*`.

Local experiments: c357 delayed a Varg-only Rows side route to round 35; it lost 0/2 direct games to c332 and scored 792:990 gems. c358 gave Issac an offensive build on Packs/Collision; it scored 11/20 proxy games versus c332's 12/20, with equal 6/8 Faisal-family wins but more opponent gems (583 vs 472). Reject both.

c359 allowed Ambush to enter mid-game at the five-shard trigger or round 100 instead of holding the shared opening to round 150. It tied c332 at 10/10 on Ambush proxies, won 52 rounds earlier on average (941 vs 993), and lowered proxy opponent gems (278 vs 330), so it was uploaded as separate test v75. The fresh [v75-likely group 7250aac0-ed63-4984-bed9-7a9fb1d685a1](https://2026a.battlecode.co.uk/game/match-groups/7250aac0-ed63-4984-bed9-7a9fb1d685a1) again lost 0–5 to Fish. Ambush submitted gems fell 582→404 and deaths rose 0→2 for one additional camp clear (6→7); the other four maps exactly repeated v74. Reject c359/v75 for live play.

The two groups add 10 completed top-50 maps: campaign **4 wins / 435 maps**, maximum streak 1, current streak **0/10**. Latest uploaded test is v75/c359; production source and ZIP remain untouched. Replay metrics and map-specific conclusions are in `analysis/live-top50-match-review-20261018.md` and `analysis/maps.md`.

### Expanse follow-ups (18 Oct 2026)

c360 moved Issac to Monster/Power Strength only on Expanse, based on the top-1 opponent's earlier strength purchases. It lost 0/2 direct games to c332 (967:952 gems) and tied the 10/10 proxy screen, but averaged 855-round wins vs c332's 836 and 656 opponent gems vs 640. Reject the gear change. c361 moved Expanse into the split phase at round 35; it also tied 10/10 proxies but averaged 857-round wins vs 836 and 954 own gems vs 976, then lost 1/2 direct games. Reject the early split. These tests reinforce that the Expanse loss needs route-level diagnosis rather than equipment or phase guesses. Latest test upload remains v75/c359; c360 and c361 were not uploaded.
### Fresh top-2 live group and follow-up screens (18 Oct 2026)

The user-supplied group link dbdcc65c-cb2f-4b28-850b-5fa691da9e34 is still the previously reviewed 09:18 UTC group against new team (4), not a fresh match. The latest uploaded test was v77, based on c363; the API does not reveal pinned versions, so attribution is by upload and queue timing.

The v76-likely group 8a811c99-40ed-46b4-b504-7cc069289079 and v77-likely group 26b836f8-650f-4b6c-9042-10121f1b7e44 against #1 Intercontinental Fish both lost 0–5. The c362 Ren role fix raised Packs from 140 to 252 submitted gems versus the earlier v74-likely sample, reduced deaths 19→14, and raised camp-clear entries 3→7. c363's Ren tank build raised Packs again to 344 gems, 11 clear entries, and 22.9k monster damage, with the same 14 deaths and zero kills. Ambush, Expanse, Fragment, and Collision replayed identically between v76 and v77.

Fresh group [e29257b6-18d9-49aa-b952-43a426e1ab2d](https://2026a.battlecode.co.uk/game/match-groups/e29257b6-18d9-49aa-b952-43a426e1ab2d) against current #2 Mite also lost 0–5, with zero API bot faults. Per-map Team A:Team B results:

| Map | Gems | Camp clears | Monster damage | Deaths | Kills |
|---|---:|---:|---:|---:|---:|
| Ambush | 356:1,024 | 7:11 | 33.6k:55.7k | 3:2 | 1:2 |
| Expanse | 540:1,116 | 16:32 | 33.5k:65.2k | 2:0 | 0:0 |
| Packs | 208:1,014 | 7:19 | 18.5k:48.5k | 13:0 | 0:10 |
| Fragment | 300:1,048 | 15:27 | 29.2k:73.2k | 14:6 | 4:13 |
| Collision | 154:1,002 | 19:36 | 26.3k:51.8k | 13:0 | 0:9 |

The Packs draft was mirrored (Cassi & Issac / Stellar / Ren). Mite's Stellar finished with 7 kills and no deaths; our Stellar had 3 deaths and about 2.1k champion damage. Our C&I pair died at rounds 52–53, before the team could convert its opening clear into sustained income. Mite's Issac used Strength equipment, while ours still bought Health gear; our Ren earned only 35 gold and bought no items in that match. The Ren tank build's gain against Fish did not transfer to Mite.

Three isolated Packs screens based on c363 did not beat its local control: c364b gave Issac Monster Strength then Power Strength (6/10 vs the same five proxies, tying c363; lost both direct games to c363); c365 applied the round-600 attack-range leash (5/10 vs c363's 6/10, and 1/2 direct); c366 reversed Issac's order to Power Strength then Monster Strength (6/10, tying c363; lost both direct games). Reject all three and keep them unuploaded.

The campaign is now **4 wins / 450 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Latest test upload remains v77/c363. Production source and submission ZIP remain unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. Continue local isolates before any new upload; the next focus is early Packs survival against Stellar and the uncontested Ambush/Expanse farm-rate gap.
### v78–v80 top-50 follow-ups (18 Oct 2026)

The user-repeated link dbdcc65c-cb2f-4b28-850b-5fa691da9e34 remains the already-reviewed 09:18 UTC 0–5 group against new team (4). Subsequent fresh groups tested separate candidates against current #2 Mite and #1 Intercontinental Fish:

- v78/c367 vs Mite, group 295d27b1-85a1-44ed-a423-77ae854b5f54: 0–5. Issac's Packs build copied Mite's Durability Strength → Jungle Strength order. Packs finished 184:1,038 gems, 5:21 clears, 17.1k:53.4k monster damage, 12:0 deaths, 0:9 kills. The other four maps repeated v77's Mite results.
- v79/c368 vs Mite, group 3b66586a-63ba-4a4f-bff3-7030e5dec3bb: 0–5. Packs finished 232:1,020, 6:20 clears, 17.8k:53.1k monster damage, 12:0 deaths, 0:9 kills. This is a small gem/survival improvement over v77's Mite Packs result (208:1,014, 7:19, 13:0 deaths, 0:10 kills), at the cost of a clear and monster damage.
- v79/c368 vs Fish, group 1980b74e-6197-4f43-8c6d-0a2a169edefe: 0–5. Packs was 256:1,008 with 10:18 clears, 21.8k:54.3k monster damage, 14:0 deaths, 0:10 kills. This did not transfer from Mite and was below v77's Fish Packs result of 344:1,028 and 11:19 clears.
- v80/c369 vs Mite, group 5e02cb8a-e151-427c-91e9-f98102325456: 0–5. Packs was 140:1,040 with 5:20 clears, 15.2k:52.3k monster damage, 13:0 deaths, 0:10 kills. The other four maps repeated the v77 Mite results.

Local Packs tests: c367's Durability/Jungle Strength Issac build tied c363 at 6/10 and went 1/2 head-to-head; c368's parity retreat rule scored 7/10 vs c363's fresh 6/10 and went 1/2 directly; c369's raw-damage target priority scored 7/10 vs c363's 6/10 and went 1/2 directly. Reject c367 and c369; c368's local gain did not transfer to Fish. v78–v80 all lost every live map and remain test-only.

Campaign is **4 wins / 470 completed top-50 maps**, maximum consecutive streak 1, current streak **0/10**. Latest test upload is v80/c369. Production source and submission ZIP remain unchanged at SHA-256 188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5 and 06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D. Continue local screening before another upload; the Packs fixes remain mixed, while Ambush and Expanse still lose mostly through camp throughput.

## v81 Expanse split live test (18 Oct 2026)

Candidate c373 was uploaded separately as v81; bundle submissions/tungtungsahur-candidate-c373-expanse-split-test.zip (SHA-256 B677E6C22BC9C1A1BC6BFDE7A91E232F50B864E3187BBD2931C382C374D15B0C), source bots/c373/src/bot.cpp (SHA-256 26177FE108D1C5E1BCC9E15AD40092FB31C146ABC25BEB16A8E5974A28C8BAFA). Expanse alone starts in mid-game routing: Cassi/Issac/Stellar share one camp; Varg farms a separate safe camp; the leader uses 0.75 gold weighting. No production files changed.

Both fresh groups lost 0–5, with zero bot faults in all ten maps:

- #2 Mite, group [d667335a-6dda-4906-afab-163abc4c1543](https://2026a.battlecode.co.uk/game/match-groups/d667335a-6dda-4906-afab-163abc4c1543): Expanse 636:1,116 gems, 20:32 camp clears, first clear r14 vs r11, 0:0 deaths. Against v77/c363, our Expanse output rose 540→636 and the first clear moved r28→r14. Other maps: Ambush 356:1,024; Packs 140:1,040; Fragment 300:1,048; Collision 154:1,002.
- #1 Intercontinental Fish, group [529e5991-2d60-46b7-970f-e634cd525c26](https://2026a.battlecode.co.uk/game/match-groups/529e5991-2d60-46b7-970f-e634cd525c26): Expanse 778:1,016 gems, 22:46 camp clears, first clear r14 vs r15, 0:0 deaths. Against the v77 sample, our Expanse output rose 584→778 and clears 17→22. Other maps: Ambush 582:1,024; Packs 92:1,012; Fragment 102:1,020; Collision 146:1,008.

The opening split transfers to both top opponents, but repeat-clear throughput remains far below theirs, so v81 is research evidence rather than a production upgrade. The other four maps retain the established farm/combat deficits. Latest campaign: **4 wins / 480 completed top-50 maps**, maximum streak 1, current **0/10**. Latest test upload is v81/c373. Production source and bundle remain unchanged at the hashes above.

## v82 Expanse Ren draft test results

c374's Issac Strength gear change on the v81 route lost 0/10 local Expanse games and banked 854–876 gems, below c373's 948 control; reject it. c375 replaced Varg with Ren as Expanse's third pick. Both fresh top-team groups lost 0–5 with zero bot faults. Expanse fell from v81's 636 to 470 gems against Mite (15:32 clears, r16 first clear, 2:0 deaths) and from 778 to 506 against Fish (17:46 clears, r16 first clear, 2:0 deaths). Other maps were unchanged. Reject c375.

c376 then split Expanse into a Cassi/Issac pair plus separate Stellar and Varg routes. It won 16/16 local games against eight controls, with 994 gems on the five same-family proxies and 969–994 against Faisal-bot, ming_bot, and starter-cpp. The full local results are in matches/league. Candidate c376 was uploaded as v83 (bundle submissions/tungtungsahur-candidate-c376-expanse-2-1-1-test.zip, SHA-256 1C207CB201B6DC14C9248735211C2170CE5B77CC50360FEB153E95677B7F3142).

v83 finished 0–5 against both top teams, with zero bot faults. Expanse reached 738:1,116 gems, 24:32 clears, first clear r14:r11 against Mite, and 796:1,016, 28:46 clears, first clear r14:r15 against Fish. Both games had zero deaths. Relative to v81, output rose by 102 gems and four clears against Mite, and 18 gems and six clears against Fish. Ambush, Packs, Fragment, and Collision matched their v81 baselines. These results validate the 2+1+1 route improvement, but Expanse still trails on repeat clearing.

Campaign is **4 wins / 500 completed top-50 maps**, maximum streak 1, current streak **0/10**. Latest test upload is v83/c376. The next local isolate is a health-gated Varg route to higher-value camps; do not promote before the live win gate. Production source and ZIP remain at the original hashes.

## Latest supplied match group: v60 vs top-5 new team(4)

The user supplied [group dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34), created with v60. It finished 0–5, with zero bot faults. Across Rushbait_v2, Rows, Lanes, Eight, and Interlock, Heavenly Court banked 2,116 gems and cleared 67 camps versus the opponent's 5,154 gems and 153 clears. Deaths were 48:12 and kills 7:29. Rows lost on farming speed despite zero deaths; Eight and Interlock caused 36 deaths combined. Prioritize clearing efficiency and safer map-specific fight/retreat behavior.

A direct v83/c376 comparison against the same #5 team and maps is running in group [bd1c7f28-ab38-464c-aa27-74c0325737d6](https://2026a.battlecode.co.uk/game/match-groups/bd1c7f28-ab38-464c-aa27-74c0325737d6). Do not count pending results yet. Live map coverage now includes ten of 17 published maps; Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, and Swirl still need top-50 matches. Campaign completed tally: **4 wins / 505 maps**, max streak 1, current 0/10. Production bot and ZIP remain unchanged.

## v83-targeted direct follow-up vs #5

Group [bd1c7f28-ab38-464c-aa27-74c0325737d6](https://2026a.battlecode.co.uk/game/match-groups/bd1c7f28-ab38-464c-aa27-74c0325737d6) finished 0–5, zero bot faults. On Rushbait_v2/Rows/Lanes/Eight/Interlock, results were 300/594/538/132/182 gems versus 1,020/1,056/1,008/1,008/1,054, with 19/9/19/7/10 camp clears and 3/0/3/19/15 deaths. The map JSON does not expose which submission version ran; it was queued immediately after v83 upload. Compared with the prior v60 group, only Rushbait_v2 clearly improved and Interlock differed sharply; drafts/seeds changed, so these samples are not paired.

Eight and Interlock remain the urgent survival targets; Rows and Lanes need farm throughput. Campaign now includes both user-provided v60 and latest-upload groups: **4 wins / 510 completed top-50 maps**, max streak 1, current 0/10. Seven of 17 official maps have no live top-50 test yet: Contest, Corners, Elkring, Monolith, Pilgrimage, Stampede, Swirl. Production files remain unchanged.
# Latest campaign status (18 Oct 2026, v88–v91)

The user re-sent the 09:18 UTC group `dbdcc65c-cb2f-4b28-850b-5fa691da9e34`; CLI confirmation shows it is the already-reviewed 0–5 set against `new team(4)`, not a new test. Four later candidates (v88–v91) were screened locally, uploaded separately, and each lost 0–5 against current #1 Intercontinental Fish. v90/c391 improved Interlock to 204 gems and a round-11 first clear; v91's mirrored lineup regressed to 88 gems and a round-28 first clear. Keep all candidates test-only. Campaign: **4 wins / 565 completed top-50 maps**, maximum streak 1, current **0/10**. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Full map metrics are in `analysis/live-top50-match-review-20261018.md`.

## Current test status (18 Oct 2026, v92–v94)

The latest user link is still that old group; it is not a fresh evaluation. v92/c395 lost 0–5 in each of three new groups versus Fish and Mite, but it extended live top-50 coverage to all 17 published maps. The v93/c397 adaptive six-body Contest draft was tested versus Mite in [group eba1da49-7ea6-4711-ac74-11972535abd3](https://2026a.battlecode.co.uk/game/match-groups/eba1da49-7ea6-4711-ac74-11972535abd3), queued immediately after upload (the pinned version is not exposed), and lost 0–5. Its Contest lineup matched Mite's six bodies, yet banked no gems and recorded 140 death events. Do not promote v92 or v93.

Candidate c399 kept Willow while adding C&I and dropping Varg, then was uploaded as test v94. Its [Mite group 528af232-c8fa-42e7-9375-240ff909d1a9](https://2026a.battlecode.co.uk/game/match-groups/528af232-c8fa-42e7-9375-240ff909d1a9) lost 0–5. Contest still banked no gems and recorded 132 death events; the opening pair Cassi/Issac died at r29. This is below v93's 140 deaths but above v92's 94 on different seeds, so it is not a proven improvement. c398, c400, and c401 also failed to show local head-to-head gains and remain unuploaded. The next Contest work should target opening movement and access to the two 200-gem Monolith camps; item logs show income and survival need fixing before item-order changes. Campaign is **4 wins / 590 completed top-50 maps**, maximum streak 1, current **0/10**. Production hashes remain `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Current continuation (18 Oct 2026, v95 result and rank-50 follow-up)

The latest supplied URL, [dbdcc65c-cb2f-4b28-850b-5fa691da9e34](https://2026a.battlecode.co.uk/game/match-groups/dbdcc65c-cb2f-4b28-850b-5fa691da9e34), is the old 0–5 group against `new team(4)` and has already been counted. Local Contest trials c402 (early Willow heal) tied its baseline; c403 (back line keeps farming) regressed. c404 mirrored Mite's Prism / Stellar / C&I / Ryth / Tavi Contest lineup, tied the local win screen at 38/40, and added 200 local gems. Submitted as test v95, its Mite group [dbffabee-68c9-4ddd-a9eb-5e59b423e846](https://2026a.battlecode.co.uk/game/match-groups/dbffabee-68c9-4ddd-a9eb-5e59b423e846) finished 0–5. Contest matched Mite's draft exactly but collapsed to 0 gems, 2:128 camp-clear entries, 141:0 deaths, and 0:117 kills; first contact was r20–21 and Ryth died at r28. Reject v95 for general use.

The follow-up group against rank-50 Bamboo Teahouse [51e941e4-5904-4c2d-bd75-87d761c2b0c3](https://2026a.battlecode.co.uk/game/match-groups/51e941e4-5904-4c2d-bd75-87d761c2b0c3) finished 0–5 with zero platform faults. It scored 0:800 gems on Contest (6:116 clears, 123:3 deaths), 0:1,020 on Swirl, 546:1,054 on Interlock, 660:1,056 on Rows, and 36:1,038 on Eight. The campaign is now **4 wins / 600 completed top-50 maps**, best streak 1, current **0/10**. v95 is rejected for general use. Production source and ZIP remain unchanged. Full details: [live match review](D:/School/University/Year2/Cambridge%20Battlecode/analysis/live-top50-match-review-20261018.md), [map notes](D:/School/University/Year2/Cambridge%20Battlecode/analysis/maps.md), and [strategy plan](D:/School/University/Year2/Cambridge%20Battlecode/bots/tungtungsahur/PLAN.md).


## Rows route diagnosis (18 Oct 2026)

The user re-sent `dbdcc65c-cb2f-4b28-850b-5fa691da9e34`; it is the already-reviewed 09:18 UTC 0-5 group against `new team(4)`, so it adds no maps. Bamboo Rows was an uncontested farm loss (660:1,056 gems, 11:17 clears, 45.544k:68.850k monster damage, no deaths). Replay capture events show our home groups 0/2/4 cleared ten times versus Bamboo's 1/3/5 sixteen times; Varg shared 66-gem captures for 22 gems while Bamboo's Varg took 66. Instrumentation shows our Varg has no eligible solo camp under the one-wolf selector and falls back to Issac's target.

Rows variants c405/c406 leader objective sync scored 4/14 and 5/14; c407 skipping Varg's capture join scored 12/14 but tied the direct c404 head-to-head 1-1. c409 allowed soloing wolf packs and scored 9/14 (7/7 side A, 2/7 side B), losing five of seven side-B games after choosing a far camp; c411 added a home-half restriction and scored 12/14 but still split 1-1 against c404. No upload is justified. Continue with a stable, side-aware Varg solo route. The campaign remains **4 wins / 600 completed top-50 maps**, maximum streak 1, current **0/10**; production source and ZIP hashes remain unchanged.


## Current campaign continuation (18 Oct 2026, test v96)

The latest user URL, `dbdcc65c-cb2f-4b28-850b-5fa691da9e34`, is the old 09:18 UTC 0-5 group against `new team(4)`, already counted. I installed the official CAMBC 2.2.5 package into `%TEMP%\cambc225-20261018\Scripts\cambc.exe`; the workspace `cambc.exe` remains 2.1.6. The authenticated 2.2.5 CLI can read the ladder, submit isolated candidates, queue unranked groups, and download raw summaries/replays. The user has already authorized unranked testing and separate test uploads.

c411's Rows home-half wolf route was uploaded as test v96 (bundle `submissions/tungtungsahur-candidate-c411-rows-home-side-wolf.zip`, SHA-256 `13BE6FF1AEE3D1FC6E2905C252A8FFDB13466D036BFF8344BD5A886A947C8BF8`). Fresh group [819e5b24-2227-4065-9eda-d49419a8568f](https://2026a.battlecode.co.uk/game/match-groups/819e5b24-2227-4065-9eda-d49419a8568f) against queue-time rank-50 umamusume finished 0-5. Exact submission pin is omitted, so call it v96-likely. Per-map results and raw summaries are in `analysis/live-top50-match-review-20261018.md` and `matches/live/819e5b24-2227-4065-9eda-d49419a8568f/`; replay archive is `matches/live/819e5b24-2227-4065-9eda-d49419a8568f.zip`.

Key findings: Rows remains an uncontested farm loss (528:1,056 gems, 11:17 clears); Lanes also has a wide throughput gap. Eight and Interlock combine low camp output with 24:6 and 15:1 deaths. Contest is the critical failure: 0:200 gems, 98:7 deaths, 7:72 kills, and the C&I pair died at r45 to enemy Ren. The raw event stream logs ten Team-A fuel-exhaustion events on Contest (six at r35-r39), plus four on Lanes and three on Eight, with zero `botFault`s. Fuel exhaustion suspends execution to the next round; profile it before assuming these are only strategy failures. c413's “early Rows” branch was inactive because Rows is Phase::mid from round 1; reject as a no-op.

Campaign: **4 wins / 605 completed top-50 maps**, max streak 1, current **0/10**. All 17 maps have live coverage. Latest test v96 is rejected for production. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. Next useful work is profiling the Contest/Lanes/Eight fuel spikes and isolating a Contest opening that preserves bodies and reaches the 200-gem camps.

## Latest continuation (18 Oct 2026, v97 and Contest carrier)

The latest user link is the already-reviewed old group; no new results came from it. c417's memoized visible-unit lists screened at 20/24 twice against c411's 17/24 and were uploaded separately as test v97. The [five-map group](https://2026a.battlecode.co.uk/game/match-groups/bab275a5-8821-4586-81e2-23b16e626e90) against queue-time rank-50 Live Love Larp finished 0-5 with no platform faults. Contest fell to 0:1,000 gems, 8:119 camp-clear entries, and 77:23 deaths. Lanes had five fuel exhaustion events on our side and four for the opponent; other maps had none.

Contest replay forensics found Issac carrying 200 Monolith gems at (24,35); enemy Tavi and Stellar were nearby by r1014, and enemy Stellar killed him at r1018 and took the gems. No ally was near to escort. The isolated c420 escort candidate scored 6/8 local proxy games versus c417's 7/8 and failed to show a direct gem advantage, so it was not uploaded. Fuel profiling suggests visibility reads and pathfinding can consume much of the 100k turn budget, but does not prove fuel exhaustion is the primary Contest failure. c416's deferral, c418's Tavi counterdraft, and c419's nearest-gold opening also lacked a reliable gain.

Campaign remains **4 wins / 610 completed top-50 maps**, maximum streak 1, current **0/10**; all 17 maps have live coverage. Production source and ZIP remain unchanged at SHA-256 `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and `06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`. See `analysis/live-top50-match-review-20261018.md`, `analysis/maps.md`, and the latest entries in `bots/tungtungsahur/PLAN.md`.

## Latest continuation (18 Oct 2026, v98 Contest escort)

c421's Contest-only threat escort screened 8/8 against four local proxy families versus a fresh c417 screen at 5/8. It was uploaded separately as test v98 (bundle SHA-256 `70FF18AFB1DF3F4ACD76CBB6E5057A977C9716C5789C7C1D31C85CE1754403ED`). The [fresh five-map group](https://2026a.battlecode.co.uk/game/match-groups/8a9a1654-7673-4da3-bbae-daaa2f5cc715) against queue-time rank-49 Please finished 0-5 without platform faults. Contest remained 0:200 gems, 85:23 deaths, 9:132 camp clears. Our Prism collected 200 at r1027; Please's Ryth took them at r1063 and banked them at r1109. The escort failed to prevent the loss. c422's “wait until the tank is hit” rule scored 1/8 locally versus c417's 5/8; do not upload it.

The user-repeated `dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is still the old 09:18 UTC 0-5 group; this does not add matches. The new group brings the campaign to **4 wins / 615 completed top-50 maps**, maximum streak 1, current **0/10**. All 17 maps have live coverage. Keep v98 test-only and production unchanged. Next, continue Contest opening/survival research and screen against stronger local controls before another upload. c417 and c421 both had local gains that failed to transfer live; c420 did not show a clear local edge.

## Latest continuation (18 Oct 2026, live pause and local Rows screens)

The user asked to pause unranked matches and continue local work autonomously. Do not create or queue new live groups until the user resumes them. Campaign state remains **4 wins / 620 maps**, best streak 1, current **0/10**. The next already-uploaded live-check candidate remains v100/c425; production source and ZIP are unchanged.

Rows local candidates c432/c433 produced byte-identical replays to c417 across six games each (monolith delay; Varg capture-join skip). Draft swaps c434/c435 replacing Ryth or Stellar with Tavi each scored 2/6 versus c417's 4/6. Reject all four and leave them local. The umamusume Rows replay shows our Varg cleared group 4 at r178/292/389 while their Varg cleared group 5 at r108/193/268/339; the next Rows experiment should instrument travel and damage time. Details are in the latest Rows follow-up in PLAN.md and analysis/maps.md.

## Latest continuation (18 Oct 2026, Contest fuel profiling)

Live unranked matches remain paused. c436/c439 local fuel traces place high costs in role execution, objective selection, scout logging, and pathfinding; some Contest turns approach the budget limit. c438 scout sampling fell one game below c425 on the 204-game strong all-map screen. c440's compute shortcut tied c425 exactly across all 204 results. Reject both as win improvements. The production bot and ZIP remain unchanged; campaign is **4 wins / 620 maps**, best streak 1, current **0/10**. v100/c425 remains the queued live-check candidate when testing resumes. Detailed measurements and run folders are in PLAN.md.

## Local Contest continuation while live matches are paused (18 Oct 2026)

The user asked to pause unranked matches and continue local work. Do not queue or create a live group until the user resumes testing. The current local candidate is c442, copied from uploaded v100/c425 with a Contest-opening limit on global burst spells. The first implementation (c441) queried extra state on every map; c442 made those reads Contest-only. The first six-proxy all-map screen scored 168/204. After moving state reads into a once-per-turn Contest-only branch, its rerun scored 168/203 with one runner error; all 191 shared non-Contest win/gem results matched c425. The first version's 204th game completed with the same win/gem result, although one Stampede game ended seven rounds later. Contest stayed 11/12 and rose from 10,200 to 11,000 gems. On the 20-opponent Contest pool, c442 scored 39/40 and 37,400 gems versus the saved c417/c425 38/40 and 36,600. This is local evidence only; c442 has not been bundled, uploaded, or tested live.

The single default-pool loss to `tralalerotrarala` collected 400 gems but banked none; its 83 deaths/36 kills contrasted with the opponent's 52/66. c442 did more monster damage (64.3k vs 27.9k) and earned more gold (3,905 vs 3,615), pointing to failure to win the teamfight and convert collected gems. c443's ranged attack while banking showed no win or gem gain. c444's raw-damage/carrier priority regressed to 8/12 versus six strong bots; c445's higher carrier weight tied c442 at 11/12 but banked fewer gems. Keep both rejected.

Campaign remains 4 wins / 620 maps; max streak 1, current 0/10. The already uploaded v100/c425 is still the next live check when testing resumes. Production source and ZIP are unchanged. Detailed run folders are in `bots/tungtungsahur/PLAN.md` and `analysis/maps.md`.

Latest local Contest follow-ups: c446's post-round-149 auto-engage matched c442 exactly across the 40-game default pool and tied its direct head-to-head, so it adds no measured gain. c447's shared sighting pursuit fell to 9/12 versus c442's 11/12 strong-proxy score. Reject both. Keep c442 local-only; the already uploaded v100/c425 is still the next live check after testing resumes. Live testing remains paused, campaign is 4 wins / 620 maps with max streak 1 and current 0/10, and production files are unchanged.

## Latest local candidate while live tests are paused (18 Oct 2026)

c450 widens c442's Contest-opening burst leash to five tiles. It scored 12/12 against six strong Contest proxies, 40/40 against the 20-opponent Contest pool, and 169/204 across six strong proxies on all 17 maps; it won both direct side-swapped tests against c442. c451's six-tile leash scored 11/12 on strong Contest proxies. c455 later added a Swirl-specific leash and is now the leading local candidate; see below for its full results. Keep both versions local-only until unranked testing resumes.

Live match groups remain paused at the user's direction. Campaign remains 4 wins / 620 maps, max streak 1, current 0/10. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged; c450 is only in `bots/c450/src/`.

The next local deficit remains Swirl (7/12 against six strong proxies). Re-screening the historical 150-damage camp-safety source also scored 7/12 and preserved the losses to both Ming sides, both Xuanming sides, and Faisal side A. This rules out that threshold as the next fix; test a more targeted combat or route change before another broad update. Run details are in PLAN.md's Swirl camp-safety section.

The Swirl tank draft (Ryth instead of Ren, preserving Varg) also scored 7/12 and banked 845 fewer gems than c450. Moving Ryth into Cassi/Issac's squad then exactly matched that candidate's 12 outcomes. Keep both rejected; the central Swirl losses still need a combat-focused fix. Details are in PLAN.md's c452/c453 section.

c455 is now the leading local-only candidate: it keeps c450's Contest leash and also applies a five-tile burst leash on Swirl against the C&I/Varg/Stellar/Vendetta draft. It scored 170/204 and 196,173 gems across six strong proxies on all maps, one win and 312 gems above c450, with all 192 shared non-Swirl outcomes unchanged. It converted Faisal side A on Swirl but still lost both sides to Ming and Xuanming; it also split 1–1 against c450 head-to-head. The full default Swirl pool remained 32/40. c456's stricter retreat was worse on gems. Do not promote c455 to production or upload it while live matches are paused; use it as the next test candidate when live testing resumes. Details are in PLAN.md's c454–c456 section.


## Latest local continuation (18 Oct 2026, Swirl follow-ups)

The user asked to keep live unranked matches paused while work continues locally. No new live groups or uploads were created. Swirl experiments c457–c466 found that the map's routes to outer camps still cross the center choke; suppressing opening burst or copying the top bot's 55%/75% survival thresholds did not improve results. Two early counterdraft attempts were invalid because the opponent's full draft was not visible when picks were finalized; corrected replay checks confirm the actual lineup.

The best targeted matchup signal is c466: keep Ren on Swirl side A and use Vendetta on side B. It scored 8/12 against six strong proxies and 30/40 in the default pool; the Vendetta roster beat Ming and Xuanming from side B, but c466 remains below c455's 32/40 default Swirl screen. A direct c466-vs-c455 screen scored 2/2, though only the side-B game changed lineup; on side A both drafted the same Ren/Ryth lineup. The repeated screen was byte-identical, so it is not another independent result. Keep c455 as the broader local candidate and c466 as a side-B hypothesis; neither is validated live. The next useful work is fixing side-A Swirl's central-choke opening and converting early camp clears safely, then resuming live tests only when the user resumes them.

Campaign remains **4 wins / 620 maps**, maximum streak 1, current **0/10**. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged; no candidate was copied into production.

## Local Swirl continuation (18 Oct 2026, c467–c476)

Live unranked testing remains paused; no new group/upload occurred. Local c476 is the strongest Swirl candidate so far: it conditionally uses Vendetta on side B and Ren/Vendetta on side A when the opponent's C&I/Varg opening is visible. It scored 10/12 against six strong Swirl opponents, 32/40 in the default Swirl pool, and 172/204 across the six strong bots on all 17 maps (197,073 gems). Compared with c455, only six Swirl side results changed; c476 converted Ming/Xuanming side-B losses into wins, for +2 wins and +900 gems. Side A still loses to both top opponents, despite raising their scores to 606 and 374 gems. This does not meet the 10-win streak goal and is not production-validated.

Rejected c471–c474 route, split, solo-farmer, and side-A gear attempts. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged; campaign remains 4 wins / 620 top-50 maps, best streak 1, current 0/10. Full data and paths are in `bots/tungtungsahur/PLAN.md` and `analysis/maps.md`.

c477–c479 tested side-A retreat thresholds, an 80-round no-fight opening, and raw-damage target selection against Ming/Xuanming. All stayed 2/4, with lower side-A gem totals than c476; reject them. Next useful work is a coordinated side-A opening/farming plan, not another isolated combat threshold. c476 remains local-only; live testing is paused and production is unchanged.

A fresh instrumented local matchup adds a clear next direction: `mingstudy-trace` beat c476 2/2 on Swirl, banking first at r45/r51. Its draft compiler routes Cassi/Issac together and assigns Varg, Stellar, and Vendetta separate camp circuits. The generic split tested in c472 lacks this assignment and lost 0/4. Prototype a bounded Swirl first-cycle route plan with immediate banking; keep it local-only until the all-map and strong-opponent screens justify more.

c480 added an 80-round altar-camp embargo to a side-A-only opening split. It reduced deaths but collapsed gem output to 18/154 against Ming/Xuanming, so reject. The instrumented top-bot replay indicates the next route plan must assign exact camp circuits and banking stops per role; a generic split is insufficient. c476 remains local-only.

## Swirl flank-opening follow-ups (18 Oct 2026)

c481/c482's lane splits regressed on Swirl side A (308/236 and 240/356 gems). c483 instead kept the team together on the opposite-flank 88-gem camp at `(13,13)` for one opening cycle. It scored 3/4 against Ming/Xuanming, raised the Ming side-A score from 606 to 885, and converted Xuanming side A from a loss at 374 to a win at 1,024. Its six-strong Swirl score matched c476 at 10/12, with +841 gems across the three top-team side-A results; the default Swirl pool remained 32/40. Strong all-map results were 171/204, 197,818 gems versus c476's 172/204, 197,073; one Lanes result varied on a separately generated map, so the single-win delta is noisy. c484's first-bank phase cutoff regressed to 4/6 against Ming/Xuanming/Faisal. Keep c476 as the balanced local baseline and c483 as a promising Swirl-specific comparison candidate; neither has live validation.

Live unranked work remains paused. The campaign remains 4 wins / 620 top-50 maps, best streak 1, current 0/10. Production source and submission ZIP remain unchanged. Run details are recorded in `bots/tungtungsahur/PLAN.md` and `analysis/maps.md`.

c485 held the opposite-flank camp through two 88-gem deposits. It matched c476/c483 at 10/12 strong and 32/40 default Swirl, winning Ming side A (1,034 gems) but losing Xuanming (684) and Faisal (924). c483 instead wins Xuanming side A and raises the Ming loss to 885; neither variant converts Faisal. c486's Ren Monster Strength first item fell to 9/12 strong. Retain c476 as the balanced local baseline and c483/c485 as matchup alternatives; no upload or production change.

## Latest local result: c488 (18 Oct 2026)

Live unranked remains paused. c488 adds a team-wide persistent Swirl opening abort when a nearby enemy Varg falls to 60% health or lower. It uses reserved shared-memory stamp 127, separate from the ordinary fight alarm. The marker fired against Faisal at r53 / 58% Varg health. c488 scored 11/12 in two independent six-proxy Swirl screens, 32/40 on the default pool, and 172/204 (198,133 gems) across six strong opponents and all 17 maps. That matches c476's win count with +1,060 gems and exceeds c483 by one win and 315 gems. Keep c488 local-only; no production edit, submission, or live group. Production hashes are unchanged and the live campaign remains 4/620 maps, best streak 1, current 0/10.

c487 is rejected: it used the ordinary fight alarm to switch out of the flank route, which could trigger on routine tank damage before its Varg condition. See `bots/tungtungsahur/PLAN.md` and `analysis/maps.md` for run folders and full results. Next local focus: Lanes and Pilgrimage, the largest remaining all-map loss clusters.

Lanes follow-up c489 split both sides from round 1 and scored 6/12; c490 split only side B and scored 5/12. They did not beat Ming or Xuanming. The split raised Ming side-B gems from 772 to 970 and prevented two deaths, but still lost 970–1,012 and gave up another side-B win. Reject the blanket split; next Lanes work needs a bank/camp route tailored to the side and visible threat.

c491's shared opening against the Ren/Stellar/C&I/Ryth/Varg Pilgrimage mirror reduced deaths but collapsed gems (556/524); reject it. Movement diagnostics c492/c493 show that a side-B Lanes split raised one Ming replay from 802 to 838 gems but still lost, 12 rounds later. At the last r525 log it had fewer camp/capture/altar steps and one fewer gem-pickup event; the final 12 rounds were not instrumented. No general route change is justified. Production source/ZIP and campaign state remain unchanged. Next local work should use these movement traces to target Lanes' farm-to-bank circuit; live unranked remains paused.

Latest local Lanes follow-up (18 Oct): c495's clean first-bank phase split tied a fresh c488 control at 7/12. It helped Ming side B (772–1,012 → 1,000–968) but gave up a Faisal side-B win (1,008–564 → 956–1,012). c496 conditioned the split on a 20-gem deficit and also tied at 7/12, with 0/2 against Ming and Xuanming. Reject both as general changes. c494 includes movement instrumentation and is not comparable. Live unranked matches remain paused; no uploads or production edits were made. See `bots/tungtungsahur/PLAN.md` and `analysis/maps.md` for run folders.

Latest local counterdraft result c498 (18 Oct): a Corners-only six-tile retreat gated on the opponent's mirror core draft (Cassi & Issac, Ren, Stellar, Ryth, Varg) changed one strong-proxy result: the meta-core side-A loss became a 1,010–572 win, with deaths reduced from 22 to 11. Strong all-map results rose 172/204→173/204. The full 20-opponent local pool tied clean c488 at 624/680 after recovering one failed control runner match; all shared results matched. Keep c498 local-only for that exact draft. Live unranked remains paused; no upload or production change.

Latest local Pilgrimage screens c499–c500 (18 Oct): Ren's fighter route did not respond to his squad flag, and all 18 outcomes matched the saved reference. c500 changed only the early shared-camp objective choice on the exact mirror draft; its turn handlers still used `team_farm`. It scored 3/18 versus 5/18 and lost the Ming side-B and Xuanming side-A wins. Reject this partial override. Live unranked remains paused; production source/ZIP remain unchanged. Full comparison is in `bots/tungtungsahur/PLAN.md`.

Latest local Pilgrimage result c503 (18 Oct): six-tile outmatched retreat only on side B scored 29/40 twice in the 20-opponent map pool versus c488's 28/40. It changed three results: Faisal-bot and my-bot side B became wins; opp-tts-locker side B became a loss. The focused strong Pilgrimage screen improved 5/18→6/18, but the six-proxy 17-map screen tied c488 at 172/204. Keep c503 local-only for further matchup work. Live unranked remains paused; production source and ZIP are unchanged. Details are in `bots/tungtungsahur/PLAN.md`.

Latest local candidate c506: role-based Pilgrimage farming from round 1, plus six-tile outmatched retreat only on side B against non-mirror drafts. It scored 7/18 twice on the focused screen, 29/40 twice on the default Pilgrimage pool (c488 28/40), and 173/204 on six strong opponents across all maps (c488 172/204). The strong all-map gain is Xuanming side B; the default-pool changes include wins versus Faisal-bot and my-bot, offset by an opp-tts-locker side-B loss. Keep local-only. Live unranked remains paused; production source/ZIP unchanged. Continue with the next weak map after recording c506.

Latest integrated local candidate c508 combines the Pilgrimage side-B/mirror strategy with a Packs early-combat leash. After two replay-collision recoveries, it scored 626/680 versus c488's 624/680: Packs 33/40 and Pilgrimage 29/40, with all other map totals unchanged. On six strong proxies across all maps it scored 173/204 versus 172/204; gains include Xuanming on Pilgrimage side B, with a Packs trade against `fx-dbllock`, Xuanming, and `opp-swirl-meta-core`. Keep local-only. Live unranked remains paused; production source and submission ZIP remain unchanged. Details are in `bots/tungtungsahur/PLAN.md`.

Update: c509's Swirl Ryth/C&I/Stellar/Tavi roster scored 5/12 strong and was rejected. c510's side-A flank opening versus the Ryth/C&I/Stellar/Tavi enemy draft tied c508 at 11/12 strong and 32/40 default Swirl; it shifted two matchups to wins and two to losses, so it remains a hypothesis. c511's Lanes Ryth→Vendetta draft swap fell to 5/12 from 7/12, including both Ming and Xuanming losses. Lanes remains a low-death farm-rate issue; the next useful experiment is a per-body camp-and-bank route, informed by `mingstudy-trace`'s draft-time planner. No candidate was promoted or uploaded. Live unranked stays paused at the user's request.

Latest local candidate is c516. Delaying Lanes' role split until round 50 scored 12/12 twice against six strong local proxies, including both Ming and Xuanming sides; the 20-opponent Lanes pool stayed at 39/40. Adding the exact-draft Corners retreat converted the `opp-swirl-meta-core` side-A loss. c516 scored 180/204 against six strong proxies over all 17 maps after recovering one replay collision, versus c508's recovered 173/204, and tied c508's 626/680 on the full default pool. This remains local evidence only. Live unranked stays paused; no production source, submission ZIP, or upload was changed. The 10-win live streak remains unverified.

Latest local follow-up c519 adds an Eight-only counterdraft: when Ren is visible and we are on side B, pick Tavi instead of Ren. The side-B mirror loss converted from 842–1,040 to a 1,012–820 win; applying Tavi on side A was harmful, so c519 preserves Ren there. The focused screen repeated at 10/12; the six-strong, all-map screen rose 180/204→181/204. The default Eight pool remained 35/40, and the recovered full 20-opponent, 17-map pool tied c516 at 626/680. Treat this as a matchup-specific result, not a broad win-rate gain. c517's exact-draft condition was unreachable and c518's both-side version regressed side A. No live group, upload, production source, or submission ZIP changed; live unranked remains paused and 10/10 is not verified. Full details and run paths are in `bots/tungtungsahur/PLAN.md`.

Latest local continuation c520–c533: Swirl's generic split routes were unsafe or too slow; c528's abort-and-stay-grouped policy raised one side-A proxy score to 674 but still lost, so c519 remains the broad candidate. Lanes safety/gear variations did not improve the 978-gem side-B bank race. These are proxy tests only. Production source and submission ZIP remain unchanged, no live group/upload was made, and the 10-win live streak is unverified. Full results are recorded in `bots/tungtungsahur/PLAN.md`.

Latest local follow-up c535–c542: on the five-map synthetic Please roster proxy, c519 scored 8/10 and c542 scored 9/10. c542 preserves c519's side-B response and extends the Tavi counterdraft to side A when Ren+Cassi/Issac+Varg+Stellar are visible; it wins both Eight proxy sides, while the full default Eight pool stays 35/40 (no gain over c519). Lanes side B remains the only five-map loss. Replacing Ryth with Tavi there or splitting from round 1 regressed; waiting until the first-bank signal improved one proxy score to 948/1,012 but did not convert the result. Treat proxy evidence separately from the official Please replay and do not count it toward the top-50 streak. Live matches remain paused; production source/ZIP and hashes are unchanged. See `bots/tungtungsahur/PLAN.md` for exact runs and metrics.

## Latest local Lanes work (18 Oct 2026)

Live unranked remains paused. Please's actual Lanes loss was a farming throughput gap (42 vs 29 camp captures, 0 deaths on either side). The only candidate retained for a narrow follow-up is c550: against the exact Please draft on the far-side spawn, Ryth Strength gear raised our bank from 802 to 984 gems, but still lost 984–1,012. It scored 39/40 in the full local Lanes pool with the same lone loss as c543. Team-wide Please gear mirroring and corrected shard thresholds regressed, so neither is promoted. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` are unchanged; no live test or upload was made. The 10-win live streak is still unverified. Run details are in `bots/tungtungsahur/PLAN.md`.

The far-side Lanes Ryth counter c550 passed the 204-game strong set at 181/204, exactly matching c519 and c542 outcome-for-outcome and gem-for-gem. The separate `opp-swirl-meta-core` bot scores 135/170 against five distinct strong local opponents versus c550's 160/170, so it is not a broad replacement despite its direct Eight matchup wins. In the mirror Eight replay, side A trailed 738–160 by r300 and dropped 270 gems; giving Tavi to side A previously collapsed the score to 176. Keep that roster rule unchanged while investigating earlier safe farming. Details are in `bots/tungtungsahur/PLAN.md`.

## Latest local candidate: c552 (18 Oct 2026)

c552 starts the farm split after a carry's first emblem only on the exact mirrored Eight draft. It converted the `opp-swirl-meta-core` side-A loss into a 1,012–892 win and raised the strong all-map result from 181/204 to 182/204, changing exactly one result. The default Eight pool remained 35/40 with identical outcomes; the full 20-opponent pool tied the recovered c519 baseline at 626/680 with no outcome changes. c552 also carries c550's far-side Lanes Ryth gear exception against the exact Please draft. The team-wide gear and shard-threshold experiments remain rejected. See `bots/tungtungsahur/PLAN.md` for full runs and caveats.

The workspace `tungtungsahur` source and ZIP now contain c552. The source builds successfully; the canonical bot passed 2/2 local Eight games against `opp-swirl-meta-core`. ZIP contents were verified byte-for-byte against all six source files. Hashes: `bot.cpp` `D150639F0CE009A5A7C82436100366BD4C8F0305CF71F003DDB2E18B9525E77C`; `draft.cpp` `C0DBA608AFCD4EAE56EEFE66D96EDBAA9D726DC58F2B60AFA784DADF2FB7A035`; ZIP `5BC212DEAE33B8AF195DB43E669216FE574B277967592CBA4D0767DAB7437892`. Live unranked is still paused and no submission was uploaded; the top-50 10-win streak remains unverified.

## Latest local candidate: c553 (18 Oct 2026)

c553 changes Ryth's Lanes gear order only on side B against the exact Please five-champion draft, buying Power Strength before Monster Strength. The two-sided synthetic Please screen repeated at 2/2, with 1,020–990 on both sides; the earlier build had lost side B 984–1,012. MingStudy side B still loses 978–1,012. Across the five-map proxy screen c553 scored 19/20 (Please 10/10, MingStudy 9/10). This narrow counter did not improve the broader pools: Lanes remained 39/40, strong all-map remained 182/204, and the 680-game local pool remained 626/680. A direct result-by-result comparison against c552 found zero changed outcomes or gem totals in that full pool.

The workspace source and ZIP now contain c553, build successfully, and the ZIP's six source files match byte-for-byte. SHA-256: `bot.cpp` `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6`; `draft.cpp` `C0DBA608AFCD4EAE56EEFE66D96EDBAA9D726DC58F2B60AFA784DADF2FB7A035`; ZIP `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA` (31,057 bytes). No live unranked match or upload was made; live matches remain paused at the user's direction. The 10-win top-50 live streak remains unverified. Full test paths and metrics are in `bots/tungtungsahur/PLAN.md`.

Follow-ups c554/c555 were gated on the Please-style C&I/Varg/Stellar/Vendetta/Tavi draft, not the actual `opp-swirl-meta-core` Ren/Stellar/C&I/Ryth/Varg draft. Their meta-core replays were byte-identical to c553 and therefore did not test a changed meta-core response. Both variants regressed the six-proxy Pilgrimage screen (c554 8/12, c555 7/12 versus c553 9/12) by changing Xuanming/Ming outcomes. Correct the gate before using these runs to draw conclusions about the meta-core matchup. c553 remains the current workspace bot; live unranked stays paused.

c555's Please-gated early strong-camp filter was rejected at 7/12. The fresh score trace against meta-core shows our first bank at round 70 for 46 gems versus its round-75 bank for 68; by round 300 its lead was 92–160 gems depending on side, while our first deaths began at rounds 75–77. This suggests an opening yield and survival deficit, but does not establish that strong camps caused the deaths. c553 remains current. No live unranked games or uploads; the official 10-win streak is unverified. Next local test should use the exact observed meta-core roster gate and measure both bank timing and deaths.

c556 used that correct Ren/Stellar/C&I/Ryth/Varg gate and shared the first camp until bank (round 120 fallback). It tied c553 at 9/12, but worsened the two meta-core scores to 556 and 252 banked gems from 940 and 732. Reject; retain the round-one split and test early survival separately. Details are in `bots/tungtungsahur/PLAN.md`.

Latest local Pilgrimage candidate c558 raises retreat to 55% health only on our side A, only through round 119, and only against the exact Ren/Stellar/C&I/Ryth/Varg lineup. It converted the meta-core side-A proxy from 940–1,014 to 1,032–420 and reduced logged deaths 22→14. Its focused screen was 10/12; strong all-map was 183/204 (one exact result gain, no other changes); the 680-game default pool stayed 626/680 with no win changes. The 55% threshold beat 50%, 60%, both-side gating, and a longer r180 window in these local screens. Keep c558 isolated; c553 remains in the main source/ZIP until official unranked results resume. No submission was uploaded, live testing remains paused, and the 10-win live streak is unverified. Full paths and comparisons are in `bots/tungtungsahur/PLAN.md`.

## Latest local follow-up: c562–c565 (19 Oct 2026)

c563 is now the strongest local matchup candidate: it keeps c558's Pilgrimage meta-core side-A survival rule and adds the 55% early retreat rule on side B only against the exact fx-dbllock draft when an enemy is within four tiles. It raised the fx-dbllock side-B proxy from 412–1,012 (21 deaths) to 1,032–872 (7 deaths), and scored 184/204 across six strong local opponents on all 17 maps versus c553's 182/204. The full 680-game local pool remained 626/680, with some matchup wins trading places, so this does not establish a broad gain or a top-50 streak.

The earlier c562 roster-only side-B rule improved fx-dbllock but gave up an opp-racer win. c564's additional side-B meta-core rule made that result worse (732–1,064→504–1,026), so it was rejected. c565 moved Ryth into squad B for that same meta-core side-B fight; its 12 focused replays were byte-identical to c563, including all scores and combat stats, so the tank-cover adjustment had no observable effect and was rejected. The decisive replay shows the economy gap: we led 46–0 at r70, but were behind 68–228 by r300; meta-core reached 500 about r850 versus our r990. We finished 732–1,064 with 16 deaths versus its 23, so the evidence points more toward bank pace than losing more fights. Current replay instrumentation lacks per-champion movement/capture counts, so the specific route/altar cause still needs measurement.

The canonical workspace source remains c553 and the submission ZIP hash remains `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. Official unranked matches are still paused, no upload was made, and the requested 10 consecutive top-50 wins remain unverified. See `bots/tungtungsahur/PLAN.md` for exact run paths and the result-by-result comparisons.

Diagnostic caveat: an isolated c563 copy with per-step movement counters (`bots/c566-trace`) changed the meta-core side-B game to 754–1,018 and 22–21 deaths; a fresh c563 control repeated 732–1,064 and 16–23 deaths. Both completed without crashes, but the logger changes match behavior. Discard its movement counts and score as candidate evidence; use replay-side analysis or a lower-overhead tracing method.

## Latest local candidate: c577 (19 Oct 2026)

c577 adjusts Pilgrimage bank routing for the map side with allied spawn at `(46,1)` against the exact Ren/Stellar/Cassi-and-Issac/Ryth/Varg lineup: it applies the enemy-half altar penalty to carriers from 46 gems instead of 100. It repeated 2/2 against the local `opp-swirl-meta-core` proxy (fresh c571 control 1/2) and improved the six-strong, 17-map screen from 184/204 to 185/204. The sole changed outcome was Pilgrimage side B against meta-core, from 732–920 to 968–920. Three other affected same-map scores remained wins. Generic application to all Pilgrimage opponents tied the strong screen at 184/204 and traded a new meta-core win for an `opp-racer` loss, so keep the exact-draft gate.

Earlier Pilgrimage gear and retreat variants did not improve the result; details and run paths are in `bots/tungtungsahur/PLAN.md`. c577 remains isolated under `bots/c577-fresh`; canonical source and ZIP remain c553 and unchanged. Official unranked matches remain paused, no upload was made, and the 10-win top-50 streak is unverified.

## Latest local candidate: c586 (19 Oct 2026)

c586 combines c577's Pilgrimage carry-routing change with a Collision side-B-only squad adjustment: Stellar joins Issac's squad on the map's south spawn side. It scored 5/6 on a repeated screen against Ming, Xuanming, and fx-dbllock (c577: 4/6), 40/40 on the default Collision pool (c571: 37/40), 186/204 against six strong local proxies on all maps (c571: 184/204), and 630/680 on the complete default local pool (c571: 626/680). The full pool gained four outcomes without new losses; three came from Collision side B against TTS-v3/v4/v5, and one from Pilgrimage side A against TTS-v5. These are local proxy results, not official unranked validation.

The intervening Collision draft, lineup, and bank-order variants regressed. Full run evidence is recorded in `bots/tungtungsahur/PLAN.md`. c586 lives under `bots/c586-fresh`; the canonical source and submission ZIP remain c553 and unchanged. Official unranked matches are still paused, with no upload and no verified 10-win top-50 streak.

## Latest local Rows follow-up: c592–c593 (19 Oct 2026)

c592 skipped Varg's shared capture on Rows. It did not change the six-strong result (11/12) or the
20-opponent Rows win count (40/40), though its mean own end score was 986.7 versus c586's 983.4 on
the fresh matched pool. The key meta-core Rows score/death trace remained unchanged.

c593 uses c586 as its base and keeps the Rows Varg/Cassi-and-Issac/Ryth/Stellar core when an enemy
Ren is visible, instead of drafting Ren and leaving Ryth out. It repeated 12/12 on two six-strong
Rows runs versus a fresh c586 control's 11/12, converting the meta-core side-A result each time. It
scored 44/44 on the standard Rows pool and 187/204 on the six-strong, all-map screen versus c586's
186/204; the only changed outcome was meta-core Rows side A (990–990 loss to 990–924 win). The
20-opponent, 17-map pool stayed 630/680, with no outcome changes. Keep c593 isolated as a narrow
local matchup candidate. Production source/ZIP are unchanged at c553; live unranked and uploads
remain paused, with the 10-win top-50 streak unverified. Full paths are in `bots/tungtungsahur/PLAN.md`.

c597 changed Ryth to Monster Strength then Power Strength on Stampede against the exact meta-core
draft. It matched c593's 11/12 in all 12 strong games with identical scores and rounds; the key
Stampede loss remained 0–720 and own deaths rose 14→17. Reject the gear change. c593 remains the only
recent isolated candidate with a repeated strong-proxy win conversion. Production source/ZIP remain
c553; live unranked and uploads remain paused.

Follow-ups c594–c596 did not improve the win count. c594 raised the Interlock meta-core side-A score
270→780 and cut deaths 29→20 but still lost and tied the controls at 11/12 strong and 43/44 standard.
c595's Ren-first Interlock lineup repeated 12/12 strong but fell to 37/44 standard, six wins below
c594; reject it. c596's Varg-first Stampede draft scored 9/12 versus c593's 11/12; reject it. These
remain local-only tests. Production source and ZIP stay at c553, and live unranked remains paused.

Ambush follow-ups c598–c599 were local-only rejects. c598's altar-range bank priority matched c593
exactly across 12 strong-proxy games and did not suppress a spell cast against a visible enemy.
c599's round-one role split stayed 10/12, converted no losses, lengthened mean game duration by
73.1 rounds, and raised mean opponent submitted gems by 40.2; reject early splitting. The c593
Ambush side-A loss also shows that its five-round `SCORE` trace can briefly lead while the enemy
holds a final tribute: it showed 974–902 at r1020 and ended at r1021. Main source/ZIP remain c553
with hashes `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and
`2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. Live unranked matches and
uploads remain paused; the 10-win top-50 streak is unverified.

Ambush follow-ups c600–c604 are recorded in `bots/tungtungsahur/PLAN.md`. c600's movement logger
was diagnostic; it measured 2,304 capture-directed steps versus 324 camp-directed steps per game
on the six-strong Ambush screen and exactly reproduced c593's match results. c601's all-non-carry
capture restriction reduced capture travel but regressed the 22-opponent pool to 41/44; c602's
active-camp refinement was an exact no-op. c603 retained telemetry and is not clean evidence.
Uninstrumented c604 gates the capture restriction to Ambush side A. It scored 44/44 on the 22-opponent
Ambush pool versus c593's fresh 43/44, 187/204 on the six-strong all-map screen (same as c593), and
631/680 on the default pool versus 630/680. Only the Ambush side-A `my-bot` result changed from loss
to win; all other default-pool outcomes matched. Its reported engine-error count (480) matches the
c593 control. Keep c604 isolated. Candidate source hash is
`6962D7B2E2E563BD99A205E5947AFD37D7790F8C137BBDEE8765A13A8CBAB34F`; production hashes remain
c553 `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and ZIP
`2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. No upload or live match was
made because the user paused live unranked work.

## Latest local follow-up: c609 Contest banking (19 Oct 2026)

The top-50 Please Contest replay shows Prism collected 200 gems at r1027 and died to Please's Ryth at r1063, dropping the full bag before banking. c609 adds a 40-step altar cost when a carrier has at least 100 gems and an altar is clearly nearer the enemy spawn. Against the same 22-opponent Contest pool, it kept the 44/44 result and changed one score: versus `tralalerotrarala` on side B, our score moved from 600–200 at round 2000 to 800–0 at round 1608. The six-strong Contest screen stayed 12/12 and matched c604 on all scores and finish rounds. c610 with an 80-step penalty produced the same results; keep the smaller c609 rule as a local candidate only.

Ambush role-join tests c607/c608 were exact no-ops versus c604. Production source and ZIP are unchanged at c553; no official match or upload was made. Live unranked remains paused and the 10-win top-50 target is not verified. Full run details are in `bots/tungtungsahur/PLAN.md`.

## Current top-team Contest lead: c613 (19 Oct 2026)

The exact-roster synthetic Please proxy uses Varg/Cassi & Issac/Stellar/Ren/Ryth. Production c553 lost both Contest sides and showed much lower gold and monster damage than the proxy. Drafting Varg first on Team A (c613) improved that proxy screen to 1/2 while preserving the 12/12 six-strong Contest result and tying production at 182/204 on the six-strong all-map screen. Its 22-opponent Contest score was 42/44 versus c604's 44/44, with two added Team-A losses, so keep it isolated for future top-50 validation. The proxy is synthetic and does not establish a live win.

c609's Contest banking rule improved one weak-proxy score and finish time but did not help against the roster-matched proxy; c611's unconditional Varg draft regressed both the broad and strong Contest pools, and c612's late Varg counter lost 0/2. Production source/ZIP remain c553. Official unranked matches and uploads remain paused; the requested 10-win streak is not verified. See `bots/tungtungsahur/PLAN.md` for run paths and hashes.

## Contest Varg leash rejected: c614 (19 Oct 2026)

Fresh c613 replay statistics show our Contest Varg under-farms and dies often against the local synthetic Please proxy (513 gold, 10,457 camp damage, 13 deaths versus its Varg's 2,295 gold, 35,947 camp damage, 1 death). c614 tried ignoring enemies beyond two tiles while farming. It rose to 911 Varg gold but fell to 8,005 camp damage and 0/2 against the proxy; the six-strong Contest screen regressed 12/12 to 11/12, losing to `ming_bot` on side A. Reject c614. The Varg route/survival issue remains unresolved; this synthetic proxy is not the real top-team bot. Runs and details are in `bots/tungtungsahur/PLAN.md`. Production source/ZIP are unchanged; live unranked tests and uploads remain paused, so 10 consecutive top-50 wins are not verified.

c615's Contest home-side camp filter exactly matched a fresh c613 control across the proxy and all 12 strong Contest records; reject it as behaviorally inactive. c616 added Power Health after Varg's Monster Strength emblem. On the proxy side-A game, Varg deaths fell 13→8 and monster damage rose 10,457→11,994, but gold slightly fell and the matchup remained 1/2; the strong Contest screen regressed 12/12→11/12 (loss to `opp-swirl-meta-core` side A). Reject c616. These experiments leave the Varg farm gap unresolved; c613 remains a local-only draft lead. Details/run folders are in `bots/tungtungsahur/PLAN.md`. Production source and ZIP remain c553; live unranked is still paused and the 10-win target remains unverified.

c617's sampled Contest Varg trace found no solo target at rounds 100, 1000, 1600, 1900, or 2000. c618 allowed a gold-only camp as the zero-value fallback when no gem camp was eligible. Varg camp damage/gold increased (10,457→18,044 damage; 513→1,160 gold on the proxy side-A replay), with deaths 13→12, but the proxy match became 0/2 and the strong Contest result repeated at 11/12 twice, losing to `ming_bot` side A. Reject c618; it improves camp stats but hurts match results. c615 was a no-op; c616's health build also regressed to 11/12. c613 remains a local-only draft lead (12/12 strong Contest, 42/44 broad Contest, tied c553 at 182/204 strong all maps, and 1/2 versus the synthetic roster proxy). The 10-win official target is still unverified. Production bot and ZIP remain c553; live unranked matches and uploads remain paused. Full runs are recorded in `bots/tungtungsahur/PLAN.md`.

## Latest local check: c619–c620 (19 Oct 2026)

c619's health-gated Varg wolf-pack rule was behaviorally inactive on both the roster-matched proxy and the six-strong Contest set. c620 combined c563's Pilgrimage survival rules with c613's Team-A Varg-first Contest draft. After replacing one replay-writer failure with a successful two-side Faisal rerun, c620 scored 184/204 on the six-strong, all-map set, exactly matching c563's wins and losses. Contest scores/timing changed in five Team-A games but no win changed; the Xuanming score fell from 1,000–0 at r1797 to 600–200 at r2000. The combined broad pool was not run, and c613's separate broad Contest screen was 42/44 versus c604's 44/44, so c620 is not a verified improvement. The replay-writer error followed a completed engine win and was not a bot crash.

Higher-ranked replay pattern remains consistent: top teams clear camps and bank gems earlier, sustain more monster damage/gold, and punish dropped carries; some losses are pure economy races, while maps such as Contest, Swirl, Collision, and Elkring add combat wipes. Candidate c563 improved one meta-core Pilgrimage side-A result and one fx-dbllock Pilgrimage side-B result and raised the six-strong screen from 182/204 to 184/204, but did not raise the 680-game local pool above 626/680. c604 is the strongest broad local candidate recorded here (187/204 strong, 631/680 default), but gains are narrow: only Ambush side A versus `my-bot` changed from loss to win. These are local proxies, not official match wins.

Production source and ZIP remain c553 with hashes `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. No live match or upload was made. Official unranked work remains paused; the 10-consecutive top-50 win goal is unverified.

## c609 full-pool verification (19 Oct 2026)

c609 adds the Contest safe-bank cost to the c604 base. Its full 680-game local pool produced 629/678 valid results with two replay-persistence failures; both engine logs record c609 wins, and isolated reruns completed both pairings 2/2. Corrected result: 631/680, matching c604's total and every per-opponent win count. The Contest tweak remains a narrow score/timing improvement, not a broader local win-rate gain. See `bots/tungtungsahur/PLAN.md` for exact run folders. No official match or upload was made.

## Stampede routing checks (19 Oct 2026)

The Varg and gem-only Tavi solo-route ideas (c621–c623) were inactive against the strong Stampede drafts. The c624 trace found only one gem camp (360 gems, strength 360) and it is intentionally blocked until r150; nearby side camps are gold-only. c625 let Tavi take a gold-only camp from r100 to r149 when no enemy or team fight alarm was active. It tied a fresh c604 control at 11/12, with +120 own final gems, −240 opponent final gems, +20 kills, and +1,650 gold over 12 games, but also +46 deaths and a 32-round longer average. c626’s shorter r120–149 window regressed to 10/12, adding a Ming side-A loss. Reject both Tavi splits for now. c624's trace is diagnostic only; its output did not measure a strategy win. Run details are in `bots/tungtungsahur/PLAN.md`.

Production remains c553; the source and submission ZIP hashes remain unchanged. These experiments are local. No official match or upload was made, and the 10-win top-50 streak is unverified.

## Swirl Ryth-signature tests c627–c628 (19 Oct 2026)

c627's added Ryth branch was inactive in the six-strong screen, but it did activate against a synthetic Swirl opponent drafted C&I/Stellar/Ryth/Varg. In the repeated two-side pair it scored 1/2 versus c604's 0/2, winning side A (920–480 vs c604's 823–983) while both lost side B. The full 20-opponent Swirl pool stayed 32/40 for both; no win changed. Against Faisal-bot, whose Swirl draft also has the Ryth/Varg core, c627's combined scores improved by 108 own gems and reduced the opponent total by 50. Keep c627 as a narrow matchup hypothesis only: its opponent is a local policy with a Mite-like draft, not Mite's bot. c628 broadened the mode to any C&I/Stellar/Ryth core and regressed the six-strong screen to 10/12 from c604's 11/12, adding a loss to `opp-swirl-meta-core` side A (818–894 vs 972–636). The mode changes retreat and early-phase policy as well as the route. Reject c628. Full runs and hashes are in `bots/tungtungsahur/PLAN.md`. Production c553/ZIP remain unchanged; live unranked matches and uploads remain paused.

## Offline Stampede work, c629–c632 (19 Oct 2026)

c629's r125 central-camp unlock regressed the six-strong Stampede screen to 9/12 from c604's 11/12, so keep the r150 safety gate. c630's Issac side-farm was a no-op because it sat in Tavi's `marksman_turn`; Issac is initialized as `Role::fighter`. c631 repeated the wrong diagnostic location, so it produced no route trace. c632 moved the policy into `fighter_turn`: when safe and out of combat, Issac can clear a separate gold/gem camp before rejoining normal team farm. The clean source repeated 11/12 on the six-strong pool, matching c604's winners, while aggregate own/opponent gem totals shifted 8,880/3,780→12,600/3,060. On the 20-bot local Stampede pool, c632 scored 37/40 twice with exact repeat results, matching c604's 37/40; it gained three matchups and lost three others, while total reported gems increased by 7,980. Keep it isolated as a local farm candidate, not a broad win-rate upgrade. This pool is local and does not establish top-50 live performance.

Candidate source/hash and full run paths are in `bots/tungtungsahur/PLAN.md`. Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain c553 at SHA-256 `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. No unranked match or upload was made; live work remains paused and the 10-win top-50 goal is unverified.

## Stampede counterdraft and equipment follow-ups c633–c637 (19 Oct 2026)

c633's global 10-tile enemy alert and c634/c635's Issac gear queues did not raise the local win count. The alert traded the meta-core side-A result for an `opp-racer` side-B loss; `opp-racer` uses Mite's recorded Stampede draft, and c633 lost there with only 940 gold and zero gems. c634 fell to 36/40 default; c635 tied c632 at 37/40 but had more deaths and less gold. c636 restricted the alert to a C&I/Ryth/Stellar/Varg draft and reached 12/12 strong, but it also changed Faisal-bot results and left the default pool at 37/40 with no win-count gain. c637 adds Ren to the core trigger. It repeated 12/12 on the six-strong Stampede set; only the synthetic Ren/C&I/Ryth/Stellar/Varg side-A matchup changed versus c632, from a loss to a win. Its default 20-bot results match c632 exactly at 37/40. Across all 17 maps against the same six local proxies, c637 scored 188/204 versus a fresh c604 control at 187/204; the only changed winner was the Stampede meta-core side-A conversion. Keep c637 isolated as a narrow draft hypothesis, not a production change; no current top-50 team was tested live.

Candidate hash and run paths are recorded in `bots/tungtungsahur/PLAN.md`. Production source and submission ZIP remain c553; no online matches or uploads were made. Live unranked work remains paused, and 10 consecutive top-50 wins remain unverified.


## Contest offline replay review and c638 (19 Oct 2026)

Deep review of the archived rank-49 Please Contest replay found its first camp clear at r27 versus ours at r48; Please's Stellar bought Focus shards at r37 versus our Stellar at r79, then killed 20 of our champions. Please led camp clears 132:9, monster damage 170.8k:48.1k, and gold 14.2k:1.9k. Our Prism carried 200 gems at r1027, lost them to Please's Ryth at r1063, and Please submitted them at r1109. No bot faults or fuel exhaustion were recorded. The early farm lead and Stellar kill streak precede the carrier loss, so farming tempo and avoiding the later wipe are the main gaps.

c638 tried Power-only gear for Varg on Contest, based on Please's build. It never activated because our final draft omitted Varg in all tested matches. Current source and candidate matched every result on the 12-game strong set and the 40-game broad Contest pool (12/12 and 40/40). Reject c638 as an inactive change; production source and ZIP remain untouched. Replay details and run paths are recorded in the analysis review and `bots/tungtungsahur/PLAN.md`.

Live unranked matches and uploads remain paused. No 10-game top-50 streak has been established.


## c639 Contest shopping recall check (19 Oct 2026)

A Contest-only rule allowed shopping recalls with visible enemies farther than 5 tiles, using the Please replay's r55-r75 sightings as motivation. It remained 12/12 on six strong proxies and added 400 own gems, but dropped the full 20-opponent Contest pool from 40/40 to 39/40. The new loss was `my-bot-v2` side B (600:600 at r2000); aggregate own gems stayed at 37,200. Reject the general rule. The replay supports investigating early safe purchases, but this broad test shows that distance-only safety is not enough. c638's gear edit was inactive because Varg was absent from our tested lineups. Neither candidate changed production or was uploaded. Full run paths and hashes are in `bots/tungtungsahur/PLAN.md`.

Live unranked matches remain paused. The top-50 10-win streak has not been achieved.


## c640 Contest opening fight leash (19 Oct 2026)

Tested reducing Contest early enemy engagement from five tiles to two for rounds 0-74. The six-strong proxy result fell to 9/12 from 12/12, adding losses to Ming side A and both Swirl meta-core sides; own gems fell 10,200 to 9,400. Reject the candidate. The slower first farm start in the Please replay does not mean a smaller fight leash works against strong local opponents. Run and hash are in `bots/tungtungsahur/PLAN.md`; production remains unchanged.


## c644 Please-order Contest candidate (19 Oct 2026)

The Please replay's draft order is Varg / Cassi & Issac / Stellar / Ren / Ryth. A synthetic roster-matched atlas-planner proxy defeated current source 0/2. c639's distant-enemy shopping recall improved only Team B; c640's shorter opening leash improved only Team A; applying both on both sides failed. c643 applied each on its winning side and reached 2/2 against the proxy, but its roster-membership gate also triggered against `opp-swirl-meta-core`, lowering the strong Contest screen to 11/12. c644 gates on Please's exact pick order and retains the side-specific behavior.

c644 beat the proxy 2/2 twice with repeat scores (A 800:400, B 200:0 at r2000), while matching the fresh current bot exactly across the six-strong Contest set (12/12) and 20-opponent pool (40/40). This is synthetic local evidence, not an official top-50 win. Keep it isolated for a future live check. Candidate hash and run folders are in `bots/tungtungsahur/PLAN.md`.

Production source/ZIP remain unchanged; unranked matches and uploads remain paused, and the 10-win streak is unverified.


### c644 local result qualification (19 Oct 2026)

The candidate's 2–0 proxy score is timeout-based and asymmetric. Against the same proxy, current source scored 200:400 on Team A (kills 48:32, deaths 51:57, gold 4,770:13,255) and 200:200 on Team B (25:30 kills, 51:37 deaths, 4,545:13,435 gold). c644 scored 800:400 on Team A (60:16 kills, 31:74 deaths, 7,320:9,130 gold) and 200:0 on Team B (22:52 kills, 73:31 deaths, 3,395:15,585 gold). Team A indicates improved combat for this proxy; Team B's narrow gem lead came with much worse deaths, kills, and earned gold. Do not describe c644 as a farming improvement or broad upgrade. It remains local and unpromoted.


## Latest offline work: c645 rejected; c646 retained locally with a Lanes correction (19 Oct 2026)

c645 extended the Stampede Issac side-camp split from round 150 to round 180. It regressed the six-strong screen to 9/12 from c637's fresh 12/12, losing to `fx-dbllock` on both sides and `opp-swirl-meta-core` side A. Reject the extension. Run and source hash are recorded in `bots/tungtungsahur/PLAN.md`.

c646 combines c644's exact-order Contest profile with c570's exact Willow-lineup Lanes gear profile. It scored 2/2 versus each matching synthetic target proxy; the proxies are not ranked executables. The archived draft audit confirms c644 matches Please's Contest lineup but c646's Lanes Willow gate does not match Please's Ren/Tavi Lanes lineup. The 20-opponent broad screen on Contest and Lanes was 79/80 (40/40 and 39/40), matching c553's win counts with no winner flips. The six-strong, 17-map screen was 182/204 and identical to c553 on winners, scores, and rounds. Keep it isolated for possible future live validation. Production `tungtungsahur` remains c553 and its ZIP is unchanged; official unranked matches/uploads remain paused, and the 10-win streak is unverified. See PLAN.md for full run paths and SHA-256.


### Correction: the archived Please Lanes draft and follow-up (19 Oct 2026)

The official group `8a9a1654-7673-4da3-bbae-daaa2f5cc715` records Contest Please picks `[9,3,4,8,0]` = Varg/C&I/Stellar/Ren/Ryth, and Lanes picks `[9,3,4,8,10]` = Varg/C&I/Stellar/Ren/Tavi. c644's Contest gate matches the archived Contest roster. c646's Team-A Lanes gate requires Willow, so it does not activate against the archived Lanes roster. Its Lanes 2/2 result is only against the separate Willow-layout proxy. Our team was Team A in the recorded Lanes loss.

Against a local proxy with the recorded Ren/Tavi Lanes roster, c647's Monster-then-Power Ryth queue kept the baseline 2/2 but did not improve farming: Team A gem differential moved 1,020:990 → 1,012:946, own gold 4,490 → 4,330, opponent gold 4,190 → 4,140. It remained 39/40 on the full local Lanes pool with no winner changes, and 12/12 on the six-strong screen. c648's Power-then-Monster queue fell to 1/2. Keep c647 as an isolated low-confidence score-margin result and reject c648. c569's Tavi-for-Ryth roster swap was 0/2 against that proxy and remains rejected. Full evidence and hashes are in `bots/tungtungsahur/PLAN.md`.

## Latest local result: c652 Contest profile (19 Oct 2026)

c652 is the current best isolated candidate for the archived Please Contest draft. Its 2-tile Team-A leash through round 99 beat the roster-matched synthetic proxy 2/2 in two identical runs; Team A finished 1,000:400 at r1998 with 77 kills, 26 deaths, and 9,555 gold versus the proxy's 5,630. Team B finished 200:0 at r2000. The other tested leash durations were weaker. c652 stayed identical to c646 on the 40-game broad and 12-game strong Contest screens. These are local proxy results, not top-50 wins. Production is still c553, and official unranked matches/uploads remain paused.

Source `bots/c652-please-contest-leash2-r100/src/bot.cpp`, SHA-256 `E4A1494097AA44CF9D4CA54B25389CFF6A3D09C0E3F2B86BAC086E26500C431E`. Runs: target `matches/league/20261019-043821-c652-please-contest-leash2-r100-direct-please-target/`, repeat `matches/league/20261019-043842-c652-please-contest-leash2-r100-direct-please-target-repeat/`, strong `matches/league/20261019-043854-c652-please-contest-leash2-r100-direct-strong-contest-screen/`, broad `matches/league/20261019-043903-c652-please-contest-leash2-r100-direct-broad-contest-screen/`. Full c649–c654 table and hashes are in `bots/tungtungsahur/PLAN.md`.
### c652 cutoff bracket (19 Oct 2026)

Local tests put a sharp target-proxy boundary at round 100: c655 stopping at 90 was identical to c652 (`<100`) on both sides; c657 extending through round 100 (`<101`) dropped Team A to a 200:400 loss; c658 through 104 lost 600:800; c656 through 109 lost 200:600. Keep c652's `<100` window; reject longer windows. This is one synthetic proxy only and does not validate a ranked matchup. Exact run paths and hashes are in `bots/tungtungsahur/PLAN.md`.
### Contest equipment check: c659 rejected (19 Oct 2026)

Testing Monster Focus first on Stellar for the exact Please Contest Team-A profile reduced the proxy result from c652's 1,000:400 to a 600:600 gem tie lost on gold (8,070:10,205). Despite fewer deaths, Team A earned less gold and scored 1/2 overall. Keep Power Focus on Contest; Monster Focus's camp bonus did not transfer from other farm maps. This is one local synthetic matchup. Source hash and run path are in `bots/tungtungsahur/PLAN.md`.
### Please Lanes route timing and early-split rejects (19 Oct 2026)

The archived Lanes loss had no deaths and was a farm-route deficit. Please's first clears were Ren r35 and Varg r41; our first was Issac r47, and our Varg did not clear until r146. Totals were 30:43 clears and 750:1,000 gems. c660's turn-one split and c661's round-45 split both fell to 1/2 against the local roster proxy, with the exact same 904:1,012 Team-A loss; the round-50 c646 control was 2/2. Keep the current round-50 timing. Full event details, source hashes, and run paths are in `bots/tungtungsahur/PLAN.md`.
### Please Lanes Varg route follow-up (19 Oct 2026)

c662's early capture-duty exception exactly matched the round-50 control on the target proxy and all 40 broad Lanes records (39/40); reject as a no-op. c663's separate passive-camp route scored 1/2 (Team A 984:1,012), and c664's separate safe active-camp route scored 1/2 (Team A 962:1,012). Both side-B games matched the control. Keep the grouped round-50 opening pending real-match validation. Full hashes and run paths are in `bots/tungtungsahur/PLAN.md`.

c665/c666 delayed c663's Varg passive solo route until round 35/40. Both scored 1/2 against the local Please-layout proxy, below the 2/2 c646 control: Team-A results were 882:1,012 at r585 and 868:1,012 at r517; both Team-B games repeated 1,020:990 at r621. Reject both. Official unranked testing remains paused; production bot and ZIP hashes are unchanged. Full evidence is in `bots/tungtungsahur/PLAN.md`.

Rows c593 recheck: its Varg/C&I/Ryth/Ren draft matched our recorded lineup against Please's Varg/C&I/Stellar/Ren Rows draft and beat the local proxy 2/2. Fresh production c553 also went 2/2 with identical drafts, scores, deaths, kills, and rounds, so this is no gain over current production. c593 vs c553 went 16/34 across all maps, with side-dependent outcomes and both Pilgrimage games lost; c563 vs c553 lost both Pilgrimage sides. Keep c553 production; c586/c593 remain proxy candidates, not validated upgrades. Full runs and limitations are in `bots/tungtungsahur/PLAN.md`.

Rows replay follow-up: in the archived Please match, the first camp clear was nearly tied (r29 us, r25 Please), but camp clears ended 11:17. Our Cassi cleared none, Issac once, Ryth three times, Ren four, Varg three; Please's five heroes had 2–5 clears each. c667 drafted Stellar after the enemy showed Varg/C&I but regressed the 24-opponent Rows screen 46/48 vs fresh c553 at 47/48, adding a `ming_bot` side-B loss and no gains. Reject it; investigate repeat-clear cadence and role actions instead of the lineup swap. Evidence and run paths are in `bots/tungtungsahur/PLAN.md`.

c667’s complete 24-opponent Rows screen is 46/48 vs fresh c553’s 47/48. No wins were gained; c667 added a `ming_bot` side-B loss. Its focused c553 matchup split by side (792:1,001 loss on A, 1,023:924 win on B), and the exact-draft proxy remained 2/2 for both. Reject c667. The replay’s sustained 11:17 camp-clear gap and Cassi’s zero clears remain the route diagnosis; see `bots/tungtungsahur/PLAN.md`.

Rows Cassi evidence: Please bought Power Focus plus Durability Focus at r32; our recorded Cassi bought Power Focus at r201, then Durability Health at r280, and dealt 4.1k monster damage versus 14.6k for Please's Cassi. c668 changed the second queue to Durability Focus but scored 46/48 vs fresh production's 47/48 across 24 Rows opponents. c669 lowered Cassi's shop return threshold to 75 gold; it lost both direct c553 games at 990 gems. Reject both. Earlier spending alone did not close the farm gap. Production bot and ZIP remain untouched; details and run paths are in `bots/tungtungsahur/PLAN.md`.

Rows c670 made Ren follow Issac's fresh camp objective while retaining fighter combat and items. It scored 47/48 across 24 opponents, exactly matching c553's 47/48 and its sole meta-core side-A loss; the exact-draft proxy remained 2/2 with lower gems than production. Reject c670; stabilizing the shared objective did not transfer into more wins.


## Offline Rows follow-ups c671–c672 (19 Oct 2026)

c671 gave Rows Cassi a separate passive camp route. It scored 4/6 in a focused local screen, losing side B against both c553 and the synthetic Please-layout proxy; the proxy control c553 itself was 2/2, so reject c671. c672 changed only Rows Ryth's first emblem to Monster Strength while retaining Power Health. It matched fresh c553 at 47/48 over 24 Rows opponents with identical winners, and averaged 1.8 rounds faster, but earned slightly fewer own gems (1,026.9 vs 1,030.6). Reject c672 as no win-rate gain.

The archived Please Rows replay helps narrow the next hypothesis: our Ryth cleared two gold-only wolf camps before his first gem camp (r190/r264, first gem clear r331), while the opposing team kept cycling groups 1/3/5. The camp damage gear change did not correct the route timing in local head-to-heads. Both candidates remain isolated; production source and ZIP remain at hashes `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. No live unranked match or upload occurred.


## Rows c673 route check (19 Oct 2026)

c673 made Rows Ryth skip gold-only camps and wait for a gem camp. It lost both sides to fresh c553 at 990 gems each (production finished at 1,012 and 1,056) despite going 2/2 against the synthetic Please-layout proxy. Reject it without a broad run: production already beat that proxy 2/2. This result suggests the two gold-only camp cycles in the archived replay can provide useful bridge income during gem-camp respawns; the next experiment should improve how the team rotates through available gem groups without removing all gold income. Production source/ZIP remain at `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`.


## Rows c674 retained as a local candidate (19 Oct 2026)

c674 lets Ren farm a safe separate gem camp on Rows, then follow Issac's objective when none is safe. Against six strong local opponents it matched c553 at 11/12 wins, while averaging 38.5 fewer opponent gems and finishing about 20 rounds sooner; the 24-opponent pool stayed 47/48 with no winner flips. The focused Please proxy remained 2/2 for both bots and the meta-core side-A loss remained, so this is only a local pace candidate, not a proven win upgrade. Retain the isolated source for future live validation. Its SHA-256 is `3693512863477E35192D40CD5EFE30A572ABACD0DADEB79346FD17A6AAE73E30`. Runs are listed in `bots/tungtungsahur/PLAN.md`. Production source/ZIP are unchanged; official unranked remains paused and the ten-win streak remains unverified.


## c675 broad local check (19 Oct 2026)

c675 combines c604 with c674's Rows Ren solo gem route. It matched c604 at 187/204 on the exact same six-strong, 17-map screen and at 631/680 on the 20-opponent default pool, with no winner changes. On the strong pool only Rows scores/finish times changed; non-Rows outcomes and finish rounds stayed exact. Keep it isolated as a local pace candidate, not a win-rate upgrade. The default run's one replay-write error was the `my-bot` Corners side-A match; a unique-directory retry confirmed the engine win 1,008–490 at r708 with zero crashes. See `summary-recovered.json` under the c675 default run for the corrected 680-game record. Production bot and ZIP are unchanged; unranked remains paused.


## Latest offline result: c680 Stampede core alert plus Issac side-camp route (19 Oct 2026)

c679's alert alone stayed 11/12 on the six strong local Stampede pool; it delayed the meta-core side-A loss but did not flip it. c680 added the safe Issac side-camp route for the first 150 rounds, including gold and low-strength wolf groups. It scored 12/12 in two identical runs. On all 17 maps versus the same six strong local proxies, c680 scored 188/204 vs c675's 187/204; the only changed winner was the targeted Stampede side-A game, from 0–720 at r913 to a 900–720 win at r1761.

This remains an offline proxy result, not a win against Univardisty's live bot. Production c553 and its ZIP are unchanged. Official unranked matches/uploads remain paused; the 10-win live streak remains 0/10. Full hashes and run paths are in `bots/tungtungsahur/PLAN.md`.


## Prior handoff state before v101 upload (19 Oct 2026)

User instruction: keep official unranked bot work paused and continue independently. Local simulations and read-only ranked replay analysis only; do not create groups, submit versions, or upload. The latest 06:12 UK ladder snapshot has 689 teams: Fish #1 (2294.7), Mite #2 (2046.9), Sneaky Bush Campers #3 (2025.2), Nyx #4 (2020.5), Univardisty #5 (1999.7), and Pantheon #10 (1925.1). The refreshed top-five ranked match lists now replace the 06:04 aliases in `analysis/`.

Fresh Stampede replays show why a high camp-clear count can still lose: Univardisty made 16 camp clears but had zero camp-gem collection; its 360 submitted gems came from Ren killing Pantheon's Stellar while she carried 360. Pantheon then recovered, repeatedly collected, and banked 1,080. In a separate Fish–Boost Stampede, Fish Stellar collected and submitted all 1,080, with four kills and no deaths. These point to safe gem carrying and repeat deposits as the core; see `analysis/top50-evaluation-20261019.md` and `analysis/maps.md`.

Best current local candidate: c686, a Stampede-only Stellar queue of Power Focus / Durability Health / Power Focus, added on the c684 base. It scored 633/680 across 17 maps and 20 local opponents, two wins above c675, plus 39/40 in two default Stampede runs and 12/12 on the six-strong Stampede screen. The full Fish queue fell to 8/12 strong. A core-only durability gate scored 37/40 default; a side-B-only gate scored 11/12 strong. Keep c686 isolated; no live top-50 bot has been tested with it.

Production `bots/tungtungsahur/src/bot.cpp` and `submissions/tungtungsahur.zip` remain unchanged at SHA-256 `3AE6567BCDD1915CD8A6043A5E070543620114766DB0AFF2596522006883E0B6` and `2E3C6592DD28BC585B38D5E32327D79F4610429025205FF93E5B6CBE9A83E8EA`. The requested live goal remains 10 consecutive official wins; verified streak is 0/10 because official matches remain paused.


## v101 test upload and next live validation (19 Oct 2026)

c686, the best current local candidate, was uploaded successfully as test version v101. Its separate
bundle is `submissions/tungtungsahur-test-c686-stampede.zip`, SHA-256
`B2920032530E5AA9D2124D5296C2D6C967B6ADEF03BF2EC783BBD8D3D0BD252A`; the source hash is
`7E2E74D1C4E0BBDECAB5726AE50BB293B62F159EC68B6DC2B89E5165200F6DB3`. The existing
`dbdcc65c-cb2f-4b28-850b-5fa691da9e34` group is stale and tests v60 against then-rank-5 new team(4).
No v101 group exists yet. Browser automation tools are not exposed in the current session, and the
attempt to open the match-group page was rejected by the desktop command guard. A fresh unranked group
using v101 against a current top-50 opponent is the next required step. Production source and ZIP are
still unchanged; the official 10-win streak remains 0/10.


## 21 October 2026: uploaded rules/API update and skill setup

The user added updated `GameRules.md` and `BotAPICpp (1).md` on 21 October. The handbook adds Golem and
Heart of Ruin, updates camp/champion values, gives Vesper +33% gold and Prism +1.5 Focus per carried gem,
sets Monolith range to 5, and says altar locks take five basic attacks to remove. These conflict with
the local 14 October runner, SDK header, and older `analysis/mechanics.md`; local league results, v101,
and the 17 October map economy tables are historical until the toolchain and maps are refreshed. The
new API documents camp-state variants/timers and visible awake/asleep camp masks; the old API export
already had `camp_group.state()`, but did not explain the variants as fully. `champion.gem_count()` still
requires the target to be visible.

Added project-scoped Claude Code skills under `.claude/skills/`: `cambc-strategy`,
`game-state-analyser`, `strategy-planner`, `opponent-modeler`, `replay-reviewer`, and
`meta-equipment-analyst`. Existing third-party skills reviewed were not suitable for match optimization.
No external plugin, dependency, bot build, match, or submission was performed. Claude Code is installed
as v2.1.177; the skill files are on disk, but slash-command discovery was not runtime-tested from this
Codex session. Open/restart Claude Code in the repository to load them.

The detailed future-game strategy and equipment review is `analysis/game-update-20261021-strategy.md`.
Production source and ZIP remain unchanged; official unranked work stays paused, and the live streak
remains 0/10.
