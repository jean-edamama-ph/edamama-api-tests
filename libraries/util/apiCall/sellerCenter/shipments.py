import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.url as dUrl
import libraries.data.payload as dPayload
import libraries.util.common as uCommon
import libraries.util.response.sellerCenter.shipment as rShipment

def getShipments(strToken):
    """
    Method: GET
    API Endpoint: /shipments?
    Params: limit | page | generalStatus | vendorId
    Response Data: guestToken
    Author: cgrapa_20230801
    """
    response = uCommon.sc.callGet(dUrl.sc.shipments, dHeaders.withToken(strToken), dParams.sc.shipments)
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
    response = uCommon.sc.callGet(dUrl.sc.shipments, dHeaders.withToken(strToken), dParams.sc.searchOrderNum(strOrderNum,strVendorId))
    dictShipmentDetails = rShipment.getShipmentDetails(response)
    return dictShipmentDetails

def callPrintPacklist(strToken, strShipmentId, strVendorId):
    response = uCommon.sc.callPatch(dUrl.sc.printPacklists, dHeaders.withToken(strToken), dPayload.sc.printPackList(strShipmentId, strVendorId))
    return response

def callPrintWayBill(strToken, strShipmentNumber, strVendorId):
    response = uCommon.sc.callPatch(dUrl.sc.printWayBill(strShipmentNumber), dHeaders.withToken(strToken), dPayload.sc.printWaybill(strShipmentNumber, strVendorId))
    return response