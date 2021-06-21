import requests
from time import sleep
from random import randint

token=''

s=requests.get('https://api.vk.com/method/groups.get', params={'access_token': token, 'v': '5.103'}).json()
groups=s['response']['items']
u=0
for element in groups:
	d=requests.get('https://api.vk.com/method/groups.leave', params={'access_token': token, 'group_id': element, 'v': '5.103'}).json()
	print(str(d)+' '+str(u))
	u+=1
	sleep(randint(0,2))