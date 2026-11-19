# v12 progress (branch v12-wip)
Source: Liu PDF split per chapter -> /workspace/wb/src/liu/NN_<title>.txt (pdftotext non-layout, liu_raw.txt)
Perf baseline: /workspace/wb/perf/base12 (copy of main v11.2), log perf/v12_before.log
- [ ] S0 perf baseline (forms,creeds,kc,index,ot m390x4)
- [ ] S1 Liu notes: _build/liu_data.py (per-book dict) — batches
- [ ] S2 Liu integration: per-book 全景要义 block (books.py), panorama page (p_liu.py), era/redemptive flow
- [ ] S3 TOC levels (L1/L2/L3/all buttons, default L1 + current branch)
- [ ] S4 FAB nav improvements
- [ ] S5 note-marking system + legend; palette
- [ ] S6 visuals/maps
- [ ] S7 perf fixes + after numbers
- [ ] S8 checks (check.py, check_ix, check_overlap + webkit)
- [ ] S9 shots, README, tag/release, deploy
