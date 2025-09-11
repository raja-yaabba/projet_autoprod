FROM python:3.11-slim
WORKDIR /app
COPY . /app
# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
EXPOSE 5000
# Use gunicorn if available, otherwise plain python
# AUTO-DETECTED ENTRY: app:app (gunicorn) from web_flask/controller.py
CMD if python -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('gunicorn') else 1)"; then \      gunicorn -w 2 -b 0.0.0.0:5000 app:app; \    else \      python web_flask/controller.py; \    fi
