# Current top-50 update and match review — 19 October 2026

## Snapshot

Using the isolated CAMBC 2.2.5 CLI, I refreshed the ladder at 06:12 UK time without creating a match.
The current snapshot [`top50-20261019-latest.json`](top50-20261019-latest.json) contains 50 of 689
teams and supersedes the earlier same-day read. The previous-day snapshot
[`top50-20261018-151904.json`](top50-20261018-151904.json) contained 50 of 618.

| Rank | Team | Rating |
|---:|---|---:|
| 1 | Intercontinental Fish | 2294.7 |
| 2 | Mite | 2046.9 |
| 3 | Sneaky Bush Campers | 2025.2 |
| 4 | Nyx | 2020.5 |
| 5 | Univardisty of Shingtonwash | 1999.7 |
| 6 | new team(4) | 1953.0 |
| 7 | procless | 1952.0 |
| 8 | Boost | 1950.9 |
| 9 | hello | 1937.1 |
| 10 | Pantheon | 1925.1 |

The archived "Please" opponent from older match reviews is not a current ladder display name.

## Recent results and drafts from the top three

The read-only `matches list` query returned 25 recent ranked map results per team, grouped into five
recent match groups. These are recent outcomes, not a season win rate. In the 06:12 snapshot,
Intercontinental Fish went 21–4, Mite 12–13, and Sneaky Bush Campers 13–12.

Draft counts below record champion appearances in those 25 map drafts. “First pick” means the team's
opening draft pick in that match.

| Team | Most common picks | First pick pattern |
|---|---|---|
| Intercontinental Fish | Stellar 25/25; Cassi & Issac 25/25; Ren 23/25; Ryth 17/25; Varg 12/25 | Stellar 23/25; Cassi & Issac 2/25 |
| Mite | Cassi & Issac 25/25; Stellar 21/25; Varg 19/25; Ryth 17/25; Ren 17/25 | Varg 19/25; Ren 4/25 |
| Sneaky Bush Campers | Stellar 24/25; Cassi & Issac 16/25; Tavi 15/25; Ren 15/25; Varg 13/25 | Ren 9/25; Cassi & Issac 7/25 |

The two highest-rated teams both use Cassi & Issac and Stellar in every recent map, but differ in
their first pick and their other three slots. That supports those champions as a common core, not a
single fixed lineup for every map. The current tungtungsahur draft already uses Cassi & Issac and
Stellar as its core and responds to visible Ren; the evidence still does not justify copying one
team's full draft unchanged. Latest raw lists: [Fish](top50-matches-20261019-latest-intercontinental-fish.json),
[Mite](top50-matches-20261019-latest-mite.json), [SBC](top50-matches-20261019-latest-sneaky-bush-campers.json),
[Nyx](top50-matches-20261019-latest-nyx.json), and
[Univardisty](top50-matches-20261019-latest-univardisty.json).

## Latest five-map groups in the 06:12 match lists

The top-five match-list refresh added two newer groups. Fish beat Sneaky Bush Campers 4–1 in
[group 44a73177-6cbd-477b-9e93-249198fd52d2](https://2026a.battlecode.co.uk/game/match-groups/44a73177-6cbd-477b-9e93-249198fd52d2),
winning Monolith, Rushbait v2, Fragment, and Eight and losing Pilgrimage. Boost beat Mite 3–2 in
[group 477f7092-fb70-42ed-aa45-34ee23daaf54](https://2026a.battlecode.co.uk/game/match-groups/477f7092-fb70-42ed-aa45-34ee23daaf54),
winning Corners, Swirl, and Interlock while Mite won Rushbait v2 and Packs. These are result-list
records; detailed converted replay summaries for these two groups have not been added.

## Earlier reviewed groups: Fish–Univardisty and Mite–Sneaky Bush Campers

The previously reviewed Fish group is [9bc92ff8-1a26-4676-9f08-060868eadd0e](https://2026a.battlecode.co.uk/game/match-groups/9bc92ff8-1a26-4676-9f08-060868eadd0e): Fish beat the current #5 Univardisty of Shingtonwash 4–1. Fish won Rushbait v2 (1,032–804), Interlock (1,026–392), Lanes (1,056–672), and Elkring (1,044–324); it lost Stampede 0–1,080. The Stampede loss was decisive at the macro level: Fish first cleared at r106 and banked no gems, with five camp-clear events and eight deaths. Univardisty first cleared at r19, made 17 clears, banked 1,080, and died twice. Their total monster damage was nearly equal (43.6k Fish, 42.8k Univardisty), so damage volume alone does not explain the failure. Fish drafted Stellar/Tavi/Prism/Cassi & Issac/Ren; Univardisty drafted Cassi & Issac/Stellar/Varg/Tavi/Ren.

The previously reviewed Mite group is [f84aa4ce-84e6-46c1-954c-27d66d67f4b2](https://2026a.battlecode.co.uk/game/match-groups/f84aa4ce-84e6-46c1-954c-27d66d67f4b2): Sneaky Bush Campers beat Mite 3–2. Mite won Pilgrimage (1,030–662) and Stampede (1,008–0); SBC won Rows (1,023–990), Corners (1,032–502), and Collision (1,012–804). Mite's Corners first clear was earlier (r11 vs r15), but SBC finished with 40 clears to Mite's 24, 11 kills to 3, and 4 deaths to 16. On Collision, Mite cleared more camps (45 vs 41) and collected slightly more gems (1,068 vs 1,056), yet banked 208 fewer after nine deaths versus two. The repeated pattern is that route progress must convert to protected deposits.

All ten converted summaries are saved as `match-summary-<match-id>.json` in this folder. The individual match IDs and map names are in the current match-list snapshots linked above.

## Earlier Fish–Mite series

The previously reviewed five-map group is [07e7aa43-8724-4689-88ae-fe299ccdb799](https://2026a.battlecode.co.uk/game/match-groups/07e7aa43-8724-4689-88ae-fe299ccdb799).
Intercontinental Fish beat Mite 3–2. Mite was recorded as Team A in all five replays, so this series
does not isolate side effects. Map results and replay-derived team totals:

| Map | Result | Gems submitted, Mite–Fish | Camp clears, Mite–Fish | Other signal |
|---|---|---:|---:|---|
| Corners (71×71) | Fish | 0–1,016 | 8–29 | Mite had 20 deaths and 1 kill; Fish had 1 death and 16 kills. Mite's first clear was r8, Fish's r18. |
| Contest (50×50) | Mite | 0–0 | 174–36 | At the 2,000-round limit, kills were 81–22, deaths 29–101, and earned gold 19,283–4,346. The API credits Mite with the win; the summary does not state its tie-break reason. |
| Elkring (30×30) | Fish | 792–1,008 | 26–27 | First clears were r10–r11. Mite collected 936; Fish collected 1,116. |
| Expanse (80×80) | Fish | 952–1,004 | 29–35 | Mite's first clear was r11 and Fish's r28; Fish later made six more clears and dealt 67.2k monster damage versus 61.4k. |
| Packs (31×31) | Mite | 1,052–884 | 22–21 | Mite collected 1,216 versus 1,092. Clear count and monster damage were nearly tied, so carrying and banking mattered. |

The clearest strategic signals are map-specific. Corners shows that a faster first clear does not help
if the team is wiped before it can bank; the winning Fish build paired damage items with health items.
On Expanse, Fish started slower but sustained more clears. Its four champions all ended with Monster
emblems followed by their Power stat. In Packs, Mite banked more despite Fish's slightly higher camp
clear and monster-damage totals. Contest was a combat-dominant match, not a gem race. These are
five observations from one fixed-side series, not universal map rules.

Full locally converted summaries for the five maps are saved as
[`Corners`](match-summary-92043a49-acde-4ac8-a4f3-8e31d89bd8c5.json),
[`Contest`](match-summary-e1a46715-5da6-4469-9ec8-a584610085a2.json),
[`Elkring`](match-summary-41ae4d40-0d12-48a3-a105-c74691a4cab9.json),
[`Expanse`](match-summary-f2f32a4f-c9cd-4417-b5d8-113ccb9eea10.json), and
[`Packs`](match-summary-99c111bd-0e63-47d5-8cc0-daf2f4bc592b.json).

## Local experiment prompted by Expanse itemization

Candidate c676 gives both Cassi and Issac Monster damage shards before Power shards on Expanse,
matching the item order visible in Fish's winning Expanse replay. On five local opponents, with both
sides tested, the production c553 control and c676 both won 10/10. The control averaged 967 submitted
gems for us versus 667 for opponents and finished in 809.5 rounds. c676 averaged 961 for us versus
716.6 for opponents and finished in 853.3 rounds. No winner changed; the candidate scored fewer gems,
gave the opponents more, and finished later. Reject this gear change.

Candidate source SHA-256: `5400C891882117B0F0D42A90113817893F37206FE501981918A4A4D4EF2C5726`.
The completed local screen is `matches/league/20261019-053803-c676-expanse-cni-monster-fresh/`;
the fresh c553 control is `matches/league/20261019-053737-tungtungsahur/`. The test was local only.

## Stampede draft follow-ups from the current #5 replay

The official Univardisty Stampede draft used Cassi & Issac / Stellar / Varg / Tavi / Ren. Candidate
c677 copied that five-pick roster on the c675 base; it scored 7/12 versus the fresh c675 control's
11/12 on the same six local strong proxies and both sides. Four of c677's five losses were on side B;
the remaining loss was `opp-racer` side A. Reject the unconditional roster copy.

Candidate c678 made the narrower change of replacing Prism with Varg while retaining Cassi & Issac,
Stellar, Ryth, and Tavi. It scored 10/12, with losses to `ming_bot` and `opp-swirl-meta-core` on side
A. The c675 control lost only to `opp-swirl-meta-core` on side A, so c678 gained no wins and added a
loss. Reject it too. Both screens completed with zero runner failures. These tests show that the
current top-5 lineup is useful evidence about its own bot, but copying it does not improve our local
matchups; the Stampede opening/route still needs work.

Candidate runs: c677 `matches/league/20261019-054352-c677-stampede-top5-draft/`; c678
`matches/league/20261019-054434-c678-stampede-varg-tank-draft/`; fresh c675 control
`matches/league/20261019-054343-c675-c604-plus-rows-ren-route/`. Draft source SHA-256: c677
`9CA3C255EA08CE7094B363D9BAEC016E5861F2DB660C048450864CD6316FB9BD`, c678
`6DB268B8757249788C99443F105A6ED1D19FBA26B56DC25BE1491F79A1EE6DF8`.

## Current bot status

c680 added a useful local Stampede opening, and c686 is now the strongest local candidate after the
follow-up item screens: it scored 633/680 across the broad local pool and 39/40 twice on Stampede.
c686 has been uploaded as test v101; a fresh group against a current top-50 team is needed to validate
whether the local gains transfer. The production source and ZIP remain at c553. The live target is 10
consecutive wins and the verified streak is 0/10. Details and rejected follow-ups are below.


## Offline Stampede follow-up c679–c680 (19 Oct 2026)

c679's tank alert by itself delayed but did not reverse the local meta-core side-A loss: the result moved from 0–720 at r913 to 480–960 at r1813, with the strong Stampede screen still 11/12. c680 combined that alert with Issac clearing a safe separate gem or gold camp during the first 150 rounds. It won 12/12 against the six strong local proxies in two identical runs; against `opp-swirl-meta-core` side A, it won 900–720 at r1761 versus c675's 0–720 loss at r913. The 17-map all-strong screen was 188/204 versus c675's 187/204, with only that winner changing.

Treat c680 as a local candidate only. It did not face Univardisty's live executable; the official unranked pause remains. Source, hashes, and run paths are recorded in `bots/tungtungsahur/PLAN.md`. Production remains c553 and the live streak remains 0/10.

## Later ranked Stampede replays (snapshot 06:12 UK, 19 Oct 2026)

Two additional ranked Stampede summaries sharpen the carry and banking diagnosis. In Univardisty of
Shingtonwash vs Pantheon ([group](https://2026a.battlecode.co.uk/game/match-groups/ce9100b7-8d73-42df-9888-77ea4ba15967),
[match summary](match-summary-b23ba484-6111-43ae-b00f-5a3cf6896476.json)), Univardisty cleared camps
16 times but collected no camp gems and submitted 360. Its Ren took the 360 gem bag from Pantheon's
Stellar after killing her at r123, then banked it at r189. Pantheon cleared 10 times, collected 1,440,
submitted 1,080, and died once; it recovered after that first stolen bag and made three later bank
cycles. Monster damage was comparable, so kills and clear count alone do not account for the result:
the repeatable gem route and protected deposits did.

In Fish vs Boost ([group](https://2026a.battlecode.co.uk/game/match-groups/2d8fc236-5f21-49e2-91e5-92362d9c2f92),
[match summary](match-summary-452a3466-5d48-42bd-a9ec-95f5b884e67e.json)), Fish won Stampede 1,080–0.
Fish made 10 camp clears and five deaths; Boost made two clears and eight deaths. Fish's Stellar
collected and submitted all 1,080 gems, had four kills and no deaths, and bought Power Focus plus
small Durability Health and Home Health queues. This fits a dedicated, protected carrier, while
remaining a single matchup rather than proof that the exact item queue transfers.

These official results are read-only ranked evidence. The local item experiment is separate: copying
Fish's full queue hurt the local strong set, while the narrower Power Focus / Durability Health / Power
Focus sequence scored well in the broad local pool. Keep replay observations distinct from candidate
results.

## c686 test v101 status (19 Oct 2026)

The c686 candidate bundle was uploaded as test submission v101 after its local screens. The bundle is
`submissions/tungtungsahur-test-c686-stampede.zip` (SHA-256
`B2920032530E5AA9D2124D5296C2D6C967B6ADEF03BF2EC783BBD8D3D0BD252A`); source SHA-256 is
`7E2E74D1C4E0BBDECAB5726AE50BB293B62F159EC68B6DC2B89E5165200F6DB3`. No fresh match group has
been created yet, so v101 has no live result and the win streak remains 0/10. The supplied group
`dbdcc65c-cb2f-4b28-850b-5fa691da9e34` is the already-reviewed v60 group versus then-rank-5
new team(4), not a v101 test.
