FROM python:3.10-slim-bullseye

RUN mkdir app
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# for migrations
COPY migrations .
#COPY aerich.ini .

COPY src/ .

EXPOSE 5000

## On Production, remove "--reload"!!
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]%
CMD aerich upgrade; uvicorn src.main:app --reload --host 0.0.0.0 --port 5000