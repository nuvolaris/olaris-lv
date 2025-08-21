#!/bin/bash
curl -sL bit.ly/get-ops | bash
echo "export OPS_BRANCH=main" >> ~/.bashrc
source ~/.bashrc
nvm use 20
ops -plugin https://github.com/nuvolaris/olaris-lv
ops lv setup "$C"
code --install-extension pgant.antonio-ops-vscode-extension@1.3.2
if test -z "$C"
then echo "Installed as index.html"
     echo "Use 'ops lv setup <comp>' to set up as <comp>.html"
fi