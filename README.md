# SVG to DXF Converter for Render

This Flask service converts uploaded SVG files into DXF using Inkscape and pstoedit.

## Endpoints

- **GET /** : health check
- **POST /to-dxf** : convert SVG to DXF
  - Form field: `file` (SVG upload)

## Local Testing

```bash
pip install -r requirements.txt
python app.py
# or
gunicorn --bind 0.0.0.0:5000 app:app
```

## Docker

```bash
docker build -t svg-to-dxf-render .
docker run -e PORT=5000 -p 5000:5000 svg-to-dxf-render
```

## Deploy on Render

1. Create a new Web Service (Docker).  
2. Connect your GitHub repo.  
3. Deploy; your service will be available at `https://<your-service>.onrender.com`.  
4. POST your SVG to `/to-dxf` and get back `output.dxf`.
