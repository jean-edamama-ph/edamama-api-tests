import libraries.util.common as uCommon

def getCartId(response):
    responseData = uCommon.getResponseData(response)
    strCartId = (responseData['data']['_id'])
    return strCartId