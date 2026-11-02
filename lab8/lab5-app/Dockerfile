FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py database.py .
RUN mkdir /data
ENV DATABASE_PATH=/data/database.db
EXPOSE 5000
CMD ["python", "app.py"]
