import requests

response = requests.post("http://127.0.0.1:5000/advs",
                         json={"password": "Ffergt43321234", "title": "1111", "description": "2222", "owner": "Ivan"},
                         )
print(response.status_code)
print(response.json())

# #
# response = requests.get("http://127.0.0.1:5000/advs/1")
# print(response.status_code)
# print(response.json())

# response = requests.delete("http://127.0.0.1:5000/advs/3")
# print(response.status_code)
# print(response.json())
