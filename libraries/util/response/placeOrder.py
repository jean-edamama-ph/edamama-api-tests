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

def getOrderNumber(response):
    """
    Objective: Get order number
        
    Params: response
    Returns: strOrderNumber
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    strOrderNumber = responseData['data']['orderNumber']
    return strOrderNumber

def getOrderDetails(response):
    """
    Objective: Get order details
        
    Params: response
    Returns: strOrderDetails
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    strOrderDetails = responseData['data']
    return strOrderDetails