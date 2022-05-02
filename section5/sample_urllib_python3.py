import urllib.parse
import urllib.request

url = 'https://www.google.com'
info = {'user': 'tim', 'passwd': '31337'}
data = urllib.parse.urlencode(info).encode()
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
  content = response.read()
  print(content)
