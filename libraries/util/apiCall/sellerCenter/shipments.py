import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def getShipments(strToken):
    """
    Method: GET
    API Endpoint: /shipments?
    Params: limit | page | generalStatus | vendorId
    Response Data: guestToken
    Author: cgrapa_20230801
    """
    response = uCommon.sc.callGet(dUrl.sc.shipments, dHeaders.withToken(strToken), dParams.sc.shipments)
    uCommon.prettyPrint(response.json())