import libraries.util.common as uCommon

def getShipmentDetails(response):
    """
    Objective: Get the shipment number from search result
        
    Params: response
    Returns: shipmentNumber
    Author: jatregenio_20240610
    """
    responseData = uCommon.getResponseData(response)
    dictShipmentDetails = responseData["body"]
    return dictShipmentDetails