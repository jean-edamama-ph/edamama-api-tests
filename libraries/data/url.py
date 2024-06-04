env = 'kpc'
baseUrl = f'https://api-v2.{env}.edamamalabs.net/api/v1'

class lgn:
    """LOGIN"""
    userLogin = '/users/login'





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