import requests
import json

url = 'http://localhost:7071'
payload = {"setOfStrings":[{"value":"Nothing is mortal"},
                           {"value":"I am immortal"},
                           {"value":"immortality"}]}

#payload = {"setOfStrings":[]} # to check empty Set
#payload = {} # to check empty body
res = requests.post(url, data=json.dumps(payload))
print res.json()
