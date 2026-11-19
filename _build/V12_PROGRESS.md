# v12 progress (branch v12-wip)
Source: Liu PDF split per chapter -> /workspace/wb/src/liu/NN_<title>.txt (pdftotext non-layout, liu_raw.txt)
Perf baseline: /workspace/wb/perf/base12 (copy of main v11.2), log perf/v12_before.log
- [x] S0 perf baseline (forms,creeds,kc,index,ot m390x4)
- [x] S1 Liu notes: _build/liu_data.py (per-book dict) — batches
- [x] S2 Liu integration: per-book 全景要义 block (books.py), panorama page (p_liu.py), era/redemptive flow
- [x] S3 TOC levels (L1/L2/L3/all buttons, default L1 + current branch)
- [x] S4 FAB nav improvements
- [x] S5 marks: mini legend strip on all content pages (+harmony), Liu block auto-marks (term **k**, contrast uo/hg, → arrows, Christ ++ug++, q line ud), keychapter kch; section icon hue cycle
- [x] S6 visuals: eraflow, exile/return map, gospel split bars, golden rings, Acts 1:8 gospel-spread map (panorama #nt-acts)
- [x] S7 perf: progress ring on scroll-settle; after numbers perf/v12_after.log (all p95 16.7–16.8, 0 scroll long tasks)
- [ ] S8 checks (check.py, check_ix, check_overlap + webkit)
- [ ] S9 shots, README, tag/release, deploy

baseline (v11.2, m390x4, gesture/script p95): forms 16.7/16.7, creeds 16.7/16.7, kc 16.7/16.8, index 16.7/16.7 (loadLt ~420ms), ot 16.7/16.7; 0 long tasks during scroll

after (v12, m390x4 solo, gesture/script p95): forms 16.7/16.7, creeds 16.7/16.7, kc 16.7/16.8, index 16.7/16.7 (loadLt ~400ms, same as base), ot 16.7/16.8, panorama 16.7/16.7; 0 long tasks during scroll
