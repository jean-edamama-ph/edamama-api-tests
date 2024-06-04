import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def getPDP(strProd, strAccessToken):
    """
    Method: GET
    API Endpoint: /product/{strProd}
    Payload: None
    Author: jatregenio_20240528
    """
    response = uCommon.callGet(dUrl.plp.skuPDP(strProd), dHeaders.bearerAuthorization(strAccessToken), strAuth=dHeaders.auth)
    respData = uCommon.getResponseData(response)
    assert respData['statusCode'] == 200, "PDP not displayed successfully."
    return response