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
