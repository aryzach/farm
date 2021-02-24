#bash
echo "start of start.sh" >> startlog.txt
sleep 2 
source /home/pi/.bashrc
PATH=/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
ps aux | grep redis | awk '{print $2}' | head -n 1 | xargs sudo kill -9
runuser -l pi -c 'redis-server &' 
sleep 2
python3 /home/pi/twistedApp/twistedApp.py & 
python3 /home/pi/zmqServer.py & 
sudo python3 /home/pi/twistedApp/app/tools/network/pingLAN.py &
echo "after pingLAN start" >> startlog.txt
ps aux | grep mosquitto | awk '{print $2}' | head -n 1 | xargs sudo kill -9
mosquitto 
sleep 2
python3 mqttServer.py &

