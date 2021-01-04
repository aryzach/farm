#bash
sleep 2 
source /home/pi/.bashrc
PATH=/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
ps aux | grep redis | awk '{print $2}' | head -n 1 | xargs sudo kill -9
runuser -l pi -c 'redis-server &' 
python3 /home/pi/twistedApp/twistedApp.py & 
python3 /home/pi/zmqServer.py & 
while ! ping -c 1 -W 1 192.168.1.158; do
    echo "Waiting for office AP" 
    sleep 1
done
sudo python3 /home/pi/twistedApp/app/tools/network/pingLAN.py &


