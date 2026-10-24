# tripytropa

Fixed-roster candidate. The 23 October strategy edits are not yet built or tested.

## Draft and roles

- 3 picks: Ryth (Tank), Vendetta (Fighter), Tavi (Marksman). Ryth leads.
- 4 picks: add Willow (Support).
- 5 picks: add Prism (Mage), who initiates before the frontline.
- Ryth prioritizes Health, Vendetta monster damage, Tavi Focus, and Willow/Prism Focus with a defensive Health emblem in their queues.

## Strategy

- Draft order stays fixed by team size: 3 picks are Ryth, Vendetta, Tavi; 4 adds Willow; 5 adds Prism. Ryth acts first with 3 or 4 picks. Prism initiates first with all 5.
- Ryth leads the primary route and takes the frontline. Vendetta farms a separate route, favoring wolves, and flanks the highest damage threat when a fight must be taken. Tavi and Willow stay behind Ryth; Prism holds a 2–4 tile spell range.
- Camp choices use map-provided rewards and stats. The estimate includes travel, clear time, the five-round capture, return to an altar, and tribute time. The bot finishes visible awake camps before waking another group and tracks visible respawn state.
- The team's score goal is tributed gems. A carrier routes to an altar before optional combat or another camp, retreats earlier with a large bag, and avoids visible enemies when a safe altar route exists. Altar locks are priced at five attacks to clear.
- In fights, target priority starts with enemy damage stats, then carried gems, then low health. Ryth uses his area stun where it catches the most enemies and resets after a basic attack. Prism uses slot 1 on enemies below 30%; otherwise slot 0 opens, followed by slot 1 when slot 0 is cooling down.
- Willow heals an ally under 30%. If at least two allies are critical, her attack reset is deferred to a later turn because the engine permits only one successful ability cast per turn.
- Ryth's Health shards also add Strength through his passive. Vendetta starts with Monster Strength for camp damage. Tavi buys Focus for her stun. Willow and Prism alternate Focus emblems with a defensive Health emblem. Focus is spell power; the updated rules do not define a mana resource or mana item.
- Existing map profiles remain for maps in the local pool; other layouts use the general reward and route scoring rather than an assumed camp reward table.

## Validation

- Built with the installed local CAMBC toolchain on 22 October 2026.
- Full local sweep: 771 runnable opponents, 10 games each across five maps and both sides; 7,710 games total.
- Result: **1,739/7,710 wins (22.55%)**. **22/771 opponents** reached at least 8/10; the requested all-opponent target is not met.
- Map results: Monolith 90/1,542; Contest 859/1,542; Expanse 350/1,542; Fragment 67/1,542; Lanes 373/1,542.
- Saved baseline: 1,676/7,710 wins (21.74%), with 17/771 opponents at 8/10 or better. The two full runs were not seed-paired, so the aggregate difference is encouraging but not a controlled causal estimate.
- Two opponent folders did not compile and one had no source; those were excluded.

The uploaded 21 October rules and API documents are newer than the installed local runner, C++ SDK, and map exports. The source update below uses mechanics exposed by the existing SDK plus current documented reward/scoring rules. New Golem/Heart of Ruin roster entries and awake/asleep query APIs still need a matching SDK/runtime before they can be exercised locally.

## Follow-up experiments (22 October 2026)

Fragment-only route, phase, banking, retreat, equipment, and draft-order variants were screened against local bots. None improved on the 22 October production build in head-to-head checks. The early back-line-to-Ryth routing variant scored 48/100 on a difficult five-map proxy set; the earlier production build repeated 54/100 on the same schedule. The 25-gem Fragment bank threshold lost all 10 direct matches to that build. Other variants tied or fell below their controls. See the [stage report](../../analysis/tripytropa-stage-20261022.md) for results.

## Strategy revision (23 October 2026)

The current source adds altar-return and tribute time to camp ranking, gives large gem bags a higher retreat threshold, banks before optional combat, prioritizes enemy damage stats with bag/finish tie-breakers, follows Prism's low-health area-skill rule, and defers Willow's reset when a heal already used this turn's ability. These edits have not been compiled or match-tested. The 22 October sweep numbers above describe the earlier source only.

Candidate sources and their match outputs are archived in `matches/candidates/`. No full 7,710-game sweep was run for these rejected variants.
