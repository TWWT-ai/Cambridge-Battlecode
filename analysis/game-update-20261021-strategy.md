# CAMBC rule/API update: strategy and equipment review

**Reviewed:** 21 October 2026  
**Scope:** uploaded `GameRules.md` and `BotAPICpp (1).md`, current bot source, prior map studies, and match records available in this workspace. This is a strategy review, not a current-version bot result.

## Executive assessment

The new handbook changes enough combat, camp, and champion values that local experiment results from 14–19 October cannot validate builds for the updated game. The strongest confirmed direction still holds at the strategic level: win by converting camp rewards into **tributed gems**, while keeping the gem carrier alive. The next code experiment should wait until the local compiler, SDK, runner, and map exports match the 21 October documents.

The useful update in the API export is more precise live state: visible camp groups distinguish alive, reward-ready, and respawning states; respawn timers are queryable; and visible awake/asleep camp masks are available. Item metadata also exposes combination count, stat bonuses, passive, and resulting item. These should support data-driven routing and buying after the SDK is refreshed.

## Version and evidence boundary

The uploaded `GameRules.md` and `BotAPICpp (1).md` were updated on 21 October. `BotAPICpp.md`, the local `cambc.exe`, the historical mechanics model, and ranked/local result records predate that update. The local SDK header confirms the mismatch: it lacks `golem`, `heart_of_ruin`, and the new awake/asleep camp queries, and its documented passive constants differ from the current handbook.

| Current handbook/API | Older workspace reference | Consequence |
|---|---|---|
| Adds Golem camps and Heart of Ruin | Local `cambc.h` has neither enum value | Old compiler cannot exercise the full updated roster or camp types. |
| Prism gains 1.5 Focus per carried gem | Local header says 0.2 Focus per gem | Prism carry/burst math must be recalculated. Do not use old Prism tests as current evidence. |
| Vesper Vale gains 33% gold; Treasure adds 20 percentage points | Local header says 20% for Vesper | Do not hard-code the old passive or use old gold forecasts. |
| Monolith has range 5 | Local header describes range 3 | Old safe-range/kiting estimates are invalid. |
| Altar locks take five basic attacks to remove | `analysis/mechanics.md` and a bot comment say three | Update logic/comments only after the matching runtime is available. |
| Current camp rewards, respawn timers, champion bases, and growths are listed in `GameRules.md` | `analysis/mechanics.md` uses earlier values (for example 50 gold per kill and old champion stats) | Rebuild farm-rate and item-value calculations from the new table. |

The API export is also newer than the local header: it documents `camp_type::golem`, `champion_draft::heart_of_ruin`, `vision::awake_camp_tiles()` and `asleep_camp_tiles()`, plus the camp-state alternatives. The old export already had `camp_group.state()`; the new export makes the variant and timer semantics explicit. This is an API/toolchain gap, not evidence that the bot can call those functions today.

For that reason, the 17-map route/supply tables are retained as **old map geometry and hypotheses only**. Their gem yields, clear times, and bank schedules were derived under the earlier camp definitions. Refresh the public map pool and regenerate group values before using exact numbers. The 19 October top-team matches are also historical evidence, not tests under the 21 October rules.

## What the updated API makes possible

- `camp_group.state()` returns alive, reward-available, or respawning; a respawning state includes the remaining timer, with zero indicating that occupied spawn tiles are blocking the respawn. Query it only when an original spawn tile is in the champion's vision; otherwise the API reports a visibility error.
- `vision::awake_camp_tiles()` and `asleep_camp_tiles()` distinguish visible camps that are currently active from those that have gone to sleep. Use this with camp range and distance to avoid taking unnecessary hits or chasing camps that do not move.
- `camp_group.gem_value()`, `gold_value()`, `spawn_tiles()`, `max_respawn_timer()`, and `state()` can replace some guessed reward/respawn ledgers when the group is visible. Cache repeated map queries within a turn to protect the 100k fuel budget.
- `item_type.info()` exposes cost, `combine_count`, stat points, passive, passive magnitude, and combination result. Prefer these values to duplicated constants once the current SDK supports them.
- `champion.gem_count()` requires the champion to be in vision. Opponent bags are therefore visible only when the opponent is visible; the API does not grant a global view of carried gems.

## Strategy for future matches

### 1. Optimize score conversion, not damage totals

Use expected **tributed gems per round** as the main objective. A camp group only pays after every monster is defeated and a champion occupies one of its spawn tiles through the five-round capture. More allies do not accelerate that timer, and allies present on the region split the reward. A respawning group can also remain blocked while a champion occupies a spawn tile.

Route selection should estimate:

`group gem reward ÷ (travel + clear + capture + altar trip/tribute + expected contest loss)`

Use gold and kill rewards as secondary inputs: they matter when they buy a timing breakpoint or decide the 2,000-round tiebreak. Do not count a cleared camp as income until its reward is captured, and do not count carried gems as score until tribute completes.

Tribute is a channel whose duration is based on the starting bag (`ceil(gems / 10)`, minimum one); it completes at the carrier's next turn start after the timer reaches zero, and it deposits the whole bag, including gems acquired while channeling. Damage alone does not stop tribute, but stun, death, or a new altar lock does. Use a lock to cancel an enemy channel or force five basic attacks; keep an interrupt or lock-breaker near the altar when the enemy can contest.

When an enemy is visible, its bag count can inform target priority. When it is hidden, assume the count is unknown. A kill transfers the victim's carried gems and grants 100 base gold; a camp kill destroys the victim's carried gems. This makes a protected carrier and selective interception stronger than pursuing kills without a score-conversion plan.

### 2. Match the route to the map's resource shape

The map study's 17-map snapshot is from 17 October, before these rules. Use its shapes only as a starting classification, then recompute exact camps and rewards from refreshed maps.

| Map shape in the saved study | Starting plan to retest under current rules |
|---|---|
| Many separated home-side camps (examples: Lanes, Corners, Expanse, Rows) | Split into independent routes after the first safe group. Prioritize short travel and overlapping a capture with ranged attacks on the next group. Select bank thresholds from actual altar distance and visible threat. |
| Sparse or slow home supply (examples: Fragment, Elkring) | Avoid long unsupported routes for low-value groups. Use smaller, safer deposits when a death would erase a large fraction of the team's score. |
| Central/contested supply (examples: Stampede, Swirl, Pilgrimage) | Keep the carrier and a responder within reinforcement distance; send only a safe farmer alone. Secure the capture before splitting further. Do not reproduce old gem-total estimates. |
| Monolith-focused objectives (Contest/Monolith in the saved map dump) | Treat the Monolith's current 20,000 health, 200 strength, and range 5 as a team objective. Estimate the full clear and return time before committing; keep the gem carrier away from its attack range and plan a bank route before the first hit. |

Draft remains map-dependent. The draft sees the whole map and can inspect camp groups; team size is 3–5 picks, and Cassi & Issac consume one pick but produce two linked bodies. The actual `draft.cpp` is already map- and opponent-aware; the simpler fixed-lineup description in the old `CLAUDE.md` was stale. The 19 October top-five snapshot showed Stellar and Cassi & Issac in all 25 recent Fish and Mite drafts, with Ren common but variable. Treat that as a strong-core hypothesis, not a universal fixed draft.

Heart of Ruin is a new candidate for contested fights: low health raises damage up to 50%, and its dash landing damages/stuns around the destination; its shield does not count as health for the passive. This may reward a shielded flank, but deliberately keeping a gem carrier at low health is unsafe. Test it first as a non-carrier diver. Re-evaluate linked Cassi/Issac risk too: either body dying kills both and drops both bags.

### 3. Equipment hypotheses by job

The new handbook says shards cost 30 gold. Five matching shards combine into an emblem; Power gives the stat equivalent of a sixth shard and has no passive. Do not interpret the Power row as six purchases. Other emblem passives do not stack, while their stats do. Use `combine_count()` when the current SDK is available.

| Job/champion | First build hypothesis | Why, and what must be measured |
|---|---|---|
| Ryth frontline | Health first when the extra survival prevents a death or holds a camp line; compare Durability Health in fight-heavy maps | Each 100 bonus health also adds 1 Strength through Ryth's passive. New Health shards add 100 health for Ryth, so they also add about 1 Strength. Compare the passive with the 10% Durability reduction and 30% Jungle camp reduction using current incoming damage. |
| Stellar and other spell casters | Power Focus is the clean damage baseline; test Monster Focus only on routes where camp damage is the bottleneck | Current spell multipliers make Focus useful in both camps and fights. Old Monster-first experiments were mixed and cannot be carried over to changed bases/camps. |
| Varg / camp farmer | Compare Power Strength to Monster Strength on multi-camp routes | Varg's basic attacks splash around the target; Monster adds 10% camp damage, while Power supplies one additional shard's stats. Recompute turns saved per purchase with new cluster health and group sizes. |
| Tavi marksman | Keep the remote-buy advantage; compare Strength for repeated attacks with Focus for the 1.4× Focus stun | Tavi can buy shards in the field but cannot buy consumables there; field Health purchases raise max health without healing. Do not return to spawn solely for an ordinary shard if route tempo is worth more. |
| Willow support | Focus for larger heals; consider one defensive line only if it prevents deaths | Her heal is up to 3×Focus at range 4. Healing is valuable when it preserves a carrier or objective push, not as a reason to slow every farming route. |
| Prism carrier/caster | Treat carried-gem Focus as a situational burst bonus, not a reason to delay banking | The current 1.5 Focus per gem is much higher than the old local constant. More gems increase spell damage but increase the loss if Prism dies; test small and large bag thresholds. |
| Vesper / gold role | Test Treasure only on a map with a profitable gold route or a long game | The current 33% passive plus Treasure's 20 percentage points is 53%, but gold is secondary to gems unless it accelerates purchases or wins the 2,000-round tiebreak. |
| Heart of Ruin / fighter | Test as a flank diver with shield and dash; avoid assigning it the main bag | Missing-health damage may improve a fight but increases death risk. Compare damage converted to kills/objectives against lost bag value. |

Recommended buy rule: complete an emblem only when its passive or stat breakpoint changes the next clear, fight, or survival outcome. A defensive emblem should be justified by avoided deaths or extra carried gems banked, not by damage reduction in isolation. Treasure, Home, Bruiser, Monster, Jungle, and Durability are situational; there is no evidence for one universal item queue under the new numbers.

### 4. Use recent match evidence carefully

The 19 October replay review found a repeatable **old-version** lesson: on Collision, Mite collected slightly more gems than Sneaky Bush Campers but banked 208 fewer after nine deaths versus two. In a separate Stampede replay, Fish's Stellar submitted all 1,080 gems with four kills and no deaths. These support measuring deposited gems, carrier deaths, and recovery—not clear count or damage alone. They do not validate the exact old gem values, builds, or routes under the 21 October rules.

## Next experiments after toolchain refresh

1. Refresh `cambc.exe`, the C++ SDK, and map exports; verify that Golem, Heart of Ruin, current passive values, and awake/asleep camp APIs match the uploaded docs.
2. Query current champion/item metadata at runtime, then rebuild the stat, camp-damage, and farm-route calculator from the 21 October values.
3. Establish a new no-enemy economy baseline and compare one change at a time: route split, camp-damage threshold, bank threshold, and carrier protection.
4. Screen both sides on every refreshed map, then use strong local opponents. Keep local proxy results separate from official unranked outcomes.
5. Update the production bot only after the refreshed runner can represent the new rules and the candidate wins a controlled comparison.

## Small workflow dry run

Applying the installed state → opponent → plan → replay workflow to the old Collision replay: the state summary flags that Mite collected more but banked less; the replay reviewer attributes the gap to nine deaths versus two, with explicit warning that the match predates the new rules; the opponent model treats the result as a conversion/survival signal rather than proof of a specific item build; the planner recommends retesting a protected carry and shorter recovery route. This is a workflow check against recorded evidence, not a new match or bot validation.

## Limitations

The official game docs URL could not be opened by the browser tool in this session, so this review uses the uploaded local exports as the current source. No game simulation, live match, bot upload, or production source edit was performed. Claude Code project-skill files are installed on disk; the current Codex session cannot verify Claude Code's slash-command runtime discovery, so restart/open Claude Code in this repository to load the project skills.
