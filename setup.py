import os, json, sys
from pathlib import Path
import shutil

os.chdir(os.getenv("OPS_PWD") or ".")
#print("pwd", os.getcwd())

#print(sys.argv)
if len(sys.argv) <2 or sys.argv[1] == "":
    dir = "packages/lovable/index"
    build = "vite build"
    name = "App"
    index = "index.html"
    c = "index"
else:
    c = sys.argv[1]
    dir = f"packages/lovable/{c}"
    index = f"{c}.html"
    build = f"vite build && mv web/index.html web/{index}"
    name = c.capitalize()

# fix package.json
try:
    pj = json.loads(Path("package.json").read_text(encoding="utf-8"))
    pj["openserverless"] = {
        "devel": "npm run dev",
        "deploy": "npm run build"
    }
    pj["scripts"]["build"] = build
    Path("package.json").write_text(json.dumps(pj, indent=2), encoding="utf-8")

    # fix vite.config.js
    file = Path("vite.config.js")
    if not file.exists():
        file = Path("vite.config.ts")
        
    vc = file.read_text()
    if(vc.find("OPSDEV_HOST") == -1):
        pos = vc.find("server: {\n") +10
        vc1 = vc[:pos] + """proxy: {
    "/api/my": {
        target: process.env.OPSDEV_HOST,
        changeOrigin: true
    }
    },
    """ + vc[pos:]
        m = "defineConfig(({ mode }) => ({\n"
        pos = vc1.find(m) + len(m)
        vc2 = vc1[:pos] + f"""build: {{
        outDir: "web"
    }},
    """ +vc1[pos:]
        vc = vc2
        file.write_text(vc, encoding="utf-8")

    # fix router
    file = Path("src/App.jsx")
    if not file.exists():
        file = Path("src/App.tsx")
    app = file.read_text(encoding="utf-8").replace("BrowserRouter", "HashRouter")
    file.write_text(app, encoding="utf-8")

    # remove index if renaming
    shutil.rmtree("web", ignore_errors=True)
    shutil.rmtree("packages", ignore_errors=True)

    os.makedirs(dir, exist_ok=True)

    Path(f"{dir}/__main__.py").write_text(f"""#--kind python:default
#--web true
#--annotation index '99:Lovable:{name}:admin:/{index}'
import {c}
def main(args):
    return {{
        "body": {c}.{c}(args)
    }} 
""")

    Path(f"{dir}/{c}.py").write_text(f"""
def {c}(args):
    return {{
        "output": "Welcome to {name}" 
    }} 
""")
except FileNotFoundError as e:
    print(f"This folder does not look like a valid Lovable app... cannot continue")