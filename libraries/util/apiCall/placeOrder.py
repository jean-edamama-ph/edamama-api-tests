import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.placeOrder as rPlaceOrder

def updatePayment(strToken, strCartId):
    """
    Method: POST
    API Endpoint: /user/carts/updatePayment
    Payload: cartId | freebieId | paymentMethod | billingAddress
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.po.updatePayment, dHeaders.withToken(strToken), dPayload.po.updatePayment(strCartId))
    
def getCart(strToken):
    """
    Method: POST
    API Endpoint: /user/getCart
    Payload: type | clearPayment | isForCheckout
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.po.getCart, dHeaders.withToken(strToken), dPayload.po.getCart)

def generateOrder(strToken, strCartId):
    """
    Method: POST
    API Endpoint: /user/orders/generate
    Payload: cartId | selectiveCartMode | paymentMethod
    Author: cgrapa_20240604
    """
    response = uCommon.callPost(dUrl.po.ordersGenerate, dHeaders.withToken(strToken), dPayload.po.ordersGenerate(strCartId))
    return response

def placeOrderAndGetOrderId(strToken, strCartId):
    """
    Method: POST
    API Endpoint: /user/orders/generate
    Payload: cartId | selectiveCartMode | paymentMethod
    Author: cgrapa_20240604
    """
    response = generateOrder(strToken, strCartId)
    strOrderId = rPlaceOrder.getOrderId(response)
    return strOrderId

def checkout(strToken, strOrderId):
    """
    Method: POST
    API Endpoint: /user/carts/checkout
    Payload: orderId
    Author: cgrapa_20240604
    """
    response = uCommon.callPost(dUrl.po.checkout, dHeaders.withToken(strToken), dPayload.po.checkout(strOrderId))
    return response