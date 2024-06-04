import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.cart.cart as rCart

def postCart(strToken, strProdId, strVariantId, intQty):
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
    
    #response = uCommon.callPost(dUrl.crt.cart, dHeaders.bearerAuthorization(strAccessToken), dPayload.crt.addToCart(strProdId, strVariantId, intQty), strAuth = dHeaders.auth)
    #respData = uCommon.getResponseData(response)
    #assert respData['statusCode'] == 200, "Item not added to cart successfully."
    #cartId = (respData['data']['_id'])
    #return cartId

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