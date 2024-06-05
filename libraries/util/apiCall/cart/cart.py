import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.cart.cart as rCart

def postCart(strToken, strProdId, strVariantId, intQty):
    """
    Method: POST
    API Endpoint: /user/carts
    Payload: prodId | variantId | quantity
    Author: cgrapa_20240604
    """
    response = uCommon.callPost(dUrl.crt.cart, dHeaders.withToken(strToken), dPayload.crt.addToCart(strProdId, strVariantId, intQty))
    return response

def addToCartAndGetCartId(strToken, strProdId, strVariantId, intQty):
    """
    Method: POST
    API Endpoint: /user/carts
    Payload: prodId | variantId | quantity
    Author: jatregenio_20240528
    """
    response = postCart(strToken, strProdId, strVariantId, intQty)
    strCartId = rCart.getCartId(response)
    return strCartId

def getCart(strToken):
    """
    Method: POST
    API Endpoint: /user/getCart
    Payload: type | clearPayment | isForCheckout
    Author: cgrapa_20240604
    """
    response = uCommon.callPost(dUrl.crt.getCart, dHeaders.withToken(strToken), dPayload.crt.getCart)
    return response

def getCartItemDetails(strToken):
    """
    Method: POST
    API Endpoint: /user/getCart
    Payload: type | clearPayment | isForCheckout
    Author: cgrapa_20240604
    """
    response = getCart(strToken)
    strItemId = rCart.getItemId(response)
    return strItemId

def getCartItemsLength(strAccessToken):
    """
    Method: POST
    API Endpoint: /user/carts/getCartItemsLength
    Payload: None
    Author: jatregenio_20240528
    """
    response = uCommon.callPost(dUrl.crt.getCartItemsLength, dHeaders.bearerAuthorization(strAccessToken), strPayload = "", strAuth = dHeaders.auth)
    respData = uCommon.getResponseData(response)
    print(respData)
    assert respData['statusCode'] == 200, 'Cart items lengeth not retrieved.' 
    cartItemsLength = (respData['data'])
    return cartItemsLength