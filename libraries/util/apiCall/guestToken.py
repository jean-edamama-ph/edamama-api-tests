import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.guestToken as rGuestToken

def getGuestToken():
    """
    Method: GET
    API Endpoint: /users/generate-guest-account
    Params: None
    Response Data: guestToken
    Author: cgrapa_20230801
    """
    response = uCommon.callGetAndValidateResponse(dUrl.gt.guestToken)
    strGuestToken = rGuestToken.guestToken(response)
    return strGuestToken