import requests

url = 'http://www.domain.es/action.php'

payload = {'name': 'ARV', 'score': 3255}
headers = {'user-agent': 'Pyasteroids'}
try:
    r = requests.post(url , headers=headers, data=payload)
    print (r.text)
    print (r.status_code)
except:
    print("Cannot connect with hiscore list")
            





