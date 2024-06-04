import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.productPage.pdp as apiPDP
import libraries.util.apiCall.cart.cart as apiCart

@pytest.mark.api()
@allure.step('test-001-wh-single-sku-item-single-qty-checkout-without-SF-cod')
def test_001_wh_single_sku_item_single_qty_checkout_without_SF_cod():
    strAccessToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    apiPDP.getPDP(dTestData.tss.whNasalAspiratorTravelCase["listName"], strAccessToken)
    strCartId= apiCart.addToCartAndGetCartId(dTestData.tss.whNasalAspiratorTravelCase["prodId"], dTestData.tss.whNasalAspiratorTravelCase["variantId"], 1, strAccessToken)
    strCartItemsLength = apiCart.getCartItemsLength(strAccessToken)

@pytest.mark.thisTest()   
def test_test():
    # LOGIN
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)
    
    # ADD ITEM TO CART AND GET CART ID
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.whNasalAspiratorTravelCase["prodId"], dTestData.tss.whNasalAspiratorTravelCase["variantId"], 1)
    
    # 
    print(strCartId)
    
    