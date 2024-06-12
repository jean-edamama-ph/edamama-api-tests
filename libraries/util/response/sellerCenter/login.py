import libraries.util.common as uCommon

def getAccessTokenAndRefreshTokenSC(response):
    """
    Objective: Get Seller Center access token
        
    Params: response
    Returns: accessToken
    Author: cgrapa_20240604
    """
    responseData = uCommon.getResponseData(response)
    accessToken = responseData['access_token']
    refreshToken = responseData['refresh_token']
    dictData = {"accessToken": accessToken, "refreshToken": refreshToken}
    return dictData