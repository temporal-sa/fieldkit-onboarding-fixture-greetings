FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
# Build the static site inside the image: web/dist is gitignored, so a
# clean clone has only web/src and web/build.py.
COPY web/src/ web/src/
COPY web/build.py web/build.py
RUN python web/build.py
EXPOSE 8000
CMD ["uvicorn", "app.web:app", "--host", "0.0.0.0", "--port", "8000"]
