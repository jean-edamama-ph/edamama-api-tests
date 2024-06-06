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

def getItemId(response, intCartItemsLength = ""):
    """
    Objective: Get item ID
        
    Params: response
    Returns: strItemId
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    if intCartItemsLength == "":
        strItemId = (responseData['data']['items'][0])['_id']
        return strItemId
    else:
        listItemId = []
        for item in range(intCartItemsLength):
            listItemId.append(responseData['data']['items'][item]['_id'])
        return listItemId

def getCartItemsLength(response):
    """
    Objective: Get the number of items in a cart
        
    Params: response
    Returns: intCartItemsLength
    Author: jatregenio_20240606
    """
    respData = uCommon.getResponseData(response)
    intCartItemsLength = (respData['data'])
    return intCartItemsLength