import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.productPage.pdp as apiPdp
import libraries.util.apiCall.cart.cart as apiCart
import libraries.util.apiCall.checkout.checkout as apiCheckout
import libraries.util.apiCall.placeOrder as apiPlaceOrder
import libraries.util.apiCall.signUp.manualSignUp as apiManualSignUp
import libraries.util.apiCall.adminPanel.adminPanel as apiAdminPanel
import libraries.util.response.placeOrder as rPlaceOrder

@pytest.mark.api()
@allure.step('test-001-wh-single-sku-item-single-qty-checkout-without-SF-cod')
def test_001_wh_single_sku_item_single_qty_checkout_without_SF_cod():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.whNasalAspiratorTravelCase["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.whNasalAspiratorTravelCase["prodId"], dTestData.tss.whNasalAspiratorTravelCase["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.api()
@allure.step('test-001-ds-sc-item-single-item-single-qty-checkout-with-sf')
def test_001_ds_sc_item_single_item_single_qty_checkout_with_sf():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    dictAPPOrderDetails = apiPlaceOrder.placeOrderAndGetOrderDetails(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, dictAPPOrderDetails['_id'])
    
    #Verify on AP
    strAPToken = apiManualLogin.postAPUserLogin(dTestData.lgn.emailAP, dTestData.lgn.password)
    dictAPOrderDetails = apiAdminPanel.getAPOrderAndDetails(strAPToken, dictAPPOrderDetails['orderNumber'])
    apiAdminPanel.compareOrderDetails(dictAPOrderDetails, dictAPPOrderDetails)

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_101_DS-SC_item-single_sku_item_single_qty_checkout_with_SF+Referral_Code')
def test_101_DS_SC_item_single_sku_item_single_qty_checkout_with_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail)

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_102_DS-SC item_multiple_items_single_qty_checkout_with_SF+Referral_Code')
def test_102_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_02, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_02)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_103_DS-SC item_single_item_single_qty_checkout_without_SF+Referral_Code')
def test_103_DS_SC_item_single_item_single_qty_checkout_without_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_03, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_03)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_104_DS-SC item - multiple items (single quantity per SKU) checkout without SF + Referral Code')
def test_104_DS_SC_item_multiple_items_single_qty_checkout_without_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_04, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_04)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_105_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Referral Code')
def test_105_DS_SC_item_single_item_single_qty_checkout_with_GW_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_05, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_05)   

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_106_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Referral Code')
def test_106_DS_SC_item_multiple_items_single_qty_checkout_with_GW_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_06, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_06)   


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_107_DS-SC item - single item (single quantity per SKU) checkout with GW w/o fee + SF + Referral Code')
def test_107_DS_SC_item_single_item_single_qty_checkout_without_GW_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_07, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_07)

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_108_DS-SC item - multiple items (single quantity per SKU) checkout GW w/o fee + SF + Referral Code')
def test_108_DS_SC_item_multiple_items_single_qty_checkout_without_GW_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_08, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_08)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_109_DS-SC item - single item (single quantity per SKU) checkout with GW w/o fee + no SF + Referral Code')
def test_109_DS_SC_item_single_item_single_qty_checkout_with_GW_no_fee_no_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_09, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_09)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_110_DS-SC item - multiple items (single quantity per SKU) checkout GW w/o fee + no SF + Referral Code')
def test_110_DS_SC_item_multiple_items_single_qty_checkout_GW_no_fee_no_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_10, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_10)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_111_DS-SC item - single item (multiple quantities per SKU) checkout with SF + Referral Code')
def test_111_DS_SC_item_single_item_multiple_qty_checkout_with_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_11, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_11)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_112_DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Referral Code')
def test_112_DS_SC_item_multiple_items_multiple_qty_checkout_with_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_12, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 5)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_12)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_113_DS-SC item - single item (multiple quantities per SKU) checkout without SF + Referral Code')
def test_113_DS_SC_item_single_item_multiple_qty_checkout_without_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_13, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_13)

    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_114_DS-SC item - multiple items (multiple quantities per SKU) checkout without SF + Referral Code')
def test_114_DS_SC_item_multiple_items_multiple_qty_checkout_without_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_14, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductN["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductN["prodId"], dTestData.tss.scTssScProductN["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_14)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_115_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + SF + Referral Code')
def test_115_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_15, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 3)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_15)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_116_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/ fee + SF + Referral Code')
def test_116_DS_SC_item_multiple_items_multiple_qty_checkout_GW_w_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_16, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 5)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_16)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_117_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + SF + Referral Code')
def test_117_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_17, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 18)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_17)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_118_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + SF + Referral Code')
def test_118_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_18, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 8)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_18)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_119_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/o fee + no SF + Referral Code')
def test_119_DS_SC_item_single_item_multiple_qty_checkout_with_GW_no_fee_no_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_19, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_19)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_120_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/o fee + no SF + Referral Code')
def test_120_DS_SC_item_multiple_items_multiple_qty_checkout_GW_no_fee_SF_Referral_Code():
    strToken = apiManualSignUp.postAndVerifyAndAddAddressToNewSignedUpAcct(dTestData.rsg.strEmail_20, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked, dTestData.add.addAddress)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductM["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductM["prodId"], dTestData.tss.scTssScProductM["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductO["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductO["prodId"], dTestData.tss.scTssScProductO["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.strReferralCode, dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    #post-testing: Delete Registered Account to be re-used
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail_20)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_121_DS-SC item - single item (single quantity per SKU) checkout with SF + Shipping voucher')
def test_121_DS_SC_item_single_item_single_qty_checkout_with_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_122_DS-SC item - multiple items (single quantity per SKU) checkout with SF + Shipping voucher')
def test_122_DS_SC_item_multiple_items_single_qty_checkout_with_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductP["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductP["prodId"], dTestData.tss.scTssScProductP["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)
    
    
@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_123_DS-SC item - single item (single quantity per SKU) checkout with GW w/ fee + SF + Shipping voucher')
def test_123_DS_SC_item_single_item_single_qty_checkout_with_GW_w_fee_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_124_DS-SC item - multiple items (single quantity per SKU) checkout GW w/ fee + SF + Shipping voucher')
def test_124_DS_SC_item_multiple_items_single_qty_checkout_GW_w_fee_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 1)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 1)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_125_DS-SC item - single item (multiple quantities per SKU) checkout with SF + Shipping voucher')
def test_125_DS_SC_item_single_item_multiple_qty_checkout_with_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_126_DS-SC item - multiple items (multiple quantities per SKU) checkout with SF + Shipping voucher')
def test_126_DS_SC_item_multiple_items_multiple_qty_checkout_with_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_127_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + Shipping voucher')
def test_127_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["flatShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_128_DS-SC item - single item (multiple quantities per SKU) checkout with GW w/ fee + SF + Shipping voucher')
def test_128_DS_SC_item_single_item_multiple_qty_checkout_with_GW_w_fee_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 4)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["percentageShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)


@pytest.mark.tssDSSC()
@pytest.mark.api()
@allure.step('test_129_DS-SC item - multiple items (multiple quantities per SKU) checkout GW w/ fee + SF + Shipping voucher')
def test_129_DS_SC_item_multiple_items_multiple_qty_checkout_GW_w_fee_SF_Shipping_voucher():
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email_03, dTestData.lgn.password)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductQ["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductQ["prodId"], dTestData.tss.scTssScProductQ["variantId"], 2)
    apiPdp.getPDP(strToken, dTestData.tss.scTssScProductR["listName"])
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.scTssScProductR["prodId"], dTestData.tss.scTssScProductR["variantId"], 2)
    intCartItemsLength = apiCart.getCartItemsLength(strToken)
    listItemId = apiCart.getCartItemDetails(strToken, intCartItemsLength)
    apiCheckout.updateMany(strToken, strCartId, listItemId, dTestData.tss.boolYesIsGW)
    apiCheckout.getCart(strToken)
    listCouponDetails, intCouponDetailsLength = apiCheckout.applyVoucherAndgetCouponListDetails(strToken, strCartId, dTestData.tss.vouchers["percentageShipping"], dTestData.tss.intPaymentMethod)
    apiPlaceOrder.updatePayment(strToken, strCartId, listCouponDetails, intCouponDetailsLength)
    apiPlaceOrder.getCart(strToken)
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)