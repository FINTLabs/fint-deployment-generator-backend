FROM python:3.8-slim
WORKDIR /app
COPY ./app /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
