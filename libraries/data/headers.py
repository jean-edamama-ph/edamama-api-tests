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