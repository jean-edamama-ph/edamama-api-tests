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
    
    
@pytest.mark.net()
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
    
fdasfdas