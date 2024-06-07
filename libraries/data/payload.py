class lgn:
    """LOGIN"""
    
    def userLogin(email, password):
        return {
            "email": email,
            "password": password
        }




class rsg:
    """REGISTRATION"""

    def userSignUp(strEmail, strPassword, strFirstName, strLastName, blnIsPolicyChecked):
        return {
                "email": strEmail,
                "password": strPassword,
                "firstName": strFirstName,
                "lastName": strLastName,
                "isPolicyChecked": blnIsPolicyChecked
        }






class prf:
    """PROFILE"""
    
    def userAddress(dictAddress):
        strFname = dictAddress["firstName"]
        strLname = dictAddress["lastName"]
        strFullName = dictAddress["fullName"]
        strPhoneNum = dictAddress["phoneNumber"]
        strRegionName = dictAddress["regionName"]
        strRegionId = dictAddress["regionId"]
        strCityName = dictAddress["cityName"]
        strCityId = dictAddress["cityId"]
        strCityRegionId = dictAddress["cityRegionId"]
        strZipCode = dictAddress["zipCode"]
        strBarangayName = dictAddress["barangayName"]
        strBarangayId = dictAddress["barangayId"]
        strBarangayCityId = dictAddress["barangayCityId"]
        strLandmark = dictAddress["landmark"]
        strBuildingNumber = dictAddress["buildingNumber"]
        strCountry = dictAddress["country"]
        blnIsDefault = dictAddress["isDefault"]
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
                "isDefault": blnIsDefault
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
    
    def updateMany(strCartId, strItemId, blnIsGW = ""):
        if type(strItemId) == str:
            if blnIsGW == "" or blnIsGW == False:
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
            else:
                return {
                        "_id": strCartId,
                        "giftInstructions": "",
                        "items": [
                            {
                            "_id": strItemId,
                            "isGiftWrapped": True,
                            "giftNote": "",
                            "isForCheckout": True
                            }
                        ]
                    } 
        elif type(strItemId) == list:
            listItems = []
            if blnIsGW == "" or blnIsGW == False:
                for item in range (len(strItemId)):
                    listItems.append(
                        {
                            "_id": strItemId[item],
                            "isGiftWrapped": False,
                            "giftNote": "",
                            "isForCheckout": True
                        }
                    )
            else:
                for item in range (len(strItemId)):
                    listItems.append(
                        {
                            "_id": strItemId[item],
                            "isGiftWrapped": True,
                            "giftNote": "",
                            "isForCheckout": True
                        }
                    )
            return {
                    "_id": strCartId,
                    "giftInstructions": "",
                    "items": listItems
            }
            
    
    getCart = {
            "type": "buy",
            "clearPayment": True,
            "isForCheckout": True
            }
    
    def applyVoucher(strCartId, strCouponCode, intPaymentMethod):
        return {
                "couponCode": strCouponCode,
                "cartId": strCartId,
                "paymentMethod": intPaymentMethod
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

    def updatePaymentWithCoupon(listCouponDetails, strCartId):
        listVoucherStack = []
        for item in range (len(listCouponDetails)):
            floatDiscountAmount = listCouponDetails[item]["discountAmount"]
            if listCouponDetails[item]["couponType"] == 1:
                intCouponType = 1
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 2:
                intCouponType = 2
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 3:
                intCouponType = 3
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 4:
                intCouponType = 4
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 5:
                intCouponType = 5
            elif listCouponDetails[item]["couponType"] == 6:
                intCouponType = 6
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 7:
                intCouponType = 7
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            elif listCouponDetails[item]["couponType"] == 8:
                intCouponType = 8
                blnIsFreeShipping = listCouponDetails[item]["isFreeShipping"]
            strCouponCode = listCouponDetails[item]["couponCode"]
            strCouponRule = listCouponDetails[item]["couponRule"]
            strTag = listCouponDetails[item]["tag"]
            blnIsSpecialCoupon = listCouponDetails[item]["isSpecialCoupon"]
            listBrand = listCouponDetails[item]["brand"]
            listPaymentMethod = listCouponDetails[item]["paymentMethod"]
            strId = listCouponDetails[item]["_id"]
            if listCouponDetails[item]["couponType"] == 5:
                listVoucherStack.append(
                    {
                        "discountAmount": floatDiscountAmount,
                        "couponType": intCouponType,
                        "couponCode": strCouponCode,
                        "couponRule": strCouponRule,
                        "tag": strTag,
                        "isSpecialCoupon": blnIsSpecialCoupon,
                        "brand": listBrand,
                        "paymentMethod": listPaymentMethod,
                        "_id": strId,
                        "referralBeans": 300
                    }
                )
            else:
                listVoucherStack.append(
                    {
                        "discountAmount": floatDiscountAmount,
                        "couponType": intCouponType,
                        "couponCode": strCouponCode,
                        "couponRule": strCouponRule,
                        "tag": strTag,
                        "isSpecialCoupon": blnIsSpecialCoupon,
                        "isFreeShipping": blnIsFreeShipping,
                        "brand": listBrand,
                        "paymentMethod": listPaymentMethod,
                        "_id": strId
                    }
                )
        return {
            "coupons": listVoucherStack,
            "isBeansUsed": False,
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
        
    def updatePaymentWithBeans(beansType, strCartId):
        return {
                "beansType": beansType,
                "cartId": strCartId,
                "freebieId": None,
                "paymentMethod": 2,
                "billingAddress": None
            }