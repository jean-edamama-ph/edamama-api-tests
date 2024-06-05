import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.productPage.pdp as apiPdp
import libraries.util.apiCall.cart.cart as apiCart
import libraries.util.apiCall.checkout.checkout as apiCheckout
import libraries.util.apiCall.placeOrder as apiPlaceOrder

@pytest.mark.api()
@allure.step('test-001-wh-single-sku-item-single-qty-checkout-without-SF-cod')
def test_001_wh_single_sku_item_single_qty_checkout_without_SF_cod():
<<<<<<< Updated upstream
=======
    strAccessToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    apiPDP.getPDP(dTestData.tss.whNasalAspiratorTravelCase["listName"], strAccessToken)
    strCartId= apiCart.addToCartAndGetCartId(dTestData.tss.whNasalAspiratorTravelCase["prodId"], dTestData.tss.whNasalAspiratorTravelCase["variantId"], 1, strAccessToken)
    strCartItemsLength = apiCart.getCartItemsLength(strAccessToken)

@pytest.mark.api()   
def test_test():
    # LOGIN
>>>>>>> Stashed changes
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