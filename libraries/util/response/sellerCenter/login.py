import libraries.util.common as uCommon

def getAccessTokenSC(response):
    """
    Objective: Get Seller Center access token
        
    Params: response
    Returns: accessToken
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    accessToken = responseData['access_token']
    return accessToken