# v12.2 progress
- [x] branch v12.2-wip from main (v12.1)
- ROOT CAUSE found: v12.1 reader CSS (app.css ~1320) added GLOBAL .lgh/.lgi (guide card icon: .lgi{width:48px;height:48px;flex:none;font-size:26px}) colliding with legend .legend-em .lgi -> legend item column forced to 48px(40px <600) => vertical char stacks + overflow over pills/tip.
- [x] before shots  - [x] fix: reader classes renamed lgd* (lgh,lgi,lgt,lgs,lgp,lgn,lgx,lgm; lgt/lgn ALSO collided with concept-map legend .cmleg) + robust legend CSS (v12.2 block end of app.css)  - [ ] checkers  - [ ] top nav  - [ ] deploy
- [x] top nav: lib.py (navHide chevron in HDR, navTab pull-tab, nvseg in tpanel, fab 'nav' btn, init script wb-nav), css v12.2 block (--topv), app.js IIFE at end (window.__nav)
