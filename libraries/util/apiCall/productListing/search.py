import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.payload as dPayload
import libraries.data.testData as dTestData
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