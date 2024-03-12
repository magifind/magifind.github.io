# Magifind.com

Jinja2 templates with blog set up with GitHub Actions CI/CD pipeline.

## How to run the website locally
1. Create a virtual environment
```bash
python3 -m venv venv
```
2. Activate the virtual environment
```bash
source venv/bin/activate
```
3. Install the dependencies
```bash
pip install -r requirements.txt
```
4. Render the website
```bash
python render.py
```
5. Run local http server on ./static folder
```bash
cd static
python -m http.server
```
6. Open the website in your browser
```bash
http://localhost:8000
```