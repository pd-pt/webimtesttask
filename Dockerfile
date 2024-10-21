FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY .env.prod .env
RUN python gen_secret.py
EXPOSE 8888
CMD ["python", "tornado_app.py"]