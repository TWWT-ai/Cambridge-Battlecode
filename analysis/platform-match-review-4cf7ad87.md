# Unranked platform match review — 17 October 2026

Match group: [4cf7ad87-2c52-452e-a9a3-59787c302e67](https://2026a.battlecode.co.uk/game/match-groups/4cf7ad87-2c52-452e-a9a3-59787c302e67). The public group response is saved in [`platform-match-group-4cf7ad87.json`](platform-match-group-4cf7ad87.json).

The group finished unranked, with Heavenly Court losing 0–5 to FRChronic. FRChronic's team performance endpoint recorded rank 58 and rating 1698.65 at 21:50 UTC, around the group's creation and finish, so this is a live unranked test but not a top-50 result. It contributes zero wins to the requested top-50 streak, which remains 0/10. The match group is unrated.

| Map | Rounds | Heavenly Court | FRChronic | Drafts (Heavenly Court / FRChronic) |
|---|---:|---:|---:|---|
| Interlock | 683 | 750 | 1004 | Stellar, C&I, Ryth, Varg / C&I, Stellar, Varg, Tavi |
| Stampede | 637 | 0 | 1080 | Stellar, C&I, Ryth, Varg, Tavi / C&I, Stellar, Tavi, Ryth, Prism |
| Elkring | 505 | 432 | 1008 | Stellar, C&I, Ryth, Varg, Tavi / C&I, Stellar, Varg, Tavi, Ren |
| Fragment | 636 | 286 | 1018 | Stellar, C&I, Ryth / C&I, Stellar, Varg |
| Pilgrimage | 930 | 596 | 1027 | Stellar, C&I, Ryth, Varg, Tavi / C&I, Stellar, Varg, Ren, Ryth |

All five matches ended with `endReason: gems`; neither side reported a bot error. The enemy won by 254, 1080, 576, 732, and 431 points respectively. FRChronic drafted Cassi & Issac plus Stellar in every game and Varg in four of five. Heavenly Court used the same draft order as the current main bot, truncated to each map's team size. The API did not provide a submission ID or version, so the exact source/WASM used cannot be confirmed.

The group-level data points to a large gem-economy gap: FRChronic reached 1004–1080 on every map while Heavenly Court scored 0–750. Stampede is the largest red flag at 0 points. This does not establish the cause; replay trajectories and statistics are still needed. Replay bundle downloads returned “Sign in to watch or download replays” from this runtime, and the per-match summary endpoint returned 401, even though the user is signed into the site in their browser. Once the five replay bundles are available locally, inspect first-capture timing, tribute trips, gem loss on death, champion deaths, and Stampede opening/shop behavior before changing strategy.

## Stampede follow-up

The live Stampede draft on Heavenly Court omitted Prism. A fresh paired local test against the same four strong proxies scored 6/8 for main and 7/8 for the isolated v115 candidate, which drafts Prism / Stellar / C&I / Ryth / Tavi on Stampede. The candidate converted the Xuanming side-A loss; both variants still tied Ming 900–900 on one side. Equipment variants buying Monster Strength first on Tavi, Prism, or both scored 7/8, 6/8, and 5/8, so none improved on current v115. Keep the equipment unchanged and use the Prism draft as an isolated candidate for the next live test. Results are in [`matches/league/20261017-2301-stampede-monster-screen/summary.json`](../matches/league/20261017-2301-stampede-monster-screen/summary.json).

The public leaderboard refresh endpoint returned `401 SIGN_IN_REQUIRED` from this runtime. The saved 14:41 UTC top-50 snapshot is therefore not a fresh ladder, although FRChronic's performance history placed it at rank 58 around this group.

Access recheck after the user supplied this link: the public group response is still readable, but the
50-team leaderboard, the Stampede per-match summary, and the replay bundle all return HTTP 401. The
group response reports `myTeamId: null`. TinyFish is installed and enabled, but no browser-action
tools are exposed in this session, so the user's signed-in browser state is not available to the API
requests here. The match review therefore remains score-and-draft level; replay-level causes are not
verified.
# Follow-up local validation

The group's main-bot Stampede lineup omitted Prism. The isolated Stampede lineup with Prism and a shared-farm phase beat the fresh #115 control 8/8 versus 7/8 on the four strong local proxies, and later scored 119/136 versus 118/136 across all 17 maps. A cached-at-initialization variant (#131) kept the same strong-proxy outcomes and scored 614/680 in two exact broad runs, compared with 612/680 for #126. This supports testing the Stampede lineup and phase change, but it does not identify the cause of the live 0-point Stampede result because replay-level data is still unavailable.

The broader local differences for #131 were Stampede +1 win, Pilgrimage +2, and Lanes -1 versus #126. These local results do not count toward the live top-50 streak. Main source and submission ZIP remain unchanged.
# Follow-up draft experiments (18 Oct 2026)

Against local proxies, putting Varg before Ryth on both 30x30 maps improved Elkring but caused more Fragment losses, so that combined change was rejected. Restricting the order change to Elkring (#133) retained the standard Fragment lineup and improved the Elkring targeted result from 7/8 to 8/8. It scored 120/136 strong-proxy wins twice and 618/680 broad-pool wins twice, versus 119/136 and 614/680 for #131. All four broad gains were on Elkring; no other map total changed.

This gives a testable map-specific candidate for a future live match, but does not explain the supplied 0–5 result. The group's submission version is unknown and the replay bundle remains inaccessible from this runtime. These proxy wins do not count toward the top-50 streak.
Pilgrimage local screens after #133 did not find an improvement. Varg-before-Ryth increased average gems against Ming but still lost both sides and lowered the targeted result to 5/8. Ren-for-Tavi also scored 5/8, trading one Ming win for two Xuanming losses. Keep the current draft in #133; live causes remain unverified without the match replay.
FRChronic's latest readable public performance-history point is rank 67 at 2026-10-17 23:00:35 UTC. The leaderboard endpoint still returns HTTP 401, so this historical point does not establish its current rank.
Swirl's Varg-before-Ryth order also failed the targeted proxy screen (3/8 versus 4/8) and left the Ming/Xuanming losses unchanged. The tested candidate has been restored to #133.

## Replay-backed update (18 October 2026)

After the user confirmed the site sign-in, the official `cambc` 2.2.5 CLI authenticated successfully. It downloaded all five match summaries and replay bundles to [`matches/live/4cf7ad87-2c52-452e-a9a3-59787c302e67/`](../matches/live/4cf7ad87-2c52-452e-a9a3-59787c302e67/). This supersedes the earlier access notes above that said the replay files were unavailable; those notes were accurate when written.

Replay metrics show all five losses were ordinary match outcomes, with zero bot faults. Heavenly Court repeatedly lost both economy and fights:

| Map | Gems submitted (HC / FRChronic) | HC deaths / kills | FRChronic deaths / kills | Replay evidence |
|---|---:|---:|---:|---|
| Interlock | 750 / 1004 | 12 / 2 | 3 / 7 | HC collected 750 and submitted it, but cleared fewer camps and dealt less champion damage. |
| Stampede | 0 / 1080 | 8 / 1 | 3 / 2 | HC collected no gems; its submitted score stayed at zero for the full match. The live lineup omitted Prism. |
| Elkring | 432 / 1008 | 14 / 2 | 3 / 12 | HC collected 522 and lost 90 before banking; the opponent cleared camps more quickly and earned over twice the gold. |
| Fragment | 286 / 1018 | 19 / 3 | 5 / 12 | Cassi and Issac both died at round 48 in the opening fight; HC collected only 319 gems. |
| Pilgrimage | 596 / 1027 | 7 / 1 | 5 / 3 | HC banked everything it collected, but the opponent cleared far more camps and earned 4,425 gold versus HC's 1,450. |

The strongest actionable map-specific clue is Stampede's missing Prism pick. The existing isolated Stampede candidate already uses Prism and a shared-farm phase, but it was only locally validated when this group ran. The older group does not expose the submission version, so it cannot be used to claim which source was tested.

## Replay archive

The summary JSON files and `.repl26a` archives were downloaded individually with `cambc 2.2.5 matches summary` and `matches download`; no data was changed in the match group. The platform group response still reports null submission IDs and versions.
