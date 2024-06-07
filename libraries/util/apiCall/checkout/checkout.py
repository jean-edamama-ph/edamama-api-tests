import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.checkout.checkout as rCheckOut

def updateMany(strToken, strCartId, strItemId, blnIsGW = ""):
    """
    Method: POST
    API Endpoint: /user/cartItems/updateMany
    Payload: _id | giftInstructions | items
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.co.updateMany, dHeaders.withToken(strToken), dPayload.co.updateMany(strCartId, strItemId, blnIsGW))

def getCart(strToken):
    """
    Method: POST
    API Endpoint: /user/getCart
    Payload: type | clearPayment | isForCheckout
    Author: cgrapa_20240604
    """
    uCommon.callPost(dUrl.co.getCart, dHeaders.withToken(strToken), dPayload.co.getCart)
    
def applyVoucher(strToken, strCartId, strCouponCode, intPaymentMethod):
    """
    Method: POST
    API Endpoint: /user/carts/applyVoucher
    Payload: couponCode | cartId | paymentMethod
    Author: jatregenio_20240605
    """
    response = uCommon.callPost(dUrl.co.applyVoucher, dHeaders.withToken(strToken), dPayload.co.applyVoucher(strCartId, strCouponCode, intPaymentMethod))
    return response

def applyVoucherAndgetCouponListDetails(strToken, strCartId, strCouponCode, intPaymentMethod):
    """
    Objective: Get the coupon details in applyVoucher response body
    Param: strToken | strCartId | strCouponCode | intPaymentMethod
    Author: jatregenio_20240606
    """
    response = applyVoucher(strToken, strCartId, strCouponCode, intPaymentMethod)
    listCouponDetails = rCheckOut.getCouponDetails(response)
    return listCouponDetails
    