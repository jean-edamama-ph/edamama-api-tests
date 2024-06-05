import libraries.util.common as uCommon

def guestToken(response):
    """
    Objective: Get guest token
    
    Params: response
    Returns: guestToken
    Author: cgrapa_20230803
    """
    responseData = uCommon.getResponseData(response)
    guestToken = responseData['data']
    return guestToken

def getAccessToken(response):
    """
    Objective: Get access token
        
    Params: response
    Returns: accessToken
    Author: cgrapa_20240604
    """
    responseDate = uCommon.getResponseData(response)
    accessToken = responseDate['data']['accessToken']
    return accessToken