FROM python:3.10-slim-bullseye

RUN mkdir app
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# for migrations
COPY migrations .

COPY src/ .

EXPOSE 5000

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]%

# Default is not set or production
ENV FASTAPI_CONFIG=$FASTAPI_CONFIG  
CMD if [ "$FASTAPI_CONFIG" = "development" ] ; \
then aerich upgrade; uvicorn src.main:app --reload --host 0.0.0.0 --port 5000; \
else aerich upgrade; uvicorn src.main:app --host 0.0.0.0 --port 5000; \
fi