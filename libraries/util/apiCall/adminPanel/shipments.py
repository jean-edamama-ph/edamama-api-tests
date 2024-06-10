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