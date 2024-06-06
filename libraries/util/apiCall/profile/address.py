import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def postAddress(strAccessToken, dictAddress):
    """
    Method: POST
    API Endpoint: /users/address
    Payload: strAccessToken | dictAddress              
    Author: jatregenio_20240605
    """
    response = uCommon.callPost(dUrl.prf.address, dHeaders.withToken(strAccessToken),dPayload.prf.userAddress(dictAddress))
    return response