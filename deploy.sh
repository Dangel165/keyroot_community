#!/bin/bash

# Nginx 자동 배포 스크립트

echo "배포 시작..."

sudo apt update
sudo apt upgrade -y


sudo apt install -y python3 python3-pip python3-venv nginx
sudo mkdir -p /var/www/keyroot_community
sudo chown -R $USER:$USER /var/www/keyroot_community


cp -r * /var/www/keyroot_community/


cd /var/www/keyroot_community
python3 -m venv venv
source venv/bin/activate


pip install -r requirements.txt
pip install gunicorn


sudo chown -R www-data:www-data /var/www/keyroot_community
sudo chmod -R 755 /var/www/keyroot_community


sudo cp nginx_config.conf /etc/nginx/sites-available/keyroot
sudo ln -sf /etc/nginx/sites-available/keyroot /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default


sudo cp keyroot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable keyroot
sudo systemctl start keyroot

sudo nginx -t
sudo systemctl restart nginx


sudo ufw allow 'Nginx Full'

echo "배포 완료!"
echo "사이트 주소: http://your-server-ip"
echo "서비스 상태 확인: sudo systemctl status keyroot"
echo "Nginx 상태 확인: sudo systemctl status nginx"