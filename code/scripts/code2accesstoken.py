import requests

client_id = str(input("Client Id: "))
client_secret = str(input("Client Secret: "))
code = str(input("Code: "))

token_response = requests.post(
    "https://www.strava.com/oauth/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
)

tokens=token_response.json()
print(tokens)
