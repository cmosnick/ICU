#!/usr/bin/env bash

# Install and start apache
sudo apt-get update
sudo apt-get install -y apache2
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
apache2ctl start

# Install flask api
printf "Y" | sudo apt-get install python-pip
cd /vagrant/api
sudo pip install Flask-API
sudo pip install flask_sqlalchemy
sudo pip install pymysql
chmod a+x app.py
python app.py &
cd ~


# Setup database
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password pass"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password pass"
sudo apt-get -y -f install mysql-server
# echo "\n\nCREATING DATABASE\n\n____________________________________\n"
mysql -uroot -ppass -e "CREATE DATABASE capstone_icu;"
mysql -uroot -ppass -e "use capstone_icu;"
mysql -uroot -ppass -D "capstone_icu" < "/vagrant/database.sql"
sudo pip install names
# Make directory for files
mkdir /database/
mkdir /database/images
sudo chmod 771 /database/images

#  Install node
sudo apt-get -y install curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get -y install nodejs
sudo npm update

