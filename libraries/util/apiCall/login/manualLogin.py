import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.guestToken as rGuestToken

def postUserLogin(strEmail, strPassword):
    """
    Method: POST
    API Endpoint: /users/login
    Payload: email | password
    Author: jatregenio_20240528
    """
    #response = uCommon.callPost(dUrl.lgn.userLogin, dHeaders.basicAuthorization(), dPayload.lgn.userLogin (strEmail, strPassword), dHeaders.auth)
    #assert respData['statusCode'] == 200, "Login unsuccessful."
    #accessToken = (respData['data']['accessToken'])
    #return accessToken
    response = uCommon.callPost(dUrl.lgn.userLogin, dHeaders.withToken(), dPayload.lgn.userLogin(strEmail, strPassword), dHeaders.auth)
    accessToken = rGuestToken.getAccessToken(response)
    return accessToken