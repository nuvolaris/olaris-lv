#!/bin/bash
cd "$(dirname "$0")"/..
rm -Rvf web packages /tmp/log
git reset --hard
#cp index.html.fixed index.html
ops lv setup chess
ops ide deploy
#npm run build
#cd web
#python -m http.server

