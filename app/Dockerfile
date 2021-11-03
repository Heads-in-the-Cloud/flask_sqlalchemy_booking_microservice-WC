FROM python:3.6

EXPOSE 5002

WORKDIR /app
COPY . .

COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD python run.py
