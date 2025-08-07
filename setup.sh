#!/bin/bash
curl -sL bit.ly/get-ops | bash
source ~/.bashrc
ops -plugin https://github.com/nuvolaris/olaris-lv
ops lv setup "$C"
