import libraries.util.common as uCommon

def guestToken(response):
    """
    Objective: Get guest token
    
    Params: response
    Returns: guestToken
    Author: cgrapa_20230803
    """
    responseData = uCommon.getResponseData(response)
    guestToken = responseData["data"]
    return guestToken