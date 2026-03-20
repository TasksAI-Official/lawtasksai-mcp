FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY glama.json .

ENV LAWTASKSAI_LICENSE_KEY=""
ENV LAWTASKSAI_API_BASE="https://lawtasksai-api-10437713249.us-central1.run.app"

EXPOSE 8080

CMD ["python", "server.py"]
