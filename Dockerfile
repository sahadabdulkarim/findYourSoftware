FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD sh -c "python -u seed_database.py && gunicorn --bind 0.0.0.0:5001 --timeout 120 run:app"
