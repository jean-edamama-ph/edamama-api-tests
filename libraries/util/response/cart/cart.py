import libraries.util.common as uCommon

def getCartId(response):
    """
    Objective: Get cart ID
        
    Params: response
    Returns: strCartId
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    strCartId = responseData['data']['_id']
    return strCartId

def getItemId(response):
    """
    Objective: Get item ID
        
    Params: response
    Returns: strItemId
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    strItemId = (responseData['data']['items'][0])['_id']
    return strItemId