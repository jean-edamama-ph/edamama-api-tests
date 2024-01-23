import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.categories as rCategories
import libraries.util.response.productListing as rProductListing

def postTypesProducts(strPayload):
    """
    Method: POST
    API Endpoint: /types/products
    Payload: page | sortby | filters | parentCategory | limit
    Author: cgrapa_20230713
    """
    response = uCommon.callPostAndValidateResponse(dUrl.plp.products, dHeaders.withToken(), strPayload, dHeaders.auth)  
    return response

def getCategories():
    """
    Method: GET
    API Endpoint: /categories
    Params: None
    Author: cgrapa_20230713
    """
    response = uCommon.callGetAndValidateResponse(dUrl.ct.categories, dHeaders.withToken(), dParams.categories, dHeaders.auth)
    return response

def validateBrands(response, strCategoryId, strBrandName, strBrandId):
    """
    Objective: Validate Items by Brand
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | BrandName | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByBrand(strCategoryId, strBrandName, strBrandId, intPage + 1))
        rProductListing.fv.validateBrandFilter(response, strBrandName)
        rProductListing.fv.detectDuplicateProductCards(response, f'Brand Filter: {strBrandName}')
    
def filterByBrand(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Brand
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | BrandName | parentCategory
    Author: cgrapa_20230803
    """
    arrOptions = rProductListing.df.getBrandFilterOptions(response)
    for strBrandOption in uCommon.progressBar(arrOptions, f'{strCategoryName} | Brand Filter:'):
        strBrandName = strBrandOption["brandName"]
        strBrandId = strBrandOption["brandId"]
        response = postTypesProducts(dPayload.plp.filterByBrand(strCategoryId, strBrandName, strBrandId))
        validateBrands(response, strCategoryId, strBrandName, strBrandId)
    uCommon.printErrorCount('Brand Filter')
    

def validateAgeGroup(response, strCategoryId, strAgeGroupOption):
    """
    Objective: Validate Items by Age Group
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByAgeGroup(strCategoryId, strAgeGroupOption, intPage + 1))
        rProductListing.fv.validateAgeGroupFilter(response, strAgeGroupOption)
        rProductListing.fv.detectDuplicateProductCards(response, f'Age Group Filter: {strAgeGroupOption}')

def filterByAgeGroup(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Age Group
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    arrOptions = rProductListing.df.getAgeGroupFilterOptions(response)
    for strAgeGroupOption in uCommon.progressBar(arrOptions, f'{strCategoryName} | Age Group Filter:'):
        response = postTypesProducts(dPayload.plp.filterByAgeGroup(strCategoryId, strAgeGroupOption))
        validateAgeGroup(response, strCategoryId, strAgeGroupOption)
    uCommon.printErrorCount('Age Group Filter')

def validateColor(response, strCategoryId, strColorName, strColorId):
    """
    Objective: Validate Items by Color
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | ColorName | color | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByColor(strCategoryId, strColorName, strColorId, intPage + 1))
        rProductListing.fv.validateColorFilter(response, strColorName)
        rProductListing.fv.detectDuplicateProductCards(response, f'Color Filter: {strColorName}')

def filterByColor(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Color
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | ColorName | color | parentCategory
    Author: cgrapa_20230803
    """
    arrOptions = rProductListing.sf.getColorFilterOptions(response)
    for strColorOption in uCommon.progressBar(arrOptions, f'{strCategoryName} | Color Filter:'):
        strColorName = strColorOption["colorName"]
        strColorId = strColorOption["colorId"]
        response = postTypesProducts(dPayload.plp.filterByColor(strCategoryId, strColorName, strColorId))
        validateColor(response, strCategoryId, strColorName, strColorId)
    uCommon.printErrorCount('Color Filter')

def validatePrice(response, strCategoryId, intMin, intMax):
    """
    Objective: Validate Items by Price
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | minPrice | maxPrice | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByPrice(strCategoryId, intMin, intMax, intPage + 1))
        rProductListing.fv.validatePriceFilter(response, intMin, intMax)
        rProductListing.fv.detectDuplicateProductCards(response, f'Price Filter: {intMin} - {intMax}')

def filterByPrice(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Price
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | minPrice | maxPrice | parentCategory
    Author: cgrapa_20230803
    """
    intMaxPrice = int(rProductListing.sf.getPriceFilterOptions(response))
    intMin = 0
    intIncrementValue = 250
    for intMin in uCommon.progressBar(range(0, intMaxPrice, intIncrementValue), f'{strCategoryName} | Price Filter:'):
        intMax = intMin + intIncrementValue
        response = postTypesProducts(dPayload.plp.filterByPrice(strCategoryId, intMin, intMax))
        validatePrice(response, strCategoryId, intMin, intMax)
    uCommon.printErrorCount('Price Filter')

def validateDiscount(response, strCategoryId, intMinDiscount, intMaxDiscount):
    """
    Objective: Validate Items by Discount
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | discountRange | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByDiscount(strCategoryId, intMinDiscount, intMaxDiscount, intPage + 1))
        rProductListing.fv.validateDiscountFilter(response, intMinDiscount, intMaxDiscount)
        rProductListing.fv.detectDuplicateProductCards(response, f'Discount Filter: {intMinDiscount}-{intMinDiscount}')

def filterByDiscount(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Discount
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | discountRange | parentCategory
    Author: cgrapa_20230803
    """
    intMinDiscount = 1
    intMaxDiscount = 100
    intIncrementValue = 10
    for intMinDiscount in uCommon.progressBar(range(intMinDiscount, intMaxDiscount, intIncrementValue), f'{strCategoryName} | Discount Filter:'):
        intMaxDiscount = intMinDiscount + 9
        response = postTypesProducts(dPayload.plp.filterByDiscount(strCategoryId, intMinDiscount, intMaxDiscount))
        validateDiscount(response, strCategoryId, intMinDiscount, intMaxDiscount)
    uCommon.printErrorCount('Discount Filter')

def validateGender(response, strCategoryId, strGenderId, strGenderName):
    """
    Objective: Validate Items by Gender
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByGender(strCategoryId, strGenderId, intPage + 1))
        rProductListing.fv.validateGenderFilter(response, strGenderName, strGenderId)
        rProductListing.fv.detectDuplicateProductCards(response, f'Gender Filter: {strGenderName}')

def filterByGender(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Gender
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    arrOptions = rProductListing.df.getGenderFilterOptions(response)
    for strGenderOption in uCommon.progressBar(arrOptions, f'{strCategoryName} | Gender Filter:'):
        strGenderName = strGenderOption["genderName"]
        strGenderId = strGenderOption["genderId"]
        response = postTypesProducts(dPayload.plp.filterByGender(strCategoryId, strGenderId))
        validateGender(response, strCategoryId, strGenderId, strGenderName)
    uCommon.printErrorCount('Gender Filter')

def validateCategoryLevel(strCategoryId, strFilterCategoryId):
    """
    Objective: Validate Category Level
    
    Method: GET
    API Endpoint: /categories
    Params: None
    Returns: strCategoryLevel
    Author: cgrapa_20230803
    """
    response = getCategories()
    strCategoryLevel = rCategories.ct.getCategoryLevel(response, strCategoryId, strFilterCategoryId)
    return strCategoryLevel

def validateCategoryL2(response, strFilterCategoryId, strFilterCategoryName):
    """
    Objective: Validate level 2 category items
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByCategoryL2(strFilterCategoryId, intPage + 1))
        rProductListing.fv.validateCategoryFilter(response, strFilterCategoryId, strFilterCategoryName)
        rProductListing.fv.detectDuplicateProductCards(response, f'Category Filter: {strFilterCategoryName}')

def validateCategoryL3(response, strFilterCategoryId, strFilterCategoryName):
    """
    Objective: Validate level 3 category items
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | id | options | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterByCategoryL3(strFilterCategoryId, intPage + 1))
        rProductListing.fv.validateCategoryFilter(response, strFilterCategoryId, strFilterCategoryName)
        rProductListing.fv.detectDuplicateProductCards(response, f'Category Filter: {strFilterCategoryName}')

def filterByCategory(response, strCategoryId, strCategoryName):
    """
    Objective: Filter and validate items by Category
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    arrOptions = rProductListing.df.getCategoryFilterOptions(response)
    for strCategoryOption in uCommon.progressBar(arrOptions, f'{strCategoryName} | Category Filter:'):
        strFilterCategoryName = strCategoryOption["categoryName"]
        strFilterCategoryId = strCategoryOption["categoryId"]
        strCategoryLevel = validateCategoryLevel(strCategoryId, strFilterCategoryId)
        match strCategoryLevel:
            case 'L2': 
                response = postTypesProducts(dPayload.plp.filterByCategoryL2(strFilterCategoryId))
                validateCategoryL2(response, strFilterCategoryId, strFilterCategoryName)
            case 'L3': 
                response = postTypesProducts(dPayload.plp.filterByCategoryL3(strFilterCategoryId))
                validateCategoryL3(response, strFilterCategoryId, strFilterCategoryName)
    uCommon.printErrorCount('Category Filter')
    

def sortByNewest(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Newest
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 1))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Newest Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 1, intPage + 1))
        rProductListing.sv.validateSortingByNewest(response, intPage + 1)
    uCommon.printErrorCount('Newest Sorting')

def sortByPriceLowToHigh(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Price - Low to High
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 2))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Price(L-H) Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 2, intPage + 1))
        rProductListing.sv.validateSortingByPriceLowToHigh(response, intPage + 1)
    uCommon.printErrorCount('Price(Low to High) Sorting')

def sortByPriceHighToLow(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Price - High to Low
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 3))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Price(H-L) Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 3, intPage + 1))
        rProductListing.sv.validateSortingByPriceHighToLow(response, intPage + 1)
    uCommon.printErrorCount('Price(High to Low) Sorting')

def sortByPopularity(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Popularity
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 4))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Popularity Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 4, intPage + 1))
        rProductListing.sv.validateSortingByPopularity(response, intPage + 1)
    uCommon.printErrorCount('Popularity sorting')

def sortByDiscountHighToLow(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Discount - Hight to Low
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 6))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Discount(H-L) Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 6, intPage + 1))
        rProductListing.sv.validateSortingByDiscountHighToLow(response, intPage + 1)
    uCommon.printErrorCount('Discount(High to Low) Sorting')

def sortByLastUpdated(strCategoryId, strCategoryName):
    """
    Objective: Sort and validate items by Last Updated
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | parentCategory
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 7))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strCategoryName} | Last Updated Sorting:'):
        response = postTypesProducts(dPayload.plp.sortBy(strCategoryId, 7, intPage + 1))
        rProductListing.sv.validateSortingByLastUpdated(response, intPage + 1)
    uCommon.printErrorCount('Last Updated Sorting')

def validateDynamicFilters(response, strCategoryId, strCategoryName):
    """
    Objective: Validate Dynamic filters
    
    Params: response | strCategoryId | strCategoryName
    Returns: None
    Author: cgrapa_20230803
    """
    arrDynamicFilters = rProductListing.df.getPlpDynamicFilters(response)
    for strDynamicFilter in arrDynamicFilters:
        match strDynamicFilter:
            case 'Brand': filterByBrand(response, strCategoryId, strCategoryName)
            case 'Category': filterByCategory(response, strCategoryId, strCategoryName)
            case 'Age Group': filterByAgeGroup(response, strCategoryId, strCategoryName)
            case 'Gender': filterByGender(response, strCategoryId, strCategoryName)

def validateStaticFilters(response, strCategoryId, strCategoryName):
    """
    Objective: Validate Static filters
    
    Params: response | strCategoryId | strCategoryName
    Returns: None
    Author: cgrapa_20230803
    """
    arrStaticFilters = rProductListing.sf.getPlpStaticFilters(response)
    for strStatic in arrStaticFilters:
        match strStatic:
            case 'Discount': filterByDiscount(response, strCategoryId, strCategoryName)
            case 'Price': filterByPrice(response, strCategoryId, strCategoryName)
            case 'Color': filterByColor(response, strCategoryId, strCategoryName)

def validateSorting(strCategoryId, strCategoryName):
    """
    Objective: Validate PLP sorting
    
    Params: strCategoryId | strCategoryName
    Returns: None
    Author: cgrapa_20230803
    """
    sortByNewest(strCategoryId, strCategoryName)
    sortByPriceLowToHigh(strCategoryId, strCategoryName)
    sortByPriceHighToLow(strCategoryId, strCategoryName)
    sortByPopularity(strCategoryId, strCategoryName)
    sortByDiscountHighToLow(strCategoryId, strCategoryName)
    sortByLastUpdated(strCategoryId, strCategoryName)

def validateCategoriesPlp(dictCategory):
    """
    Objective: Validate PLP through Categories
    
    Params: dictCategory
    Returns: None
    Author: cgrapa_20230803
    """
    response = postTypesProducts(dPayload.plp.products(dictCategory["strCategoryId"]))
    validateDynamicFilters(response, dictCategory["strCategoryId"], dictCategory["strCategoryName"])
    validateStaticFilters(response, dictCategory["strCategoryId"], dictCategory["strCategoryName"])
    validateSorting(dictCategory["strCategoryId"], dictCategory["strCategoryName"])

def validateSearchResults(response, strSearchTerm, blnPhrase = False):
    """
    Objective: Validate PLP through search results
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Checking Results:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1))
        rProductListing.srv.validateSearchResults(response, strSearchTerm, blnPhrase)
        rProductListing.fv.detectDuplicateProductCards(response, f'Atlas Search: {strSearchTerm}')
    uCommon.printErrorCount('Atlas Search')

def sortByRelevance(strSearchTerm):
    """
    Objective: Sort and validate items by Relevance
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Relevance Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1))
        rProductListing.sv.validateSortingByRelevance(response, intPage + 1)
    uCommon.printErrorCount('Relevance Sorting')

def sortSearchByNewest(strSearchTerm):
    """
    Objective: Sort and validate items by Newest
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Newest Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 1))
        rProductListing.sv.validateSortingByNewest(response, intPage + 1)
    uCommon.printErrorCount('Newest Sorting')

def sortSearchByPriceLowToHigh(strSearchTerm):
    """
    Objective: Sort and validate items by Price - Low to High
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Price(L-H) Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 2))
        rProductListing.sv.validateSortingByPriceLowToHigh(response, intPage + 1)
    uCommon.printErrorCount('Price(Low to High) Sorting')

def sortSearchByPriceHighToLow(strSearchTerm):
    """
    Objective: Sort and validate items by Price - High to Low
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Price(H-L) Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 3))
        rProductListing.sv.validateSortingByPriceHighToLow(response, intPage + 1)
    uCommon.printErrorCount('Price(High to Low) Sorting')

def sortSearchByPopularity(strSearchTerm):
    """
    Objective: Sort and validate items by Popularity
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Popularity Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 4))
        rProductListing.sv.validateSortingByPopularity(response, intPage + 1)
    uCommon.printErrorCount('Popularity sorting')

def sortSearchByDiscountHighToLow(strSearchTerm):
    """
    Objective: Sort and validate items by Discount - High to Low
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Discount(H-L) Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 6))
        rProductListing.sv.validateSortingByDiscountHighToLow(response, intPage + 1)
    uCommon.printErrorCount('Discount(High to Low) Sorting')

def sortSearchByLastUpdated(strSearchTerm):
    """
    Objective: Sort and validate items by Last Updated
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in uCommon.progressBar(range(intPages), f'{strSearchTerm} | Last Updated Sorting:'):
        response = postTypesProducts(dPayload.plp.search(strSearchTerm, intPage + 1, 7))
        rProductListing.sv.validateSortingByLastUpdated(response, intPage + 1)
    uCommon.printErrorCount('Last Updated Sorting')

def validateSearchedBrands(response, strSearchTerm, strBrandId):
    """
    Objective: Validate searched items by Brand
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterSearchByBrand(strSearchTerm, strBrandId, intPage + 1))
        rProductListing.fv.validateBrandFilter(response, strBrandId)
        rProductListing.fv.detectDuplicateProductCards(response, f'Brand Filter: {strBrandId}')

def filterSearchByBrand(response, strSearchTerm):
    """
    Objective: Filter and validate searched items by Brand
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    arrOptions = rProductListing.df.getBrandFilterOptions(response)
    for strBrandOption in uCommon.progressBar(arrOptions, f'{strSearchTerm} | Brand Filter:'):
        strBrandId = strBrandOption["brandId"]
        response = postTypesProducts(dPayload.plp.filterSearchByBrand(strSearchTerm, strBrandId))
        validateSearchedBrands(response, strSearchTerm, strBrandId)
    uCommon.printErrorCount('Brand Filter')

def validateSearchedGender(response, strSearchTerm, strGenderId, strGenderName):
    """
    Objective: Validate searched items by Gender
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterSearchByGender(strSearchTerm, strGenderId, intPage + 1))
        rProductListing.fv.validateGenderFilter(response, strGenderName, strGenderId)
        rProductListing.fv.detectDuplicateProductCards(response, f'Gender Filter: {strGenderName}')

def filterSearchByGender(response, strSearchTerm):
    """
    Objective: Filter and validate searched items by Gender
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    arrOptions = rProductListing.df.getGenderFilterOptions(response)
    for strGenderOption in uCommon.progressBar(arrOptions, f'{strSearchTerm} | Gender Filter:'):
        strGenderName = strGenderOption["genderName"]
        strGenderId = strGenderOption["genderId"]
        response = postTypesProducts(dPayload.plp.filterSearchByGender(strSearchTerm, strGenderId))
        validateSearchedGender(response, strSearchTerm, strGenderId, strGenderName)
    uCommon.printErrorCount('Gender Filter')

def validateSearchedAgeGroup(response, strSearchTerm, strAgeGroupOption):
    """
    Objective: Validate searched items by Age Group
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterSearchByAgeGroup(strSearchTerm, strAgeGroupOption, intPage + 1))
        rProductListing.fv.validateAgeGroupFilter(response, strAgeGroupOption)
        rProductListing.fv.detectDuplicateProductCards(response, f'Age Group Filter: {strAgeGroupOption}')

def filterSearchByAgeGroup(response, strSearchTerm):
    """
    Objective: Filter and validate searched items by Age Group
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    arrOptions = rProductListing.df.getSearchAgeGroupFilterOptions(response)
    for strAgeGroupOption in uCommon.progressBar(arrOptions, f'{strSearchTerm} | Age Group Filter:'):
        response = postTypesProducts(dPayload.plp.filterSearchByAgeGroup(strSearchTerm, strAgeGroupOption))
        validateSearchedAgeGroup(response, strSearchTerm, strAgeGroupOption)
    uCommon.printErrorCount('Age Group Filter')

def validateColor(response, strCategoryId, strColorName):
    """
    Objective: Validate searched items by Color
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterSearchByColor(strCategoryId, strColorName, intPage + 1))
        rProductListing.fv.validateColorFilter(response, strColorName)
        rProductListing.fv.detectDuplicateProductCards(response, f'Color Filter: {strColorName}')

def filterSearchByColor(response, strSearchTerm):
    """
    Objective: Filter and validate searched items by Color
    
    Method: POST
    API Endpoint: /types/products
    Payload: searchInput | isMobile | search | page | limit | color | filter | sortby
    Author: cgrapa_20231123
    """
    arrOptions = rProductListing.sf.getColorFilterOptions(response)
    for strColorOption in uCommon.progressBar(arrOptions, f'{strSearchTerm} | Color Filter:'):
        strColorName = strColorOption["colorName"]
        response = postTypesProducts(dPayload.plp.filterSearchByColor(strSearchTerm, strColorName))
        validateColor(response, strSearchTerm, strColorName)
    uCommon.printErrorCount('Color Filter')

def validateFiltersSearchPlp(strSearchTerm):
    """
    Objective: Validate Dynamic filters
    
    Params: strSearchTerm
    Returns: None
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.searchLimit1(strSearchTerm))
    arrDynamicFilters = rProductListing.df.getPlpDynamicFilters(response)
    for strDynamicFilter in arrDynamicFilters:
        match strDynamicFilter:
            case 'Brand': filterSearchByBrand(response, strSearchTerm)
            case 'Gender': filterSearchByGender(response, strSearchTerm)
            case 'AgeGroup': filterSearchByAgeGroup(response, strSearchTerm)

def validateStaticFiltersSearchPlp(strSearchTerm):
    """
    Objective: Validate Static filters
    
    Params: strSearchTerm
    Returns: None
    Author: cgrapa_20231123
    """
    response = postTypesProducts(dPayload.plp.searchLimit1(strSearchTerm))
    arrStaticFilters = rProductListing.sf.getPlpStaticFilters(response)
    for strStaticFilter in arrStaticFilters:
        match strStaticFilter:
            case 'Color': filterSearchByColor(response, strSearchTerm)
            #case 'Price': ##### DISABLED ON ATLAS #####
            #case 'Discount': ##### DISABLED ON ATLAS #####

def validateSearchSorting(strSearchTerm):
    """
    Objective: Validate Search sorting
    
    Params: strSearchTerm
    Returns: None
    Author: cgrapa_20231123
    """
    sortByRelevance(strSearchTerm)
    sortSearchByDiscountHighToLow(strSearchTerm)
    sortSearchByLastUpdated(strSearchTerm)
    sortSearchByNewest(strSearchTerm)
    sortSearchByPopularity(strSearchTerm)
    sortSearchByPriceHighToLow(strSearchTerm)
    sortSearchByPriceLowToHigh(strSearchTerm)

def validateSearchPlp(strSearchTerm, blnCheckSorting = True, blnCheckFiltering = True):
    """
    Objective: Validate Search PLP
    
    Params: strSearchTerm | blnCheckSorting | blnCheckFiltering
    Returns: None
    Author: cgrapa_20231123
    """
    if strSearchTerm == "unilove":
        strSearchTerm = "uni-love"
    response = postTypesProducts(dPayload.plp.search(strSearchTerm))
    intWordCount = uCommon.splitPhraseToWords(strSearchTerm, True)
    if intWordCount == 1:
        validateSearchResults(response, strSearchTerm)
    else:
        validateSearchResults(response, strSearchTerm, True)
    if blnCheckSorting == True:
        validateSearchSorting(strSearchTerm)
    if blnCheckFiltering == True:
        validateFiltersSearchPlp(strSearchTerm)
        validateStaticFiltersSearchPlp(strSearchTerm)