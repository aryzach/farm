import RPi.GPIO as G
import time

G.setmode(G.BCM)

trig = 26
echo = 16 

G.setup(trig, G.OUT)
G.setup(echo, G.IN)

G.output(trig, G.LOW)
G.output(trig, G.HIGH)

time.sleep(.00001)
G.output(trig, G.LOW)

while G.input(echo)==0:
    pst = time.time()
while G.input(echo)==1:
    pet = time.time()

pd = pet - pst
d = round(pd * 17150,2)

print(d)
