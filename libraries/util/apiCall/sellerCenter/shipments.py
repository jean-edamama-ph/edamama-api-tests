import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.url as dUrl
import libraries.data.payload as dPayload
import libraries.util.common as uCommon
import libraries.util.response.sellerCenter.shipment as rShipment

def getShipments(strToken, strVendorId):
    """
    Method: GET
    API Endpoint: /shipments?
    Params: limit | page | generalStatus | vendorId
    Response Data: guestToken
    Author: cgrapa_20230801
    """
    response = uCommon.sc.callGet(dUrl.sc.shipments, dHeaders.withToken(strToken), dParams.sc.shipments(strVendorId))
    return response

def searchShipments(strToken, strOrderNum, strVendorId):
    """
    Method: GET
    API Endpoint: /shipments?
    Params: limit | page | generalStatus | orderNumber | vendorId
    Response: response
    Author: jatregenio_20240610
    """
    response = uCommon.sc.callGet(dUrl.sc.shipments, dHeaders.withToken(strToken), dParams.sc.searchOrderNum(strOrderNum,strVendorId))
    return response

def searchAndGetShipmentDetails(strToken, strOrderNum, strVendorId):
    """
    Method: GET
    API Endpoint: /shipments?
    Params: limit | page | generalStatus | orderNumber | vendorId
    Response: response
    Author: jatregenio_20240610
    """
    response = searchShipments(strToken, strOrderNum, strVendorId)
    dictShipmentDetails = rShipment.getShipmentDetails(response)
    return dictShipmentDetails

def patchPrintPacklist(strToken, strShipmentId, strVendorId):
    """
    Method: Update Order to Print Packlist
    API Endpoint: /shipments/printPacklists
    Params: strToken | strShipmentId | strVendorId 
    Response: response
    Author: jatregenio_20240610
    """
    response = uCommon.sc.callPatch(dUrl.sc.printPacklists, dHeaders.withToken(strToken), dPayload.sc.printPackList(strShipmentId, strVendorId))
    return response

def patchPrintWayBill(strToken, strShipmentNumber, strVendorId):
    """
    Method: Update Order to Print Waybill
    API Endpoint: /shipments/{strShipmentNumber}/printWaybill
    Params: strToken | strShipmentNumber | strVendorId 
    Response: response
    Author: jatregenio_20240610
    """
    response = uCommon.sc.callPatch(dUrl.sc.printWayBill(strShipmentNumber), dHeaders.withToken(strToken), dPayload.sc.printWaybill(strShipmentNumber, strVendorId))
    return response

def postCognitoIdp(strToken, strClientId, strAuthFlow):
    """
    Method: Post cognito idp to gain access in aws
    API Endpoint: https://cognito-idp.ap-southeast-1.amazonaws.com/
    Params: strToken | strClientId | strAuthFlow 
    Response: response
    Author: jatregenio_20240610
    """
    response = uCommon.sc.callPost(dUrl.lgn.sc.cognitoIdpUrl, dHeaders.withToken(strToken), dPayload.sc.cognitoIdp(strToken, strClientId, strAuthFlow))
    return response