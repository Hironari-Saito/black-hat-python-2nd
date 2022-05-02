import requests

url = 'https://www.google.com'
data = {'user': 'tim', 'passwd': '31337'}
response = requests.post(url, data=data)

# response.text: string, response.content: byte
print(response.text)
