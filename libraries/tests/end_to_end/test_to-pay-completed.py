import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.productPage.pdp as apiPdp
import libraries.util.apiCall.cart.cart as apiCart
import libraries.util.apiCall.checkout.checkout as apiCheckout
import libraries.util.apiCall.placeOrder as apiPlaceOrder
import libraries.util.apiCall.signUp.manualSignUp as apiManualSignUp
import libraries.util.apiCall.adminPanel.orders as apiApOrders
import libraries.util.apiCall.adminPanel.shipments as apiApShipments
import libraries.util.apiCall.adminPanel.rewards as apiApRewards
import libraries.util.apiCall.sellerCenter.login as apiScLogin
import libraries.util.apiCall.sellerCenter.shipments as apiScShipments
import libraries.util.common as uCommon

def getDictOrderData(dictOrderData):
    listOrderItems = []
    intOderDataLength = len(dictOrderData["orderItems"])
    for item in range (intOderDataLength):
        if item + 1 < intOderDataLength:
            if dictOrderData["orderItems"][item]["product"]["seller"]["_id"] == dictOrderData["orderItems"][item + 1]["product"]["seller"]["_id"]:
                listOrderItems.append(
                    dictOrderData["orderItems"][item]["product"]["seller"]["_id"]
                ) 
                break
        listOrderItems.append(
            dictOrderData["orderItems"][item]["product"]["seller"]["_id"]
        )   
    return listOrderItems

def executeScTestSteps(strScToken, strAPToken, strOrderNumber, strVendorId):
    uCommon.log(0, '[SC] Step 1: Search shipment using order number and take note of the shipment details.')
    dictShipmentDetails = apiScShipments.searchAndGetShipmentDetails(strScToken, strOrderNumber, strVendorId)
    strShipmentId = dictShipmentDetails["orderShipments"][0]["_id"]
    strShipmentNum = dictShipmentDetails["orderShipments"][0]["shipmentNumber"]
    
    uCommon.log(0, '[SC] Step 2: Process the frist shipment and update order to "Print Packlist"')
    apiScShipments.patchPrintPacklist(strScToken, strShipmentId, strVendorId)
    
    uCommon.log(0, '[SC] Step 3: Process the frist shipment and update order "Print AWB and Book"')
    apiScShipments.patchPrintWayBill(strScToken, strShipmentNum, strVendorId)
    
    uCommon.log(0, '[SC] Step 4: Go to AP and get First Mile shipment details.')
    dictApShipmentDetailsFirstMile = apiApShipments.getApShipmentDetails(strAPToken, strShipmentNum)
    try:
        strTrackingNumFirstMile = dictApShipmentDetailsFirstMile["milestones"][0]["trackingNumber"]
    except KeyError:
        strTrackingNumFirstMile = dictApShipmentDetailsFirstMile["milestones"][1]["trackingNumber"]
    
    uCommon.log(0, '[SC] Step 5: Mimic courier behavior - update First Mile to "Shipped".')
    apiApShipments.patchMimicCourierBehavior(strAPToken, strTrackingNumFirstMile, dTestData.tss.orderShipmentSTatus["shipped"])
    
    uCommon.log(0, '[SC] Step 6: Mimic courier behavior - update First Mile to "Delivered".')
    apiApShipments.patchMimicCourierBehavior(strAPToken, strTrackingNumFirstMile, dTestData.tss.orderShipmentSTatus["delivered"])
    
    uCommon.log(0, '[SC] Step 7: Set Last Mile to "Ready To Ship"')
    apiApShipments.patchPrint(strAPToken, strShipmentNum, dTestData.tss.printType["wayBill"])
    
    uCommon.log(0, '[SC] Step 8: Get Last Mile Shipment Details"')
    dictApShipmentDetailsLastMile = apiApShipments.getApShipmentDetails(strAPToken, strShipmentNum)
    strTrackingNumLastMile = dictApShipmentDetailsLastMile["milestones"][0]["trackingNumber"]
    
    uCommon.log(0, '[SC] Step 9: Mimic courier behavior - update Last Mile to "Shipped".')
    apiApShipments.patchMimicCourierBehavior(strAPToken, strTrackingNumLastMile, dTestData.tss.orderShipmentSTatus["shipped"])
    
    uCommon.log(0, '[SC] Step 10: Mimic courier behavior - update Last Mile to "Delivered".')
    apiApShipments.patchMimicCourierBehavior(strAPToken, strTrackingNumLastMile, dTestData.tss.orderShipmentSTatus["delivered"])


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-001-ds-sc-item-single-item-single-qty-checkout-with-sf')
def test_001_ds_sc_item_single_item_single_qty_checkout_with_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-002-ds-sc-item-multiple-item-single-qty-checkout-with-sf')
def test_002_ds_sc_item_multiple_item_single_qty_checkout_with_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-003-ds-sc-item-single-item-single-qty-checkout-w/o-sf')
def test_003_ds_sc_item_single_item_single_qty_checkout_without_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-004-ds-sc-item-multiple-item-single-qty-checkout-w/o-sf')
def test_004_ds_sc_item_multiple_item_single_qty_checkout_without_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Step 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-005-ds-sc-item-single-item-multiple-qty-checkout-with-sf')
def test_005_ds_sc_item_single_item_multiple_qty_checkout_with_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-006-ds-sc-item-multiple-item-multiple-qty-checkout-with-sf')
def test_006_ds_sc_item_multiple_item_multiple_qty_checkout_with_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-007-ds-sc-item-single-item-multiple-qty-checkout-w/o-sf')
def test_007_ds_sc_item_single_item_multiple_qty_checkout_without_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 4:Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-008-ds-sc-item-multiple-item-multiple-qty-checkout-without-sf')
def test_008_ds_sc_item_multiple_item_multiple_qty_checkout_without_sf():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-009-ds-sc-item-single-item-single-qty-checkout-with-GW w/ fee + SF')
def test_009_ds_sc_item_single_item_single_qty_checkout_with_GW_with_fee_plus_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-010-ds-sc-item-multiple-item-single-qty-checkout-with-GW w/ fee + SF')
def test_010_ds_sc_item_multiple_item_single_qty_checkout_with_GW_with_fee_plus_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-011-ds-sc-item-single-item-single-qty-checkout-with-GW w/o fee + no SF')
def test_011_ds_sc_item_single_item_single_qty_checkout_with_GW_without_fee_plus_no_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-012-ds-sc-item-multiple-item-single-qty-checkout-with-GW w/o fee + no SF')
def test_012_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_no_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-013-ds-sc-item-single-item-multiple-qty-checkout-with-GW w/ fee + SF')
def test_013_ds_sc_item_single_item_multiple_qty_checkout_with_GW_with_fee_plus_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-014-ds-sc-item-multiple-item-multiple-qty-checkout-with-GW w/ fee + SF')
def test_014_ds_sc_item_multiple_item_single_qty_checkout_with_GW_with_fee_plus_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-015-ds-sc-item-single-item-multiple-qty-checkout-with-GW w/o fee + no SF')
def test_015_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-016-ds-sc-item-multiple-item-multiple-qty-checkout-with-GW w/o fee + no SF')
def test_016_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_no_SF():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-017-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + SF + Bean Rewards-partially-covered')
def test_017_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-018-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/o fee + SF + Bean Rewards-partially-covered')
def test_018_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-019-ds-sc-item-single-items-multiple-qty-checkout-GW w/ fee + SF + Bean Rewards-partially-covered')
def test_019_ds_sc_item_single_item_multiple_qty_checkout_with_GW_with_fee_plus_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-020-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/ fee + SF + Bean Rewards-partially-covered')
def test_020_ds_sc_item_multiple_item_single_qty_checkout_with_GW_with_fee_plus_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-021-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + no SF + Bean Rewards-partially-covered')
def test_021_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-022-ds-sc-item-multiple-items-multiple-qty-checkout-GW wo/ fee + no SF + Bean Rewards-partially-covered')
def test_022_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Rewards_partially_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
      
      
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-023-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + SF + Bean Rewards-fully-covered')
def test_023_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, '[Pre-condition Started]: Login to AP and update the rewards capping.')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-024-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/o fee + SF + Bean Rewards-fully-covered')
def test_024_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_without_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, '[Pre-condition Started]: Login to AP and update the rewards capping.')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-025-ds-sc-item-single-items-multiple-qty-checkout-GW w/ fee + SF + Bean Rewards-fully-covered')
def test_025_ds_sc_item_single_item_multiple_qty_checkout_with_GW_with_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, '[Pre-condition Started]: Login to AP and update the rewards capping.')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-026-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/ fee + SF + Bean Rewards-fully-covered')
def test_026_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_with_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, '[Pre-condition Started]: Login to AP and update the rewards capping.')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 5)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-027-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + no SF + Bean Rewards-fully-covered')
def test_027_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Rewards_fully_covered():
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-028-ds-sc-item-multiple-items-multiple-qty-checkout-GW wo/ fee + no SF + Bean Rewards-fully-covered')
def test_028_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Rewards_fully_covered():
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPUpdate, dTestData.ap.maxCapPercentUpdate)
    uCommon.log(0, '[Pre-condition Completed]: Rewards capping updated.')
    
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["rewards"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    uCommon.log(0, '[Post-condition Started]: Update the rewards capping to the original values.')
    apiApRewards.putRewardsCapping(strAPToken, dTestData.ap.maxCapPHPOrig, dTestData.ap.maxCapPercentOrig)
    uCommon.log(0, '[Post-condition Completed]: Rewards capping updated to the original values.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-035-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + SF + Bean Credits-fully-covered')
def test_035_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_SF_Beans_Credits_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-036-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/o fee + SF + Bean Credits-fully-covered')
def test_036_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_without_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-037-ds-sc-item-single-items-multiple-qty-checkout-GW w/ fee + SF + Bean Credits-fully-covered')
def test_037_ds_sc_item_single_item_multiple_qty_checkout_with_GW_with_fee_plus_SF_Beans_Credits_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-038-ds-sc-item-multiple-items-multiple-qty-checkout-GW w/ fee + SF + Bean Credits-fully-covered')
def test_038_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_with_fee_plus_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 4)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-039-ds-sc-item-single-items-multiple-qty-checkout-GW w/o fee + no SF + Bean Credits-fully-covered')
def test_039_ds_sc_item_single_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Credits_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-040-ds-sc-item-multiple-items-multiple-qty-checkout-GW wo/ fee + no SF + Bean Credits-fully-covered')
def test_040_ds_sc_item_multiple_item_multiple_qty_checkout_with_GW_without_fee_plus_no_SF_Beans_Rewards_fully_covered():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, strBeansType = dTestData.tss.strBeansType["credits"])
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-041-ds-sc-item-single-item-single-qty-checkout-w/ SF + Edamama voucher')
def test_041_ds_sc_item_single_item_single_qty_checkout_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-042-ds-sc-multiple-single-item-single-qty-checkout-w/ SF + Edamama voucher')
def test_042_ds_sc_item_multiple_item_single_qty_checkout_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-043-ds-sc-item-single-item-single-qty-checkout-w/o SF + Edamama voucher')
def test_043_ds_sc_item_single_item_single_qty_checkout_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-044-ds-sc-multiple-single-item-single-qty-checkout-w/o SF + Edamama voucher')
def test_044_ds_sc_item_multiple_item_single_qty_checkout_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-045-ds-sc-item-single-item-single-qty-checkout-with-GW w/ fee + SF + Edamama voucher')
def test_045_ds_sc_item_single_item_single_qty_checkout_with_GW_with_fee_plus_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-046-ds-sc-item-multiple-item-single-qty-checkout-with-GW w/ fee + SF + Edamama voucher')
def test_046_ds_sc_item_multiple_item_single_qty_checkout_with_GW_with_fee_plus_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-047-ds-sc-item-single-item-single-qty-checkout-with-GW w/o fee + SF + Edamama voucher')
def test_047_ds_sc_item_single_item_single_qty_checkout_with_GW_without_fee_plus_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-048-ds-sc-item-multiple-item-single-qty-checkout-with-GW w/o fee + SF + Edamama voucher')
def test_048_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-049-ds-sc-item-single-item-single-qty-checkout-with-GW w/o fee + no SF + Edamama voucher')
def test_049_ds_sc_item_single_item_single_qty_checkout_with_GW_without_fee_plus_no_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-050-ds-sc-item-multiple-item-single-qty-checkout-with-GW w/o fee + no SF + Edamama voucher')
def test_050_ds_sc_item_multiple_item_single_qty_checkout_with_GW_without_fee_plus_no_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-051-ds-sc-item-single-item-multiple-qty-checkout-w/ SF + Edamama voucher')
def test_051_ds_sc_item_single_item_multiple_qty_checkout_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-052-ds-sc-multiple-single-item-multiple-qty-checkout-w/ SF + Edamama voucher')
def test_052_ds_sc_item_multiple_item_multiple_qty_checkout_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-053-ds-sc-item-single-item-multiple-qty-checkout-w/o SF + Edamama voucher')
def test_053_ds_sc_item_single_item_multiple_qty_checkout_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-054-ds-sc-multiple-single-item-multiple-qty-checkout-w/o SF + Edamama voucher')
def test_054_ds_sc_item_multiple_item_multiple_qty_checkout_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-055-ds-sc-item-single-item-multiple-qty-checkout-with-GW w/ fee + SF + Edamama voucher')
def test_055_ds_sc_item_single_item_multiple_qty_checkout_GW_with_fee_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-056-ds-sc-item-multiple-item-multiple-qty-checkout-with-GW w/ fee + SF + Edamama voucher')
def test_056_ds_sc_item_multiple_item_multiple_qty_checkout_GW_with_fee_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-057-ds-sc-item-single-item-multiple-qty-checkout-with-GW w/o fee + SF + Edamama voucher')
def test_057_ds_sc_item_single_item_multiple_qty_checkout_GW_without_fee_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-058-ds-sc-item-multiple-item-multiple-qty-checkout-with-GW w/o fee + SF + Edamama voucher')
def test_058_ds_sc_item_multiple_item_multiple_qty_checkout_GW_without_fee_with_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-059-ds-sc-item-single-item-multiple-qty-checkout-with-GW w/o fee + no SF + Edamama voucher')
def test_059_ds_sc_item_single_item_multiple_qty_checkout_GW_without_fee_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-060-ds-sc-item-multiple-item-multiple-qty-checkout-with-GW w/o fee + no SF + Edamama voucher')
def test_060_ds_sc_item_multiple_item_multiple_qty_checkout_GW_without_fee_without_SF_plus_Edamama_Voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['edamama'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel and validate order details')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 7: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 8: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
       
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_101_DS-SC_item-single_sku_item_single_qty_checkout_with_SF+Referral_Code')
def test_101_DS_SC_item_single_sku_item_single_qty_checkout_with_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_102_DS-SC item_multiple_items_single_qty_checkout_with_SF+Referral_Code')
def test_102_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_02)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_02, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and add items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    
    uCommon.log(0, 'Step 3: Take note of the number of items in the cart')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 7: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_103_DS-SC item_single_item_single_qty_checkout_without_SF+Referral_Code')
def test_103_DS_SC_item_single_item_single_qty_checkout_without_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_03)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_03, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_104_DS-SC item - multiple items (single quantity per SKU) checkout without SF + Referral Code')
def test_104_DS_SC_item_multiple_items_single_qty_checkout_without_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_04)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_04, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_105_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Referral Code')
def test_105_DS_SC_item_single_item_single_qty_checkout_with_GW_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_05)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_05, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_106_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Referral Code')
def test_106_DS_SC_item_multiple_items_single_qty_checkout_with_GW_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_06)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_06, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.') 


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_107_DS-SC item - single item (single quantity per SKU) checkout with GW w/o fee + SF + Referral Code')
def test_107_DS_SC_item_single_item_single_qty_checkout_without_GW_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_07)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_07, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_108_DS-SC item - multiple items (single quantity per SKU) checkout GW w/o fee + SF + Referral Code')
def test_108_DS_SC_item_multiple_items_single_qty_checkout_without_GW_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_08)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_08, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_109_DS-SC item - single item (single quantity per SKU) checkout with GW w/o fee + no SF + Referral Code')
def test_109_DS_SC_item_single_item_single_qty_checkout_with_GW_no_fee_no_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_09)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_09, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_110_DS-SC item - multiple items (single quantity per SKU) checkout GW w/o fee + no SF + Referral Code')
def test_110_DS_SC_item_multiple_items_single_qty_checkout_GW_no_fee_no_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_10)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_10, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_111_DS-SC item - single item (multiple quantities per SKU) checkout with SF + Referral Code')
def test_111_DS_SC_item_single_item_multiple_qty_checkout_with_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_11)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_11, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 3)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_112_DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Referral Code')
def test_112_DS_SC_item_multiple_items_multiple_qty_checkout_with_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_12)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_12, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 5)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_113_DS-SC item - single item (multiple quantities per SKU) checkout without SF + Referral Code')
def test_113_DS_SC_item_single_item_multiple_qty_checkout_without_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_13)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_13, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add item on cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_114_DS-SC item - multiple items (multiple quantities per SKU) checkout without SF + Referral Code')
def test_114_DS_SC_item_multiple_items_multiple_qty_checkout_without_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_14)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_14, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_115_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + SF + Referral Code')
def test_115_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_15)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_15, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 3)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_116_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/ fee + SF + Referral Code')
def test_116_DS_SC_item_multiple_items_multiple_qty_checkout_GW_w_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_16)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_16, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 5)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_117_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + SF + Referral Code')
def test_117_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_17)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_17, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 18)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_118_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + SF + Referral Code')
def test_118_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_18)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_18, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 8)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_119_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + no SF + Referral Code')
def test_119_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_no_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_19)

    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_19, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_120_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + no SF + Referral Code')
def test_120_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_SF_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_20)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_20, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_121_DS-SC item - single item (single quantity per SKU) checkout with SF + Shipping voucher')
def test_121_DS_SC_item_single_item_single_qty_checkout_with_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_122_DS-SC item - multiple items (single quantity per SKU) checkout with SF + Shipping voucher')
def test_122_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout items on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_123_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Shipping voucher')
def test_123_DS_SC_item_single_item_single_qty_checkout_with_GW_w_fee_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_124_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Shipping voucher')
def test_124_DS_SC_item_multiple_items_single_qty_checkout_GW_w_fee_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')   
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_125_DS-SC item - single item (multiple quantities per SKU) checkout with SF + Shipping voucher')
def test_125_DS_SC_item_single_item_multiple_qty_checkout_with_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_126_DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Shipping voucher')
def test_126_DS_SC_item_multiple_items_multiple_qty_checkout_with_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_127_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + Shipping voucher')
def test_127_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_128_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + SF + Shipping voucher')
def test_128_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 4)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["percentageShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_129_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/ fee + SF + Shipping voucher')
def test_129_DS_SC_item_multiple_items_multiple_qty_checkout_GW_w_fee_SF_Shipping_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["percentageShipping"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_130_DS-SC item - single item (single quantity per SKU) checkout with SF + Edamama & Brand voucher')
def test_130_DS_SC_item_single_item_single_qty_checkout_with_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_131_DS-SC item - multiple items (single quantity per SKU) checkout with SF + Edamama & Brand voucher')
def test_131_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_132_DS-SC item - single item (single quantity per SKU) checkout without SF + Edamama & Brand voucher')
def test_132_DS_SC_item_single_item_single_qty_checkout_without_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_133_DS-SC item - multiple items (single quantity per SKU) checkout without SF + Edamama & Brand voucher')
def test_133_DS_SC_item_multiple_items_single_qty_checkout_without_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_134_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Edamama & Brand voucher')
def test_134_DS_SC_item_single_item_single_qty_checkout_with_GW_w_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_135_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Edamama & Brand voucher')
def test_135_DS_SC_item_multiple_items_single_qty_checkout_GW_w_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')

@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_136_DS-SC item - single item (single quantity per SKU) checkout with GW w/o fee + SF + Edamama & Brand voucher')
def test_136_DS_SC_item_single_item_single_qty_checkout_with_GW_no_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_137_DS-SC_item_multiple_items_single_qty_checkout_GW w/o fee + SF + Edamama & Brand voucher')
def test_137_DS_SC_item_multiple_items_single_qty_checkout_GW_no_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')    
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_138_DS-SC_item_single_item_single_qty_checkout_with GW w/o fee + no SF + Edamama & Brand voucher')
def test_138_DS_SC_item_single_item_single_qty_checkout_with_GW_no_fee_no_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_139_DS-SC item - multiple items (single quantity per SKU) checkout GW w/o fee + no SF + Edamama & Brand voucher')
def test_139_DS_SC_item_multiple_items_single_qty_checkout_GW_no_fee_no_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_140_DS-SC item - single item (multiple quantities per SKU) checkout with SF + Edamama & Brand voucher')
def test_140_DS_SC_item_single_item_multiple_qty_checkout_with_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_141_DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Edamama & Brand voucher')
def test_141_DS_SC_item_multiple_items_multiple_qty_checkout_with_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_142_DS-SC item - single item (multiple quantities per SKU) checkout without SF + Edamama & Brand voucher')
def test_142_DS_SC_item_single_item_multiple_qty_checkout_without_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_143_DS-SC item - multiple items (multiple quantities per SKU) checkout without SF + Edamama & Brand voucher')
def test_143_DS_SC_item_multiple_items_multiple_qty_checkout_without_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_144_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + SF + Edamama & Brand voucher')
def test_144_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_04, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 7)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_145_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/ fee + SF + Edamama & Brand voucher')
def test_145_DS_SC_item_multiple_items_multiple_qty_checkout_GW_w_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_146_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + SF + Edamama & Brand voucher')
def test_146_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_147_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + SF + Edamama & Brand voucher')
def test_147_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_05, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)

    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_148_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + no SF + Edamama & Brand voucher')
def test_148_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_no_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Voucher')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_149_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + no SF + Edamama & Brand voucher')
def test_149_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_no_SF_Edamama_Brand_voucher():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')    
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)

    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["edamama"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_151_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Brand_Sponsored_1_Brand_Sponsored_2')
def test_151_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Brand_Sponsored_1_Brand_Sponsored_2():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductDD["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductDD["prodId"], dTestData.tss.scTssScProductDD["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductBB["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductBB["prodId"], dTestData.tss.scTssScProductBB["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')    
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)

    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_151_DS-SC item - multiple items (single quantity per SKU) checkout without SF + Brand Sponsored 1 & Brand Sponsored 2')
def test_153_DS_SC_item_multiple_items_single_qty_checkout_without_SF_Brand_Sponsored_1_Brand_Sponsored_2():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')    
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)

    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_152_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Brand Sponsored 1 & Brand Sponsored 2')
def test_155_DS_SC_item_multiple_items_single_qty_checkout_GW_w_fee_SF_Brand_Sponsored_1_Brand_Sponsored_2():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductDD["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductDD["prodId"], dTestData.tss.scTssScProductDD["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductBB["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductBB["prodId"], dTestData.tss.scTssScProductBB["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')    
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)

    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand2"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_170_DS-SC item - single item (single quantity per SKU) checkout with SF + Brand Sponsored & Referral Code')
def test_170_DS_SC_item_single_item_single_qty_checkout_with_SF_Brand_Sponsored_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_171_DS-SC item - multiple items (single quantity per SKU) checkout with SF + Brand Sponsored & Referral Code')
def test_171_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Brand_Sponsored_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_02)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_02, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add Items')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_172_DS-SC item - single item (single quantity per SKU) checkout without SF + Brand Sponsored & Referral Code')
def test_172_DS_SC_item_single_item_single_qty_checkout_without_SF_Brand_Sponsored_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_03)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_03, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    
    uCommon.log(0, 'Step 4: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 5: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 7: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    """uCommon.log(0, 'Step 8: Place Order')
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)"""
    
    uCommon.log(0, 'Step 8: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 9: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 10: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 11: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_173_DS-SC item - multiple items (single quantity per SKU) checkout without SF + Brand Sponsored & Referral Code')
def test_173_DS_SC_item_multiple_items_single_qty_checkout_without_SF_Brand_Sponsored_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_04)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_04, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)

    uCommon.log(0, 'Step 3: Take note of the numbers of items added')
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 7: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 9: Verify order and shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 10: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])

    uCommon.log(1, 'TEST PASSED.')


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_174_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Brand Sponsored & Referral Code')
def test_174_DS_SC_item_single_item_single_qty_checkout_with_GW_w_fee_SF_Brand_Sponsored_Referral_Code():
    uCommon.log(0, 'Pre-Test: Delete Registered Account to be re-used')
    apiManualSignUp.deleteRegisteredAcct(dTestData.rsg.strEmail_05)
    
    uCommon.log(0, 'Step 1: Sign up and Login')
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_05, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked, dTestData.add.addAddress)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    
    uCommon.log(0, 'Step 3: Add Items to cart.')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId, dTestData.tss.blnYesIsGW)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Apply Vouchers')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["scBrand1"], dTestData.tss.intPaymentMethod)
    
    uCommon.log(0, 'Step 6: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 7: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails["_id"])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 9: Verify order and shipment and order details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 10: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)
    
    uCommon.log(0, 'Steps : Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])
    
    uCommon.log(1, 'TEST PASSED.')
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test-190-DS-SC item - single item (single quantity per SKU) checkout with SF + Gift Card 1 & Gift Card 2')
def test_190_ds_sc_item_single_item_single_qty_checkout_with_SF_plus_Gift_Card_1_and_Gift_Card_2():

    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard1'], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard2'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 7: Verify shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Step 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])
        
    uCommon.log(1, 'TEST PASSED.')
        

@pytest.mark.tssDCC()
@pytest.mark.api()
@allure.step('test-191-DS-SC item - multiple items (single quantity per SKU) checkout with SF + Gift Card 1 & Gift Card 2')
def test_191_ds_sc_item_multiple_item_single_qty_checkout_with_sf_plus_Gift_Card_1_and_Gift_Card_2():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard1'], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard2'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 7: Verify shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])
        
    uCommon.log(1, 'TEST PASSED.')



@pytest.mark.tssDSCC()
@pytest.mark.api()
@allure.step('test-201-DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Gift Card 1 & Gift Card 2')
def test_201_ds_sc_item_multiple_item_multiple_qty_checkout_with_SF_plus_Gift_Card_1_and_Gift_Card_2():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 2: Visit PDPs (Product Details Page) and items to cart')
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    
    uCommon.log(0, 'Step 3: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 4: Select MOP (Mode Of Payment)')
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard1'], dTestData.tss.intPaymentMethod)
    listCouponDetails = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers['giftCard2'], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Place Order')
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    strOrderNumber = dictAPPOrderDetails["orderNumber"]
    #print Order Number for reference when tester needs to manual check
    print(strOrderNumber)
    listVendors = getDictOrderData(dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 6: Login to Admin Panel')
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    
    uCommon.log(0, 'Step 7: Verify shipment details')
    dictAPOrderDetails = apiApOrders.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiApOrders.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)
    
    uCommon.log(0, 'Step 8: Login to Seller Center')
    dictScToken = apiScLogin.loginOAuth2(dTestData.lgn.sc.email, dTestData.lgn.sc.password)

    uCommon.log(0, 'Steps 9: Processing Shipments. ')
    for item in range (len(listVendors)):
        executeScTestSteps(dictScToken["accessToken"], strAPToken, strOrderNumber, listVendors[item])
        
    uCommon.log(1, 'TEST PASSED.')
