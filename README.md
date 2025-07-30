# SVG to DXF Converter (File & URL)

This Flask service converts SVG to DXF via Inkscape and pstoedit. Supports two endpoints:

- **POST /to-dxf**: multipart/form-data with `file` SVG upload  
- **POST /to-dxf-url**: JSON `{ "url": "<svg-download-url>" }`

## Run Locally

```bash
pip install -r requirements.txt
python app.py
# or
gunicorn --bind 0.0.0.0:5000 app:app
```

## Docker

```bash
docker build -t svg-to-dxf-url .
docker run -e PORT=5000 -p 5000:5000 svg-to-dxf-url
```

## Deploy on Render

1. Create a new Web Service (Docker).  
2. Connect to this repo.  
3. Deploy and test:
   - `curl https://<service>/to-dxf -F "file=@input.svg"`
   - `curl -X POST https://<service>/to-dxf-url -H "Content-Type:application/json" -d '{"url":"<url>"}'`
