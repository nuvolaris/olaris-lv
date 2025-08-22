#!/bin/bash
source /usr/local/share/nvm/nvm.sh
nvm use 20
curl -sL bit.ly/get-ops | bash
code --install-extension ms-vscode.test-adapter-converter
code --install-extension hbenl.vscode-test-explorer
code --install-extension pgant.antonio-ops-vscode-extension@1.3.2
echo "export OPS_BRANCH=main" >> ~/.bashrc
source ~/.bashrc
ops -plugin https://github.com/nuvolaris/olaris-lv
echo 'export PATH="$HOME/.ops/olaris-lv/.venv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
ops lv setup "$C"
ops lv new "${C:-index}" lovable
if test -z "$C"
then echo "Installed as index.html"
     echo "Use 'ops lv setup <comp>' to set up as <comp>.html"
     echo "Reload the configuration by source ~/.bashrc or restart your terminal."
else 
fi
