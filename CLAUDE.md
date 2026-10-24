# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

C++ bots for Cambridge Battlecode 2026a (CAMBC), compiled to WASM by `cambc.exe`. The bot being developed is
`bots/tungtungsahur`. Everything else in `bots/` is either an opponent or an experiment copy.

- Current uploaded game rules: `GameRules.md`; current uploaded C++ API export: `BotAPICpp (1).md`.
  `BotAPICpp.md` is the older 14 October export. The 21 October documents are newer than the workspace
  runner/SDK: the local header lacks Golem, Heart of Ruin, and awake/asleep camp masks and has conflicting
  passive constants. Do not treat old local leagues as validation under the current handbook until the
  toolchain and maps are refreshed. See `analysis/game-update-20261021-strategy.md`.
- `bots/tungtungsahur/PLAN.md` is the numbered experiment log with results; `REPORT.md` is the user-facing
  summary. Analyst reports (map layouts, mechanics, opponent study) are in `analysis/*.md`.

## Commands (repo root, Windows; Git Bash or PowerShell)

```bash
./cambc.exe build <bot>                                   # compile one bot
./cambc.exe run <botA> <botB> --map corners [--view]      # one match; bundle saved under replays/
python tools/league.py <bot> --opps $(cat tools/opps22b.txt) --jobs 18 --tag note   # standard 440-game league
python tools/league.py <bot> --opps ming_bot --maps collision,lanes                 # subset of opponents/maps
python tools/league.py <bot> --opps zz-idle                # economy speed test (no opponent)
python tools/race.py <league dir> <league dir>             # compare per-map rounds-to-1000 between runs
python tools/scout.py <.repl26a or platform logs.zip> [a|b]   # summarise SCOUT lines of one match
python tools/deaths.py <league dir> <bot>                  # deaths per opponent in a league run
./cambc.exe bundle tungtungsahur -o <dir>                  # writes <dir>/tungtungsahur.zip (upload bundle)
```

- `league.py` plays every opponent on every map from both sides via `run-batch`, prints wins / average gems /
  average winning round, and saves `matches/league/<timestamp>-<bot>/summary.json` (with a per-game list) plus
  `matches/league/history.csv`. Opponent lists: `tools/opps22b.txt` (standard), `tools/opps-all.txt` (every bot).
- Historical local reference numbers (pre-21 October rules): about 394/440 on `opps22b`, ming_bot 16-18/20,
  all Faisal variants won. These are not current-rule validation.
- `cambc.exe login` / `submit` need the user's platform account: give the user the command, never run it.

## Gotchas

- Results are deterministic but chaotic: any change (even extra fuel use or a debug print) reshuffles single
  games. About ±8 league wins or ±30 rounds on one map is noise; judge changes on full league totals.
- Never run several `cambc run` at once (CMake configure race). `run-batch` compiles unreliably here, so
  `league.py` builds bots first; start a second concurrent league ~20 s after the first.
- Python `write_text` on Windows turns LF into CRLF, which breaks `patch` and diffs: write bytes.
- Every champion runs its own bot instance (statics are per champion). Team coordination is only the 8 bytes of
  shared memory (`team.h`) plus the 1024-byte draft memory.
- Reading a unit that died or left vision throws and costs the champion its whole turn; use the `alive()`,
  `safe_pos()` and `attempt()` helpers in `bot.cpp`.
- Fuel is 100k per turn; big maps (lanes, corners, expanse) are tight. Per-turn work is cached
  (`groups()`, `blocked_tiles()`, `visible_enemies()`); avoid full-map bitboard ops per camp group.
- `GroupInfo` is aggregate-initialised: add new fields at the end.
- `cambc::vision::altar_lock_at` returns our own lock when both teams locked an altar; use `enemy_lock_at`.

## Architecture of `bots/tungtungsahur/src`

- `main.cpp`: turn loop; draft turns call `play_draft()`, others `Bot::play_turn()`; exceptions are logged as
  `bot error (turn lost)`.
- `draft.cpp`: map- and opponent-aware lineups; inspect the source as the draft source of truth. Cassi & Issac
  are one draft pick but two linked champion bodies.
- `team.h`: shared-memory layout. Bytes 0-2 objective (camp tile + stamp, +128 = hunting), 3-5 Ryth's anchor,
  6 fight alarm, 7 danger alarm; the top bits of bytes 6/7 are the mid/late game flags.
- `bot.cpp`, `Bot::play_turn` order: SCORE/SCOUT logging, shop, survive, `update_ledger`, `choose_objective`,
  `burst` (spells on enemies), `bank`, `shopping_trip`, `peel`/`place_lock`, then the role turn
  (Ryth tank, Issac fighter, Tavi marksman, Stellar/Cassi mage, Varg farmer).
- Phases (`game_phase()`):
  - early, until Stellar or Varg owns an emblem or round 600: the whole team works Ryth's camp
    (`team_farm`), only Stellar/Varg capture (`capture_duty`), and gold counts double in `choose_camp`;
  - mid: squads A (Ryth, Stellar, Tavi) and B (Issac, Cassi), Varg solo-farms or helps B; engage only within 5
    tiles, stay out of the enemy half (`off_limits`/`deep`), back off when outnumbered by 2;
  - late (Stellar owns 3 emblems): fight anything in sight unless outmatched.
- Camp model: `groups()` holds static per-group info, `ready_round()` is the respawn ledger, `taken_until()`
  marks captures someone else covers; `choose_camp` values gems (+gold early) per turn of walk + clear + capture.
- Keep the stdout formats: `SCORE round ours theirs` every 5 rounds (parsed by `league.py`) and the `SCOUT ...`
  lines (parsed by `scout.py`/`deaths.py`). Platform logs contain only our own stdout, so they are the only
  view of opponents there.

## Experiment workflow

1. Copy `bots/tungtungsahur/src` to `bots/cand-<name>/src`, change it, build, and compare with the league and
   the race test against the current main.
2. To promote: keep the old main as `bots/opp-tts-v<N>`, copy the candidate into `bots/tungtungsahur` and
   `bots/tungtungsahur-best`, rebuild `submissions/tungtungsahur.zip`, and log the experiment in `PLAN.md`.
3. Don't modify opponent bots. `bots/Faisal-bot` currently holds a copy of our old v8 code; the original
   Faisal-bot is `bots/faisal-orig` (same as root `bot/src`).
