import os, json, sys
from pathlib import Path

os.chdir(os.getenv("OPS_PWD") or ".")

#print(sys.argv)
if len(sys.argv) <2 or sys.argv[1] == "":
    tgt = "web"
    dir = "packages/frontend/root"
    base = "/"
else:
    c = sys.argv[1]
    dir = f"packages/frontend/{c}"
    tgt = f"web/{c}"
    base = f"/{c}/"

# fix package.json
pj = json.loads(Path("package.json").read_text(encoding="utf-8"))
pj["openserverless"] = {
    "devel": "npm run dev",
    "deploy": "npm run build"
}
Path("package.json").write_text(json.dumps(pj, indent=2), encoding="utf-8")

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
    outDir: "{tgt}"
}},
""" +vc1[pos:]
    vc = vc2
Path("vite.config.js").write_text(vc, encoding="utf-8")

os.makedirs(dir, exist_ok=True)
Path(f"{dir}/__main__.py").write_text(f"""#--kind python:default
#--web true
HTML = \"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GPT Engineer</title>
    <script type="module" crossorigin src="{base}assets/index-DTpGHxC9.js"></script>
    <link rel="stylesheet" crossorigin href="{base}assets/index-k5Wx7e2c.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
\"""

def main(args):
    return {{
        "body": HTML,
        "headers": {{"Content-Type": "text/html"}},
        "statusCode": 200
     }} 
""")


