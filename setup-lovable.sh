#!/bin/bash
curl -sL bit.ly/get-ops | bash
source ~/.bashrc
ops -plugin https://github.com/nuvolaris/olaris-lv
ops lv setup "$C"
if test -z "$C"
then echo "Installed as index.html"
     echo "Use 'ops lv setup <comp>' to set up as <comp>.html"
fi