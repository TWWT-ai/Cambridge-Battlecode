# Cambridge Battlecode 2026A: game, strategy, and C++ from zero

> A beginner-first handbook for the Tarot Club repository. Rules/API researched 13 October 2026; repository status refreshed 14 October 2026 through GitHub `main` at `e341ad05`.

This guide teaches two things together:

1. how the CAMBC 2026A game actually works; and
2. enough modern C++ to read, change, and test this team's bot.

You do **not** need to know C++ already. Read the first three parts in order, then use the later parts as a reference while experimenting.

## What is fact, and what is a strategy idea?

This distinction matters throughout the guide:

- **Rule** means it is stated in the current CAMBC handbook or C++ API.
- **Repository fact** distinguishes the local `xuanming/localdev` checkout from the newer GitHub `main` snapshot named above.
- **Team plan** means it comes from [`docs/strategy.md`](../docs/strategy.md). It is a reasoned starting strategy called FOUNDRY, not an official rule and not proof of optimal play.
- **Measured roadmap** means replay-derived evidence and proposed work recorded in [`Analysis1.md`](Analysis1.md) and the linked GitHub issues; a proposal is not implemented until stated otherwise.
- **Recommendation** means a hypothesis that should be tested in matches.
- **Analogy** means an idea borrowed from another programming game or robotics research. The underlying principle may transfer; that other game's rules do not.

When sources disagree, use this order:

1. the behavior of the current match engine;
2. the generated SDK header installed by `cambc init`;
3. the current [C++ API page](https://2026a.battlecode.co.uk/game/api);
4. the current [game handbook](https://2026a.battlecode.co.uk/game/docs);
5. the local exports [`docs/BotAPICpp.md`](../docs/BotAPICpp.md) and [`docs/GameRules.md`](../docs/GameRules.md);
6. this guide and team strategy notes.

The public event landing page is useful for dates and a broad description, but its short marketing FAQ is not the precise game specification.

---

# Part I — The game in plain English

## The one-minute explanation

Each team programs several **champions**. The champions move on a grid and act automatically; no human controls them during a match.

The normal economic loop is:

```text
choose a camp
    -> travel to it
    -> defeat every monster in its connected group
    -> stand on a spawn tile and capture for five capture phases
    -> receive gold and carried gems
    -> travel next to an altar
    -> channel a tribute
    -> turn carried gems into permanent team score
```

Gold buys permanent stat upgrades. Gems are only safe and score-bearing after tribute.

The first team to tribute **1,000 gems** wins immediately. If nobody reaches 1,000 by the end of round 2,000, compare:

1. tributed gems;
2. lifetime gold earned;
3. champion kills; then
4. Team B wins an exact tie.

The economic loop is central, but the teams share the map. You may contest camps, steal carried gems by killing their carrier, defend or block altars, and use vision to ambush opponents.

## A concrete miniature example

Suppose Vendetta clears a Wolf camp worth 90 gold and 22 gems.

1. Killing the Wolf is not enough. Vendetta must still capture its camp region.
2. Once the entire connected camp group is dead, an uncontested ally occupies an original monster spawn tile.
3. The capture phase starts a five-phase timer. More allies do not make it faster.
4. When capture finishes, allies standing in the region split the reward.
5. Vendetta now *carries* 22 gems. They do not yet count toward victory.
6. At an altar, 22 starting gems make tribute last `ceil(22 / 10) = 3` owner turn ends.
7. If Vendetta survives and is not stunned or blocked by an enemy altar lock, the tribute resolves at the start of her next turn after the timer reaches zero.
8. The team permanently gains 22 submitted gems.

If an enemy champion kills Vendetta before banking, that killer receives her carried gems and 50 gold. If a camp kills her, the carried gems disappear instead.

## The four layers of a strong bot

A helpful mental model is to split decision-making into four layers:

```text
strategy     Which champions and overall style should we use?
macro        Which champion should handle which camp, altar, or enemy?
tactics      Should this champion fight, retreat, bank, or interrupt right now?
mechanics    Which exact move, attack, ability, item, or ward call is legal?
```

A bot can have brilliant combat mechanics and still lose because two champions visit the same empty camp. It can have a good camp schedule and still lose because it never retries a move blocked by a hidden enemy. Build and test all four layers separately.

---

# Part II — Exact rules that drive strategy

## 1. Drafting

Before ordinary play, each team chooses between three and five champion selections, depending on the map.

- The entire static map is visible during draft.
- Picks occur one at a time and both teams reveal simultaneously.
- Your own team cannot select the same champion choice twice.
- The opponent may select the same champion as you.
- Cassi & Issac are one draft choice but create two separately acting bodies and bot instances; their lives remain linked, so either death kills both.
- If the bot yields, crashes, or runs out of fuel without picking, the engine fills missing picks randomly.

The draft is more than roster selection. It is the only time the bot gets all static map information plus a large planning budget. It can write up to **1,024 bytes** into draft memory. Every gameplay bot instance later receives a read-only snapshot of those bytes.

Useful draft work includes:

- list all connected camp groups and their combined rewards;
- calculate static routes or distance tables;
- classify choke points, isolated regions, safe altars, and teleport opportunities;
- assign opening jobs and build plans;
- encode that plan compactly into draft memory.

The first draft turn gets ten times the normal fuel budget, so expensive static computation belongs there when possible.

## 2. Rounds, champion turns, and action allowances

A **round** contains engine phases and one turn for every champion. It is not the same as one champion turn.

At round start, the engine processes:

1. camp respawns;
2. existing spell and ward updates;
3. camp captures;
4. camp actions; then
5. champion turns.

Teams alternate champion turns, and the team that starts swaps every round. Within a team, champions act by higher priority first, then draft order. `set_priority(...)` changes next round's ordering and persists until changed again.

At the start of an individual champion turn, zero-valued timers resolve in this order:

1. respawn;
2. ward recharge;
3. buff and shield expiry;
4. channel completion.

At turn end, timers decrement. Reaching zero does **not** immediately resolve the effect; it waits for that champion's next turn start. Spawn healing still occurs at turn end.

### Normal action budget

Each champion normally has:

- one ordinary move;
- one basic attack; and
- at most one successful ability cast across the two ability slots.

Important exceptions:

- A melee champion may normally walk and basic-attack in the same turn.
- A ranged champion's walk and basic attack consume the same allowance, so it normally chooses one.
- Some abilities say they **exclude walking**.
- An attack-reset ability restores the basic attack allowance.
- Starting a channel prevents other actions until completion or cancellation.
- Wards and consumables have their own availability rules.

Never assume that because a method exists it is legal now. Ask the API with methods such as `can_move()`, `can_attack()`, `can_cast()`, `is_ready()`, and `can_buy(...)` before committing.

## 3. Grid, coordinates, and distance

Maps are rectangular grids from 30×30 through 100×100 tiles. `cambc::vec2` stores an integer `(x, y)` position or displacement.

Most game ranges use **Chebyshev distance**:

```text
distance = max(abs(x1 - x2), abs(y1 - y2))
```

That means a diagonal neighbor is distance one, not approximately 1.414. From `(3, 3)`, all eight surrounding tiles are at Chebyshev distance one.

In a match, the bot uses this calculation to answer questions such as “can I attack that adjacent champion?”, “am I close enough to tribute?”, or “which camp is nearer?” This small example compares two hypothetical map tiles:

```cpp
// `vec2` stores integer map coordinates as an x/y pair.
cambc::vec2 a{3, 3}; // A champion or objective at column 3, row 3.
cambc::vec2 b{4, 4}; // One diagonal step away from `a`.

// `const auto` asks C++ to infer the numeric return type and prevents
// accidental reassignment after this distance has been calculated.
const auto distance = a.chebyshev_distance(b); // Result: 1, not sqrt(2).
```

Syntax:

- `cambc::vec2` is the type inside namespace `cambc`.
- `a{3, 3}` uses brace initialization.
- `const` says `distance` will not be reassigned.
- `auto` asks the compiler to infer the return type.
- `a.chebyshev_distance(b)` calls a member function on object `a`.
- `//` begins a comment that ends with the line.

## 4. Terrain and movement

| Tile | Walk onto it? | Dash across/onto it? | Blocks sight? | Important detail |
|---|---:|---:|---:|---|
| Ordinary floor | Yes | Yes | No | Normal tile. |
| Wall | No | No | Yes | A dash cannot cross it. |
| Hole | No | May cross | No | A legal dash may cross a hole but cannot land on it. |
| Bush | Yes | Yes | Yes from outside | A champion inside sees across its connected bush cluster and outward. |
| Altar | No | No | No rule says it blocks sight | Stand within distance one to tribute. |
| Enemy spawn | No | No legal landing | Not terrain occlusion | Allied spawn is shop/heal territory. |

Ordinary walking moves to one of eight neighboring tiles. Dash abilities move up to two legal steps. A teleport crystal selects a destination up to three tiles away, ignores intervening terrain, and channels for three owner turn ends. Its destination still cannot be a wall, hole, altar, enemy spawn, or occupied tile.

### Hidden bush occupants: a special failure case

The engine's movement mask includes what the champion currently knows. A hidden enemy may therefore occupy a seemingly legal bush tile.

- Trying that tile returns `false` instead of throwing.
- The tile becomes revealed to this champion for the rest of the round.
- The failed attempt preserves the relevant movement allowance, cooldown, or consumable.
- The bot may try a different legal destination.
- Trying a destination already known to be invalid raises `cambc::error`.

So `false` is not merely “give up”; it can mean “new information, replan and retry.” The same hidden-obstruction convention applies to dashes and teleport starts.

## 5. Vision and wards

Every champion has vision radius eight, calculated by symmetric shadowcasting.

- Walls and bushes occlude vision.
- Holes do not.
- From inside a bush, the champion sees through its connected bush cluster and outward.
- Each champion owns one ward with range six.
- A ward may be placed within two tiles when its charge is ready.
- The ward is permanent, cannot be damaged, and placing another replaces it.
- The ward charge refreshes once per round.
- Allied champions do **not** share ordinary vision or ward vision.

This last rule is easy to miss. If Varg sees an enemy gem carrier, Vendetta's bot instance does not automatically see it. Varg must encode the observation into the eight-byte team memory if the information is important enough.

The static map is already known from draft. Use wards for changing information: altar approaches, camp contests, choke points, likely gem-return routes, or bushes that hide an ambush.

## 6. Camps

Camp monsters are stationary producers. A group consists of monsters whose original spawn tiles are connected cardinally—up, down, left, or right, not diagonally.

| Monster | Health | Strength | Attack range | Gold | Gems | Group respawn contribution |
|---|---:|---:|---:|---:|---:|---:|
| Wolf | 1,350 | 20 | 3 | 90 | 22 | 40 rounds |
| Elk | 2,400 | 60 | 3 | 160 | 36 | 60 rounds |
| Gem cluster | 500 | 0 | 0 | 0 | 24 | 50 rounds |
| Gold cluster | 500 | 0 | 0 | 35 | 0 | 50 rounds |
| Monolith | 20,000 | 200 | 5 | 300 | 200 | 150 rounds |

Rules that matter:

- Damage wakes a camp group.
- Camps target the nearest champion in range.
- Camps see through bushes, have vision eight, and never chase.
- Every monster in the connected group must die before capture begins.
- To capture, at least one ally must occupy an original spawn tile and no enemy may contest the region.
- Capture takes five capture phases. Extra allies do not accelerate it.
- An empty or contested capture region resets progress.
- On completion, all allied champions present in the region split the group's combined rewards.
- Integer remainders go to the lowest-ID champion.
- Respawn begins after capture, using the longest respawn time among the group's members.
- Any occupied original spawn tile delays the entire group from respawning.

### Why “clear time” and “capture time” are different

The camp is economically worthless until capture finishes. A route planner must count:

```text
travel + attacks/spells needed + five capture phases + banking travel + tribute
```

A champion that kills a camp and walks away has created an opportunity for the opponent. A champion that keeps standing on the spawn tile after the respawn timer expires can also accidentally suppress future income.

## 7. Gems, tribute, and altar locks

There are two different gem numbers:

- **carried gems**, held by one champion and vulnerable to death; and
- **submitted/tributed gems**, permanent team score.

To tribute, a living champion with at least one gem stands within Chebyshev distance one of an altar and starts a channel.

```text
duration = max(1, ceil(gems_when_started / 10)) owner turn ends
```

Examples:

| Starting bag | Countdown ticks |
|---:|---:|
| 1–10 | 1 |
| 11–20 | 2 |
| 21–30 | 3 |
| 91–100 | 10 |

The starting turn counts as the first tick. Completion occurs at the **next turn start** after the timer reaches zero.

Niche but strategically powerful details:

- The duration is fixed from the starting bag.
- Completion submits the champion's entire *current* bag, including gems gained after the channel started.
- Camp capture happens before channel completion in a round.
- Damage does not interrupt tribute.
- Stun, death, or a newly placed enemy altar lock does interrupt it.
- A one-tick tribute is not instantaneous; it resolves next turn start.

An altar lock costs ten gold. It may be placed on an altar within two tiles, immediately cancels enemy tribute there, and blocks only the opposing team. It takes three basic attacks to remove. Attempting to tribute against an enemy lock is converted by the engine into an attack on that lock.

## 8. Combat and abilities

Basic attacks deal the champion's current Strength before modifiers:

- melee attack range: one;
- ranged attack range: three;
- the target must be visible.

Ability effects scale from Focus. For example, a `2 × Focus` spell cast with 130 Focus has 260 raw effect before mitigation or caps.

Every champion has two ability slots. Normally:

- only one successful ability cast is allowed per turn across both slots;
- a used slot receives an eight-owner-turn-end cooldown;
- unit-targeted abilities need a valid visible target;
- ground-targeted abilities select a tile;
- some abilities exclude ordinary walking that turn;
- a failed hidden-obstruction attempt may return `false` without consuming the cast.

Use the SDK's `damage_amount(target)`, `heal_amount(target)`, `valid_tiles()`, and target-category queries rather than duplicating complicated rules when possible.

## 9. Channels

| Channel | Duration | Damage interrupts? | Stun interrupts? | Death interrupts? | Manual cancel? |
|---|---:|---:|---:|---:|---:|
| Recall | 5 ticks, or 3 with Home | Yes | Yes | Yes | Yes |
| Tribute | `max(1, ceil(starting gems / 10))` | No | Yes | Yes | Yes |
| Teleport crystal | 3 ticks | No | Enemy stun does | Yes | No |

All channel timers decrement at their owner's turn end and resolve at the next owner turn start after reaching zero.

## 10. Gold, shards, emblems, and consumables

Gold improves individual champions. Ordinary champions buy on allied spawn or while dead. Tavi has special shopping rules described later.

A shard costs 30 gold and adds that champion's growth amount to Strength, Focus, or Health. Five matching shards combine automatically into an emblem. Stats from all shards keep stacking, including shards in duplicate emblems, but the same emblem family's passive does not stack twice.

| Family | Stat value | Passive |
|---|---|---|
| Monster | 5 matching shards | Deal 10% more damage to camps. |
| Power | 6 matching shards | No passive; one extra shard's stat value. |
| Durability | 5 matching shards | Take 10% less incoming damage. |
| Treasure | 5 matching shards | Gain 20% more gold. |
| Jungle | 5 matching shards | Take 30% less damage from camps. |
| Home | 5 matching shards | Recall takes three rather than five ticks. |
| Bruiser | 5 chosen + 1 of each other stat | Mixed stats, no passive. |

Other details:

- Buying Health while on spawn heals by the gained amount.
- Tavi buying Health in the field raises maximum health but does not heal.
- Only Tavi can sell, at spawn, for full purchase value.
- Refunded gold does not count as newly earned gold for the tiebreak.
- Vesper's built-in +20% gold and Treasure's +20 percentage points combine to +40%.
- Consumables cost ten gold and a champion may carry at most one of each type.
- The two consumables are altar lock and teleport crystal.

## 11. Death, respawn, recall, and healing

When an enemy champion gets the kill:

- the killer receives all of the victim's carried gems;
- the killer receives 50 gold;
- assists receive no gold.

When a camp gets the kill, carried gems are destroyed. Cassi and Issac die together and jointly grant only one 50-gold kill reward, while both bags are lost/transferred according to the kill.

Respawn takes 60 owner turn-end ticks. Dead champions still receive turns and may shop. When the timer has elapsed and a spawn tile is available, the champion respawns at its next turn start with full health and reset abilities.

Recall:

- takes five owner turn ends, or three with the Home emblem;
- is interrupted by damage, stun, or death;
- preserves carried gems;
- arrives at spawn at turn start;
- requires remaining on spawn until that turn end to receive the full heal.

## 12. Fuel and deterministic computation

The engine limits computation using Wasmtime **fuel**, a deterministic approximation of instruction cost.

- C++ and Rust: 100,000 fuel per ordinary turn.
- OCaml: five times the C++ limit.
- Python: 25 times the C++ limit.
- First draft turn: ten times normal.
- Each champion's first gameplay turn: twice normal.
- Unused fuel does not carry forward.

If a bot runs out of fuel, execution is suspended and resumes from that point on its next turn. That is dangerous: code may resume halfway through a decision with assumptions that are one round old. Prefer explicit fuel guards around optional work.

For example, a champion can skip an expensive optional search when little fuel remains. The surrounding top-level loop must still reach `end_turn()`; this snippet only shows the guard inside a helper or turn function:

```cpp
// Read the deterministic compute budget that remains for this bot turn.
if (cambc::fuel_remaining() < 1'000) {
    // Stop this example's turn immediately instead of beginning work that
    // might be suspended halfway through with stale game observations.
    cambc::end_turn();
}
```

`1'000` is the same integer as `1000`; the apostrophe is a C++ digit separator for readability.

## 13. The two memories

| Memory | Size | Written when? | Read when? | Best use |
|---|---:|---|---|---|
| Draft memory | 1,024 bytes | Draft | Draft and all later champion instances | Static map plan, opening assignments, route metadata. |
| Shared memory | 8 bytes | During match | All allied instances during match | Urgent, changing team coordination. |

Each champion runs its own bot instance and retains its own ordinary C++ member variables between its turns. Those variables are **not** automatically shared with allies.

---

# Part III — Champion reference and strategic reading

## Complete roster

All champions have vision eight, walk one, two eight-turn ability slots, and at most one successful ability cast per turn.

| Champion | Style | Health + growth | Strength + growth | Focus + growth | Passive / slot 0 / slot 1 |
|---|---|---:|---:|---:|---|
| Cassi | Ranged | 700 + 71.25 | 30 + 3.5 | 70 + 15 | Linked death / 2× Focus single-target at range 4, excludes walk / range-4 one-round stun, walk-compatible |
| Issac | Melee | 900 + 95 | 40 + 4.75 | 100 + 10 | Linked death / attack reset / dash 2 |
| Ryth | Melee | 1,200 + 100 | 50 + 5 | 100 + 10 | Gains Strength equal to 1% of bonus Health / 1× Focus radius-1 damage+stun at ground range 4, excludes walk / attack reset |
| Vesper Vale | Ranged | 900 + 100 | 45 + 5 | 100 + 10 | +20% gold / attack reset / dash 2 |
| Prism | Ranged | 700 + 75 | 35 + 3.5 | 80 + 10 | +0.2 Focus per carried gem / 1.5× Focus damage+stun at range 4, excludes walk / 1× Focus radius-1 ground damage at range 4, excludes walk |
| Stellar | Ranged | 750 + 75 | 35 + 3.5 | 100 + 10 | None / 2× Focus single-target at range 4, excludes walk / 1.4× Focus radius-1 ground damage at range 4, excludes walk |
| Vendetta | Melee | 800 + 100 | 70 + 5 | 100 + 10 | Any kill, including a camp monster, resets both ability cooldowns / attack reset / dash 2 |
| Marcella | Melee | 1,200 + 100 | 45 + 5 | 50 + 10 | Immune to stun / reset and empower next attack to stun / 2× Focus single-target at range 4, excludes walk |
| Tavi | Ranged | 750 + 75 | 35 + 5 | 100 + 10 | Buy shards anywhere; sell at spawn / attack reset / 2.2× Focus damage+stun at range 4, excludes walk |
| Willow | Ranged | 700 + 50 | 45 + 3 | 105 + 5 | None / heal another ally for up to 3× Focus at range 4, walk-compatible / attack reset |
| Ren | Melee | 900 + 100 | 40 + 5 | 100 + 10 | Retaliates for 0.2× Focus, even when dying / 1.25× Focus damage+stun at range 4, excludes walk / dash 2 |
| Varg | Melee | 1,000 + 100 | 50 + 5 | 100 + 10 | Basic attacks splash Strength to other valid targets in radius 1 / attack reset / 2.5× Focus self-shield for five turns |

“Growth” is the amount one matching shard adds for that champion. For example, one Focus shard adds 15 Focus to Cassi but only 5 Focus to Willow.

## How to reason about a champion

Do not rank champions using base damage alone. Ask:

1. **Camp throughput:** How many turns and how much health does this champion spend clearing likely camp groups?
2. **Action economy:** Does its useful spell exclude walking? Can an attack reset create a second attack?
3. **Survivability:** Can it safely carry gems and finish tribute?
4. **Mobility:** Can it reach camps, contest captures, escape, or cross holes?
5. **Economy:** Does it generate extra gold or avoid shopping travel?
6. **Matchup:** Does stun, stun immunity, splash, healing, or retaliation change an important fight?
7. **Map fit:** Are camps packed for Varg, isolated for fast farmers, or separated by terrain that favors dashes/teleports?

### Current code and proposed FOUNDRY draft orders

GitHub `main` at `e341ad05` currently implements this fixed priority:

```text
Vendetta -> Cassi & Issac -> Varg -> Tavi -> Vesper Vale
-> Marcella -> Stellar -> Ren -> Prism -> Ryth -> Willow
```

For a three-selection draft, that becomes Vendetta, Cassi & Issac, and Varg. The implementation does not currently inspect the enemy draft or select from map features.

Why this is plausible:

- Vendetta is intended to turn camp kills into repeated attack-reset/dash availability.
- Cassi contributes high ranged camp damage and control while Issac supplies a melee tank from the same selection.
- Varg's passive clears packed groups efficiently and his kit can tank.
- Tavi buys shards without returning to spawn and has a powerful damaging stun.
- Vesper converts camp cycling into more gold and has ranged attacks plus mobility.

The present runtime does not realise all of those reasons: it uses damaging/CC camp spells, but not Vendetta/Vesper attack-reset and dash cycles, Varg's shield, or a reliable Cassi-behind-Issac formation. A theoretically good draft pick is only useful when the executor uses its kit.

Why it is not sacred: new replay and platform data already suggest a different order. Open issue #35 proposes:

```text
Varg -> Cassi & Issac -> Stellar -> Tavi -> Ren -> Ryth
-> Vendetta -> Marcella -> Willow -> Prism -> Vesper Vale
```

Across the issue's 1,925-game sample for teams rated at least 1,600, Ren, Stellar, and Tavi had higher pick-presence win rates than Vendetta or Vesper, and the top eight teams rarely opened with Vendetta. This is correlation rather than proof—the strongest teams influence those statistics—but it is better evidence than intuition alone. Treat both orders as hypotheses to compare from both sides on every map.

---

# Part IV — C++ from zero, in the context of this bot

## 1. What happens to C++ source code?

You write human-readable files such as `bot.cpp`. A compiler checks their types and syntax and turns them into a WebAssembly module that CAMBC can run.

In this repository:

```text
bots/starter-cpp/src/main.cpp    program loop and draft/game dispatch
bots/starter-cpp/src/draft.cpp   draft decisions
bots/starter-cpp/src/bot.cpp     champion-turn decisions
bots/starter-cpp/src/bot.h       Bot class declaration
bots/starter-cpp/src/random.h    small helper
```

`starter-cpp` is the reference example. There are currently two different FOUNDRY states to keep separate:

- This local `xuanming/localdev` checkout remains at `966ec857`, where `foundry` is still essentially a scaffold.
- GitHub `main` at `e341ad05` contains the developed planner, encoded plan, runtime FSM, navigation, ledger, champion-specific economy, camp spell casting, tactical modules, and expanded replay metrics.

Therefore, `cambc build foundry` builds whichever FOUNDRY source exists in the branch actually checked out. A successful local build does not prove that you built the newer GitHub implementation.

The usual command is:

```powershell
cambc build starter-cpp
```

The platform's build setup finds the source files and compiles them. You should not manually edit generated SDK files or `.cambc/` build output.

## 2. The smallest useful program loop

This is the architecture used by the starter. It creates one persistent `Bot` object for the current champion process, chooses draft logic before the match and turn logic during the match, and always yields control back to the engine:

```cpp
// Angle brackets include the installed CAMBC SDK; quotes include files from
// this bot project.
#include <cambc.h>
#include <exception>
#include <iostream>
#include "bot.h"
#include "draft.h"

int main() {
    // Construct this champion's Bot once. Its member variables survive from
    // one turn to the next, but are not automatically shared with allies.
    Bot bot;

    // CAMBC resumes the same WebAssembly program every time this bot may act,
    // so the process deliberately runs forever.
    while (true) {
        try {
            // During draft, select champions and write the static match plan.
            if (cambc::is_draft()) {
                play_draft();
            } else {
                // During gameplay, let this champion make its decisions.
                bot.play_turn();
            }
        } catch (const std::exception& error) {
            // Log unexpected failures for replay diagnosis. Catching here
            // prevents one bad decision from bypassing the final yield.
            std::cout << "bot error: " << error.what() << '\n';
        }

        // Every path must yield. Leaving this inside the infinite loop but
        // outside `try` ensures it also runs after a caught exception.
        cambc::end_turn();
    }
}
```

Read it one piece at a time:

- `#include <cambc.h>` makes SDK declarations visible to this source file.
- Angle brackets normally mean a library/SDK header; quotes normally mean a project header.
- `int main()` is the program's entry function. `int` is its return type.
- `{ ... }` encloses a block.
- `Bot bot;` constructs one `Bot` object. Because it is outside the loop, its member fields survive across turns for this champion instance.
- `while (true)` repeats forever. `true` is a Boolean value.
- `if (...) { ... } else { ... }` chooses one branch.
- `cambc::is_draft()` uses `::` to look up a name inside namespace `cambc`.
- `bot.play_turn()` uses `.` to call a method on an object.
- `try` and `catch` prevent a standard C++ exception from killing the guest loop.
- `const std::exception& error` means “refer to this exception without copying or changing it.”
- `<<` sends pieces to the output stream.
- `'\n'` is one newline character.
- Every ordinary statement ends in `;`.

Keep `cambc::end_turn()` outside the `try`. Even after a handled error, the bot must yield to the engine.

## 3. Headers, source files, declarations, and definitions

A header commonly declares a class. In the game, this example remembers which camp group the current champion is pursuing between turns and exposes the function called by the main loop:

```cpp
// Prevent duplicate declarations if several source files include this header.
#pragma once

class Bot {
    // Private persistent state. `-1` is a sentinel meaning "no target yet".
    int target_group = -1;

public:
    // Public declaration: main.cpp is allowed to call this once per turn.
    void play_turn();
};
```

The source file then defines what that champion actually does when the engine gives it a turn:

```cpp
// Import the matching class declaration before defining its method.
#include "bot.h"

// `Bot::` says this function belongs to the Bot class declared above.
void Bot::play_turn() {
    // Read observations, choose legal actions, and update persistent state.
    // Real movement/combat/banking logic would go here.
}
```

Syntax:

- `class Bot` defines a new type.
- Class members are private by default. `target_group` cannot be accessed freely from outside.
- `public:` changes the access level of following members.
- `void` means a function returns no value.
- `Bot::play_turn` means “the `play_turn` method belonging to `Bot`.”
- `int target_group = -1;` both declares and initializes an integer member. `-1` can mean “no target.”
- `#pragma once` prevents the header from being included more than once in one translation unit.

Each selected champion gets a separate process/instance, so `target_group` persists for that champion but is not shared with allied champion processes.

## 4. Fundamental values and types

Common types in the bot:

| Type | Meaning | Example |
|---|---|---|
| `bool` | `true` or `false` | `bool threatened = false;` |
| `int` | ordinary signed integer | `int attempts = 0;` |
| `std::uint8_t` | exactly 8 unsigned bits | one shared-memory byte |
| `std::uint32_t` | exactly 32 unsigned bits | rounds, gems, gold |
| `std::uint64_t` | exactly 64 unsigned bits | fuel count |
| `float` | fractional number | health and stats |
| `cambc::vec2` | two integer coordinates | `cambc::vec2 p{4, 7};` |

Use `auto` when the initializer makes the type clear and writing it out would add noise:

During a champion turn, these locals capture the current round and provide access to the one champion this process is authorized to control:

```cpp
// Copy the current round number into an immutable local value.
const auto round = cambc::round_number();

// Bind a reference to the authenticated self object; actions such as move,
// attack, recall, and shop must be called through this object.
auto& me = cambc::self();
```

These two uses differ:

- `const auto round` stores a value that cannot be reassigned.
- `auto& me` stores a reference, an alias for the engine's authenticated champion object. The `&` avoids copying and lets us call its action methods.

Use explicit fixed-width types where byte layout matters, especially shared/draft memory.

## 5. Operators used constantly

This simplified retreat decision shows how ordinary C++ operators combine live champion health with strategic state:

```cpp
// `0.35f` means 35% as a float. The comparison produces a boolean.
const bool low_health = me.health() < me.max_health() * 0.35f;

// Recall only when both conditions hold: health is low AND we are not already
// safe on spawn. `!` negates the existing `at_spawn` boolean.
const bool should_recall = low_health && !at_spawn;
```

| Operator | Meaning |
|---|---|
| `=` | assign |
| `==`, `!=` | equal, not equal |
| `<`, `<=`, `>`, `>=` | comparisons |
| `+`, `-`, `*`, `/` | arithmetic |
| `!condition` | logical NOT |
| `a && b` | logical AND; `b` is skipped if `a` is false |
| `a \|\| b` | logical OR; `b` is skipped if `a` is true |
| `++i` | increase `i` by one |
| `x += y` | same as `x = x + y` |

The `f` in `0.35f` makes the literal a `float`, matching the SDK's health values.

Short-circuiting is useful for safety:

Before attacking a visible enemy or camp, the bot should check its action allowance and avoid querying live properties when the target is not visible:

```cpp
// `&&` evaluates left to right and stops as soon as one condition is false.
// That ordering protects the later live health query from a hidden target.
if (me.can_attack() && target.is_visible() && target.health() > 0) {
    // This is still only a teaching shape: production code must also verify
    // range and target category before attempting the action.
    me.attack(target);
}
```

If `can_attack()` is false, later checks are not evaluated. Still, visibility must be checked before querying live hidden properties.

## 6. Control flow

### `if`, early return, and priority rules

At the start of a champion turn, urgent or mutually exclusive states can finish the decision early. This example preserves an existing tribute channel, otherwise begins a planned retreat:

```cpp
// A channeling champion should not issue unrelated actions that would be
// illegal or would cancel the current objective.
if (me.is_submitting_gems()) {
    return;
}

// A higher-priority survival decision pre-empts normal farming for this turn.
if (should_recall) {
    me.recall();
    return;
}
```

An early `return` exits the current function. This is a clear way to express a priority hierarchy, but it can accidentally discard remaining legal actions. For example, immediately returning after a melee basic attack wastes a possible walk or spell. Return only when the rest of the turn is genuinely finished.

### Counting loop

Navigation code may deliberately allow a small, bounded number of retries after a hidden bush occupant is revealed. This loop demonstrates the counter syntax without risking an unbounded turn:

```cpp
// Start at zero; continue while below two; increment after each iteration.
for (int attempt = 0; attempt < 2; ++attempt) {
    // At most two movement/pathfinding attempts happen here.
}
```

The three clauses mean initialization; continue condition; update.

### Range-based loop

Target selection commonly examines each camp currently visible to this champion. The range-based loop handles that collection one snapshot at a time:

```cpp
// `const auto&` avoids copying each camp snapshot and prevents modification.
for (const auto& camp : cambc::vision::camps()) {
    // Score, attack, or remember this visible camp here.
}
```

`const auto&` avoids copying and prevents modification. The container returned by `vision::camps()` owns its elements for the duration of the loop.

## 7. Containers you will meet

### Fixed-size array

An immutable array is useful for a small policy table known at compile time—for example, candidate gem thresholds that an experiment will compare:

```cpp
// The type promises exactly four integers; braces supply all four values.
const std::array<int, 4> thresholds{10, 20, 30, 40};

// C++ indices start at zero, so `[0]` reads the first threshold: 10.
const int first = thresholds[0];
```

`std::array<int, 4>` contains exactly four integers. Indexing begins at zero. `thresholds[0]` is the first value.

### Growable vector

Draft planning often discovers a variable number of valid destinations. A vector can collect those positions as the map is analysed:

```cpp
// Start with an empty growable collection of map positions.
std::vector<cambc::vec2> goals;

// Append one candidate destination at coordinate (4, 7).
goals.push_back(cambc::vec2{4, 7});
```

`std::vector<T>` stores a runtime-sized sequence of `T`. `push_back` appends. Vectors allocate memory, so repeated construction in hot turn logic can cost fuel.

### Optional value

Pathfinding cannot always provide a next step: the champion may already be at a goal or every route may be blocked. The optional forces the bot to handle that absence safely:

```cpp
// The result either contains a direction vector or contains no value.
const auto next = field.next_move_from(me.position());

// Never dereference an optional until its value has been checked.
if (next.has_value()) {
    // `*next` retrieves the contained direction for the movement action.
    me.move(*next);
}
```

`std::optional<cambc::vec2>` either contains a direction or contains nothing. `has_value()` checks. `*next` accesses the contained value. Empty can mean already at a root or unreachable, so context still matters.

### Variant

A camp group has one of several state shapes. `std::variant` safely stores one alternative at a time:

Here the champion has vision of a camp group and wants to use its visible respawn timer without incorrectly treating every state as respawning:

```cpp
// Capture the group's currently visible state variant once for this decision.
const auto state = group.state();

// Test the active alternative before retrieving its respawn-specific fields.
if (std::holds_alternative<cambc::map::camp_group_respawning>(state)) {
    const auto respawn =
        std::get<cambc::map::camp_group_respawning>(state);
    // Use `respawn.timer` to avoid walking toward a camp that is not ready.
}
```

The angle-bracket part, `<Type>`, is a template argument: it tells the generic standard-library function which alternative to test or retrieve. Calling `std::get` for the wrong alternative throws, so test first.

## 8. Enums and state machines

An enum gives names to a fixed set of values:

These values describe the champion's current macro job, making persistent turn-to-turn state clearer than unexplained integers:

```cpp
// `enum class` creates a distinct, type-safe set of named states.
enum class Goal {
    travel,
    clear,
    capture,
    haul,
    bank,
    pitstop
};

class Bot {
    // A newly constructed champion begins by travelling toward assigned work.
    Goal goal = Goal::travel;
};
```

`enum class` is safer than plain integers: the compiler prevents accidentally mixing a `Goal` with a camp index or round number.

A state machine says what behavior owns the champion now and when to transition:

During `play_turn()`, this dispatcher sends the champion to exactly one macro-state handler. The helper names below are conceptual Bot methods, not CAMBC SDK calls:

```cpp
// Inspect the persistent state selected by earlier turns and observations.
switch (goal) {
case Goal::travel:
    // Move toward the currently assigned camp or objective.
    travel_toward_target();
    break;
case Goal::clear:
    // Attack/cast against the assigned camp group.
    clear_target_group();
    break;
case Goal::capture:
    // Remain in the cleared spawn region through the capture phases.
    hold_capture_region();
    break;
case Goal::haul:
    // Carry earned gems toward an altar approach tile.
    travel_toward_altar();
    break;
case Goal::bank:
    // Begin or preserve the tribute channel that turns carried gems into score.
    start_or_continue_tribute();
    break;
case Goal::pitstop:
    // Buy upgrades and finish recovery before returning to the route.
    shop_and_recover();
    break;
}
```

The method names above are architectural examples, not current SDK methods. You would implement them in your `Bot` class. `break` exits the `switch` case so execution does not fall into the next one.

## 9. Functions and templates

A normal helper:

Planning code can wrap the SDK's Chebyshev calculation when it wants an ordinary integer cost for comparing camps or objectives:

```cpp
// Parameters are copied because `vec2` values are tiny coordinate pairs.
int distance(cambc::vec2 a, cambc::vec2 b) {
    // Convert the SDK result explicitly to the integer type promised above.
    return static_cast<int>(a.chebyshev_distance(b));
}
```

- The function accepts two `vec2` values and returns `int`.
- `static_cast<int>(...)` requests an explicit, compiler-checked conversion.
- Parameters passed by value are local copies; tiny values such as `vec2` are fine to copy.

The starter uses a function template so the same attack logic works for champions and camps:

This helper illustrates a shared legality gate for different visible target types. It is deliberately simple: production combat should also account for action ordering, damage, shields, and strategic value.

```cpp
// Ask the compiler to generate this helper for every compatible target type.
template<class Target>
// `const Target&` observes the target without copying or modifying it.
bool attack_if_in_range(const Target& target) {
    auto& me = cambc::self();

    // Short-circuit before querying health when the target is hidden.
    if (!me.can_attack() || !target.is_visible() || target.health() <= 0) {
        return false;
    }

    // The attack mask contains the tiles this champion can currently hit.
    if (!me.attack_tiles().is_set(target.position())) {
        return false;
    }

    // All teaching-example checks passed, so attempt the basic attack.
    me.attack(target);
    return true;
}
```

`template<class Target>` lets the compiler create a version for each compatible target type. This is powerful, but beginners should first write ordinary functions when only one concrete type is needed.

## 10. Namespaces and aliases

Long qualified names are precise:

For example, navigation code can declare an empty map mask while making it explicit that `bitboard` belongs to the CAMBC SDK:

```cpp
cambc::bitboard blocked; // A tile set that will later hold obstacles.
```

For a source file, a namespace alias can reduce clutter:

The alias changes only how the source is written; it does not create a different bitboard type or change any game behaviour:

```cpp
namespace bc = cambc;  // Let `bc::` mean the same thing as `cambc::` here.
bc::bitboard blocked;  // Exactly the same SDK type as above.
```

Avoid `using namespace cambc;` in headers because it imports every name and can create confusing collisions. Narrow aliases or individual `using` declarations are easier to reason about.

## 11. Exceptions versus ordinary `false`

CAMBC action calls have an important two-level failure model:

- A newly discovered hidden obstruction commonly returns `false`; refresh observations and try another legal choice.
- A call already known to be invalid throws, commonly `cambc::error` or a standard exception; this usually indicates a bot bug or stale assumption.

Do not use exceptions as routine branching. Check preconditions first, handle the documented `false` case, and keep the top-level catch as a final safety net and diagnostic.

---

# Part V — The C++ API as a mental model

The API reference is large because it documents hundreds of methods, but most bot code uses four categories.

## 1. Static map information: `cambc::map`

Draft code can read these values to understand the complete fixed battlefield before selecting champions or assigning camp routes. They describe map geometry and original camp definitions, not live enemy positions:

```cpp
// Each `const auto` stores one immutable snapshot/value for this calculation.
const auto walls = cambc::map::walls();
const auto holes = cambc::map::holes();
const auto altars = cambc::map::altars();
const auto groups = cambc::map::camp_groups();

// Dimensions help validate coordinates or size planning buffers.
const auto width = cambc::map::width();
const auto height = cambc::map::height();
```

This information is ideal for draft planning because terrain and original camp definitions are static. The repository currently contains nine published maps: `collision`, `corners`, `elkring`, `expanse`, `interlock`, `lanes`, `monolith`, `packs`, and `rows`. Do not hardcode their layouts; query map metadata.

## 2. Current observations: `cambc::vision`

During a champion turn, these calls capture what that champion can currently observe. A bot can use the snapshots for target selection, collision avoidance, and hostile-lock detection, but must not treat them as permanent world truth:

```cpp
// Tiles currently visible to this champion under walls/bush vision rules.
const auto visible_tiles = cambc::vision::visible_tiles();

// Currently visible dynamic objects; hidden objects are absent.
const auto camps = cambc::vision::camps();
const auto enemies = cambc::vision::champions(cambc::team::enemy);
const auto locks = cambc::vision::altar_locks(cambc::team::enemy);
```

These are what the current champion can see now. They may change after moving or after a failed hidden-obstruction action.

`cambc::champions(team)` and `cambc::vision::champions(team)` are not interchangeable:

- the first gives handles for the whole roster, including hidden champions;
- the second gives currently visible champion views.

Many live properties—position, health, bag contents—cannot safely be queried on a hidden handle. Check `is_visible()` or use the vision list.

## 3. Authenticated self and actions: `cambc::self()`

Every champion process controls exactly one authenticated body. A turn function normally gets that reference once, then checks which action allowances remain before doing expensive planning:

```cpp
// `auto&` binds an alias to the engine-owned self object rather than copying it.
auto& me = cambc::self();

if (me.can_move()) { /* choose and attempt one legal movement action */ }
if (me.can_attack()) { /* choose and attempt a legal basic-attack target */ }
if (me.can_cast()) { /* choose at most one successful spell this turn */ }
```

Actions are self-only. A handle representing an ally or enemy is for observation/targeting; calling movement or shopping on it is invalid.

## 4. Team/global state

Macro policy can use the score and round to become more conservative near victory or more urgent near the round limit. The fuel value guards optional computation rather than changing game rules:

```cpp
// These values are stable enough to read once for the current decision.
const auto round = cambc::round_number();
const auto our_score = cambc::global_submitted_gems(cambc::team::ally);
const auto enemy_score = cambc::global_submitted_gems(cambc::team::enemy);

// Fuel is the deterministic compute budget remaining in this bot turn.
const auto fuel = cambc::fuel_remaining();
```

Use these to change endgame urgency and guard optional computation.

## 5. Bitboards: sets of map tiles

A `cambc::bitboard` is an efficient mask covering the map. A set bit means “this tile belongs to the set.”

Navigation builds one obstacle mask by taking the union of static terrain and currently visible occupied champion tiles. It then removes the moving champion's own tile so the path search can begin there:

```cpp
// `|` returns the union: a tile is blocked if it is a wall OR a hole OR an
// altar. The expression continues across lines until the semicolon.
auto blocked = cambc::map::walls()
             | cambc::map::holes()
             | cambc::map::altars();

// `|=` modifies the existing mask in place, adding all currently visible
// champion-occupied tiles to the static obstacles.
blocked |= cambc::vision::champion_tiles();

// `champion_tiles()` includes us. Clear our own bit or the pathfinder would
// consider its starting tile impassable.
blocked.set(cambc::self().position(), false);
```

The operators are set algebra:

| C++ | Set meaning | Example question |
|---|---|---|
| `a \| b` | union | wall **or** hole? |
| `a & b` | intersection | visible **and** occupied? |
| `a & ~b` | difference | in `a` but not `b`? |
| `~a` | complement | every in-bounds tile not in `a` |
| `a.is_set(p)` | membership | is position `p` in `a`? |
| `a.count()` | cardinality | how many tiles? |
| `a.positions()` | materialize positions | iterate every set tile |

`|=` modifies the mask in place. `|` returns a new result. Calling `positions()` allocates a vector, so do it only when you actually need individual coordinates.

A tactical routine might create this radius mask to ask which enemies, allies, or camp members lie within two Chebyshev tiles of the current champion:

```cpp
// Start with no selected tiles; draw operations add bits to the mask.
cambc::bitboard nearby;
nearby.clear();

// Add every in-bounds tile at Chebyshev distance two or less from `me`.
nearby.draw_chebyshev(me.position(), 2);
```

## 6. Distance fields: many goals, one efficient search

`move_towards(target)` is convenient for one target. A distance field is stronger when many tiles count as success—for example, every legal tile adjacent to any unlocked altar.

In the game, a gem carrier can use this pattern to route toward the nearest currently legal tribute position around any altar. The example demonstrates the data flow and C++ operators; production banking must additionally exclude hostile-locked or strategically unsafe altars and should reuse scratch storage:

```cpp
// `goals` will become the union of every tile from which tribute is in range.
cambc::bitboard goals;
goals.clear();

// `.positions()` materializes the altar mask as individual coordinates.
// `const auto altar` copies each small `vec2` position for this iteration.
for (const auto altar : cambc::map::altars().positions()) {
    // Build the approach area for this one altar from an empty mask.
    cambc::bitboard approach;
    approach.clear();

    // Add all tiles within the official Chebyshev tribute range. This also
    // initially includes tiles that may be illegal to stand on.
    approach.draw_chebyshev(altar, cambc::constants::submit_gems_range);

    // `|=` is set union in place: accumulate this altar's approach tiles
    // without discarding goals added for earlier altars.
    goals |= approach;
}

// A route may not enter static terrain, the enemy spawn, or a tile visibly
// occupied by a dynamic object. Each `|` combines another obstacle set.
auto blocked = cambc::map::walls()
             | cambc::map::holes()
             | cambc::map::altars()
             | cambc::map::spawn_region(cambc::team::enemy)
             | cambc::vision::champion_tiles()
             | cambc::vision::camp_tiles()
             | cambc::vision::teleport_tiles();

// Our own champion appears in `champion_tiles()`. Clear that one bit so the
// shortest-path search is allowed to start from `me.position()`.
blocked.set(me.position(), false);

// `~blocked` is the complement (tiles not blocked). `&=` is intersection in
// place, so this keeps only approach tiles that are legal destinations.
goals &= ~blocked;

// A distance field records the shortest number of steps from reachable tiles
// to the nearest root/goal. `visited` is reusable scratch/output storage.
cambc::distance_field field;
cambc::bitboard visited;

// Search outward from every legal goal while refusing to cross `blocked`.
field.compute(blocked, goals, visited);

// The result is an optional direction delta. It is empty if our tile was not
// reached or is already a goal, so it must be checked before dereferencing.
const auto direction = field.next_move_from(me.position());

// `&&` short-circuits: `can_move()` is checked only when a direction exists.
if (direction && me.can_move()) {
    // Unary `*` extracts the `vec2` stored inside the optional. The movement
    // call returns whether the attempted step succeeded.
    const bool moved = me.move(*direction);
    if (!moved) {
        // A hidden occupant may just have been revealed. Recompute or try
        // another optimal direction from field.next_moves_from(...).
    }
}
```

The goals are distance zero “roots”; distance values grow outward from them. `next_move_from` returns a direction delta toward a root.

The example deliberately shows the concepts, not a complete production navigator. A production version should distinguish unreachable from hidden-collision failure, exclude hostile altar-lock goals, reuse scratch objects, and respond to changed occupancy.

## 7. Abilities safely

During combat, a champion should filter ability use through remaining action allowance, cooldown, target category, visibility, and geometric range. This example tries slot zero against the first visible in-range enemy and stops after one successful cast:

```cpp
// Get our controllable champion and its two bound ability views.
auto& me = cambc::self();
auto abilities = me.abilities();
auto& first = abilities[0]; // `[0]` selects the first ability slot.

// `&&` short-circuits cheap legality gates before target searching.
if (me.can_cast() && first.is_ready() && first.can_target_enemies()) {
    // `valid_tiles()` is geometric range only, not complete action legality.
    const auto range = first.valid_tiles();

    // Iterate only enemies visible to this champion right now.
    for (const auto& enemy : cambc::vision::champions(cambc::team::enemy)) {
        if (range.is_set(enemy.position())) {
            // `use` returns true only when the cast succeeds. A false result
            // can reveal a previously hidden obstruction without spending it.
            const bool cast = first.use(enemy);
            if (cast) {
                // Only one successful spell is allowed this turn.
                break;
            }
            // `false` may mean a hidden obstruction was revealed.
        }
    }
}
```

Subtleties:

- `abilities()` returns the two bound ability views in `std::array`.
- `[0]` is slot zero.
- `valid_tiles()` is geometric range only. It does not by itself prove readiness, target category, visibility, or legal occupancy.
- Only one successful spell may be cast per turn.
- After a successful melee-compatible spell, do not automatically throw away other legal move/attack actions.

For damage decisions, prefer `first.damage_amount(enemy)` over manually multiplying Focus because the API can include mitigation, shields, passives, and health caps.

## 8. Buying before returning while dead

Dead champions can shop, so the ordering below is intentional. This turn function spends affordable gold before checking life state, letting a dead champion use otherwise wasted turns to prepare upgrades for its eventual respawn:

```cpp
void Bot::play_turn() {
    // Actions and state queries for this process go through authenticated self.
    auto& me = cambc::self();

    // `const auto` stores one exact SDK item enum for this purchase attempt.
    const auto item = cambc::item_type::monster_shard_of_strength;
    if (me.can_buy(item)) {
        // Buying is legal while dead when the champion satisfies shop rules.
        me.buy(item);
    }

    // Only after shopping do we stop movement/combat logic for a dead body.
    if (!me.is_alive()) {
        return;
    }

    // Living champion movement, combat, farming, and banking decisions follow.
}
```

If you write `if (!me.is_alive()) return;` first, the bot wastes every dead shopping turn.

Use exact item names from the current SDK. The family and stat are both part of the enumerator, such as `monster_shard_of_strength` or `power_shard_of_focus`.

## 9. Correct hostile-lock handling

Checking `has_altar_lock(altar)` only answers whether some visible lock exists, and an allied lock permits your tribute. Before choosing an altar, the bot can instead scan the enemy-filtered visible lock list. This helper answers only whether the specified altar is visibly hostile-locked; hidden or later state can still change:

```cpp
// Accept the altar coordinate by value and return a true/false answer.
bool altar_blocked_for_us(cambc::vec2 altar) {
    // The team filter avoids treating our own lock as hostile.
    for (const auto& lock :
         cambc::vision::altar_locks(cambc::team::enemy)) {
        // Coordinate equality identifies the requested altar.
        if (lock.position() == altar) {
            return true;
        }
    }
    // No currently visible enemy lock matched this altar.
    return false;
}
```

The team-filtered list also handles the API detail that `altar_lock_at(altar)` prefers an allied lock if both teams have a lock on the same altar.

If a hostile lock is visible and in attack range, explicitly attack the lock. That is clearer and safer than intentionally calling `submit_gems` and relying on its implicit conversion to an attack.

## 10. Hidden-blocker retry

When movement returns `false`, a hidden occupant may have been revealed without consuming the movement allowance. This teaching helper permits one recomputation attempt while preventing an accidental infinite retry loop:

```cpp
// Return true when one of the attempts moves successfully.
bool move_with_one_retry(cambc::vec2 target) {
    auto& me = cambc::self();

    // Continue for at most two attempts and only while movement remains legal.
    for (int attempt = 0; attempt < 2 && me.can_move(); ++attempt) {
        // `move_towards` recomputes using observations available at this call.
        if (me.move_towards(target)) {
            return true;
        }
        // Fresh vision may now show the hidden blocker. Production code should
        // refresh occupancy and choose an alternative, not blindly repeat.
    }
    // Neither attempt produced movement.
    return false;
}
```

This demonstrates the documented retry, but a production navigator should not blindly call the same unreachable target twice. After `false`, refresh visible occupancy and select an alternate next step or goal.

## 11. Draft code and the 1,024-byte plan

The starter randomly selects among current roster indices and writes `"hello world"`. That demonstrates the API, not a competitive draft.

A robust encoded plan begins with a version and a fully zero-initialized buffer. Draft code can encode compact route metadata once, then every allied champion process can decode the same plan during gameplay. This simplified example writes three fields explicitly rather than copying a compiler-dependent struct layout:

```cpp
#include <array>
#include <cstddef>

// `{}` zero-initializes all 1,024 bytes, preventing stale unwritten tail data.
std::array<std::byte, 1024> plan{};

// Fixed offsets define a tiny wire format understood by every decoder.
plan[0] = std::byte{1}; // Format version: change when the layout changes.
plan[1] = std::byte{3}; // Number of champion/squad routes encoded later.

// `static_cast` explicitly converts the chosen integral index into one byte.
plan[2] = static_cast<std::byte>(chosen_camp_index);

// Assignment submits the complete plan to engine-managed draft memory.
cambc::draft_memory = plan;
```

Why not copy a C++ struct's raw bytes immediately?

- A compiler may insert padding between fields.
- Multi-byte integers have byte-order concerns.
- Layout changes can silently break old decoding.
- Explicit bytes make the space budget visible.

Also note a niche API behavior: assigning to `draft_memory` submits bytes to the engine but does not mutate the object’s already captured readable snapshot. Short writes leave later engine bytes unchanged. Writing a full zero-filled 1,024-byte buffer avoids stale tails.

## 12. Eight-byte shared memory

Eight bytes are too small for a replicated world model. Use them for exceptions and coordination events.

During the match, allied champion processes have only eight shared bytes. This conceptual protocol gives important offsets names, reads the current objective, and stamps the message with the current round modulo 256 so readers can reject stale information:

```cpp
// The underlying values are byte indices, but `enum class` prevents them from
// being mixed accidentally with unrelated camp, champion, or round integers.
enum class SharedByte : std::size_t {
    frame = 0,
    objective = 1,
    alarm = 2
};

// Index shared memory using the named objective offset, then explicitly
// convert the stored byte into an unsigned 8-bit integer for local use.
const auto objective = static_cast<std::uint8_t>(
    cambc::shared_memory[
        static_cast<std::size_t>(SharedByte::objective)]);

// Publish a compact freshness tag. Converting to uint8_t intentionally keeps
// only the low eight bits, so readers must compare within a short age window.
cambc::shared_memory[
    static_cast<std::size_t>(SharedByte::frame)] =
    static_cast<std::uint8_t>(cambc::round_number());
```

Important concepts:

- `enum class` names offsets without treating them as arbitrary integers.
- `static_cast` makes intended conversions explicit.
- Writing a round modulo 256 lets readers reject stale messages if the expiration window is much smaller than 256.
- Multiple champions can write in one round. Turn order determines which write is seen last.
- Reading/writing invokes the host and costs fuel. Read once into locals, decide, then write a compact update.

FOUNDRY proposes this complete eight-byte layout:

| Byte | Proposed meaning |
|---:|---|
| 0 | frame parity/version |
| 1–2 | last important enemy sighting |
| 3 | contested camp plus alarm bit |
| 4 | low claim bits |
| 5 | high claim bits plus relief flag |
| 6 | tribute alarm |
| 7 | checksum |

That is a team plan, not an SDK requirement. Before implementation, write encoding/decoding tests and specify exactly how every bit maps to values and how stale messages expire.

---

# Part VI — From a legal bot to a strategic bot

## 1. Do not optimize “nearest camp”; optimize the whole scoring cycle

The nearest camp may be a bad choice if it has low reward, long clear time, is already assigned, or leaves the carrier far from a safe altar.

A first scoring model is:

```text
cycle_turns =
    travel_to_camp
  + estimated_clear_turns
  + capture_turns
  + travel_to_altar
  + tribute_turns

safe_gems = camp_gems * probability_of_success

value = safe_gems / max(1, cycle_turns)
```

Then penalize:

- likely enemy contest;
- expected health loss;
- duplicated allied assignment;
- carrier death risk;
- hostile altar locks or stun threats;
- delaying a higher-value camp's respawn cycle;
- using a strong interceptor when a weaker farmer could do the job.

This is inspired by resource-return games such as Halite, where good bots evaluate the outward trip, collection, and return rather than only resource density. The formula's *structure* transfers; its weights must be learned from CAMBC games.

## 2. Estimate clear time, not just reward

A rough basic-attack-only estimate is:

```text
hits = ceil(monster_health / effective_damage_per_hit)
```

But actual service time depends on:

- ability burst and cooldowns;
- attack reset timing;
- Varg splash against packed groups;
- Vendetta resets after individual monster kills;
- ranged movement/attack conflict;
- travel between live monster positions;
- camp damage forcing recall;
- another champion helping, which may or may not be worth the lost parallelism.

Prefer the API's live damage predictions when deciding whether an attack or spell kills. For draft planning, use immutable champion/camp design stats and validate estimates against replay statistics.

## 3. Allocate champions globally

If every champion greedily chooses its own best camp, several may accidentally choose the same one while another valuable camp idles. That is different from an intentional squad: replay evidence shows strong teams often pair a durable melee leader with a ranged damage dealer, clearing hostile camps faster while the melee body absorbs retaliation. Current measurements report allied co-hits on 30% of camp-hit rounds for the top two teams, compared with only 8% for FOUNDRY.

The assignment unit should therefore be a **champion or a planned squad**, not automatically one solo champion per camp. With only a few bodies, a small exhaustive assignment can be simpler than a sophisticated optimization library.

During draft planning, structures like these can hold the inputs to a simple assignment search. The utility function converts camp reward, travel/service time, danger, and champion suitability into one comparable score; the numerical weights are hypotheses to benchmark, not official game constants:

```cpp
// Public fields bundle the facts the planner knows about one possible job.
struct Task {
    int group_index;     // Stable index of the camp group to service.
    int gems;            // Gem reward if the group is captured.
    int gold;            // Gold reward used for future upgrades.
    int estimated_turns; // Travel + clear + capture estimate.
    int danger;          // Team-defined contest/damage risk estimate.
};

// Champion-specific terms let the same task score differently for each body.
struct ChampionProfile {
    int camp_efficiency; // Expected suitability for clearing this work.
    int risk_tolerance;  // How strongly danger should penalize this champion.
};

// References avoid copying the records; `const` promises not to modify them.
int utility(const ChampionProfile& champion, const Task& task) {
    // Positive terms reward economic output and champion suitability.
    // Negative terms charge for time and risk. The result is only meaningful
    // relative to other tasks evaluated with the same weights.
    return task.gems * 100
         + task.gold * 20
         + champion.camp_efficiency
         - task.estimated_turns * 30
         - task.danger * champion.risk_tolerance;
}
```

`struct` is like a class whose members are public by default. This example stores related data under meaningful field names.

A draft planner can recursively try each unused task for each champion/squad and keep the assignment with maximum total utility. Squad utility must include combined DPS, which member tanks, formation travel, and the opportunity cost of not farming in parallel. During play, recompute only when important facts change: death, contest, delayed respawn, enemy carrier, or unreachable route.

## 4. Separate long-term job from temporary interrupt

Store the route/job separately from urgent behavior. At runtime, this enum can represent a temporary reason to suspend—but not erase—the champion's assigned camp route. Once the emergency finishes, `none` allows the macro state machine to resume:

```cpp
// These are conceptual policy states, not values supplied by the CAMBC SDK.
enum class Interrupt {
    none,              // Follow the ordinary assigned route.
    retreat,           // Prevent imminent death or protect carried gems.
    tribute,           // Convert a valuable bag into permanent team score.
    break_lock,        // Remove a hostile lock blocking the chosen altar.
    defend_capture,    // Prevent an enemy from resetting our capture progress.
    intercept_carrier  // Pursue an exposed enemy carrying valuable gems.
};
```

If a champion detours to survive one enemy turn, it should not permanently forget its scheduled camp. A useful decision order is:

```text
maintain an active channel when it should continue
    -> shop while dead or on spawn
    -> prevent immediate death / secure winning tribute
    -> remove hostile altar lock
    -> deny an almost-complete enemy capture
    -> kill or peel an exposed high-gem carrier
    -> resume the macro state machine
```

The exact order is contextual. “Always fight” and “always flee” are both exploitable policies.

## 5. FOUNDRY's implemented runtime machine

The current GitHub implementation uses these broad states:

```text
BOOT / CHANNEL / TACTIC / PITSTOP / BANK
TRAVEL / CLEAR / CAPTURE / HAUL / IDLE
```

Its decision guards broadly run in this order:

```text
continue channel -> tactic offer -> capture hold -> retreat/shop trip
-> bank -> select/clear camp -> pre-position for respawn -> idle
```

This is a real implementation, not merely a proposed diagram. It includes target hysteresis, an observed camp ledger, hidden-blocker retries, unreachable-target cooldowns, a camp-fitness gate, contested-sortie blacklisting, and damaging/CC camp casts. It still does not execute the full strategic design: route ordering is often replaced by nearest actionable work, several plan flags are unused, and resets, shields, dashes, healing, formations, and squad coordination remain incomplete.

Possible transition conditions:

| From | To | Condition |
|---|---|---|
| `TRAVEL` | `CLEAR` | Target group is visible and alive. |
| `TRAVEL` | `CAPTURE` | Target group is already cleared and reward is available. |
| `CLEAR` | `CAPTURE` | Every monster in the connected group is dead. |
| `CAPTURE` | `HAUL` | Reward completes and this champion has gems. |
| `HAUL` | `BANK` | Beside a usable altar. |
| `BANK` | `PITSTOP` or `TRAVEL` | Tribute completes; decide whether shopping is worth the detour. |
| Any living state | interrupt | Threat, lock, contest, carrier opportunity, or critical low health. |

Do not transition only because a local object disappeared from vision. An invisible group is “unknown,” not necessarily dead, alive, or respawning.

## 6. Camp ledger and periodic scheduling

Camp production is deterministic after your own confirmed capture:

```text
ready_at = capture_completion_round + group.max_respawn_timer()
```

Store `ready_at` in the champion's plan/ledger. Arrive shortly before the next spawn rather than wandering. Remember that an occupied spawn tile delays the whole group; schedule departure as well as arrival.

Enemy captures and fights create uncertainty. Represent state honestly:

```text
confirmed ready round
visible alive
visible reward available
visible respawning with timer
unknown because outside vision
```

Never turn “not visible” into “not present.”

## 7. Solo capture by default

Because more allies do not accelerate capture and rewards split among those present, one designated capturer is usually best. Other champions can leave the region to begin the next job.

Exceptions include:

- an enemy is close enough that the capturer needs protection;
- the planned recipient should be Vesper for bonus gold;
- gems must reach a champion already channeling the capture-overlap tribute trick;
- split rewards reduce death risk or enable several immediate purchases;
- an ally must remain to keep the region uncontested after another leaves.

These are testable exceptions, not reasons to crowd every capture.

## 8. Banking is a risk decision

The starter banks every positive bag immediately. That is safe in one sense but may waste most of the match walking.

Compare:

```text
bank_now =
    carried_gems * tribute_success_probability
  - travel_cost
  - channel_exposure

continue_farming =
    expected_extra_gems
  - extra_death_risk
  - risk_of_missing_endgame
```

Lower the banking threshold when:

- current gems would reach 1,000;
- health is low;
- enemies or stun abilities threaten the route;
- an altar is safe now but may soon be locked;
- too few rounds remain for another complete cycle;
- the bag is large enough that death creates a huge swing.

Raise it when:

- the route and altar are controlled;
- the next camp is nearby and safe;
- capture will add gems to a tribute whose duration is already locked;
- banking travel dominates the time cost.

A death can be close to a double swing: your team loses the chance to submit the bag, then the killer may submit the stolen gems.

## 9. The capture-overlap tribute technique

Because capture phases occur before channel completion and tribute duration is fixed at channel start:

1. stand beside an altar and on a camp spawn tile only where map geometry permits;
2. begin tribute with a small bag, ideally 1–10 gems for one tick;
3. the timer reaches zero at turn end;
4. the next round's capture phase grants more gems;
5. the channel completes at that champion's turn start and submits the whole new bag.

This is a real timing consequence of the rules, but only specific map geometry supports it. It is also vulnerable to stun, death, contest, and enemy altar lock. Build a targeted engine test before making it central to a route.

## 10. Combat should serve the economy

Ask what a fight accomplishes:

- steals a valuable bag;
- protects your carrier or tribute channel;
- denies or secures a capture;
- removes an altar lock;
- delays an opponent's 1,000th gem;
- claims a high-throughput camp route.

If it does none of these, the expected reward may be lower than another camp cycle.

### Hard invariants versus soft scores

Use hard filters for actions that must not happen:

```text
never voluntarily abandon a tribute that wins now without a stronger reason
never walk a large carrier into known lethal damage
never cast a spell at an invalid category
never assign two solo farmers to the same exclusive route accidentally
```

Then score remaining legal actions using soft preferences:

```text
+ progress toward objective
+ expected damage / kill value
+ protection for carrier
- predicted incoming damage
- congestion
- recent tile repetition
- distance from escape or altar
```

This is easier to tune than a giant nest of special-case `if` statements.

## 11. Action ordering and champion class

For each candidate turn, consider legal sequences, not isolated actions.

Melee might:

```text
walk -> attack -> reset -> attack
attack -> kill and refresh -> dash -> reset -> attack
spell -> walk -> attack, if that spell is walk-compatible
```

Ranged might:

```text
attack -> reset -> attack
walk and give up the ordinary attack
cast a walk-excluding spell and stay
cast a compatible reset, then use the restored attack allowance as permitted
```

Do not assume every textual sequence is legal for every current state; query action availability again after each action. The engine is the arbiter.

These sequences are strategy examples. Current GitHub FOUNDRY casts damaging/CC camp spells but does not yet implement the complete reset/dash/shield/heal sequences above.

## 12. Tank selection and camp aggro

Camps attack the nearest champion. You can deliberately position a durable or Jungle-equipped champion closest while fragile damage dealers attack farther away.

This is now a measured priority rather than a theoretical refinement. In the decoded losses, ranged FOUNDRY bodies took roughly 2–2.5 times the camp damage of comparable top-team bodies. Cassi and Issac were especially problematic: they averaged 12.5 tiles apart, so Cassi often tanked alone even though Issac's purpose in the pair is to stand closer.

This requires care:

- Chebyshev ties need deterministic understanding/testing.
- Walking a ranged damage dealer may sacrifice its attack.
- One champion absorbing all damage may force an early recall.
- Varg's shield and splash make it a natural pack tank, but only if the saved team turns exceed the cost of grouping.

## 13. Wards and timestamped evidence

The map is not unknown; dynamic state is. Treat an enemy sighting as time-stamped evidence:

When a champion or ward sees an enemy carrier, the bot can remember this small record after the enemy leaves vision. The round is essential because the stored coordinate becomes less trustworthy every turn:

```cpp
struct LastSeenEnemy {
    cambc::vec2 position;          // Last tile on which the enemy was visible.
    std::uint32_t round;           // Round of observation for staleness checks.
    std::uint32_t carried_gems;    // Economic importance at that observation.
};
```

As the sighting ages, expand the possible region by movement capability and reduce confidence. A three-round-old location is not a current coordinate.

High-value ward positions include:

- bushes beside altars;
- approaches to Monolith or other high-value groups;
- narrow route intersections;
- enemy return paths;
- a capture region that your farmer must temporarily leave.

## 14. Turn priority as traffic control

`set_priority` is not only a combat tool. It can reduce ally collision and coordinate sequences.

A reasonable context-dependent priority order is:

```text
winning or large gem carrier
    > endangered ally / peel
    > lock breaker or tribute escort
    > active capturer
    > ordinary farmer
    > scout
```

Because the change applies next round, plan one round ahead. When equal routes can conflict, deterministic tie-breaking by champion identity keeps all instances consistent without another shared byte.

## 15. Current FOUNDRY builds

PR #41 replaced broad role queues with queues selected from the champion's actual type. Each named queue entry means “complete this shard/emblem step”; the final entry repeats as the open-ended tail:

- **Varg, Vendetta, Marcella, Issac, Vesper, Ryth, Ren:** Power Strength -> Power Health -> Power Strength repeatedly.
- **Cassi, Stellar, Prism:** Power Focus -> Durability Health -> Power Focus repeatedly.
- **Tavi:** Power Focus -> Power Strength -> Power Focus repeatedly.
- **Willow:** Power Strength repeatedly.

Healthy non-Tavi champions with at least 180 unspent gold, no visible threat, and at most 10 carried gems can recall for a shop trip. Tavi is excluded because she buys shards in the field.

The merged change improved the two-sided local matchup against the previous FOUNDRY from 9/18 to 11/18 wins and cut mean final unspent gold to roughly 42–56 per champion. It missed its 12/18 target by one match, so these are measured defaults rather than proven optimal builds. The older Treasure/Jungle/Monster and late Tavi sell path in `docs/strategy.md` is now historical design context, not the current executable queue.

These are recommendations. Important questions to measure:

- Does an incomplete five-shard path delay too much raw power?
- Which camp damage breakpoints save a whole attack turn?
- Does Treasure repay 150 gold early enough on each route?
- Does survivability prevent enough recall/death downtime to beat damage?
- Does late selling actually improve win probability rather than merely final stats?

---

# Part VII — Starter baseline and current FOUNDRY status

## What `starter-cpp` does

The current `starter-cpp` is useful for learning API calls. It is not a competitive bot. It:

- drafts randomly;
- writes only `"hello world"` to draft memory;
- chooses a random Power stat;
- overwrites four shared bytes with the round;
- logs every turn;
- shops only after checking it is alive, missing dead shopping turns;
- never casts abilities;
- attacks the first target in API order;
- returns immediately after attacking, even when melee actions remain;
- banks any nonzero bag immediately;
- treats allied locks as if they block tribute;
- cannot solve the all-altars-hostile-locked case;
- may leave spawn on recall-arrival turn before full healing;
- does not deliberately handle a `false` hidden-block result;
- randomizes next-round priority;
- ignores camp value, respawn schedule, contest risk, and assigned roles.

That is normal for starter code. Keep it as a correctness-floor opponent, not as proof that a strategy is ladder-ready.

## What GitHub FOUNDRY now does

GitHub `main` at `e341ad05` has moved far beyond the starter. It now includes:

- draft-time map atlas and POI distance compilation;
- a validated plan encoded into the 1,024-byte draft memory;
- static camp assignment and route construction;
- runtime travel, clear, capture, bank, retreat, shopping, haul, and idle states;
- camp respawn observations and predicted ready rounds;
- hidden-blocker navigation retries;
- champion-specific item queues and deliberate shop trips;
- damaging/CC abilities against camps;
- channel interruption, carrier ganks, altar locks, capture denial, and poke tactics;
- a replay decoder and two-sided evaluation tools.

It also has measured weaknesses:

- In 75 platform losses, first capture averaged round 68 versus opponents' round 42 and the top two teams' round 26.
- Only 8% of camp-hit rounds involved multiple allied attackers, versus 30% for the top two teams.
- Cassi and Issac averaged 12.5 tiles apart despite sharing one life.
- Our losses averaged 8.1 deaths and 3.3k champion damage, versus opponents' 2.5 deaths and 9.7k damage.
- Across all 150 decoded platform games, we recalled 24.45 times per game versus 10.43 for opponents and died 7.25 times versus 4.42.
- Of those deaths, 4.92 per game happened while already below the executor's 40% retreat floor, versus 3.73 for opponents; 6.79 followed recent enemy-champion damage, versus 2.72.
- Only 17 linked Cassi/Issac death events were detected across all 150 games. Their separation remains strategically bad, but linked fate is not the main explanation for the team's overall death gap.
- The draft remains fixed; squads, grouped openings, focus fire, joint retreat, wards, and full ability micro are not yet implemented.

The recall and death-cause labels are replay-derived heuristics. For example, “death after champion damage” means the champion took enemy-champion damage during the report's recent-round window; it does not prove which exact action killed it or which single decision was wrong. Even with that limitation, the gaps are large enough to make survival a measured priority.

The current development plan therefore focuses first on correctness, timely retreat, and avoidable recall/death downtime, then on linked Cassi/Issac behaviour, general tank/ranged squads, a grouped opening, coordinated fights, and a meta-informed draft. See [`Analysis1.md`](Analysis1.md) for the detailed evidence and roadmap.

## Where to modify bot code—and where not to

There are two repository states to keep straight.

### In this old local branch

The local `bots/foundry/` is still close to `starter-cpp`. If you experiment here:

| Goal | File to change |
|---|---|
| Champion decisions such as movement, combat, banking, recall, and shopping | `bots/foundry/src/bot.cpp` |
| Persistent fields or helper declarations used by those decisions | `bots/foundry/src/bot.h` |
| Champion selection and draft-memory writing | `bots/foundry/src/draft.cpp` and `draft.h` |
| Small deterministic random helper, only if random behaviour itself is under test | `bots/foundry/src/random.h` |

Normally leave `main.cpp` alone. Its job is to keep one `Bot` object alive, dispatch draft/game turns, catch failures, and always call `cambc::end_turn()`.

### In the developed GitHub FOUNDRY

After that implementation is deliberately integrated into your development branch, make each change in the module that owns the decision:

| Behaviour | Main files |
|---|---|
| Draft picks and draft-time orchestration | `draft.cpp`, `draft.h` |
| Static map facts and points-of-interest | `atlas.cpp`, `atlas.h` |
| Camp assignment, route planning, roles, and compiled plans | `planner.cpp`, `planner.h`, `plan.h` |
| Runtime state transitions, retreat, clearing, capturing, hauling, and banking | `exec.cpp`, `exec.h` |
| Purchases, builds, shop trips, and consumables | `econ.cpp`, `econ.h` |
| Movement and distance-field navigation | `nav.cpp`, `nav.h` |
| Camp observations and respawn tracking | `ledger.cpp`, `ledger.h` |
| Visible-state helper structures | `obs.h` |
| Ganks, peel, locks, denial, poke, and tactical arbitration | `tactic/` |
| Eight-byte live team protocol | `wire.h` |

Change `plan.h` or `wire.h` only as a coordinated protocol change. Every producer and consumer must agree on field meaning, bounds, versioning, and stale-data handling; an isolated bit-layout edit can silently corrupt every champion's decisions.

### Do not edit these for ordinary strategy work

- `bots/starter-cpp/`: keep it unchanged as the reference/tutorial opponent.
- `sdk/`: generated API bindings; refresh them with the official tool rather than hand-editing.
- `.cambc/`, `bot-injected.wasm`, CMake/Ninja output, and other build artifacts.
- `maps/`: published binary maps are benchmark inputs, not strategy code.
- `docs/GameRules.md` and `docs/BotAPICpp.md`: exported references, not places to change engine behaviour.
- `factory/`: automation infrastructure, not bot policy.
- The remote `factory/ci-pair` branch: do not switch to or modify somebody else's work merely to develop bot behaviour.
- `tools/replay/` merely to make a weak result look better. Change analysis tooling only as a separately validated tooling task.
- Replays, downloaded platform data, temporary manifests, logs, or statistics output. Keep them outside tracked source.

Do not copy a change into both `foundry` and `starter-cpp`. Make the strategy change in the candidate bot, keep a frozen previous bot as the baseline, and let the benchmark reveal whether the change helped.

## A sensible implementation order from here

The old foundational steps above are largely implemented on GitHub `main`. The current evidence-based order is:

1. close remaining stale-handle, planner-DPS, and retreat/lock correctness issues;
2. reduce deaths below the retreat floor, deaths after enemy contact, and low-value recalls;
3. keep Cassi and Issac together with Issac tanking and joint retreat;
4. generalise that logic into melee/ranged farming squads;
5. group the team for the first high-value camps before splitting;
6. coordinate engage, focus fire, crowd control, and disengage;
7. test the meta-informed draft order;
8. add remaining ability micro and equipment-aware camp estimates;
9. improve value-per-time routing, capture ownership, wards, and denial profitability.

At every step, compare both sides against the previous bot, starter, and adversarial opponents using `tools/replay/local_eval.sh`. Starter wins are a minimum correctness gate, not the main performance test.

---

# Part VIII — Fuel-aware C++ optimization

## Correctness comes first

A fast wrong bot loses quickly. Optimize after measuring fuel or seeing a repeated hot path.

## High-value optimizations

### Move static work into draft or first turn

Terrain, camp spawn positions, camp rewards, map symmetry, and static point-to-point distances do not change. Compute once and encode/reuse.

### Use bitboard operations

Union/intersection/complement are native bulk map operations. They are generally preferable to asking the host about every tile in nested C++ loops.

### Reuse scratch storage

Many API types provide `_into` methods. A long-lived `Bot` can keep this bitboard as scratch storage and overwrite it each turn, avoiding a fresh allocation whenever the champion needs its current visible-area mask:

```cpp
// This object can be a persistent Bot member rather than a new local each turn.
cambc::bitboard visible;

// The `_into` API fills caller-owned storage with the current observation.
cambc::vision::visible_tiles_into(visible);
```

Persistent scratch bitboards and distance fields avoid repeated allocations. Do not reuse stale dynamic content without overwriting it.

### Avoid repeated host calls

At the beginning of one decision phase, copy stable engine observations into locals. Later scoring code can reuse them without repeatedly crossing the WebAssembly host boundary:

```cpp
// Read the scalar once; the round cannot change during this bot turn.
const auto round = cambc::round_number();

// Materialize the current visible enemies once for this phase of the decision.
const auto enemies = cambc::vision::champions(cambc::team::enemy);
```

Read once when a value is stable for the decision, then use the local. After an action changes position/vision, refresh the observations that can change.

### Avoid materializing positions unnecessarily

`mask.is_set(p)` is cheap membership. `mask.positions()` constructs a vector of every set tile. Use the latter only for actual iteration.

### Stop optional work safely

Before beginning optional route optimization or exhaustive target scoring, the bot can return to its top-level turn loop when the remaining deterministic fuel falls below an empirically chosen reserve:

```cpp
// `safety_margin` must leave enough fuel for invariant-preserving cleanup and
// for the outer loop to call `cambc::end_turn()` safely.
if (cambc::fuel_remaining() < safety_margin) {
    // Exit this helper/turn function; do not partially write a shared protocol.
    return;
}
```

Choose `safety_margin` empirically and remember the top-level loop still calls `end_turn()`. Never yield halfway through a write protocol or partially update persistent state without a resumable design.

## Optimizations to postpone

- elaborate custom allocators;
- full space-time multi-agent pathfinding;
- machine learning in the turn loop;
- hand-unrolled code without profiles;
- clever bit packing before the protocol meaning is stable;
- global A* every turn when SDK distance fields or cached guidance suffice.

Reliable simple navigation plus stuck detection is more valuable than an “optimal” planner that occasionally exhausts fuel or follows stale paths.

---

# Part IX — Build, run, inspect, and improve

## 1. Current workspace status

This local checkout is on `xuanming/localdev` at `966ec857`. It contains the restored SDK at [`sdk/cpp/cambc.h`](../sdk/cpp/cambc.h), but it does **not** contain the developed FOUNDRY now present on GitHub `main` at `e341ad05`. The read-only GitHub branch listing currently shows `main` and `factory/ci-pair`. No pull, merge, branch switch, commit, or push was performed while updating this guide.

The installed CLI currently reports 2.1.6 while `cambc.toml` records SDK 2.1.5, so an SDK/CLI warning is expected. The local rules, C++ API export, strategy document, SDK header, and `cambc.toml` have the same Git blob hashes as GitHub `main` at the refresh date, so the rule/API material in this guide is not stale even though the local bot implementation is behind. Do not hand-edit the SDK; coordinate SDK refreshes with the team because `cambc init` updates generated workspace files.

## 2. Basic commands

From the repository root:

```powershell
cambc --version
cambc build starter-cpp
cambc build foundry
cambc run foundry starter-cpp --map expanse --view
```

Create a new C++ bot only when you really want another implementation directory:

```powershell
cambc new experiment-name --lang cpp
```

Refresh maps:

```powershell
cambc maps pull
```

The network must be able to reach the official platform. Existing custom/edited maps are meant to be preserved by map refresh.

## 3. Three different kinds of match

“Benchmarking” can mean three different things. Keep them separate:

| Match type | Where it runs | Elo effect | Best use |
|---|---|---|---|
| Local `cambc run`/`run-batch` | Your computer | None; it never reaches the ladder | Fast development, controlled A/B tests, complete replay bundles |
| Platform unranked challenge | Official servers | None | Validate the uploaded bot and server environment against another team's submitted bot |
| Platform ranked group | Official servers | Changes Elo | Final external evaluation after local and unranked gates pass |

The public match API confirms the distinction. A sampled unranked Heavenly Court group had `kind: "unranked"`, `ratedAt: null`, and null `ratingBefore`/`ratingAfter` values. Ranked groups had `kind: "ranked"`, a non-null `ratedAt`, and numerical before/after ratings.

The currently sampled platform groups each contain five games. That is observed platform behaviour on 14 October 2026, not a permanent game rule. A complete local map-and-side comparison is larger: nine published maps × two team positions = **18 matches** per opponent.

## 4. Smoke test versus completed match

A short smoke test catches compilation, startup, and early-turn failures quickly:

```powershell
cambc run foundry starter-cpp --map expanse --rounds 50
```

This is not a performance benchmark. It cannot prove endgame behaviour, and `--statistics` requires a completed game. For final statistics, remove the round cap:

```powershell
cambc run foundry starter-cpp --map expanse --statistics replays/foundry-expanse.json
```

Use `--view` when you want the visualiser to open immediately, and `-o <directory>` when you need a particular replay-bundle destination. Do not lower `--fuel` during normal evaluation unless the experiment is specifically about fuel robustness.

## 5. Replays and logs

Open the latest replay bundle or a named one:

```powershell
cambc view
cambc view replays/<replay-bundle>.repl26a
```

A local bundle contains the game replay plus both teams' stdout and debug streams. A decoded replay can expose the post-match action timeline and full recorded state for analysis. That does **not** mean a champion could see the full state while deciding: during the match, ordinary vision, bushes, walls, and stale information still applied. When reviewing a decision, judge it using only information available to that champion at that time.

Watch for:

- idle turns;
- repeated movement failures;
- accidental duplicate routes versus intentional squad farming;
- whether a melee squad member takes camp aggro while ranged allies remain safely behind;
- first-capture round and collected gems by round 100;
- Cassi/Issac separation and whether either retreats alone;
- abandoned or contested capture timers;
- occupied spawn tiles delaying respawn;
- unsafe carried gems and gems lost on death;
- excessive recalls, recalls begun at unnecessarily high health, or retreats started too late;
- leaving spawn before the arrival-turn heal;
- unused abilities and reset opportunities;
- bad target order;
- tribute interrupted by a predictable stun/lock;
- bot exceptions or fuel exhaustion.

## 6. Built-in batch tests

`cambc run-batch` is the built-in way to run independent matches in parallel. Create a four-column manifest with one match per line:

```text
bots/foundry bots/foundry-v1 maps/expanse.map26a replays/candidate-a-expanse.repl26a
bots/foundry-v1 bots/foundry maps/expanse.map26a replays/candidate-b-expanse.repl26a
```

The columns are bot A, bot B, map file, and output replay. Repeat both orders for all nine maps, then run:

```powershell
cambc run-batch matches.txt --jobs 2
```

Use unused replay names; batch runs reject existing replay or diagnostic outputs. `--timeout` is a wall-clock safety limit per runner process. It does not change deterministic turn fuel. A `--rounds` cap is useful for smoke batches but prevents final-statistics conclusions.

The older `tools/score.py` runs one completed match and checks assertions such as:

```powershell
python tools/score.py foundry starter-cpp --map expanse --assert "botFaults==0" "submittedGems>=100"
```

At the time of review, both `tools/score.py` and the newer local-evaluation script expect `cambc.exe` in the repository root, while this checkout exposes `cambc` globally and has no root executable. They will fail until that expected executable is supplied or the scripts are deliberately changed to resolve the CLI from `PATH`. Do not report an unrun command as a passed gate.

## 7. Two-sided local replay reports

Current GitHub `main` contains `tools/replay/local_eval.sh`. It builds both bots, runs every requested map in both team positions, extracts the resulting replays, and prints the same behaviour metrics used for platform scouting:

```bash
tools/replay/local_eval.sh foundry foundry-v1
```

With no map arguments, this produces the full 18-match comparison. To debug a smaller map subset first:

```bash
tools/replay/local_eval.sh foundry foundry-v1 expanse lanes
```

On Windows, run the script through Git Bash or WSL; it is Bash, not PowerShell. It also requires:

- the newer `tools/replay/` files from GitHub `main`;
- `./cambc.exe` at the repository root under the script's current implementation;
- Node.js for `extract.mjs`;
- Python 3 for `report.py`.

Those replay tools are not present in this old local branch unless the team deliberately integrates them. This guide update does not pull, switch, or copy them.

## 8. Download and analyse public platform replays

The newer tool can find a public team ID, download finished match-group metadata and replay bundles, extract trajectories, validate decoded totals, and produce a storyboard. From a checkout that actually contains `tools/replay/`:

```bash
python3 tools/replay/platform.py find "Heavenly Court"
python3 tools/replay/platform.py team <team-id> <scratch-dir>
node tools/replay/extract.mjs <scratch-dir>/replays <scratch-dir>/trajectories
python3 tools/replay/report.py <scratch-dir>/trajectories \
  --groups <scratch-dir>/groups --team <team-id> --check
python3 tools/replay/story.py <scratch-dir>/trajectories/<match-id>.json \
  --side 0 --upto 200 --step 10
```

On Windows, `python` may be the command instead of `python3`. For `story.py`, use `--side 0` when your team was team A in that game and `--side 1` when it was team B; the downloaded match-group JSON records the sides.

Keep `<scratch-dir>` outside tracked source. Do not commit downloaded opponent replays, decoded trajectories, group JSON, or ladder snapshots.

## 9. What the replay report measures

The current `report.py` metrics answer different questions:

| Area | Metrics | Interpretation |
|---|---|---|
| Economy and tempo | `firstCapture`, `gems<=r100`, `sg@100`, `sg@200`, `sg@300`, `firstTribute`, `tributes`, `tribBag` | How quickly camps become score and how large/frequent tribute trips are |
| Coordination | `campCoHit`, `cassiIssacDist`, `nearestAlly`, `allyWithin2` | Whether champions form useful local groups instead of behaving as isolated farmers |
| Positioning | `enemyHalf` | How much alive time is spent closer to the enemy spawn than the team's own spawn |
| Survival | `recalls`, `recallHpPct`, `deaths<=r150`, `deaths`, `deathsBelowFloor`, `deathsToChampions`, `gemsLostOnDeath` | Retreat timing, downtime, combat exposure, and economic loss |
| Combat | `champDmg`, `killsEnemyHalf`, `killsOwnHalf` | Damage pressure and where kills occur |
| Activity | `idle` | A proxy for alive rounds without a move, attack, cast, channel, or shop action |

Several are deliberately heuristic:

- A recall is inferred from an alive champion teleporting more than three tiles onto its own spawn.
- `deathsBelowFloor` compares the last alive health to the executor's 40% retreat floor.
- `deathsToChampions` means enemy-champion damage appeared during the preceding few rounds; it is not an exact killing-blow label.
- Own/enemy half is based on which team's average starting spawn is nearer.

Use these metrics to locate suspicious games, then inspect the replay. Do not turn one proxy into a causal claim without watching the relevant sequence.

## 10. A fair A/B testing matrix

For a serious change:

```text
candidate versus a frozen previous bot
    × all nine published maps
    × candidate as team A and as team B
    = 18 matches per opponent
```

The engine and repository bots are designed to be deterministic for the same inputs. Repeating an identical bot/map/side match is therefore a **reproducibility check**, not a new independent statistical sample. Useful variation comes from maps, team positions, immutable bot versions, and opponents with different strategies.

Maintain a small opponent league:

1. `starter-cpp` as a correctness floor;
2. the previous submitted FOUNDRY as the main regression baseline;
3. current stable FOUNDRY;
4. a greedy farmer;
5. a capture-denial or respawn-blocking bot;
6. a large-bag carrier hunter;
7. an altar-lock bot;
8. a conservative small-bag banker.

Track aggregate wins, but also split by map and team side and inspect the worst losses. A strategy that wins ten of eighteen while catastrophically failing one map or one simple counter still has a real defect.

## 11. Acceptance sequence and submission

Use this order for every candidate:

1. Build the candidate without faults.
2. Run a short local smoke test.
3. Run at least one completed match with final statistics.
4. Run the 18-game, all-map, both-side comparison against the frozen previous bot.
5. Run the same candidate against the adversarial opponent league.
6. Upload it and use an unranked platform challenge to verify server compilation, the submitted version, and official replay behaviour without risking Elo.
7. Inspect the unranked five-game group's map results, official statistics, logs, and worst replay.
8. Submit/use it for ranked play only after those gates pass.

The platform's current unranked groups expose replay URLs and full official end statistics while leaving rating fields null. Ranked groups record rating changes. This makes unranked the right server-side dress rehearsal, not a substitute for the broader 18-game local matrix.

After the evidence is satisfactory:

```powershell
cambc login
cambc submit foundry
```

Or create a browser-uploadable archive:

```powershell
cambc bundle foundry -o submissions
```

Never submit generated builds, replays, scratch files, secrets, or a bot that only passed a shortened match. Record the source commit, bot label/version, build time, and bundle hash for every upload so platform results remain attributable.

---

# Part X — Known ambiguities and targeted engine probes

The current documentation contains a few contradictions. Do not silently pick whichever number helps a strategy.

## 1. Monolith attack range

- Camp table: Monolith range five.
- General camp-detail sentence: all monsters range three.
- Restored header metadata/comments have also disagreed with the table in inspected versions.

Resolution: query `camp.attack_range()`/design metadata at runtime and create a small controlled match that places a champion at distances three, four, and five. Record engine version and replay.

## 2. Camp sleep trigger

- Intro wording: a camp sleeps after not taking damage for two turns.
- Detail wording/header constant: a camp sleeps after two rounds without an in-range champion.

Resolution: probe four cases—near with no damage, far with no damage, intermittent range, and damage from range—and observe when aggression ends.

## 3. Teleport and walls

- A terrain table says a teleport crystal can “reach walls.”
- Exact movement rules forbid landing on walls.

Safe interpretation: crystals ignore/cross intervening walls but require a legal non-wall landing. Let SDK masks/engine validate; never intentionally target a wall in production.

## 4. Tribute into a hostile lock

- Rules say it converts to an attack on the lock.
- The API exposes an altar-locked invalid-action error in some generated material.

Safe implementation: inspect the lock's team and explicitly attack a hostile lock when legal.

## 5. Homepage versus handbook language/fuel list

The event homepage still showed C/C++/Rust/Python and Python at 20× compute. The current handbook/workspace supports C++, Rust, Python, and OCaml and specifies Python 25×, OCaml 5× relative to the 100,000 C++/Rust budget.

Resolution: use the live handbook, generated workspace, and engine—not the short marketing FAQ—for precise implementation rules.

Keep a `probe` bot or focused test functions for questions like these. A replay demonstrating behavior is stronger evidence than a guess.

---

# Part XI — Exercises that teach C++ and the game together

## Exercise 1: deterministic draft

Replace random choice with a preferred legal list. This draft-phase array expresses a stable pick priority so repeated matches do not receive an accidental random composition. It is only the preference table; the exercise still needs legality checks against both teams' existing picks before calling the SDK's draft action:

```cpp
// Class template argument deduction infers the champion enum type and the
// number of entries from the brace-initialized values.
const std::array preferred{
    // Earlier entries have higher priority when they remain legal to draft.
    cambc::champion_draft::vendetta,
    cambc::champion_draft::cassi_and_issac,
    cambc::champion_draft::varg,
    cambc::champion_draft::tavi,
    cambc::champion_draft::vesper_vale
};
```

Loop through it and pick the first entry not already in your team's `current_draft`. Learn `std::array`, enums, `std::find`, and deterministic fallback.

Success: repeated drafts on the same team size choose the intended legal order and never rely on random missing picks.

## Exercise 2: dead shopping

Move shopping ahead of the dead early return. Learn ordering, `can_buy`, and why dead champions still act.

Success: replay/log shows purchases during the 60-turn death timer without faults.

## Exercise 3: one ability per kit

For each drafted champion, identify slot types and cast only after checking `can_cast`, `is_ready`, target category, visibility, and geometric range.

Success: abilities appear in replay, no invalid-target errors, and melee remaining actions are not always discarded.

## Exercise 4: hostile lock awareness

Allow tribute through allied locks, route away from or break hostile locks, and handle all-altars-blocked state.

Success: no permanent wandering and no allied-lock false positives.

## Exercise 5: camp FSM

Store a target group and `Goal` enum. Implement travel, clear, capture, and leave.

Success: one champion stays through the full uncontested capture and vacates before blocking respawn.

## Exercise 6: hidden blocker retry

When movement returns `false`, update the blocked mask and choose another step.

Success: a bush-obstruction test uses the still-available movement allowance without throwing.

## Exercise 7: risk-aware banking

Start with a simple threshold, then condition it on health, distance, enemy visibility, team score, and remaining rounds.

Success: fewer low-value cross-map trips without a large increase in gem deaths.

## Exercise 8: non-duplicating assignment

Assign different opening groups in draft memory. Add deterministic relief when one champion dies.

Success: all selected champions agree on assignments without consuming the live eight-byte word for static facts.

## Exercise 9: fuel measurement

Log `fuel_remaining()` around navigation and targeting only in controlled development builds.

Success: identify real hot paths, remove the logs afterward, and keep a safe margin without premature rewrites.

---

# Part XII — Glossary

| Term | Meaning here |
|---|---|
| API | The functions/types the SDK exposes to the bot. |
| Bot instance | One running copy of your program for one champion/body. |
| Camp group | Cardinally connected original monster spawns sharing capture/reward/respawn behavior. |
| Capture phase | Round-start engine phase that starts/decrements/resolves camp capture. |
| Channel | Multi-turn action: recall, tribute, or teleport. |
| Chebyshev distance | `max(abs(dx), abs(dy))`; diagonals count as one. |
| Cooldown | Owner-turn-end ticks before an ability/item becomes usable again. |
| Draft memory | 1,024-byte plan written in draft and read-only during play. |
| Fuel | Deterministic computation budget per bot turn. |
| Handle/view | C++ object referring to an engine entity; live queries may require visibility. |
| Macro | Long-horizon assignments, routes, economy, and win plan. |
| Micro | Exact movement/attack/spell choices in a local situation. |
| Root | A goal tile with distance zero in a distance field. |
| Shared memory | Eight mutable bytes shared among allied bot instances. |
| Snapshot | Data captured at a moment; it does not automatically update. |
| Spawn region | Allied shop/heal area; enemy spawn is illegal movement territory. |
| Tick | One decrement at the owning champion's turn end unless specified otherwise. |
| Tribute | Channel converting carried gems into permanent team score. |
| Vision mask | Bitboard of tiles currently visible to this champion and its ward. |

---

# Part XIII — Sources and further reading

## Primary CAMBC sources

- [Official CAMBC 2026A handbook](https://2026a.battlecode.co.uk/game/docs)
- [Official C++ API reference](https://2026a.battlecode.co.uk/game/api)
- [First bot / workspace guide](https://2026a.battlecode.co.uk/game/docs/first-bot)
- [Official patch notes](https://2026a.battlecode.co.uk/game/patch-notes) — check this before relying on any balance-sensitive number
- [CLI download page](https://2026a.battlecode.co.uk/game/download)
- [Official public match API example: an unranked five-game group](https://2026a.battlecode.co.uk/api/v1/match-groups/86c93b67-a25c-49d5-b110-b80003e4c75a)
- [Repository at the inspected `e341ad05` snapshot](https://github.com/FHL-08/Tarot-Club-Cambc2026/tree/e341ad050288b87a07c2384bbdf0bea283732698)
- [Merged PR #43: recall and death-cause replay metrics](https://github.com/FHL-08/Tarot-Club-Cambc2026/pull/43)
- Local rule export: [`docs/GameRules.md`](../docs/GameRules.md)
- Local C++ API export: [`docs/BotAPICpp.md`](../docs/BotAPICpp.md)
- Restored SDK header: [`sdk/cpp/cambc.h`](../sdk/cpp/cambc.h)
- Team's FOUNDRY architecture and strategy contract: [`docs/strategy.md`](../docs/strategy.md)
- Current implementation/performance review: [`owndocs/Analysis1.md`](Analysis1.md)

The live documentation is a JavaScript application. On 13 October 2026, its bundle and the local exports agreed on the core rule text, and both live/local C++ references contained 537 documented method entries. On this refresh, the local rule/API/SDK files were byte-identical at the Git blob level to the files on current GitHub `main`; consult the live patch notes for changes published after the exported files.

## Transferable strategy sources

These are inspiration, not CAMBC rules:

- [MIT Battlecode overview](https://battlecode.org/about.html) — programming-game themes: pathfinding, resource management, communication, combat, and compute limits.
- [MIT Battlecode postmortem archive](https://battlecode.org/past.html) — primary competitor reports across years.
- [The Kragle 2025 postmortem](https://battlecode.org/assets/files/postmortem-2025-the-kragle.pdf) — goal systems, macro/micro, economy, pathfinding, testing.
- [SPAARK 2025 postmortem](https://battlecode.org/assets/files/postmortem-2025-spaark.pdf) — candidate scoring and action-order micro.
- [No Thoughts 2023 postmortem](https://battlecode.org/assets/files/postmortem-2023-no-thoughts.pdf) — hybrid local pathfinding and A/B-test tooling.
- [Official Halite III repository](https://github.com/HaliteChallenge/Halite-III) and [TheDuck314's sixth-place C++ bot](https://github.com/TheDuck314/halite2018) — resource collection, return modes, collision priority, whole-cycle evaluation.
- [Screeps API](https://docs.screeps.com/api/) — path reuse and cost-based navigation under CPU constraints.
- Gerkey and Matarić, [A Formal Analysis and Taxonomy of Task Allocation in Multi-Robot Systems](https://robotics.stanford.edu/~gerkey/research/final_papers/mrta-taxonomy.pdf) — framing champion-to-task allocation as an assignment problem.
- David Silver, [Cooperative Pathfinding](https://ojs.aaai.org/index.php/AIIDE/article/view/18726) — reservations and windowed cooperative search; likely later-stage inspiration rather than a first CAMBC implementation.
- Hart, Nilsson, and Raphael, [A Formal Basis for the Heuristic Determination of Minimum Cost Paths](https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf) — original A* paper.

Previous Cambridge Battlecode years used different games. Reuse engineering lessons such as explicit roles, state machines, robust navigation, and replay-driven iteration, but never import old cores/ores/builders/conveyors rules into 2026A.

---

# Final checklist for every champion turn

Before yielding, mentally ask:

```text
What can this champion actually see?
Is it dead, channeling, stunned, or on its recall-arrival spawn turn?
Can it shop before returning?
What macro job is stored?
Is there an urgent economic interrupt?
Which moves/attacks/casts remain legal after each chosen action?
Could a hidden occupant return false and permit a retry?
Will this action protect, earn, steal, or submit gems?
Did persistent state and shared bytes remain internally consistent?
Is enough fuel left to finish safely and yield?
```

If the bot answers those questions reliably, it has moved beyond a starter script into a system you can improve scientifically.
