import math
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

def getPostProcessOrderAndShipmentDetails(response, strVendorId):
    responseData = uCommon.getResponseData(response)
    strVendors = responseData["body"]
    intIndex = 0
    for strVendorIndex, strVendor in enumerate(strVendors):
        strSeller = (strVendor["seller"])["_id"]
        if strSeller == strVendorId:
            intIndex = strVendorIndex
    strUserId = ((responseData["body"][intIndex])["user"])["_id"]
    strName = ((responseData["body"][intIndex])["user"])["name"]
    strEmail = ((responseData["body"][intIndex])["user"])["email"]
    strPhoneNumber = ((responseData["body"][intIndex])["deliveryAddress"])["phoneNumber"]
    strStreetHouse = ((responseData["body"][intIndex])["deliveryAddress"])["landmark"]
    strCity = (((responseData["body"][intIndex])["deliveryAddress"])["city"])["name"]
    strRegion = (((responseData["body"][intIndex])["deliveryAddress"])["region"])["name"]
    strZipCode = ((responseData["body"][intIndex])["deliveryAddress"])["zipCode"]
    strAltRecepient = ((responseData["body"][intIndex])["deliveryAddress"])["fullName"]    
    strOderNumber = (responseData["body"][intIndex])["orderNumber"]
    intPaymentMethod = (responseData["body"][intIndex])["paymentMethod"]
    strSeller = ((responseData["body"][intIndex])["seller"])["name"]
    strShipmentNumber = (responseData["body"][intIndex])["shipmentNumber"]
    intStatus = (responseData["body"][intIndex])["status"]
    strFacility = (responseData["body"][intIndex])["facility"]
    strOrderDate = (responseData["body"][intIndex])["createdAt"][:10]
    intTotalAmount = ((responseData["body"][intIndex])["financeViewItems"][0])["collectibleAmount"]
    strProductName = (((responseData["body"][intIndex])["financeViewItems"][0])["product"])["name"]
    strVariant = (((responseData["body"][intIndex])["financeViewItems"][0])["variant"])["combinationName"]
    strSku = ((responseData["body"][intIndex])["financeViewItems"][0])["sku"]
    dictApOrderAndShipmentDetails = {"strUserId": strUserId,
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
                          "intStatus": intStatus,
                          "strFacility": strFacility,
                          "strOrderDate": strOrderDate,
                          "intTotalAmount": math.ceil(float(intTotalAmount)),
                          "strProductName": strProductName,
                          "strVariant": strVariant,
                          "strSku": strSku}
    return dictApOrderAndShipmentDetails