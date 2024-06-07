env = 'kpc'
baseUrl = f'https://api-v2.{env}.edamamalabs.net/api/v1'
scBaseUrl = 'https://v5.api.pre.nonprod.edamamalabs.net/api/seller/v1'

class lgn:
    """LOGIN"""
    userLogin = '/users/login'
    apLogin = '/admin/login'




    class sc:
        """SELLER CENTER"""
        redirectUri = 'https://www.seller.pre.edamamalabs.net'
        authBaseUrl = 'https://edamama-pre-seller.auth.ap-southeast-1.amazoncognito.com/oauth2/authorize'
        tokenUrl = 'https://edamama-pre-seller.auth.ap-southeast-1.amazoncognito.com/oauth2/token'





class rsg:
    """REGISTRATION"""
    userSignUp = '/users/signup'




class gt:
    """GUEST TOKEN"""
    guestToken = '/users/generate-guest-account'





class plp:
    """PRODUCT LISTNG"""
    products = '/types/products'
    getCuratedTypes = '/shop/curated-types?'
    curatedTypesProducts = '/shop/curated-types/products'
    discountSpotlight = '/discount/spotlight'
    def skuPDP(sku):
        return f'/product/{sku}'





class ct:
    """CATEGORIES"""
    categories = '/categories'





class crt:
    """CART"""
    cart = '/user/carts'
    getCartItemsLength = '/user/carts/getCartItemsLength'
    getCart = '/user/getCart'





class co:
    """CHECKOUT"""
    
    updateMany = '/user/cartItems/updateMany'
    getCart = '/user/getCart'
    applyVoucher = '/user/carts/applyVoucher'





class po:
    """PLACE ORDER"""
    
    updatePayment = '/user/carts/updatePayment'
    getCart = '/user/getCart'
    ordersGenerate = '/user/orders/generate'
    checkout = '/user/carts/checkout'
    
class prf:
    """PROFILE"""
    address = '/users/address'
    
    
class ap:
    """ADMIN PANEL"""
    def orderDetails(strOrderNumber):
        return f'/admin/getOrder/{strOrderNumber}'





class sc:
    """SELLER CENTER"""
    
    shipments = '/shipments?'