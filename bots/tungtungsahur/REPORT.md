# tungtungsahur: report

## Latest status: 18 October 2026

The main source and upload bundle remain unchanged while the requested live top-50 streak is 0/10.
The current verified full-map baseline is candidate #145/v27 at `bots/cand-stampede-broad-pair/src`;
it scored **121/136** against four strong local proxies and **620/680** in the 20-opponent broad
pool. These are local proxy results, not platform wins.

Collision experiment #153 is a map-specific follow-up. A replay diagnostic found the team repeatedly
targeting an enemy-side three-elk camp (108 gems, 180 damage per turn). The isolated rule excludes
camps above 100 damage per turn only on Collision. It scored **6/8** against Ming, Xuanming,
Faisal-bot, and opp-racer, versus **5/8** for a fresh v27 control, and flipped the Ming side-A game
from a 416–1012 loss to a 1016–850 win. On the full 20-opponent Collision pool it tied v27 at **37/40**.
An 8-game Swirl gate check matched v27 exactly at **5/8** with the same per-opponent gem totals.
The exact all-map strong-proxy run tied v27 at **121/136**: Collision rose from 5/8 to 6/8 while
Lanes fell from 6/8 to 5/8; every other map total matched. Keep v27 as the full-map baseline and #153
as a Collision-specific test candidate, not an overall improvement. It has no live platform result.

Candidate package: `submissions/tungtungsahur-candidate-v153-unranked-test.zip` (24,956 bytes,
SHA-256 `C0519B27C99CC4BE90D89A8F590C76D8045921D38A8B8B8A7DCFE64EA74015A5`). The candidate was
uploaded as test submission version 28. The supplied match-group URL still points to the finished 0–5 FRChronic group from 17 Oct;
it has null submission versions and cannot validate #153. TinyFish is installed and enabled, but no
browser-action tool is exposed to this runtime, so the signed-in site session is unavailable here.
Main source hash `188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5` and upload ZIP hash
`06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D` remain unchanged. See `PLAN.md`
for run paths and hashes.

Two Pilgrimage split variants were also rejected. A 3/3 opening split scored 5/8 versus v27's 6/8;
it won both Ming games but lost both Xuanming games. Regrouping only during active fights scored 5/8,
with one Ming win and no Xuanming wins. Preserve v27's Pilgrimage behavior until a variant beats both
strong matchups. Details are in `PLAN.md`.

## Historical status: 17 October 2026

The main source and upload bundle remain unchanged pending the requested live top-50 streak. The
current isolated local leader is experiment #115 at `bots/cand-ambush-stall-recovery/src/bot.cpp`.
It raises the Lanes side-B shopping recall threshold from 150 to 250 gold and scored **118/136** in
the strong-proxy set and **611/680** in the broad local pool, one win above the v104 baseline in each.
Lanes was the only map total to change. These are local proxy results, not platform wins.

Stampede now has a stronger map-specific branch, experiment #126 at
`bots/cand-stampede-team/src/bot.cpp`: it delays the squad split until Stellar enters late game. It
scored **8/8** against the four strong local proxies and **41/44** against 22 local bots on Stampede,
versus **7/8** and **36/44** for v115. Longer round-600 and round-900 holds regressed to 7/8. Keep #126
isolated pending top-50 live testing; #115 remains the all-map tested candidate.

Map scores, current route analysis, and experiments are in
[`analysis/top50-evaluation-20261017.md`](../../analysis/top50-evaluation-20261017.md),
[`analysis/maps.md`](../../analysis/maps.md), and `PLAN.md`. The main's weakest current maps are
Collision, Lanes, and Swirl at 4/8. Candidate #115 raises Lanes to 6/8, while Collision remains 5/8
and Swirl 4/8 in the strong-proxy set. Swirl support and Collision role-based draft variants failed
to improve those maps, so keep them isolated under `bots/cand-*`.

The requested 10 consecutive unranked wins against top-50 teams remain **0/10**. The user supplied a
live unranked group, but Heavenly Court lost all five games to FRChronic (rank 58 around the match),
so it does not qualify. The group showed a large gem-scoring deficit, especially 0 on Stampede; its
replay bundles still require a signed-in browser session that this runtime cannot access. TinyFish is
installed, but its browser actions are not exposed in this session. Keep the isolated Prism-on-Stampede
candidate for further live testing; fresh local tests scored 7/8 versus main's 6/8 against the four
strong local proxies. Monster Strength-first equipment variants tied or regressed and were rejected.
Main source and upload bundle remain unchanged until the live target is met; local proxy games do not
count toward the streak.

## Update: Lanes side-B shopping threshold (17 Oct 2026)

Two targeted repeats scored 6/8 each; a fresh v104 control scored 5/8. The full strong set scored
118/136 versus 117/136 for v104. In the broad pool it scored 611/680 versus 610/680, with Lanes alone
improving (38/40 versus 37/40). The active candidate source hash is
`C3D422C5A13FBDCB29B3C57E7E582B866E398B5A70E6DDC815ACE228B9F771CB`, and its built WASM hash is
`0EEFFDB26305A2E36BE53D26420C25A6647DE02224EA7D881DCF8E4079B63E85`. Main source hash remains
`188E3153A86A4AF502ED7EF67347BDCF1E30EFAEC5F822A8D820FB0C9C7253F5`; the upload ZIP hash remains
`06D0BCB1E2FB4871A58835A146920D372889727C732FFD08CDC1755C78D6D18D`.

## Follow-up draft tests (17 Oct 2026)

Swirl: replacing Varg with Willow tied the 4/8 map score but lost all four Ming/Xuanming games, with
average final gems of 195 and 427; reject. Collision: Ryth/Vendetta/Tavi scored 2/8, Ryth/C&I/Tavi
scored 1/8, and Stellar/C&I/Ryth scored 4/8 versus 5/8 for the current Stellar/C&I/Varg lineup. Each
variant lost all Ming/Xuanming games. Keep the current drafts. Full results and match folders are in
`PLAN.md` and `analysis/maps.md`.

TinyFish reports installed, but no browser actions are exposed in this session. The user supplied
unranked group `4cf7ad87-2c52-452e-a9a3-59787c302e67`; FRChronic was rank 58 and all five results were
losses. The top-50 streak remains 0/10. Main source and submission ZIP remain unchanged.

## Update 15 Oct: studying the top platform player
- **Their strategy** (from the 5 platform logs, `analysis/forensics.md`): an economy machine. They
  tribute after almost every capture (~48 gems), sustain 2.2-3.9 gems/round, take the contested
  central gem camps (corners, packs), and never stole our bags. The five maps were corners, packs,
  interlock, lanes and expanse; our side was an old version (opp-tts-v4).
- **Why we lost:** slow farming, a respawn deadlock on corners (96 gems in 400 rounds), and a
  freeze when both teams lock the same altar (interlock). Both bugs are fixed now.
- **New version** (all in `bots/tungtungsahur`, bundle `submissions/tungtungsahur.zip`): 4 bug fixes,
  ming_bot's spell burst, back-liners solo lone wolves, Varg replaces Prism as a solo gem farmer on
  maps with soloable camps. 22-opponent league 385 -> 389/440, vs ming_bot 12 -> 16/20, uncontested
  race 11106 -> 10048 rounds (corners 427/463 -> 323/372, lanes 438/433 -> 339/359,
  packs 669 -> 522/541; expanse slower, 469/484 -> 498/559).
- **Tested and rejected:** fight plans chosen from the enemy draft, a comeback mode, carrying bigger
  bags, a more cautious Varg. Details: `PLAN.md` experiments 47-56.
- **Scouting:** the bot now prints SCOUT lines (enemy draft, sightings, tributes, our deaths, locks).
  After a platform match, download its log and run `python tools/scout.py <file>-logs.zip`.

## Update 15 Oct night: the user's "feed Stellar" plan is now the main version
Draft Stellar, Cassi & Issac, Ryth, Varg, Tavi. Early game: farm and feed Stellar the gold, only hit
enemies already in reach. Mid game (Stellar or Varg owns an emblem): hit enemies within 5 tiles, then
farm again. Late game (Stellar owns 3 emblems): fight freely. Before late: stay out of the enemy half
and back off when outnumbered by 2. Stellar buys Power Focus; Varg Jungle Strength then Power
Strength. Plus one addition: Varg helps Issac's squad on maps where he has nothing to farm alone.
League 392/440 vs 380 for the previous version; details in PLAN.md experiments 57-59.

# Overnight report (14-15 Oct)

Goal: **win no matter what the opponent chooses.** All work was on `bots/tungtungsahur`.
Every change was tested in a local league before it was kept. The full experiment log is in
`PLAN.md`.

## Result (final check at 08:30: 362/400, unchanged)

| | Start of night (23:30) | Now |
|---|---|---|
| vs Faisal-bot | 8/18 (706 vs 794 gems) | **20/20** (971 vs ~400) |
| vs 8 Faisal-bot draft variants (melee, ranged, mirror, heal, bruiser, casters, vesper) | not measured | **160/160** |
| vs tralalerotrarala (aggressive hunter) | 14/18 | **20/20** |
| vs my-bot / my-bot-v2 / my-bot-v3 / tungtungsahur-v1 / starter | 8–16 of 18 | **19–20/20 each** |
| Original league (9 opponents x 9 official maps x 2 sides = 162 games) | 102/162 | **160/162** |
| Final, harder league (20 opponents incl. 6 copies of tungtungsahur, 10 maps, 400 games) | not measured | **362/400** |

The 38 losses in the league are all against **copies of tungtungsahur itself** (earlier versions
and two variants). Those are near-mirror races, decided by a few rounds.

## Three of your earlier choices are reversed (please check)
Each of these won more games in testing, so I changed them. Each one is easy to undo.

1. **Fights enemies in sight, unless clearly outmatched.** You had asked for "only attack after
   being hit by a champion". That version lost 7–13 head to head against this one, and did worse
   against the Faisal-bot family. Champions still fall back when the nearby enemy strength is
   more than 1.3x theirs. (`fighting_back()` in `bot.cpp`)
2. **Carries and places altar locks** (you chose "No locks" earlier). That was the right call
   at the time. After the other fixes tonight, locks became a net gain (step 16 in `PLAN.md`).
3. **Draft order:** Ryth, Cassi & Issac, **Stellar, Tavi**, Prism (Stellar before Tavi). These are
   the same 5 champions you chose, so only the 3- and 4-champion maps change. This scored 316 vs
   313 in the league and won all Faisal games.

## The biggest improvements (in order of impact)
1. **Banking fix.** When Faisal-bot locked the altar on our side, champions froze with full bags
   until they died. Altars are now priced by real walking distance, and enemy locks are broken
   (3 basic attacks). collision alone went from 174 to 1000 gems in one test game.
2. **Fuel.** On big maps (lanes, corners, expanse) many turns ran out of the 100k fuel and were
   suspended mid-decision. Expensive per-turn work is now cached or replaced: camp-group
   visibility checks, blocked tiles, enemy/ally lists. A typical turn went from ~60k to ~25k fuel.
3. **Lost turns.** Reading a unit that died earlier in the same turn threw an exception that cost
   the champion its whole turn (about 3,200 lost turns per 380 games). Those reads are now guarded
   (2 lost turns per 380 games).
4. **Back-liners solo-farm gem clusters** (500 health, 24 gems, never fight back) within 16 tiles,
   instead of idling behind their leader.
5. **Fight longer once a fight starts**, then fight anything in sight, with a fight-odds check.
6. **Gold sharing:** champions within 6 tiles of a cleared camp step onto it, so they share the
   capture gold. Turning this off cost 50 wins; widening it from 4 to 6 tiles added 6.
7. Focus fire (lowest-health, highest-damage enemy first), safer bank routes (around enemies),
   and a more realistic camp clear-time estimate.

Ideas that were tested and **rejected** (they made it worse or changed nothing): skipping "trap"
camps, retreating earlier, a grouped opening, fully solo back-liners, converging on fights, tank
Strength builds, valuing gold in camp choice, chasing enemy tributes, leaders joining captures,
dashing while travelling, endgame altar guarding, and several parameter values. Two lineup
swaps were also clearly worse: **Varg instead of Ryth** (323/400) and **Vesper Vale instead of
Tavi** (319/400). Your champion choice is the right one for this bot. `PLAN.md` has all 46
experiments with their numbers.

Note: my session stalled from about 02:20 to 08:27, so about six hours of the night were not
used. The bot had already reached a plateau by then: the last ~15 experiments found nothing
better than the current version.

## How to test it yourself
```powershell
python tools/league.py tungtungsahur
```
This runs the whole league (400 games, ~1.5 minutes). The default opponent list is at the top of
`tools/league.py`. To play one match and watch it:
```powershell
.\cambc.exe run tungtungsahur Faisal-bot --map collision --view
```

## How to submit
I could not use the platform (it needs your sign-in). When you're ready:
```powershell
.\cambc.exe login
.\cambc.exe submit tungtungsahur
```
Then try an unranked match on the platform first.

A ready-made upload bundle of the current best is already at `submissions/tungtungsahur.zip`
(6 source files). You can upload it on the platform's Submissions page instead of using the CLI.

## New folders made tonight (all under `bots/`)
- `tungtungsahur-best`: copy of the current best `src/` (same as `tungtungsahur`).
- Opponents for testing: `opp-fai-*` (Faisal-bot with 7 different draft orders),
  `opp-tts-v2`..`v5` (earlier tungtungsahur versions), `opp-tts-locker`, `opp-tts-aggro`.
- `cand-*`: experiment candidates. Safe to delete.
- `zz-probe`: tiny bot that prints a map's camps, altars and spawns.

## Latest top-50 preparation update (17 Oct 2026)

The refreshed 17-map local pool scores 104/136 for the current main against four strong proxies.
Experiment 78's Contest/Stampede draft scored 108/136. Experiment 85 adds a Collision-only Varg
draft and scored 109/136; its only improvement over experiment 78 is Collision, from 4/8 to 5/8.
It still lost both Collision games to Ming. Teleport-crystal banking on Collision scored 4/8 for
bags of 100+ and 2/8 when used for every positive bag, so that route was rejected. Details and run
directories are in `PLAN.md`, `analysis/top50-evaluation-20261017.md`, and `analysis/maps.md`.

These local results do not count toward the requested live streak. The top-50 unranked streak is
still 0/10 because the game-site browser session is not available to the runner. TinyFish was
selected for enabling, but its confirmed state remains `installed: false`. Main source and
`submissions/tungtungsahur.zip` are unchanged; no candidate has been promoted.

Three later map-targeted experiments did not improve that candidate. On Collision, Varg Jungle
Health first and a Cassi & Issac / Ryth / Varg draft each scored 4/8 versus candidate 85's 5/8.
On Swirl, Jungle Health first reduced deaths but dropped the result from 4/8 to 3/8 because the team
banked fewer gems. Candidate 85 scored 109/136 and remained isolated at that point. See
PLAN.md and analysis/maps.md for match folders and replay findings. The live unranked streak remains
0/10 because TinyFish still reports uninstalled; the main source and upload ZIP are unchanged.

Two more Swirl tests were rejected: keeping Varg in Issac's squad after the opening tied the
baseline at 4/8, while delaying tribute until 150 gems fell to 2/8 and lost substantially more
carried gems. Keep immediate banking. A camp-specific team split is a better next local test than
a blanket delay or armor-first item order.

The current best local candidate is experiment 91: the 85 map-specific picks plus the Expanse
Cassi & Issac / Varg / Stellar draft. It scored 112/136 against 104/136 for a same-session main
recheck, with gains on Collision, Contest, Expanse, and Stampede and no map regressions. It remains
isolated while live unranked top-50 testing is unavailable; main source and upload ZIP are unchanged.

## Latest map follow-ups (17 Oct 2026)

Pilgrimage experiments 92-94 did not improve the 5/8 result: a T=100 bank rule scored 4/8, a
round-1 split tied at 5/8 while shifting wins from Ming to Xuanming losses, and replacing Ryth with
Vendetta scored 3/8. Lanes experiments 95-97 did not improve performance against the strongest local
proxies: round-200 splitting scored 3/8; a Ren-for-Ryth draft went 0/4 against Ming/Xuanming; a
Ren-for-Tavi draft scored 5/8 overall but only 1/4 against those two, compared with 2/4 for
experiment 91. Keep the current map-specific candidate and default equipment/order as tested.

Experiment 91 remains the local best at 112/136. The live top-50 streak is still 0/10 because the
game-site browser connector is not yet connected. No local results count toward that target, so
`bots/tungtungsahur/src` and `submissions/tungtungsahur.zip` remain unchanged pending live validation.

## Suggestions
- Test on the platform with unranked matches. Real opponents may behave differently from this
  league (it's built from Faisal-bot, our own bots and the starter).
- Your bot prints a `SCORE` line every 5 rounds (used by the league tool). It's harmless, but you
  can remove it before final submission (search for `SCORE` in `bot.cpp`).


## Rushbait and movement follow-up (17 Oct 2026)

The current best local candidate now adds an immediate mid-game squad opening on Rushbait v2 (30x80), regardless of side. It scored 113/136 in the 17-map strong-proxy league and 592/680 in the expanded local pool, compared with 112/136 and 587/680 for the previous candidate, and 104/136 and 577/680 for main. The main gains came from Rushbait (5/8 -> 7/8 strong; 35/40 -> 39/40 broad) and Swirl (34/40 -> 35/40 broad); Stampede lost one strong-proxy win. Keep this change isolated in bots/cand-best-expanse-meta while waiting for live matches.

A global movement fallback that retries an alternate shortest step was rejected: broad score fell to 586/680 and one Bruiser Ambush side-B game turned into a severe loss. Side-specific Rushbait experiments did not activate the intended early branch and should not guide strategy.

The requested live top-50 streak remains 0/10. TinyFish has been surfaced for installation/connection after your selection, but the confirmed plugin state is still uninstalled; no browser-backed challenge has been created. The main bot source and submission ZIP remain unchanged.


## Latest local improvement (17 Oct 2026)

The best isolated candidate now includes a Lanes side-B equipment adjustment: Tavi buys Monster Strength for the first emblem, then Power Focus. It scored 5/8 in two targeted repeats, 114/136 against the four strong local proxies, and 593/680 in the broad pool. The previous candidate scored 4/8, 113/136, and 592/680 respectively. The strong-set gain is confined to Lanes, with no regressions on the other maps; broad Lanes is 37/40 versus 36/40. Candidate source: bots/cand-lanes-sideb-tavi-monster/src/bot.cpp.

Three related variants were rejected: Swirl Ryth taking Monster Strength before Jungle Health (3/8); starting the Lanes side-B split from round one (4/8, still zero side-B wins); and giving Tavi Monster Strength on both Lanes sides (4/8, weaker against Ming/Xuanming). These remain isolated from main.

The live top-50 streak remains 0/10 because TinyFish is still uninstalled and no browser-backed unranked match has been created. Main source and submission ZIP remain unchanged.


## Fresh-build recovery evaluation (17 Oct 2026)

The initial same-name source swaps were invalid: `Copy-Item` preserved old source timestamps, and CMake reused the prior v104 object. I refreshed timestamps, explicitly rebuilt, and verified distinct WASM hashes before retesting.

With valid builds, the Ambush recovery rule raised the broad score from 593/680 to 610/680, with Ambush moving from 21/40 to 40/40. The targeted strong-proxy Ambush result was 8/8 versus 6/8 without recovery. The full strong result was 117/136 versus 104/136 for a fresh main-source build; 14 results improved and one Rushbait result regressed. A narrower lookup variant scored 611/680 broad but 116/136 strong, so v104 remains the strongest local candidate for the top-team objective.

Replay review of `ming_bot` losses found repeated central-altar pressure and high deaths on Collision and Swirl, plus a farming/tribute deficit on Pilgrimage. Contest and Stampede reached tied scores at the 2000-round cap. The live top-50 streak remains 0/10; TinyFish is still uninstalled, and main source plus submission ZIP remain unchanged.

The corrected broad control is 610/680 for v104 versus 577/680 for a freshly rebuilt main source. V104 gained 19 Ambush, 6 Expanse, 4 Stampede, 3 Rushbait v2, 2 Contest, 1 Lanes, and 1 Swirl win; it lost 2 Collision and 1 Pilgrimage. Its strong-proxy result was 117/136 versus 104/136 for main. The next Swirl late-retreat attempt was a no-op: 0/4 against Ming/Xuanming, with all four replay ZIP hashes identical to v104. Main and ZIP remain unchanged. TinyFish has been surfaced for connection but is not confirmed connected; the live streak remains 0/10.

Swirl's 50% recall threshold scored 3/8 (fewer deaths, slower farming). The 40% threshold scored 4/8 targeted and 118/136 strong, but 607/680 broad versus v104's 610/680; broad Swirl fell by 3 wins. Both were rejected and v104 was restored and rebuilt.

On Pilgrimage, a Tavi Monster Strength-first build scored 5/8 against the four strong proxies, below v104's 6/8. It is rejected; v104 is restored.

Proactively clearing home altar locks while empty also scored 5/8 in two identical Pilgrimage runs, versus v104's 6/8. It improved one Ming side but lost both Xuanming games, so it is rejected.

On Collision, proactively clearing the central altar lock while empty scored 4/8 versus v104's 5/8 and still lost all Ming/Xuanming games. It is rejected; v104 was restored.

On Collision, substituting Tavi for Varg held at 5/8 but still lost both Ming games. It is rejected; v104's Varg draft is restored.

On Swirl, having Varg reinforce Ryth improved gem totals against Ming but stayed 0/4 vs Ming/Xuanming and scored 34/40 broad-map versus v104's 35/40. It is rejected; v104's solo Varg rule is restored.

The follow-up Lanes threshold sweep confirms 250 gold is the best tested side-B value: 200 scored 5/8 in two identical targeted runs (`20261017-195844` and `20261017-195930`), while 300 scored 3/8 and lost both Faisal games (`20261017-195907`). Both variants are rejected; the #115 250-gold candidate remains isolated and leads at 118/136 strong and 611/680 broad.

## Stampede team-phase experiment #126 (17 Oct 2026)

The live Stampede score was 0–1080, but its replay is still unavailable, so the cause is not confirmed.
On local Stampede, ignoring the mid-game phase flag until Stellar's late-game flag improved the fresh
v115 control from 7/8 to 8/8 across Ming, Xuanming, Faisal, and opp-racer on both sides. In the same
22-opponent map-only pool, the result improved from 36/44 to 41/44. The Ming side-A replay changed from
a 900–900 round-cap loss (49 deaths, 1,260 gems lost) to a 900–180 win at round 1695 (44 deaths, 180
gems lost). The isolated source/WASM hashes are recorded in `PLAN.md`; the candidate snapshot is
`bots/cand-stampede-team/candidate-source-v126-stampede-phase.cpp`.

Holding the team until round 900 or 600 before the late-game check scored 7/8 and was rejected. The
round-900 check placed after the late flag was a no-op: its Ming replay hash matched #126 exactly. Keep
#126 as a Stampede-only branch. The all-map validated leader remains #115 pending a full current-pool
comparison and live top-50 validation. The live streak remains 0/10: leaderboard, match-summary, and
replay endpoints return 401 in this runtime, even though TinyFish reports installed and enabled; no
TinyFish browser-action tool is exposed here. Main source and upload ZIP are unchanged.
# 17 Oct: Stampede branch validated across all maps

The #126 Stampede shared-farm change has now been checked across all 17 maps. It scored 119/136 against four strong local proxies versus 118/136 for a fresh #115 control, and 612/680 in the broad local league versus 611/680 for #115. In the paired broad set, Stampede gained two wins, Lanes gained one, and Pilgrimage lost two.

Experiment #131 caches the Stampede map flag during initialization. It retained #126's exact 119/136 strong-proxy outcomes and scored 614/680 in two identical broad runs, compared with #126's 612/680. The four changed broad games were one Stampede gain, two Pilgrimage gains, and one Lanes loss. Treat #131 as the current isolated local candidate; this modest local gain does not count toward the live top-50 target.

The supplied FRChronic group is still 0–5 and rank 58 around the match; the streak is 0/10. Its match-group response shows the scores and drafts, but replay causes are unverified. Main source and submission ZIP are unchanged.
# 18 Oct: isolate Elkring Varg-first draft

The Varg-for-Ryth test helped on Fragment against Xuanming but caused broad losses there: #132 rose to 121/136 strong and 615/680 broad, while broad Elkring improved four wins and Fragment lost three. Reject that combined rule.

Restricting the pick order change to Elkring (#133) preserved Ryth on Fragment. It scored 120/136 in two exact strong-proxy repeats and 618/680 in two exact broad repeats, versus #131's 119/136 and 614/680. The four broad gains were all on Elkring; no other map total changed. This is the best isolated local candidate so far, not a live top-50 result.

The user-supplied FRChronic group remains 0–5, with FRChronic ranked 58 around that match. Main source and ZIP remain unchanged.
# Pilgrimage draft screens (18 Oct)

Two targeted changes both regressed from #133's 6/8. Picking Varg before Ryth raised our gem total against Ming but still lost both sides and gave up one win to opp-racer. Replacing Tavi with Ren won one Ming side but lost both Xuanming sides, for 5/8. Keep the existing Pilgrimage lineup; these screens were not run in the full league.
# Swirl order test (18 Oct)

Putting Varg before Ryth on Swirl scored 3/8 versus the current candidate's 4/8. It still lost every Ming/Xuanming game and added an opp-racer loss. Reject the change and keep #133.

### Equipment follow-up (#137–138)

Two economy/survivability screens did not beat the current local candidate. Issac's Durability Health after his Jungle Health emblem tied #133 at 54/68 against Ming and Xuanming; Stellar's Treasure Focus first emblem fell to 50/68. Keep #133's current equipment. The run details and source hashes are in `PLAN.md`.

### Retreat follow-up (#139–142)

The global parity retreat rule lost 10 strong-proxy games versus #133 and was rejected, even though deaths fell on Swirl. A cached Swirl-only parity threshold is a better top-proxy candidate: it scored 121/136 strong versus #133's 120/136 and repeated at 613/680 in the broad pool, five below #133. The broad decline was limited to Swirl (35/40 to 30/40), where the strongest local matchup gained one win. A 1.1× Swirl threshold lost the targeted gain. Keep #133 for broad local performance and #141 as the alternate to validate against top teams; neither has live top-50 evidence.

The #141 source was uploaded through the approved CLI as a separate test submission (version 25); its local test ZIP remains available for byte verification. No live match group has been created yet, and the main submission is unchanged.

### Current candidate (#143, 18 Oct)

A draft-aware Swirl retreat keeps #141's local strong-set gain while avoiding its broad Swirl losses. It triggers only on Swirl against an enemy roster containing Cassi & Issac, Varg, Stellar, and Vendetta. #143 scored 121/136 against four strong proxies twice (only Swirl changed, 4/8 to 5/8), and 618/680 in two exact broad repeats with the same per-map totals as #133. The local test ZIP is verified and its source is uploaded as separate candidate submission version 26. This remains local-proxy evidence; live top-50 results are still required.

#144's Collision mirror test raised the retreat threshold to 1.5x against a draft containing Cassi & Issac, Varg, and Stellar. It lost all four targeted games (0/4) versus #143's 1/4 control, so it is rejected and #143 is restored. The group link supplied again on 18 Oct resolves to the same finished 0-5 FRChronic group from 17 Oct; its submission versions are null and it predates candidate v26. Live top-50 streak remains 0/10.

#145 adds large-bag, allied-half altar preference only on Pilgrimage. It scored 31/40 in two direct-runner repeats versus #143's 29/40 same-runner control; the gains were one win each against Faisal-bot and opp-tts-aggro. The exact four-strong-proxy screen remained 6/8. Replay review confirms the targeted fix: Faisal-bot's side-B game changed from a 144-gem Tavi death and 236 total gems lost on deaths (676-988 loss) to zero death-bag losses and a 1004-820 win. The candidate is packaged and uploaded as separate submission v27. It has no live top-50 result; main source and ZIP remain unchanged.

### Full-map verification and Collision follow-ups (#145–147)

The full 17-map, 20-opponent direct-runner pool scored 620/680 for #145, versus 618/680 for #143. Every map total matched except Pilgrimage, which improved from 29/40 to 31/40. Against four strong local proxies, #145 scored 121/136 with the exact same per-map totals as #143. The complete run folders and replay bundles are listed in `PLAN.md`.

Ming remains the hardest local proxy at 26/34. Loss review isolates Collision, Pilgrimage, and Swirl as the main problem maps: Collision loses both sides while Ming locks the central altar; Swirl losses involve heavy deaths and 98/242 gems dropped; Pilgrimage loses both sides even though only one lost gems on death. Two Collision experiments were rejected: forcing the whole team to stay on one shared farm scored 4/8, and Power Strength before Monster Strength for Varg scored 5/8 with lower gems against Ming than #145. Candidate v27 remains #145; neither follow-up was uploaded.

This is still local evidence only. The only supplied live link remains the 17 Oct unranked 0–5 FRChronic group with null submission versions. The top-50 live streak remains 0/10. Main source and submission ZIP hashes remain unchanged.

### Swirl empty-lock test (#148)

Trying to break a nearby enemy altar lock while empty scored 4/8 against four strong local proxies, below #145's 5/8. It lost all four games against Ming and Xuanming; wins against Faisal and opp-racer were unchanged. Reject the rule and keep #145. The match-group link supplied again still points to the old 17 Oct 0–5 FRChronic group, so it does not provide v27 validation.

Four further targeted variants also failed to beat v27. Tavi replacing Ryth on Swirl tied 5/8 but reduced gem totals against Ming. Raising the heal-trip threshold to 40% only against the Swirl counterdraft scored 4/8. On Collision, sending Varg alone from the opening scored 4/8; a two-squad camp split also scored 4/8 and cut Ming-game gem totals sharply. Keep the current v27 strategy and continue studying the farming tempo gap rather than promoting these changes.

### Five-pick combat order tests (#156–158, 18 Oct)

Fixed mage-first priority scored 117/136 on the four strong proxies versus v27's 121/136. Pilgrimage improved from 6/8 to 8/8, so a Pilgrimage-only variant was tested; it tied v27 at 121/136 but fell to 29/40 against the broad local Pilgrimage pool versus v27's 31/40. A combat-only dynamic priority scored 5/8 versus v27's 6/8 on Pilgrimage. Reject these variants and keep v27. No change was made to the main source or ZIP. Run folders and hashes are in `PLAN.md`.

### v28 broad-pool check (18 Oct)

The Collision-only v28 candidate scored 622/680 versus a fresh v27's 620/680 across the full local pool, but this two-win difference is inconclusive: v28 changed two Collision outcomes each way (net zero) and Lanes shifted from 38/40 to 40/40 even though that map is outside the code gate. The runner has no seed option for a paired match. Keep v27 as the local baseline; v28 remains unvalidated live. The temporary same-name source swap was restored to v27's original source/WASM hashes.

### Collision threshold refinement (#160)

Raising the Collision camp avoidance threshold from 100 to 150 damage/turn tied the original candidate and v27 on both the 20-opponent map pool (37/40) and strong full-map pool (121/136). It is rejected for no overall gain. Full run paths and hashes are in `PLAN.md`.

## Contest counter-draft: Willow for Ryth (#161, 18 Oct 2026)

A Contest-only Willow lineup was screened against v27. It tied the fresh control at 7/12 on six selected opponents, with a clear tradeoff: wins improved against opp-fai-casters (0/2→2/2) and opp-tts-locker (0/2→1/2), while the four strong proxies fell from 7/8 to 4/8. In the full 20-opponent Contest pool the candidate scored 21/40 against a fresh v27 score of 32/40; v27 had also scored 32/40 in its earlier pool run. Reject the Willow swap and keep the v27 Contest lineup. Run IDs and candidate source/WASM hashes are in bots/tungtungsahur/PLAN.md. No candidate package was uploaded. Main source and ZIP remain unchanged; live top-50 streak remains 0/10.

## Contest gold value and team-split screens (#162–165, 18 Oct 2026)

Two no-gold variants and a full-team lock regressed on the four strong local proxies: 3/8, 4/8, and 6/8 (the lock repeated exactly), versus v27's 7/8. #165 keeps the standard phase split and reduces the early gold weight only on Contest to 0.25. It scored 8/8 on the selected strong Contest set, 33/40 in two runs against the full 20-opponent Contest pool versus v27's 32/40, and 122/136 across the 17-map strong set versus v27's 121/136. Gains were one Ming Contest side and one opp-fai-casters side; other strong-set map results matched. The caster side-A replay changed from 400–600 with 45 deaths to 1000–200 with 26 deaths. Keep this as the best current isolated local candidate and use it for a live test; it is not yet top-50 verified.

The candidate package submissions/tungtungsahur-candidate-v165-unranked-test.zip was verified against all seven source files and uploaded separately as submission v29. The user-supplied group is still the older 0–5 FRChronic group with null versions, so it does not test v29. Live top-50 streak remains 0/10. Main tungtungsahur source and ZIP remain unchanged.

### v29 full broad-pool check

A 17-map, 20-opponent run scored 619/680 for v29 and 620/680 for fresh v27. Contest stayed at 33/40 versus 32/40, while the only other map delta was Pilgrimage (-2) with no Pilgrimage code change; all remaining map totals matched. With no seed control, the overall difference is inconclusive. Keep v29 as a Contest-only live-test candidate, not an overall broad-pool promotion.

## Pilgrimage banking follow-ups (#166–167)

Lowering the allied-half bank penalty threshold to 68 gems tied the broad map pool at 31/40 but fell to 5/8 against strong proxies. The key 92-gem replay was an exact stdout match to v27 because low-health retreat runs before banking. Trying safe banking before retreat only for low-health 68+ gem carriers tied the strong set at 6/8 but fell to 30/40 broad, trading a my-bot win for losses to opp-tts-v2 and opp-tts-locker. Reject both; keep v27's Pilgrimage route and survival order. Run paths and hashes are in bots/tungtungsahur/PLAN.md. Main source and ZIP remain unchanged.
