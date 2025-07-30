import os, io, subprocess, tempfile, requests
from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route("/to-dxf", methods=["POST"])
def to_dxf_file():
    if "file" not in request.files:
        return "No SVG uploaded", 400

    svg = request.files["file"]
    with tempfile.TemporaryDirectory() as tmp:
        in_svg  = os.path.join(tmp, "in.svg")
        out_eps = os.path.join(tmp, "out.eps")
        out_dxf = os.path.join(tmp, "out.dxf")

        svg.save(in_svg)
        _run_inkscape(in_svg, out_eps)
        _run_pstoedit(out_eps, out_dxf)

        return send_file(out_dxf,
                         mimetype="application/dxf",
                         as_attachment=True,
                         download_name="output.dxf")

@app.route("/to-dxf-url", methods=["POST"])
def to_dxf_url():
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return "JSON body with { \"url\": \"...\" } required", 400

    # 1) fetch the SVG from your URL
    resp = requests.get(data["url"], stream=True)
    if resp.status_code != 200:
        return f"Could not fetch URL ({resp.status_code})", 400

    with tempfile.TemporaryDirectory() as tmp:
        in_svg  = os.path.join(tmp, "in.svg")
        out_eps = os.path.join(tmp, "out.eps")
        out_dxf = os.path.join(tmp, "out.dxf")

        with open(in_svg, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)

        _run_inkscape(in_svg, out_eps)
        _run_pstoedit(out_eps, out_dxf)

        return send_file(out_dxf,
                         mimetype="application/dxf",
                         as_attachment=True,
                         download_name="output.dxf")


def _run_inkscape(inp, out):
    try:
        subprocess.run([
            "inkscape", inp,
            "--batch-process",
            "--export-type=eps",
            "--export-filename", out
        ], check=True)
    except subprocess.CalledProcessError as e:
        abort(500, f"Inkscape failed: {e}")

def _run_pstoedit(inp, out):
    try:
        subprocess.run([
            "pstoedit", "-f", "dxf", "-dt", "-ssp", inp, out
        ], check=True)
    except subprocess.CalledProcessError as e:
        abort(500, f"pstoedit failed: {e}")

@app.route("/")
def index():
    return "SVG→DXF Converter is live"

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
