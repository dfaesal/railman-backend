#! /bin/bash
sudo mkdir -p /home/ec2-user/railman
sudo cp -Rf /app/backend /home/ec2-user/railman
cd /home/ec2-user/railman
docker cp railmanDb_backup.dump postgresql:/var/lib/postgresql/data/railmanDb_backup.dump
docker exec -it postgresql createdb -U postgres -h localhost -p 5432 railman
docker exec -it postgresql pg_restore -U postgres -h localhost -p 5432 -F c -v -d railman /var/lib/postgresql/data/railmanDb_backup.dump
sudo yum install python3-pip -y
sudo pip install -r requirements.txt
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
pkill -f runserver
sudo python3 manage.py runserver 0.0.0.0:8000 &