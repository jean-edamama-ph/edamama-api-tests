import libraries.util.common as uCommon

def getShipmentDetails(response):
    responseData = uCommon.getResponseData(response)
    dictShipmentDetails = responseData["body"]
    return dictShipmentDetails