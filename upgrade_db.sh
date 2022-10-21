#source ./backend/env/bin/activate

sudo docker-compose exec traffic_forecast aerich migrate
sudo docker-compose exec traffic_forecast aerich upgrade