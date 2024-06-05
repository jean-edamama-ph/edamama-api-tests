import libraries.data.headers as dHeaders
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def getPDP(strToken, strProd):
    """
    Method: GET
    API Endpoint: /product/{strProd}
    Payload: None
    Author: jatregenio_20240528
    """
    response = uCommon.callGet(dUrl.plp.skuPDP(strProd), dHeaders.withToken(strToken))
    return response