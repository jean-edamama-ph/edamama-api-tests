class lgn:
    """LOGIN"""
    
    def userLogin(email, password):
        return {
            "email": email,
            "password": password
        }




class rsg:
    """REGISTRATION"""

    def userSignUp(strEmail, strPassword, strFirstName, strLastName, boolIsPolicyChecked):
        return {
                "email": strEmail,
                "password": strPassword,
                "firstName": strFirstName,
                "lastName": strLastName,
                "isPolicyChecked": boolIsPolicyChecked
        }






class prf:
    """PROFILE"""
    
    def userAddress(strFname, strLname, strFullName, strPhoneNum, strRegionName, strRegionId, strCityName, strCityId, strCityRegionId, strZipCode, strBarangayName, strBarangayId,
                    strBarangayCityId, strLandmark, strBuildingNumber, strCountry, boolIsDefault):
        return {
                "firstName": strFname,
                "lastName": strLname,
                "fullName": strFullName,
                "phoneNumber": strPhoneNum,
                "region": {
                    "name": strRegionName,
                    "_id": strRegionId,
                },
                "city": {
                    "name": strCityName,
                    "_id": strCityId,
                    "regionId": strCityRegionId,
                },
                "zipCode": strZipCode,
                "barangay": {
                    "name": strBarangayName,
                    "_id": strBarangayId,
                    "cityId": strBarangayCityId,
                },
                "landmark": strLandmark,
                "buildingNumber": strBuildingNumber,
                "country": strCountry,
                "isDefault": boolIsDefault
        }

class plp:
    """PRODUCT LISTING"""
    
    def products(strCategoryId):
        return {
                "page": 1,
                "sortby": 4,
                "filters": [],
                "parentCategory": strCategoryId,
                "limit": 1
            }
    
    def filterByBrand(strCategoryId, strBrandName, strBrandId, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [
                    {
                        "_id": "brand",
                        "options": [
                            strBrandId
                        ]
                    }
                ],
                "BrandName": strBrandName,
                "parentCategory": strCategoryId
            }
    
    def filterByColor(strCategoryId, strColorName, strColorId, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "ColorName": strColorName,
                "color": [
                    strColorId
                ],
                "parentCategory": strCategoryId
            }
    
    def filterByPrice(strCategoryId, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "minPrice": intMin,
                "maxPrice": intMax,
                "parentCategory": strCategoryId
            }
    
    def filterByDiscount(strCategoryId, intMinDiscount, intMaxDiscount, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "discountRange": f'{intMinDiscount}-{intMaxDiscount}',
                "parentCategory": strCategoryId
            }
    
    def filterByAgeGroup(strCategoryId, strAgeGroupOption, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [
                    {
                        "_id": "ageGroup",
                        "options": [
                            strAgeGroupOption
                        ]
                    }
                ],
                "parentCategory": strCategoryId
            }
        
    def filterByGender(strCategoryId, strGenderId, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [
                    {
                        "_id": "gender",
                        "options": [
                            strGenderId
                        ]
                    }
                ],
                "parentCategory": strCategoryId
            }
    
    def filterByCategoryL2(strCategoryId, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "parentCategory": strCategoryId
            }
        
    def filterByCategoryL3(strCategoryId, intPage = 1):
        return {
                "page": intPage,
                "sortby": 4,
                "filters": [
                    {
                        "_id": "category",
                        "options": [
                            strCategoryId
                        ]
                    }
                ],
                "parentCategory": "",
                "limit": 1
            }
        
    def sortBy(strCategoryId, intSortOption, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": intSortOption,
                "filters": [],
                "parentCategory": strCategoryId
            }
    
    def search(strSearchTerm, intPage = 1, intSortOption = 0):
        return {
                "searchInput": strSearchTerm,
                "isMobile": False,
                "search": strSearchTerm,
                "page": intPage,
                "limit": 100,
                "color": [],
                "filter": [
                    {
                        "_id": "brand",
                        "options": []
                    },
                    {
                        "_id": "ageGroup",
                        "options": []
                    },
                    {
                        "_id": "gender",
                        "options": []
                    }
                ],
                "sortby": intSortOption
            }
    
    def searchLimit1(strSearchTerm):
        return {
                "filters": [],
                "limit": 1,
                "page": 1,
                "search": strSearchTerm,
                "sortBy": 0
            }
    
    def filterSearchByBrand(strSearchTerm, strBrandId, intPage = 1):
        return {
                "searchInput": strSearchTerm,
                "isMobile": False,
                "search": strSearchTerm,
                "page": intPage,
                "limit": 100,
                "color": [],
                "filter": [
                    {
                        "_id": "brand",
                        "options": [
                            strBrandId
                        ]
                    },
                    {
                        "_id": "ageGroup",
                        "options": []
                    },
                    {
                        "_id": "gender",
                        "options": []
                    }
                ],
                "sortby": "0"
            }
    
    def filterSearchByGender(strSearchTerm, strGenderId, intPage = 1):
        return {
                "searchInput": strSearchTerm,
                "isMobile": False,
                "search": strSearchTerm,
                "page": intPage,
                "limit": 100,
                "color": [],
                "filter": [
                    {
                        "_id": "brand",
                        "options": []
                    },
                    {
                        "_id": "ageGroup",
                        "options": []
                    },
                    {
                        "_id": "gender",
                        "options": [
                            strGenderId
                        ]
                    }
                ],
                "sortby": "0"
            }
    
    def filterSearchByAgeGroup(strSearchTerm, strGroupOption, intPage = 1):
        return {
                "searchInput": strSearchTerm,
                "isMobile": False,
                "search": strSearchTerm,
                "page": intPage,
                "limit": 100,
                "color": [],
                "filter": [
                    {
                        "_id": "brand",
                        "options": []
                    },
                    {
                        "_id": "ageGroup",
                        "options": [
                            strGroupOption
                        ]
                    },
                    {
                        "_id": "gender",
                        "options": []
                    }
                ],
                "sortby": "0"
            }
    
    def filterSearchByColor(strSearchTerm, strColorName, intPage = 1):
        return {
                "searchInput": strSearchTerm,
                "isMobile": False,
                "search": strSearchTerm,
                "page": intPage,
                "limit": 100,
                "color": [
                    strColorName
                ],
                "filter": [
                    {
                        "_id": "brand",
                        "options": []
                    },
                    {
                        "_id": "ageGroup",
                        "options": []
                    },
                    {
                        "_id": "gender",
                        "options": []
                    }
                ],
                "sortby": "0"
            }
    
    def filterSearchByPrice(strSearchTerm, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "search": strSearchTerm,
                "color": [],
                "filter": [],
                "minPrice": intMin,
                "maxPrice": intMax,
                "sortby": 0,
                "isMobile": False
            }
    
    def curatedProducts(strCuratedLname):
        return {
                "limit":100,
                "page":1,
                "sortby":4,
                "filters":[],
                "curatedType": strCuratedLname
            }
    
    def filterCuratedByPrice(strId, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "minPrice": intMin,
                "maxPrice": intMax,
                "curatedType": strId
            }
    
    discountSpotlight = {}
    
    def discountSpotlightProducts(strUuid):
        return {
                "limit": 100,
                "page": 1,
                "sortby": 4,
                "filters": [],
                "productSpotlight": strUuid
            }
    
    def filterDiscountSpotlightByPrice(strId, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "productSpotlight": strId,
                "minPrice": intMin,
                "maxPrice": intMax
            }
    
    snsProducts = {
                "limit": 100,
                "page": 1,
                "sortby": 4,
                "filters": [],
                "productSpotlight": "subscribe"
            }
    
    def filterSnsByPrice(strId, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "productSpotlight": strId,
                "minPrice": intMin,
                "maxPrice": intMax
            }
    
    def brandProducts(strBrandName):
        return {
                "limit": 100,
                "page": 1,
                "sortby": 4,
                "filters": [],
                "brandName": strBrandName
            }
    
    def filterBrandByPrice(strId, intMin, intMax, intPage = 1):
        return {
                "limit": 100,
                "page": intPage,
                "sortby": 4,
                "filters": [],
                "brandName": strId,
                "minPrice": intMin,
                "maxPrice": intMax
            }
        




class crt:
    def addToCart(strProdId, strVariantId, intQty):
        return {
                "items":[
                    {
                     "productId": strProdId,
                     "variantId": strVariantId,
                     "quantity": intQty
                     }],
                "type":"buy"
                }
    
    getCart = {
            "type": "buy",
            "clearPayment": True,
            "isForCheckout": False
            }





class co:
    """CHECK OUT"""
    
    def updateMany(strCartId, strItemId):
        return {
                "_id": strCartId,
                "giftInstructions": "",
                "items": [
                    {
                    "_id": strItemId,
                    "isGiftWrapped": False,
                    "giftNote": "",
                    "isForCheckout": True
                    }
                ]
            }
    
    getCart = {
            "type": "buy",
            "clearPayment": True,
            "isForCheckout": True
            }





class po:
    """PLACE ORDER"""
    
    def updatePayment(strCartId):
        return {
                "cartId": strCartId,
                "freebieId": None,
                "paymentMethod": 2,
                "billingAddress": None
            }
    
    getCart = {
            "type": "buy",
            "clearPayment": False,
            "isForCheckout": True
        }
    
    def ordersGenerate(strCartId):
        return {
                "cartId": strCartId,
                "selectiveCartMode": True,
                "paymentMethod": 2
            }
    
    def checkout(strOrderId):
        return {
                "orderId": strOrderId
            }