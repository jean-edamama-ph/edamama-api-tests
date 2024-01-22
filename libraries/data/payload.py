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