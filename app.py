import os
import io
import subprocess
import tempfile
from flask import Flask, request, send_file, abort

app = Flask(__name__)

@app.route("/to-dxf", methods=["POST"])
def to_dxf():
    if "file" not in request.files:
        return "No SVG uploaded", 400

    # Read uploaded SVG into a temp file
    svg = request.files["file"]
    with tempfile.TemporaryDirectory() as tmp:
        svg_path = os.path.join(tmp, "input.svg")
        eps_path = os.path.join(tmp, "intermediate.eps")
        dxf_path = os.path.join(tmp, "output.dxf")

        svg.save(svg_path)

        # 1) SVG → EPS via Inkscape
        inkscape_cmd = [
            "inkscape",
            svg_path,
            "--batch-process",
            "--export-type=eps",
            "--export-filename", eps_path
        ]
        try:
            subprocess.run(inkscape_cmd, check=True)
        except subprocess.CalledProcessError as e:
            abort(500, description=f"Inkscape failed: {e}")

        # 2) EPS → DXF via pstoedit
        pstoedit_cmd = [
            "pstoedit",
            "-f", "dxf",
            "-dt",    # use legacy DXF (desktop)
            "-ssp",   # no spline approximation
            eps_path,
            dxf_path
        ]
        try:
            subprocess.run(pstoedit_cmd, check=True)
        except subprocess.CalledProcessError as e:
            abort(500, description=f"pstoedit failed: {e}")

        # Send back the DXF
        return send_file(
            dxf_path,
            mimetype="application/dxf",
            as_attachment=True,
            download_name="output.dxf"
        )

@app.route("/")
def index():
    return "SVG→DXF Converter is live"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
