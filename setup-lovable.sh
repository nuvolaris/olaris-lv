#!/bin/bash
curl -sL bit.ly/get-ops | bash
code --install-extension ms-vscode.test-adapter-converter
code --install-extension hbenl.vscode-test-explorer
code --install-extension pgant.antonio-ops-vscode-extension@1.3.2
echo "export OPS_BRANCH=main" >> ~/.bashrc
source ~/.bashrc
source /usr/local/share/nvm/nvm.sh
use nvm 20
ops -plugin https://github.com/nuvolaris/olaris-lv
ops lv setup "$C"
ops lv new "$C" lovable
if test -z "$C"
then echo "Installed as index.html"
     echo "Use 'ops lv setup <comp>' to set up as <comp>.html"
fi
