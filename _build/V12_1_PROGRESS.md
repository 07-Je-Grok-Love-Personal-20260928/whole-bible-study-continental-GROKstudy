# v12.1 progress (branch v12.1-wip)
Goal: full verbatim web reading edition of 刘道顺《新旧约圣经全景》 (user says authorized). Source PDF via PyMuPDF (stream-order chars + positions for paragraphs); reference = pdftotext -raw.
- [ ] R1 extractor _build/liu_extract.py -> _build/data/liu/book.json; verify vs pdftotext raw
- [ ] R2 reader pages liu.html + liu-*.html (p_reader.py), 重点导读, marks, icons
- [ ] R3 build assert (verbatim per chapter), cross-links (66 cards, panorama, nav)
- [ ] R4 CSS typography, themes
- [ ] R5 checks (check.py 6 widths, check_ix, check_overlap chromium 7 + webkit 390), perf
- [ ] R6 deploy (tag v12.1-20261119, surge, netlify), README, shots
