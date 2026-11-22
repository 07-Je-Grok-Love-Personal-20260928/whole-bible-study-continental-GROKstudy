# v12.2 progress
- [x] branch v12.2-wip from main (v12.1)
- ROOT CAUSE found: v12.1 reader CSS (app.css ~1320) added GLOBAL .lgh/.lgi (guide card icon: .lgi{width:48px;height:48px;flex:none;font-size:26px}) colliding with legend .legend-em .lgi -> legend item column forced to 48px(40px <600) => vertical char stacks + overflow over pills/tip.
- [x] before shots  - [x] fix: reader classes renamed lgd* (lgh,lgi,lgt,lgs,lgp,lgn,lgx,lgm; lgt/lgn ALSO collided with concept-map legend .cmleg) + robust legend CSS (v12.2 block end of app.css)  - [ ] checkers  - [ ] top nav  - [ ] deploy
- [x] top nav: lib.py (navHide chevron in HDR, navTab pull-tab, nvseg in tpanel, fab 'nav' btn, init script wb-nav), css v12.2 block (--topv), app.js IIFE at end (window.__nav)
- [x] check_layout.py written; full run #1 (old css) logs /tmp/cl/*.log — found: gospels/kings table cells narrow-stack (fix: .tw td/th min-width:3.4em), vertical writing-mode false positives (excluded), .lev content-visibility escape false positives (checker forces cv visible), flaky .fabt click liu-nt02 c1440
- [x] README v12.2 written
- [ ] run #2 full (/tmp/cl2) ; perf; deploy
- 15:10 run#2 first attempt (14:50) hung at 0 CPU after load spike (liu-nt07 goto timeouts) -> killed; checker now logs per-page progress to .err + 20s default timeout; rerun 4 procs x3 profiles, timeout 2700, logs /tmp/cl2
- 15:15 EARLY DEPLOY of eecf183-build: stage /workspace/wb/stage122; surge whole-bible-study-20261122-v12-2-grokstudy.surge.sh OK; netlify site id 84faa794-3da6-446d-8fbf-b52355e331d8 created + deploy --prod OK. Pending: run#2 results, merge main, tag/release, verify.
