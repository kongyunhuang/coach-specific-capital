# Derived data tables (not shipped)

Nothing from StatsBomb is redistributed in this repository. The analysis runs on the derived tables below,
which are built from licensed StatsBomb data, so they are **not shipped**. They are available from the
corresponding author on reasonable request for verification. The analysis code that builds and uses them will be
released with the full paper.

| File | One row per | Rows | Content |
|---|---|---|---|
| `panel.parquet` | team-match | 4,560 | match and team identifiers, season, the head coach on the day, and every StatsBomb team-statistics field for that match (184 columns); 33 of them are the style dimensions |
| `spells.parquet` | coach-club spell | 144 | club, coach, first and last match date, number of matches, seasons covered, spell identifier |
| `change_events_final.csv` | in-season coaching change | 54 | club, season, new coach and predecessor with their spell identifiers and match counts; the installation analysis keeps the 21 changes whose predecessor and successor spells are both long enough |
| `minutes_panel.csv` | player-team-match | 69,922 | minutes played, from the position clocks in the lineups |
| `team_match_index.csv` | team-match | 4,560 | coach identifiers per match, used to align the minutes panel with the spell table |

Four match-level outputs of the analysis carry match or team identifiers and are held back for the same reason
(`cost_incidence_profile_real.csv`, `cost_incidence_did_control_cache.csv`, `placebo_example_draw.csv`,
`reconcile_coach_defs.csv`). They are listed in `.gitignore`.
