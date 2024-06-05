import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.productPage.pdp as apiPdp
import libraries.util.apiCall.cart.cart as apiCart
import libraries.util.apiCall.checkout.checkout as apiCheckout
import libraries.util.apiCall.placeOrder as apiPlaceOrder
import libraries.util.apiCall.signUp.manualSignUp as apiManualSignUp

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