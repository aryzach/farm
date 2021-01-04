curl 'https://192.168.1.44:8443/api/login' --data-binary '{"username":"twistedfields","password":"=9M8R+M7i","strict":true}' --compressed --insecure -c cookies.txt

curl 'https://192.168.1.44:8443/api/s/default/stat/device' --insecure -b cookies.txt -c cookies.txt | python -m json.tool > output.json

import json



with open("output.json",'r') as f:
        jlines = json.load(f)

ips = list(map(lambda x: x['ip'], jlines['data']))
names = list(map(lambda x: x['name'], jlines['data']))
 

print(ips)
print(names)
