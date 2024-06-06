import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.placeOrder as rPlaceOrder

def getAPOrder(strToken, strOrderNumber):
    """
    Method: GET
    API Endpoint: /admin/getOrder/{strOrderNumber}
    Payload: None
    Author: abernal_20240605
    """
    response = uCommon.callGet(dUrl.ap.orderDetails(strOrderNumber), dHeaders.withToken(strToken))
    return response

def getAPOrderAndDetails(strToken, strOrderNumber):
    """
    Method: GET
    API Endpoint: /admin/getOrder/{strOrderNumber}
    Payload: None
    Author: abernal_20240605
    """
    dictAPOrderDetails = {}
    response = getAPOrder(strToken, strOrderNumber)
    dictAPOrderDetails = rPlaceOrder.getOrderDetails(response)
    return dictAPOrderDetails

def compareOrderDetails(apResponse, appResponse):
    """
    Objective: Comparing order details from AP and APP.
        
    Params: apResponse, appResponse
    Returns: None
    Author: abernal_20240606
    """
    breakpoint()
    assert apResponse['_id'] == appResponse['_id'], f'Order ID is not the same.'
    assert apResponse['orderNumber'] == appResponse['orderNumber'], f'Order number is not the same.'
    assert apResponse['createdAt'] == appResponse['createdAt'], f'Time created is not the same.'
    assert apResponse['deliveryAddress'] == appResponse['deliveryAddress'], f'Delivery address is not the same.'
    assert apResponse['billingAddress'] == appResponse['billingAddress'], f'Billing address is not the same.'
    #assert apResponse['finalStatus'] == appResponse['finalStatus'], f'Final status is not the same.'
    assert apResponse['giftInstructions'] == appResponse['giftInstructions'], f'Gift Instructions is not the same.'
    assert apResponse['noOfItems'] == appResponse['noOfItems'], f'Number of items are not the same.'
    assert apResponse['hasLootBag'] == appResponse['hasLootBag'], f'Has Loot Bag is not the same.'
    assert apResponse['orderSummary'] == appResponse['orderSummary'], f'Order Summary is not the same.'
    assert apResponse['paymentMethod'] == appResponse['paymentMethod'], f'Payment Method is not the same.'
    assert apResponse['platform'] == appResponse['platform'], f'Platform is not the same.'
    assert apResponse['totalQuantity'] == appResponse['totalQuantity'], f'Total Quantity is not the same.'
    assert apResponse['user'] == appResponse['user'], f'User details is not the same.'