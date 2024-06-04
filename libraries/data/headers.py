from requests.auth import HTTPBasicAuth

import libraries.util.apiCall.guestToken as apiGuestToken

auth = HTTPBasicAuth('edamama', 'edamama@123')

def withToken(strToken = ''):
  """GENERATE TOKEN"""
  if strToken == '':
    headers = {"Guest-Token": apiGuestToken.getGuestToken(), "Api-Key": "1234"}
  else:
    headers = {"Authorization": f'Bearer {strToken}', "Api-Key": "1234"}
  return headers

def basicAuthorization():
  headers = {
    "Content-Type": "application/json", 
    "Authorization": "Basic ZWRhbWFtYTplZGFtYW1hQDEyMw==",
    "Api-Key": "1234"
    }
  return headers

def bearerAuthorization(accessToken):
  headers = {
    "Content-Type": "application/json", 
    "Guest-Token": apiGuestToken.getGuestToken(),
    #"Authorization": '"' + "Bearer " + accessToken + '"',
    "Authorization": '"' + f'Bearer {accessToken}' + '"',
    "Api-Key": "1234"
    } 
  return headers