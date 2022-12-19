# Microservice Traffic Forecast

Trabajo final de estudios para finalizar mi titulación 'Máster Universitario en Ingeniería de Telecomunicación', en la Universidad Politécnica de Cartagena.

* Nombre del trabajo: `Diseño y desarrollo de un microservicio para la gestión de información de monitorización y predicciones de tráfico en red`
* Promoción: `2022-2023`
* Estado: _EN PROCESO_

## How to's
### Start aplication (development)
- `docker compose up traffic_forecast`
- URLs:
  - app: http://localhost:5000/
  - swagger: http://localhost:5000/docs/
  - redoc (swagger alternative): http://localhost:5000/redoc 
  - adminer: http://localhost:8080/

### Start aplication (production)
- `docker compose up -f docker-compose_production.yml traffic_forecast`

### Start aplication (without Docker)
- `uvicorn src.main:app --reload --host 0.0.0.0 --port 5000`

### Database InfluxDB: ranii.pro

* URL: https://tfm-influx.ranii.pro:8443/

* Username: admin
* Password: r**22
* Org: e-lighthouse
* bucket: traffic-forecast

### Database SQL migrations

#### Initialize database models
- `docker compose exec traffic_forecast aerich init -t src.database.config.TORTOISE_ORM`
- `docker compose exec traffic_forecast aerich init-db` 

#### Upgrade database models
- `docker compose exec traffic_forecast aerich migrate`
- `docker compose exec traffic_forecast aerich upgrade`
