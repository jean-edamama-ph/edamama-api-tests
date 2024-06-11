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
import libraries.util.apiCall.sellerCenter.login as apiScLogin
import libraries.util.apiCall.sellerCenter.shipments as apiScShipments
import libraries.util.common as uCommon


@pytest.mark.api()
@allure.step('test-001-wh-single-sku-item-single-qty-checkout-without-SF-cod')
def test_001_wh_single_sku_item_single_qty_checkout_without_SF_cod():
    uCommon.log(0, 'Step 1: Login to edamama')
    strToken = apiManualLogin.postUserLogin(dTestData.lgn.email, dTestData.lgn.password)

    uCommon.log(0, 'Step 2: Visit PDP (Product Details Page)')
    apiPdp.getPDP(strToken, dTestData.tss.whNasalAspiratorTravelCase["listName"])
    
    uCommon.log(0, 'Step 3: Add item to cart')
    strCartId = apiCart.addToCartAndGetCartId(strToken, dTestData.tss.whNasalAspiratorTravelCase["prodId"], dTestData.tss.whNasalAspiratorTravelCase["variantId"], 1)
    strItemId = apiCart.getCartItemDetails(strToken)
    
    uCommon.log(0, 'Step 4: Checkout item on cart')
    apiCheckout.updateMany(strToken, strCartId, strItemId)
    apiCheckout.getCart(strToken)
    
    uCommon.log(0, 'Step 5: Select MOP (Mode Of Payment)')
    apiPlaceOrder.updatePayment(strToken, strCartId)
    apiPlaceOrder.getCart(strToken)
    
    uCommon.log(0, 'Step 6: Place Order')
    strOrderId = apiPlaceOrder.placeOrderAndGetOrderId(strToken, strCartId)
    apiPlaceOrder.checkout(strToken, strOrderId)