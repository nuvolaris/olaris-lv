import os, json, sys
from pathlib import Path

os.chdir(os.getenv("OPS_PWD") or ".")

print(sys.argv)
if len(sys.argv) <2 or sys.argv[1] == "":
    dir = "packages/lovable/index"
    extra = None
    name = "App"
    index = "index.html"
else:
    c = sys.argv[1]
    dir = f"packages/lovable/{c}"
    index = f"{c}.html"
    extra = f" && mv web/index.html web/{index}"
    name = c.capitalize()

# fix package.json
pj = json.loads(Path("package.json").read_text(encoding="utf-8"))
pj["openserverless"] = {
    "devel": "npm run dev",
    "deploy": "npm run build"
}
if extra and pj["scripts"].get("build").find("&&") == -1:
    pj["scripts"]["build"] += extra
Path("package.json").write_text(json.dumps(pj, indent=2), encoding="utf-8")

# fix vite.config.js
vc = Path("vite.config.js").read_text()
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
Path("vite.config.js").write_text(vc, encoding="utf-8")

os.makedirs(dir, exist_ok=True)
os.makedirs("web", exist_ok=True)
Path(f"{dir}/__main__.py").write_text(f"""#TODO: customize this file
#--kind python:default
#--web true
#--annotation index '99:Lovable:{name}:admin'
def main(args):
    return {{
        "body": {{"iframe": "/{index}" }}
     }} 
""")

# fix router
app = Path(f"src/App.jsx").read_text(encoding="utf-8").replace("BrowserRouter", "HashRouter")
Path(f"src/App.jsx").write_text(app, encoding="utf-8")

