# v11 progress (branch v11-wip)
Freeze point: tag v10-20261024 + release exist (verified 2026-11-14).
## Done
- [x] S0 freeze verified, branch v11-wip
## Remaining
- [x] S1 24 keyless sources (curl-verified; CARTO removed: API KEY placeholder), 5 kinds, source picker + status dot, fallback tested (Esri+EOX blocked → MODIS)
- [x] S2 6 new maps (nations, judges, elijah, prophets, roman, creeds) → 19 maps, geo_v11.py
- [x] S3 讲解动画 journey player for all 19 maps (journey.js, WAAPI transform marker, phone auto-scroll)
- [x] S4 culture: archaeology timeline (15) + worldview table; geo: arc + source table
- [x] S5 note marking v11 CSS (pen highlighter, under-rules, paragraph pins)
- [x] S6 two vivid themes: aurora 极光霓彩 (dark), spring 春日晴空 (light) → 12 themes
- [x] S7 overflow check all widths + interactive (check_ix DONE all 9 widths, 0 BAD/ERR: 320-414,768 386 checks; 1024-1920 411 checks) — static check.py clean at all 9 widths (chk11_all.log, 225 rows); check_ix running per width via /workspace/wb/perf/ix11/run.sh (logs ix11/w<W>.log; only BAD/ERR/PG lines). NOTE: run sequentially, parallel chromes are 20x slower on shared box
- [ ] S8 perf 4x — running /workspace/wb/perf/run11b.sh (results v11/<page>_<prof>.json, skips done ones; re-run to resume). First pass under box load 18 discarded (v11_loaded/)
- [ ] S9 deploy (merge, tag v11-20261114, release, README, Pages, Netlify, surge), shots
