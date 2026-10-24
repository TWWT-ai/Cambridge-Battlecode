#include <cambc.h>
#include "draft.h"
#include <algorithm>
#include <array>

void play_draft() {
    using cambc::champion_draft;
    constexpr std::array lineup{
        champion_draft::ryth,
        champion_draft::vendetta,
        champion_draft::tavi,
        champion_draft::willow,
        champion_draft::prism,
    };
    const auto size = std::min<std::size_t>(cambc::draft::team_size(), lineup.size());
    const auto chosen = cambc::draft::current_draft(cambc::team::ally);
    for (std::size_t i = 0; i < size; ++i)
        if (std::find(chosen.begin(), chosen.end(), lineup[i]) == chosen.end()) {
            cambc::draft::pick(lineup[i]);
            return;
        }
}
