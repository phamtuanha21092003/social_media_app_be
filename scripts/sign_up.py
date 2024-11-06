import requests

url = "http://127.0.0.1:5000/apis/auth/sign_up"
headers = {
    "Content-Type": "application/json"
}

datas = [
    {
        "email": "b2@gmail.com",
        "name": "b2",
        "password": "1"
    },
    {
        "email": "b3@gmail.com",
        "name": "b3",
        "password": "1"
    },
    {
        "email": "b4@gmail.com",
        "name": "b4",
        "password": "1"
    },
    {
        "email": "b5@gmail.com",
        "name": "b5",
        "password": "1"
    },
    {
        "email": "b6@gmail.com",
        "name": "b6",
        "password": "1"
    },
    {
        "email": "b7@gmail.com",
        "name": "b7",
        "password": "1"
    },
    {
        "email": "b8@gmail.com",
        "name": "b8",
        "password": "1"
    },
    {
        "email": "b9@gmail.com",
        "name": "b9",
        "password": "1"
    },
    {
        "email": "b10@gmail.com",
        "name": "b10",
        "password": "1"
    }
]

for data in datas:
    response = requests.post(url, headers=headers, json=data)
