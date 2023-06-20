from fyers_api import fyersModel
from fyers_api import accessToken
from flask import Flask
from flask import abort, redirect, request
import json

apiCredFile = open("./apicred.json")
apiCredJson = json.load(apiCredFile)

client_id = apiCredJson["ClientID"]
secret_key = apiCredJson["SecretID"]
redirect_uri = apiCredJson["RedirectURI"]
response_type = "success"


session=accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri, 
    response_type="code",
    grant_type="authorization_code",
    state=response_type
)

url = session.generate_authcode()
print(url)

# auth_code = input("Enter auth code: ")
# session.set_token(auth_code)
# token_response = session.generate_token()

# # Serializing json
# tokenResponse_object = json.dumps(token_response, indent=4)

# with open("store_token.json", "w") as outfile:
#     outfile.write(tokenResponse_object)

app = Flask(__name__)

@app.route('/login')
def login():
    # redirec to https://api.fyers.in/api/v2/generate-authcode?client_id=HYMR3Q21NV-100&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Ffyers%2Fapi%2Fsuccess&response_type=code&state=success
    redirect_fyer_api_login_url = "https://api.fyers.in/api/v2/generate-authcode?client_id=HYMR3Q21NV-100&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Ffyers%2Fapi%2Fsuccess&response_type=code&state=success"
    return redirect(redirect_fyer_api_login_url)

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

   
@app.route('/fyers/api/success')
def storeToken():
    auth_code = request.args.get("auth_code")
    session.set_token(auth_code)
    token_response = session.generate_token()

    # Serializing json
    tokenResponse_object = json.dumps(token_response, indent=4)

    with open("store_token.json", "w") as outfile:
        outfile.write(tokenResponse_object)
    return "Token updated!"



if __name__ == '__main__':
   app.run(debug = True, port = 8080)