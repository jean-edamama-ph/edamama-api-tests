import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def updateMany(strToken, strCartId, strItemId):
    """
    Method: POST
    API Endpoint: /user/cartItems/updateMany
    Payload: _id | giftInstructions | items
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.co.updateMany, dHeaders.withToken(strToken), dPayload.co.updateMany(strCartId, strItemId))

def getCart(strToken):
    """
    Method: POST
    API Endpoint: /user/getCart
    Payload: type | clearPayment | isForCheckout
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.co.getCart, dHeaders.withToken(strToken), dPayload.co.getCart)