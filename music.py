import requests
import time
import json

constants = {
	'time':5,
	'siteAbs':'https://vk.com/al_audio.php',
}
cookie = 'remixlang=1; remixrefkey=key; remixscreen_depth=24; audio_vol=100; _ym_uid=1468403369762901044; remixtst=b2c99173; remixflash=25.0.0; remixlhk=496c67edb4624dfc2e; remixsid=95c617f2545beb79b8d13bca10b98718861d6d24056ede364b58c; remixsslsid=1; remixdt=0; remixseenads=1; remixcurr_audio=deanon_456239561'
data='{"act":"reload_audio", "al":"1",'
data1='act=load_section; al=1; claim=0; offset=1; owner_id=deanon; playlist_id=-1; type=playlist'
def remakeToJson(string):
	json='{"'
	temp=''
	for symbol in string:
		if symbol == '=':
			json = json + temp + '":"'
			temp = ''
			continue
		if symbol == ';':
			json = json + temp + '","'
			temp = ''
		if symbol == ' ':
			temp = ''
			continue
		else:
			temp = temp + symbol
	json = json + temp + '"}'
	return json

r = requests.post('https://vk.com/al_audio.php',data=json.loads(remakeToJson(data1)),cookies=json.loads(remakeToJson(cookie)))
musicList = json.loads(r.text[r.text.find('<!json>')+7:r.text.rfind('<!><div class="audio_pl_snippet _audio_pl _audio_pl')])['list']
for i in range(len(musicList)):
	r = requests.post('https://vk.com/al_audio.php',data=json.loads(data+'"ids":"'+str(musicList[i][1])+'_'+str(musicList[i][0])+'"}'),cookies=json.loads(remakeToJson(cookie)))
	try:
		print(json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][3]+'::'+json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][4])
	except IndexError:
		print('мистер вконтач изъял запись, мы немного соснуле')
		print('\n')
		continue
	print(json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][2])
	print(str(i)+'/'+str(len(musicList)))
	music = requests.get(json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][2])
	try:
		musicFile = open(json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][3]+'::'+json.loads(r.text[r.text.find('json')+5:len(r.text)-10])[0][4],'wb')
	except BaseException:
		musicFile = open(str(musicList[i][1])+'_'+str(musicList[i][0]),'wb')
	musicFile.write(music.content)
	musicFile.close
	print('\n')
	time.sleep(5)
print('Done!')
