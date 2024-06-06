import libraries.util.common as uCommon

def getCouponDetails(response):
    """
    Objective: Get coupon details
        
    Params: response
    Returns: coupon details list
    Author: jatregenio_20240606
    """
    responseData = uCommon.getResponseData(response)
    listCouponDetails = responseData["data"]["payment"]["coupons"]
    return listCouponDetails