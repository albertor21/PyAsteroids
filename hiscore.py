import requests

url = 'http://www.domain.com/action.php'

payload = {'name': 'ARV', 'score': 2455}
headers = {'user-agent': 'Pyasteroids'}
r = requests.post(url , headers=headers, data=payload)

print (r.text)
print(r.status_code)


