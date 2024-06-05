import libraries.util.common as uCommon

def getOrderId(response):
    """
    Objective: Get order ID
        
    Params: response
    Returns: strOrderId
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    strOrderId = responseData['data']['_id']
    return strOrderId