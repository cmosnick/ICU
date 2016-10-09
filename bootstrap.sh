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
pip install Flask-API
chmod a+x app.py
python app.py &
cd ~


# Setup database
sudo apt-get install mysql-client-core-5.5


