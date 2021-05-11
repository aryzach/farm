#bash
echo "start of start.sh" >> startlog.txt
sleep 2 
source /home/pi/.bashrc
PATH=/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
ps aux | grep redis | awk '{print $2}' | head -n 1 | xargs sudo kill -9
runuser -l pi -c 'redis-server &' 
sleep 2

# point port 80 to port 5000 
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 5000


# add to routing table to ping from two interfaces
sudo route add -host 8.8.8.8 gw 192.168.1.1
sudo route add -host 8.8.8.8 gw 192.168.2.1

python3 /home/pi/twistedApp/twistedApp.py & 
python3 /home/pi/zmqServer.py & 
sudo python3 /home/pi/twistedApp/app/tools/network/pingLAN.py &
echo "after pingLAN start" >> startlog.txt
ps aux | grep mosquitto | awk '{print $2}' | head -n 1 | xargs sudo kill -9
#mosquitto &
sleep 2
#python3 mqttServer.py &

