#source ./env/bin/activate

sudo docker-compose exec traffic_forecast aerich init -t src.database.config.TORTOISE_ORM
# Success create migrate location ./migrations
# Success generate config file aerich.ini

sudo docker-compose exec traffic_forecast aerich init-db
# Success create app migrate location migrations/models
# Success generate schema for app "models"