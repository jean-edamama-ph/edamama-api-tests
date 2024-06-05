env = 'kpc'
baseUrl = f'https://api-v2.{env}.edamamalabs.net/api/v1'

class lgn:
    """LOGIN"""
    userLogin = '/users/login'





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
<<<<<<< Updated upstream
    getCart = '/user/getCart'
=======
>>>>>>> Stashed changes




<<<<<<< Updated upstream

class co:
    """CHECKOUT"""
    
    updateMany = '/user/cartItems/updateMany'
    getCart = '/user/getCart'





class po:
    """PLACE ORDER"""
    
    updatePayment = '/user/carts/updatePayment'
    getCart = '/user/getCart'
    ordersGenerate = '/user/orders/generate'
    checkout = '/user/carts/checkout'
    
=======
class prf:
    """PROFILE"""
    address = '/users/address'
>>>>>>> Stashed changes
