import requests

# Suponiendo que tu IP es 192.168.1.100
response = requests.get('http://192.168.51.3:5000/usuario/3')
print(response.json())