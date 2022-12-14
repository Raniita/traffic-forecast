# Traffic Forecast

Trabajo Final de Master

## Start aplication (development)
- `docker compose up traffic_forecast`
- URLs:
  - app: http://localhost:5000/
  - swagger: http://localhost:5000/docs/
  - redoc (swagger alternative): http://localhost:5000/redoc 
  - adminer: http://localhost:8080/

## Start aplication (production)
- `docker compose up -f docker-compose_production.yml traffic_forecast`

## Start aplication (without Docker)
- `uvicorn src.main:app --reload --host 0.0.0.0 --port 5000`

## InfluxDB ranii.pro

* URL: https://tfm-influx.ranii.pro:8443/

* Username: admin
* Password: r**22
* Org: e-lighthouse
* bucket: traffic-forecast

## Database migrations

### Init database models
- `docker compose exec traffic_forecast aerich init -t src.database.config.TORTOISE_ORM`
- `docker compose exec traffic_forecast aerich init-db` 

### Upgrade database models
- `docker compose exec traffic_forecast aerich migrate`
- `docker compose exec traffic_forecast aerich upgrade`
