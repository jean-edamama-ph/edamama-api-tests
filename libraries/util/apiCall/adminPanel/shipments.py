import libraries.data.url as dUrl
import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.params as dParams
import libraries.util.common as uCommon
import libraries.util.response.adminPanel.shipments as rApShipments


def getApShipments(strToken, strShipmentNum):
    """
    Objective: GET Admin Panel Shipments
    Params: strToken, strShipmentNum
    Returns: None
    Author: jatregenio_20240610
    """
    response = uCommon.asc.callGet(dUrl.ap.shipments(strShipmentNum), dHeaders.withToken(strToken))
    return response
    
def getApShipmentDetails(strToken, strShipmentNum):
    """
    Objective: GET Shipments response data
    Params: strToken, strShipmentNum
    Returns: dictApShipmentDetails 
    Author: jatregenio_20240610
    """
    response = getApShipments(strToken, strShipmentNum)
    dictApShipmentDetails = rApShipments.getShipmentDetails(response)
    return dictApShipmentDetails

def patchMimicCourierBehavior(strToken, strTrackingNum, strStatus):
    """
    Objective: PATCH Shipments response data
    Params: strToken, strShipmentNum
    Returns: dictApShipmentDetails 
    Author: jatregenio_20240610
    """
    response = uCommon.asc.callPatch(dUrl.ap.mimicCourierBehavior(strTrackingNum), dHeaders.withToken(strToken), strParams = "", strPayload=dPayload.ap.mimicCourierBehavior(strStatus), strAuth="")
    return response

def patchPrint(strToken, strShipmentNum, strPrintType):
    """
    Objective: PATCH Print
    Params: strToken | strShipmentNum | strPrintType
    Returns: dictApShipmentDetails 
    Author: jatregenio_20240610
    """
    response = uCommon.asc.callPatch(dUrl.ap.print(strShipmentNum), dHeaders.withToken(strToken), strParams = dParams.asc.print(strPrintType), strPayload = "", strAuth = "")
    return response

def getOrdersShipment(strToken, strOrderId):
    response = uCommon.asc.callGet(dUrl.ap.sellerOrders(strOrderId), dHeaders.withToken(strToken))
    return response

def getApOrderAndShipmentDetails(strToken, strOrderId, strVendorId):
    shipmentResponse = getOrdersShipment(strToken, strOrderId)
    dictApOrderAndShipmentDetails = rApShipments.getPostProcessOrderAndShipmentDetails(shipmentResponse, strVendorId)
    return dictApOrderAndShipmentDetails

def compareApAndScDetails(dictApOrderAndShipmentDetails, dictScOrderAndShipmentDetails):
    uCommon.validateValues(dictApOrderAndShipmentDetails["strUserId"], dictScOrderAndShipmentDetails["strUserId"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strName"], dictScOrderAndShipmentDetails["strName"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strEmail"], dictScOrderAndShipmentDetails["strEmail"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strPhoneNumber"], dictScOrderAndShipmentDetails["strPhoneNumber"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strStreetHouse"], dictScOrderAndShipmentDetails["strStreetHouse"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strCity"], dictScOrderAndShipmentDetails["strCity"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strRegion"], dictScOrderAndShipmentDetails["strRegion"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strZipCode"], dictScOrderAndShipmentDetails["strZipCode"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strAltRecepient"], dictScOrderAndShipmentDetails["strAltRecepient"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strOderNumber"], dictScOrderAndShipmentDetails["strOderNumber"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["intPaymentMethod"], dictScOrderAndShipmentDetails["intPaymentMethod"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strSeller"], dictScOrderAndShipmentDetails["strSeller"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strShipmentNumber"], dictScOrderAndShipmentDetails["strShipmentNumber"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["intStatus"], dictScOrderAndShipmentDetails["intStatus"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strFacility"], dictScOrderAndShipmentDetails["strFacility"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strOrderDate"], dictScOrderAndShipmentDetails["strOrderDate"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["intTotalAmount"], dictScOrderAndShipmentDetails["intTotalAmount"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strProductName"], dictScOrderAndShipmentDetails["strProductName"])
    uCommon.validateValues(dictApOrderAndShipmentDetails["strVariant"], dictScOrderAndShipmentDetails["strVariant"])