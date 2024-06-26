import libraries.data.headers as dHeaders
import libraries.data.params as dParams
import libraries.data.payload as dPayload
import libraries.data.testData as dTestData
import libraries.data.url as dUrl
import libraries.util.common as uCommon
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

def getSpotlightCuratedTypes():
    """
    Method: GET
    API Endpoint: /shop/curated-types?
    Params: forSpotlight
    Response Data: lName | title
    Author: cgrapa_20240220
    """
    response = uCommon.callGetAndValidateResponse(dUrl.plp.getCuratedTypes, dHeaders.withToken(), dParams.curatedTypesSpotlight, dHeaders.auth)
    return response

def postCuratedTypesProducts(strPayload):
    """
    Method: POST
    API Endpoint: /types/products
    Payload: page | sortby | filters | parentCategory | limit
    Author: cgrapa_20230713
    """
    response = uCommon.callPostAndValidateResponse(dUrl.plp.curatedTypesProducts, dHeaders.withToken(), strPayload, dHeaders.auth)  
    return response

def validatePrice(response, strId, intMin, intMax):
    """
    Objective: Validate Items by Price
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | minPrice | maxPrice | parentCategory
    Author: cgrapa_20230803
    """
    intPages = rProductListing.plp.calculatePlpPages(response)
    for intPage in range(intPages):
        response = postTypesProducts(dPayload.plp.filterCuratedByPrice(strId, intMin, intMax, intPage + 1))
        rProductListing.fv.validatePriceFilter(response, intMin, intMax)
        rProductListing.fv.detectDuplicateProductCards(response, f'Price Filter: {intMin} - {intMax}')

def filterByPrice(response, strId, strName, strSetMinMax = '', blnEnableIncrement = False):
    """
    Objective: Filter and validate items by Price
    
    Method: POST
    API Endpoint: /types/products
    Payload: limit | page | sortby | filters | minPrice | maxPrice | parentCategory
    Author: cgrapa_20230803
    """
    if blnEnableIncrement == True:
        intIncrementValue = dTestData.plp.intPriceFilterIncrement
    else:
        intIncrementValue = int(rProductListing.sf.getPriceFilterOptions(response))
    match strSetMinMax:
        case 'minOnly':
            intMin = dTestData.plp.intPriceFilterMin
            intBaseMaxPrice = int(rProductListing.sf.getPriceFilterOptions(response))
            intMax = intBaseMaxPrice
        case 'maxOnly':
            intMin = 0
            intMax = dTestData.plp.intPriceFilterMax
            intBaseMaxPrice = dTestData.plp.intPriceFilterMax
        case _:
            intMin = dTestData.plp.intPriceFilterMin
            intMax = dTestData.plp.intPriceFilterMax
            intBaseMaxPrice = intMax
    for intMin in uCommon.progressBar(range(intMin, intBaseMaxPrice, intIncrementValue), f'{strName} | Price Filter:'):
        intMax = intMin + intIncrementValue
        if intMax > intBaseMaxPrice:
            intMax = intBaseMaxPrice
        response = postTypesProducts(dPayload.plp.filterCuratedByPrice(strId, intMin, intMax))
        validatePrice(response, strId, intMin, intMax)
    uCommon.printErrorCount('Price Filter')

def validateStaticFilters(response, strId, strName):
    """
    Objective: Validate Static filters
    
    Params: response | strCategoryId | strCategoryName
    Returns: None
    Author: cgrapa_20230803
    """
    arrStaticFilters = rProductListing.sf.getPlpStaticFilters(response)
    for strStatic in arrStaticFilters:
        match strStatic:
            case 'Price': filterByPrice(response, strId, strName, 'minOnly')

def validateCuratedPlp():
    """
    Objective: Validate PLP through Curated Products
    
    Params: dictCategory
    Returns: None
    Author: cgrapa_20230803
    """
    response = getSpotlightCuratedTypes()
    arrCuratedTypes = rProductListing.cp.getCuratedLnameAndTitles(response)
    for dictCuratedType in arrCuratedTypes:
        response = postCuratedTypesProducts(dPayload.plp.curatedProducts(dictCuratedType["strCuratedLname"]))
        validateStaticFilters(response, dictCuratedType["strCuratedLname"], dictCuratedType["strCuratedTitle"])