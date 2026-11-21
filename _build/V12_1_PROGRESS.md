# v12.1 progress (branch v12.1-wip)
Goal: full verbatim web reading edition of 刘道顺《新旧约圣经全景》 (user says authorized). Source PDF via PyMuPDF (stream-order chars + positions for paragraphs); reference = pdftotext -raw.
- [x] R1 extractor _build/liu_extract.py -> _build/data/liu/book.json; verify vs pdftotext raw
- [x] R2 reader pages liu.html + liu-*.html (p_reader.py), 重点导读, marks, icons
- [x] R3 build assert (verbatim per chapter), cross-links (66 cards, panorama, nav)
- [x] R4 CSS typography, themes (reviewed night/paper/sepia/contrast 390+1440 ok)
- [ ] R5 checks (check.py 6 widths, check_ix, check_overlap chromium 7 + webkit 390), perf
- [ ] R6 deploy (tag v12.1-20261121, surge, netlify), README, shots
  R1 note: 1175 paras; norm(paras)==pdftotext -raw norm (200000 chars) except 1 stray glyph U+06E8 p.224 (ARTIFACTS)
  R2/R3 verified (resume): build OK, 77 liu pages, verbatim coverage 100% 76 ch, 0 mismatches; 66 cards+panorama link; 经授权转载 present
## R5 log
- build OK (00:25): quotes 184, mermaid 12, links 18089/0 broken, Liu verbatim 76 ch / 1162 segs / 200000=200000 chars / 100% / 0 mismatches; 103 html pages
- README drafted for v12.1 (R6 links prefilled; R5 results line to fill)
- check.py 320/390/768: 103 pages each, 0 problems (logs /workspace/wb/logs/v121/check_W.jsonl[.done]; runner run_check.sh skips done widths)
- check.py 1024/1440/1920: 103 pages each, 0 problems (all 6 widths done)
- check_ix 390: 1478 checks 0; check_ix 1440: 1581 checks 0 BAD/ERR (logs v121/ix_390.log); runner run_r5b.sh (ix 1440 → overlap chromium 320,390,600,768,1024,1440,1920 → webkit 390), .done markers
## R6 log
- 02:05 early deploy of 519331b: surge whole-bible-study-20261121-v12-1-grokstudy.surge.sh OK; netlify site created id 8a251d7c-5da0-4be2-8631-2ed833bc1751, deploy --prod OK (stage dir /workspace/wb/stage121 = git ls-files minus _build, no CNAME). overlap runner still going (chromium 768). Tag/release held until overlap done.
- 02:12 merged main 1b33ea5 pushed (Pages); verify: 103/103 html 200 on Pages, surge, netlify (script /workspace/wb/verify121.sh)
- R5 overlap partial: liu.html 768 ltoc multicol overlap -> grid groups (.ltocg); legendbox clip-x 670>665 at 1024 on 24 pages -> .lgi .it wraps <=1100px. Rebuilt OK. Need recheck 768+1024 after runner.
- R5 overlap chromium 7w done: overlap 4 (liu 768) + clip-x 24 (1024) -> fixed; webkit 390: page-hscroll 57 liu pages (WebKit hanging-punctuation) -> fixed; recheck running (logs ov_wk_recheck.log, ov_ch_recheck.log, recheck.done)
- rechecks: webkit 390 (57 pages) 0; chromium 768/1024 (25 pages) 0; check.py spot 390/1024 0
- perf9 m390x4: liu-ot29 p95 16.8 jank 0 lt 0; liu.html p95 16.8 jank 0 (load lt 105ms)
- shots /workspace/wb/shots/v12_1/{liu,liu-ot02}_{webkit_390,chromium_1440}_*.png
- [x] R5 done. Next: merge main, redeploy surge+netlify, tag+release, verify
