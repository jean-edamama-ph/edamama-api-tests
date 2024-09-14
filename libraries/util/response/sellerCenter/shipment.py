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

def getOrderDetailsAndStatus(response):
    responseData = uCommon.getResponseData(response)
    strUserId = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["user"])["_id"]
    strName = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["user"])["name"]
    strEmail = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["user"])["email"]
    strPhoneNumber = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["phoneNumber"]
    strStreetHouse = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["landmark"]
    strCity = (((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["city"])["name"]
    strRegion = (((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["region"])["name"]
    strZipCode = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["zipCode"]
    strAltRecepient = ((((responseData["body"])["orderShipments"][0])["customerOrder"])["deliveryAddress"])["fullName"]
    strOderNumber = ((responseData["body"])["orderShipments"][0])["orderNumber"]
    intPaymentMethod = (((responseData["body"])["orderShipments"][0])["customerOrder"])["paymentMethod"]
    strSeller = (((responseData["body"])["orderShipments"][0])["vendor"])["name"]
    strShipmentNumber = ((responseData["body"])["orderShipments"][0])["shipmentNumber"]
    intStatus = ((responseData["body"])["orderShipments"][0])["status"]
    strFacility = 'SellerCenter'
    strOrderDate = ((responseData["body"])["orderShipments"][0])["createdAt"][:10]
    intTotalAmount = ((responseData["body"])["orderShipments"][0])["collectibleAmount"]
    strProductName = (((responseData["body"])["orderShipments"][0])["orderShipmentItems"][0])["productName"]
    strVariant = (((responseData["body"])["orderShipments"][0])["orderShipmentItems"][0])["productVariantCombinationName"]
    strSku = (((responseData["body"])["orderShipments"][0])["orderShipmentItems"][0])["edamamaSku"]
    dictScOrderAndShipmentDetails = {"strUserId": strUserId,
                                    "strName": strName,
                                    "strEmail": strEmail,
                                    "strPhoneNumber": strPhoneNumber,
                                    "strStreetHouse": strStreetHouse,
                                    "strCity": strCity,
                                    "strRegion": strRegion,
                                    "strZipCode": strZipCode,
                                    "strAltRecepient": strAltRecepient,
                                    "strOderNumber": strOderNumber,
                                    "intPaymentMethod": intPaymentMethod,
                                    "strSeller": strSeller,
                                    "strShipmentNumber": strShipmentNumber,
                                    "strShipmentNumber": strShipmentNumber,
                                    "intStatus": intStatus,
                                    "strFacility": strFacility,
                                    "strOrderDate": strOrderDate,
                                    "intTotalAmount": intTotalAmount,
                                    "strProductName": strProductName,
                                    "strVariant": strVariant,
                                    "strSku": strSku}
    return dictScOrderAndShipmentDetails