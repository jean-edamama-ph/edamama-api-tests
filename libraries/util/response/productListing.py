import math

import libraries.util.common as uCommon
import libraries.data.testData as dTestData

errorLog = []

class plp:
    """PRODUCT LISTING PAGE"""
    
    def calculatePlpPages(response):
        """
        Objective: Calculate PLP pages
        
        Params: response
        Returns: intPages
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        intTotalCount = responseData["data"]["totalCount"]
        intPages = math.ceil(intTotalCount / 100)
        return intPages





class df:
    """DYNAMIC FILTERS"""
    
    def getPlpDynamicFilters(response):
        """
        Objective: Get PLP dynamic filters
        
        Params: response
        Returns: arrFilters
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = []
        for strFilterName in responseData["data"]["filters"]:
            arrFilters.append(strFilterName["name"])
        return arrFilters
    
    def getBrandFilterOptions(response):
        """
        Objective: Get Brand filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = df.getPlpDynamicFilters(response)
        arrOptions = []
        for strOption in (responseData["data"]["filters"][arrFilters.index('Brand')])["options"]:
            dictData = {"brandName" : strOption["name"], "brandId": strOption["_id"]}
            arrOptions.append(dictData)
        return arrOptions
    
    def getAgeGroupFilterOptions(response):
        """
        Objective: Get Age Group filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = df.getPlpDynamicFilters(response)
        arrOptions = []
        for strOption in (responseData["data"]["filters"][arrFilters.index('Age Group')])["options"]:
            arrOptions.append(strOption["_id"])
        return arrOptions
    
    def getSearchAgeGroupFilterOptions(response):
        """
        Objective: Get Age Group filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = df.getPlpDynamicFilters(response)
        arrOptions = []
        for strOption in (responseData["data"]["filters"][arrFilters.index('AgeGroup')])["options"]:
            arrOptions.append(strOption["_id"])
        return arrOptions
    
    def getGenderFilterOptions(response):
        """
        Objective: Get Gender filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = df.getPlpDynamicFilters(response)
        arrOptions = []
        for strOption in (responseData["data"]["filters"][arrFilters.index('Gender')])["options"]:
            dictData = {"genderName" : strOption["name"], "genderId": strOption["_id"]}
            arrOptions.append(dictData)
        return arrOptions
    
    def getCategoryFilterOptions(response):
        """
        Objective: Get Category filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = df.getPlpDynamicFilters(response)
        arrOptions = []
        for strOption in (responseData["data"]["filters"][arrFilters.index('Category')])["options"]:
            dictData = {"categoryName" : strOption["name"], "categoryId": strOption["_id"]}
            arrOptions.append(dictData)
        return arrOptions




class sf:
    """STATIC FILTERS"""
    
    def getPlpStaticFilters(response):
        """
        Objective: Get PLP static filters
        
        Params: response
        Returns: arrFilters
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrFilters = []
        for strFilterName in responseData["data"]["staticFilters"]:
            arrFilters.append(strFilterName["name"])
        return arrFilters

    def getPriceFilterOptions(response):
        """
        Objective: Get Price filter options
        
        Params: response
        Returns: intMax
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        intMax = ((responseData["data"])["priceInfo"])["max"]
        return intMax

    def getColorFilterOptions(response):
        """
        Objective: Get Color filter options
        
        Params: response
        Returns: arrOptions
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrOptions = []
        for strOption in (responseData["data"]["staticFilters"][2])["options"]:
            dictData = {"colorName": strOption["name"], "colorId": strOption["_id"]}
            arrOptions.append(dictData)
        return arrOptions





class fv:
    """FILTER VALIDATION"""
    
    def validateBrandFilter(response, strBrandName):
        """
        Objective: Validate items by using Brand filter
        
        Params: response | strBrandName
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            try:
                strItemBrandName = (strItem["brand"])["name"]
                uCommon.validateText(strItemBrandName, strBrandName, f'Item "{strItemName}" with Brand "{strItemBrandName}" found on applied Brand filter: {strBrandName}', False)
            except AssertionError as strError:
                errorLog.append(f'\n[BRAND FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateAgeGroupFilter(response, strAgeGroupOption):
        """
        Objective: Validate items by using Age Group filter
        
        Params: response | strAgeGroupOption
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            arrAgeGroupOptions = strItem["ageGroup"]
            try:
                if arrAgeGroupOptions == []:
                    raise KeyError
                else:
                    uCommon.findTextInArray(strAgeGroupOption, arrAgeGroupOptions, f'Item "{strItemName}" belonging to Age Group "{uCommon.joinArray(arrAgeGroupOptions)}" found on applied Age Group filter: {strAgeGroupOption}')
            except AssertionError as strError:
                errorLog.append(f'\n[AGE GROUP FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
            except KeyError:
                errorLog.append(f'\n[API] ISSUE: Item "{strItemName}" does not have any Age Group Option but appeared on applied Age Group filter: {strAgeGroupOption}')
                uCommon.errorCounter()

    def validateColorFilter(response, strColorName):
        """
        Objective: Validate items by using Color filter
        
        Params: response | strColorName
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            arrItemColorNames = []
            try:
                for strItemColorName in strItem["color"]:
                    arrItemColorNames.append(strItemColorName["name"])
                uCommon.findTextInArray(strColorName, arrItemColorNames, f'Item "{strItemName}" with Colors "{uCommon.joinArray(arrItemColorNames)}" found on applied Color filter: {strColorName}', False)
            except AssertionError as strError:
                errorLog.append(f'\n[COLOR FILTER] ISSUE: {strError}')
                uCommon.errorCounter()

    def validatePriceFilter(response, intMin, intMax):
        """
        Objective: Validate items by using Price filter
        
        Params: response | intMin | intMax
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            try:
                intItemPrice = (strItem["productDisplay"][0])["finalDiscountedPrice"]
                assert intItemPrice >= intMin and intItemPrice <= intMax, f'Item "{strItemName}" with Price "₱{intItemPrice}" found on applied Price Filter: ₱{intMin} - ₱{intMax}'
            except AssertionError as strError:
                errorLog.append(f'\n[PRICE FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateDiscountFilter(response, intMinDiscount, intMaxDiscount):
        """
        Objective: Validate items by using Discount filter
        
        Params: response | intMinDiscount | intMaxDiscount
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            try:
                intItemDiscountPercentage = strItem["maxDiscountPercentage"]
                assert intItemDiscountPercentage >= intMinDiscount and intItemDiscountPercentage <= intMaxDiscount, f'Item "{strItemName}" should not be displayed in Discount Range Filter: {intMinDiscount}%-{intMaxDiscount}%'
            except AssertionError as strError:
                errorLog.append(f'\n[DISCOUNT FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateGenderFilter(response, strGenderName, strGenderId):
        """
        Objective: Validate items by using Gender filter
        
        Params: response | strGenderName | strGenderId
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            try:
                strItemGenderId = strItem["gender"]
                match strItemGenderId:
                    case '1': strItemGenderName = 'Boy'
                    case '2': strItemGenderName = 'Girl'
                    case '3': strItemGenderName = 'Unisex'
                    case '4': strItemGenderName = 'N/A'
                uCommon.validateText(strGenderId, strItemGenderId, f'Item "{strItemName}" with "{strItemGenderName}" found on applied Gender filter: {strGenderName}')
            except AssertionError as strError:
                errorLog.append(f'\n[GENDER FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
            except KeyError:
                errorLog.append(f'\n[API] ISSUE: Item "{strItemName}" is not assigned to a Gender Category but appeared on applied Gender filter: {strGenderName}')
                uCommon.errorCounter()
    
    def validateCategoryFilter(response, strFilterCategoryId, strFilterCategoryName):
        """
        Objective: Validate items by using Category filter
        
        Params: response | strFilterCategoryId | strFilterCategoryName
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        for strItem in arrItems:
            strItemName = strItem["name"]
            arrCategories = strItem["category"]
            try:
                arrCategoryIds = []
                arrCategoryNames = []
                for strCategory in arrCategories:
                    arrCategoryIds.append(strCategory["_id"])
                    arrCategoryIds.append(strCategory["parentId"])
                    arrCategoryNames.append(strCategory["name"])
                uCommon.findTextInArray(strFilterCategoryId, arrCategoryIds, f'Item "{strItemName}" belonging to "{uCommon.joinArray(arrCategoryNames)}" found on applied Category filter: {strFilterCategoryName}')
            except AssertionError as strError:
                errorLog.append(f'\n[CATEGORY FILTER] ISSUE: {strError}')
                uCommon.errorCounter()
                    
    def detectDuplicateProductCards(response, strFilterName):
        """
        Objective: Detect PLP duplicate product cards
        
        Params: response | strFilterName
        Returns: None
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrItemName = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            try:
                if intItemQuantity > 0:
                    arrItemName.append(strItemName)
            except TypeError:
                errorLog.append(f'\n[API] ISSUE: Item "{strItemName}" returned NULL quantity while filtering by {strFilterName}')
                uCommon.errorCounter()
        dictRepeatedCards = uCommon.detectDuplicates(arrItemName)
        if uCommon.getArrayCount(dictRepeatedCards) > 0:
            for strRepeatedCard in dictRepeatedCards:
                try:
                    assert 1 == 0, f'Item "{strRepeatedCard}" has a duplicate product card while filtering by {strFilterName}'
                except AssertionError as strError:
                    errorLog.append(f'\n[PRODUCT CARDS] DUPLICATE DETECTED: {strError}')
                    uCommon.errorCounter()





class sr:
    """SORTING"""
    
    def getCreationDates(response):
        """
        Objective: Get item Creation Dates
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrCreationDates = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            strItemCreationDate = strItem["createdAt"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrCreationDates.append(strItemCreationDate)
                arrItemNames.append(strItemName)
        dictData = {"arrCreationDates": arrCreationDates, "arrItemNames": arrItemNames}
        return dictData
    
    def getPricesLowToHigh(response):
        """
        Objective: Get item Prices from Low to High
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrPrices = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            intItemPrice = (strItem["productDisplay"][0])["finalDiscountedPrice"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrPrices.append(intItemPrice)
                arrItemNames.append(strItemName)
        dictData = {"arrPrices": arrPrices, "arrItemNames": arrItemNames}
        return dictData

    def getPricesHighToLow(response):
        """
        Objective: Get item Prices from High to Low
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrPrices = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            intItemPrice = (strItem["productDisplay"][0])["finalDiscountedPrice"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrPrices.append(intItemPrice)
                arrItemNames.append(strItemName)
        dictData = {"arrPrices": arrPrices, "arrItemNames": arrItemNames}
        return dictData
    
    def getNumberOfOrders(response):
        """
        Objective: Get item Number of Orders
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrNumberOfOrders = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            intItemNumberOfOrders = strItem["noOfOrders"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrNumberOfOrders.append(intItemNumberOfOrders)
                arrItemNames.append(strItemName)
        dictData = {"arrNumberOfOrders": arrNumberOfOrders, "arrItemNames": arrItemNames}
        return dictData
    
    def getDiscounts(response):
        """
        Objective: Get item Discounts
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrDiscounts = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            intItemDiscount = (strItem["productDisplay"][0])["discountPercentage"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrDiscounts.append(intItemDiscount)
                arrItemNames.append(strItemName)
        dictData = {"arrDiscounts": arrDiscounts, "arrItemNames": arrItemNames}
        return dictData
    
    def getModificationDates(response):
        """
        Objective: Get item Modification Dates
        
        Params: response
        Returns: dictData
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrModifiedDates = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            strModifiedDate = strItem["lastModifiedAt"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrModifiedDates.append(strModifiedDate)
                arrItemNames.append(strItemName)
        dictData = {"arrModifiedDates": arrModifiedDates, "arrItemNames": arrItemNames}
        return dictData
    
    def getSearchScore(response):
        """
        Objective: Get item Search Scores
        
        Params: response
        Returns: None
        Author: cgrapa_20231123
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrSearchScores = []
        arrItemNames = []
        for strItem in arrItems:
            strItemName = strItem["name"]
            strItemScore = strItem["score"]
            intItemQuantity = (strItem["productDisplay"][0])["quantity"]
            if intItemQuantity > 0:
                arrSearchScores.append(strItemScore)
                arrItemNames.append(strItemName)
        dictData = {"arrSearchScores": arrSearchScores, "arrItemNames": arrItemNames}
        return dictData




class sv:
    """SORTING VALIDATION"""
    
    def validateSortingByNewest(response, intPage):
        """
        Objective: Validate item sorting by Newest
        
        Params: response
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getCreationDates(response)
        arrCreationDates = dictData["arrCreationDates"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedCreationDates = uCommon.sortArray(arrCreationDates, True)
        for intIndex, strCreationDate in enumerate(arrCreationDates):
            try:
                intCorrectRank = arrSortedCreationDates.index(strCreationDate) + 1
                intIncorrectRank = intIndex + 1
                assert strCreationDate == arrSortedCreationDates[intIndex], f'Item "{arrItemNames[intIndex]}" with Creation Date "{strCreationDate}" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[NEWEST SORTING] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateSortingByPriceLowToHigh(response, intPage):
        """
        Objective: Validate item sorting by Price - Low to High
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getPricesLowToHigh(response)
        arrPrices = dictData["arrPrices"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedPrices = uCommon.sortArray(arrPrices)
        for intIndex, intPrice in enumerate(arrPrices):
            try:
                intCorrectRank = arrSortedPrices.index(intPrice) + 1
                intIncorrectRank = intIndex + 1
                assert intPrice == arrSortedPrices[intIndex], f'Item "{arrItemNames[intIndex]}" with Price "₱{intPrice}" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[PRICE(L-H) SORTING] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateSortingByPriceHighToLow(response, intPage):
        """
        Objective: Validate item sorting by Price - High to Low
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getPricesHighToLow(response)
        arrPrices = dictData["arrPrices"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedPrices = uCommon.sortArray(arrPrices, True)
        for intIndex, intPrice in enumerate(arrPrices):
            try:
                intCorrectRank = arrSortedPrices.index(intPrice) + 1
                intIncorrectRank = intIndex + 1
                assert intPrice == arrSortedPrices[intIndex], f'Item "{arrItemNames[intIndex]}" with Price "₱{intPrice}" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[PRICE(H-L) SORTING] ISSUE: {strError}')
                uCommon.errorCounter()

    def validateSortingByPopularity(response, intPage):
        """
        Objective: Validate item sorting by Popularity
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getNumberOfOrders(response)
        arrNumberOfOrders = dictData["arrNumberOfOrders"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedNumberOfOrders = uCommon.sortArray(arrNumberOfOrders, True)
        for intIndex, intNumberOfOrders in enumerate(arrNumberOfOrders):
            try:
                intCorrectRank = arrSortedNumberOfOrders.index(intNumberOfOrders) + 1
                intIncorrectRank = intIndex + 1
                assert intNumberOfOrders == arrSortedNumberOfOrders[intIndex], f'Item "{arrItemNames[intIndex]}" with "{intNumberOfOrders} Orders" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[POPULARITY SORTING] ISSUE: {strError}')
                uCommon.errorCounter()

    def validateSortingByDiscountHighToLow(response, intPage):
        """
        Objective: Validate item sorting by Discount - High to Low
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getDiscounts(response)
        arrDiscounts = dictData["arrDiscounts"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedDiscounts = uCommon.sortArray(arrDiscounts, True)
        for intIndex, intDiscount in enumerate(arrDiscounts):
            try:
                intCorrectRank = arrSortedDiscounts.index(intDiscount) + 1
                intIncorrectRank = intIndex + 1
                assert intDiscount == arrSortedDiscounts[intIndex], f'Item "{arrItemNames[intIndex]}" with Discount "{intDiscount}%" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[DISCOUNT(H-L) SORTING] ISSUE: {strError}')
                uCommon.errorCounter()

    def validateSortingByLastUpdated(response, intPage):
        """
        Objective: Validate item sorting by Last Updated
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getModificationDates(response)
        arrModifiedDates = dictData["arrModifiedDates"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedModifiedDates = uCommon.sortArray(arrModifiedDates, True)
        for intIndex, strModifiedDate in enumerate(arrSortedModifiedDates):
            try:
                intCorrectRank = arrSortedModifiedDates.index(strModifiedDate) + 1
                intIncorrectRank = intIndex + 1
                assert strModifiedDate == arrSortedModifiedDates[intIndex], f'Item "{arrItemNames[intIndex]}" with Modification Date "{strModifiedDate}" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[LAST UPDATED SORTING] ISSUE: {strError}')
                uCommon.errorCounter()
    
    def validateSortingByRelevance(response, intPage):
        """
        Objective: Validate item sorting by Last Updated
        
        Params: response | intPage
        Returns: None
        Author: cgrapa_20230803
        """
        dictData = sr.getSearchScore(response)
        arrSearchScores = dictData["arrSearchScores"]
        arrItemNames = dictData["arrItemNames"]
        arrSortedSearchScores = uCommon.sortArray(arrSearchScores)
        for intIndex, strModifiedDate in enumerate(arrSortedSearchScores):
            try:
                intCorrectRank = arrSortedSearchScores.index(strModifiedDate) + 1
                intIncorrectRank = intIndex + 1
                assert strModifiedDate == arrSortedSearchScores[intIndex], f'Item "{arrItemNames[intIndex]}" with Search Score: "{strModifiedDate}" should be in rank {intCorrectRank} instead of {intIncorrectRank} | Page: {intPage}'
            except AssertionError as strError:
                errorLog.append(f'\n[LAST UPDATED SORTING] ISSUE: {strError}')
                uCommon.errorCounter()





class src:
    """SEARCH"""
    
    def getSearchResults(response):
        """
        Objective: Compile Search Result Attributes
        
        Params: response
        Returns: arrItemNames
        Author: cgrapa_20231123
        """
        responseData = uCommon.getResponseData(response)
        arrItems = (responseData["data"])["products"]
        arrItemNames = []
        for strItem in arrItems:
            arrColors = []
            strItemName = strItem["name"]
            strBrandName = (strItem["brand"])["name"]
            strCategoryName = (strItem["category"][0])["name"]
            for strColor in strItem["color"]:
                arrColors.append(strColor["name"])
            strDescription = strItem["description"]
            dictData = {"strItemName": strItemName, "strBrandName": strBrandName, "strCategoryName": strCategoryName, "arrColors": arrColors, "strDescription": strDescription}
            arrItemNames.append(dictData)
        return arrItemNames





class srv:
    """SEARCH RESULTS VALIDATION"""
    
    def validateSearchTermInAttributes(strAttributeValue, strSearchTerm, blnPhrase = False):
        """
        Objective: Compile Search Result Attributes
        
        Params: response
        Returns: boolean
        Author: cgrapa_20230803
        """
        if blnPhrase == False:
            strCleanAttributeValue = uCommon.cleanPunctuations(strAttributeValue)
            arrAttributeValue = uCommon.splitPhraseToWords(strCleanAttributeValue)
            if strSearchTerm.casefold() not in [strValue.casefold() for strValue in arrAttributeValue]:
                return False
            else:
                return True
        else:
            arrSearchTermWords = uCommon.splitPhraseToWords(strSearchTerm)
            blnExists = any(strSearchTermWord.casefold() in strAttributeValue.casefold() for strSearchTermWord in arrSearchTermWords)
            if blnExists == False:
                return False
            else:
                return True

    def validateSearchTermInColors(arrColors, strSearchTerm, blnPhrase = False):
        """
        Objective: Validate if PLP items contains the search term in every color
        
        Params: arrColors | strSearchTerm | blnPhrase
        Returns: None
        Author: cgrapa_20231123
        """
        blnInColorName = False
        for strColorName in arrColors:
            if blnPhrase == False:
                blnInColors = srv.validateSearchTermInAttributes(strColorName, strSearchTerm)
            else:
                blnInColors = srv.validateSearchTermInAttributes(strColorName, strSearchTerm, blnPhrase)
            if blnInColors == True:
                blnInColorName = blnInColors
                break
        return blnInColorName
    
    def validateItems(strItem, strSearchTerm, blnPhrase = False):
        """
        Objective: Validate if PLP items contains the search term
        
        Params: strItem | strSearchTerm | blnPhrase
        Returns: None
        Author: cgrapa_20231123
        """
        strItemName = strItem["strItemName"]
        strBrandName = strItem["strBrandName"]
        strCategoryName = strItem["strCategoryName"]
        strDescription = strItem["strDescription"]
        arrColors = strItem["arrColors"]
        if blnPhrase == False:
            blnInItemName = srv.validateSearchTermInAttributes(strItemName, strSearchTerm)
            blnInBrandName = srv.validateSearchTermInAttributes(strBrandName, strSearchTerm)
            blnInCategoryName = srv.validateSearchTermInAttributes(strCategoryName, strSearchTerm)
            blnInDescription = srv.validateSearchTermInAttributes(strDescription, strSearchTerm)
            blnInColorName = srv.validateSearchTermInColors(arrColors, strSearchTerm)
        else:
            blnInItemName = srv.validateSearchTermInAttributes(strItemName, strSearchTerm, blnPhrase)
            blnInBrandName = srv.validateSearchTermInAttributes(strBrandName, strSearchTerm, blnPhrase)
            blnInCategoryName = srv.validateSearchTermInAttributes(strCategoryName, strSearchTerm, blnPhrase)
            blnInDescription = srv.validateSearchTermInAttributes(strDescription, strSearchTerm, blnPhrase)
            blnInColorName = srv.validateSearchTermInColors(arrColors, strSearchTerm, blnPhrase)
        arrHits = [blnInItemName, blnInBrandName, blnInCategoryName, blnInColorName, blnInDescription]
        return any(blnHits == True for blnHits in arrHits)
    
    def validateCharacterChangeCondition(strSearchTerm):
        intSearchTermCharacterCount = uCommon.getArrayCount(strSearchTerm)
        if intSearchTermCharacterCount >= 8 and intSearchTermCharacterCount <= 29:
            return 1
        elif intSearchTermCharacterCount > 29:
            return 2
        else:
            return 0
    
    def validateTypoApplied(strSearchTerm, strAttributeWord):
        """
        Objective: Validate if typo is applied
        
        Params: strSearchTerm | strAttributeWord
        Returns: None
        Author: cgrapa_20231123
        """
        intAllowedCharacterChange = srv.validateCharacterChangeCondition(strSearchTerm)
        intAddedSubtractedCharacter = abs(len(strSearchTerm) - len(strAttributeWord))
        strAttributeLower = strAttributeWord.lower()
        intCount = intAddedSubtractedCharacter
        if strAttributeLower.startswith(strSearchTerm[0]) and len(strSearchTerm) == len(strAttributeWord):
            for index in range(len(strSearchTerm)):
                if strSearchTerm[index] != strAttributeLower[index]:
                    intCount +=1
        elif strAttributeLower.startswith(strSearchTerm[0]) and intAllowedCharacterChange == intAddedSubtractedCharacter:
            intMinLength = min(len(strSearchTerm), len(strAttributeLower))
            for index in range(intMinLength):
                if strSearchTerm[index] != strAttributeLower[index]:
                    intCount += 1
        if intCount <= intAllowedCharacterChange:
            return True
        else:
            return False

    def validateTypoConditions(strAttributeValue, strSearchTerm, blnPhrase = False):
        """
        Objective: Validate typo conditions
        
        Params: strAttributeValue | strSearchTerm | blnPhrase
        Returns: None
        Author: cgrapa_20231123
        """
        strCleanValue = uCommon.cleanPunctuations(strAttributeValue)
        arrItemWords = uCommon.splitPhraseToWords(strCleanValue)
        blnTypoApplied = False
        if blnPhrase == False:
            for strItemWord in arrItemWords:
                blnTypoHit = srv.validateTypoApplied(strSearchTerm, strItemWord)
                if blnTypoHit == True:
                    blnTypoApplied = True
                    break
            return blnTypoApplied
        else:
            arrSearchTermWords = uCommon.splitPhraseToWords(strSearchTerm)
            arrPhraseHits = []
            for strSearchTermWord in arrSearchTermWords:
                for strItemWord in arrItemWords:
                    blnTypoHit = srv.validateTypoApplied(strSearchTermWord, strItemWord)
                    if blnTypoHit == True:
                        blnTypoApplied = True
                        arrPhraseHits.append(blnTypoApplied)
            return any(blnHits == True for blnHits in arrPhraseHits)
    
    def validateColorsTypoConditions(arrColors, strSearchTerm):
        """
        Objective: Validate attributes through Typo - Color Attribute
        
        Params: arrColors | strSearchTerm
        Returns: None
        Author: cgrapa_20231123
        """
        for strColorName in arrColors:
            strCleanName = uCommon.cleanPunctuations(strColorName)
            arrItemWords = uCommon.splitPhraseToWords(strCleanName)
            blnTypoApplied = False
            for strItemWord in arrItemWords:
                strItemWordLower = strItemWord.lower()
                if len(strItemWord) == len(strSearchTerm) and strItemWordLower.startswith(strSearchTerm[0]):
                    blnTypoApplied = True
                    break                
        return blnTypoApplied
    
    def validateTypo(strItem, strSearchTerm, blnPhrase = False):
        """
        Objective: Validate attributes through Typo
        
        Params: strItem | strSearchTerm | blnPhrase
        Returns: None
        Author: cgrapa_20231123
        """
        strItemName = strItem["strItemName"]
        strBrandName = strItem["strBrandName"]
        strCategoryName = strItem["strCategoryName"]
        arrColors = strItem["arrColors"]
        if blnPhrase == False:
            blnTypoInNameApplied = srv.validateTypoConditions(strItemName, strSearchTerm)
            blnTypoInBrandNameApplied = srv.validateTypoConditions(strBrandName, strSearchTerm)
            blnTypoInCategoryNameApplied = srv.validateTypoConditions(strCategoryName, strSearchTerm)
            blnTypoInColorNameApplied = srv.validateColorsTypoConditions(arrColors, strSearchTerm)
        else:
            blnTypoInNameApplied = srv.validateTypoConditions(strItemName, strSearchTerm, blnPhrase)
            blnTypoInBrandNameApplied = srv.validateTypoConditions(strBrandName, strSearchTerm, blnPhrase)
            blnTypoInCategoryNameApplied = srv.validateTypoConditions(strCategoryName, strSearchTerm, blnPhrase)
            blnTypoInColorNameApplied = srv.validateColorsTypoConditions(arrColors, strSearchTerm)
        arrHits = [blnTypoInNameApplied, blnTypoInBrandNameApplied, blnTypoInCategoryNameApplied, blnTypoInColorNameApplied]
        return any(blnHits == True for blnHits in arrHits)
    
    def validateOneWaySynonymMatch(strItem, arrSynonyms):
        """
        Objective: Validate attributes through One Way Synonym Match
        
        Params: strSearchTerm
        Returns: None
        Author: cgrapa_20231123
        """
        arrItemWords = uCommon.splitPhraseToWords(strItem)
        blnSynonymMatch = False
        for strItemWord in arrItemWords:
            if strItemWord in arrSynonyms:
                blnSynonymMatch = True
        return blnSynonymMatch
    
    def getSynonymSetIndex(strSearchTerm):
        """
        Objective: Get synonym index from Two Way Synonym Set of words
        
        Params: strSearchTerm
        Returns: None
        Author: cgrapa_20231123
        """
        arrSynonymSets = dTestData.plp.src.synonym
        for arrSynonymSet in arrSynonymSets:
            for key, values in arrSynonymSet.items():
                if strSearchTerm.lower() in values:
                    strSetNumber = key
                else:
                    strSetNumber = None
        return strSetNumber
        
    def validateTwoWaySynonymMatch(strItem, strSearchTerm):
        """
        Objective: Validate attributes through Two Way Synonym Match
        
        Params: strItem | strSearchTerm
        Returns: None
        Author: cgrapa_20231123
        """
        strCleanValue = uCommon.cleanPunctuations(strItem)
        arrItemWords = uCommon.splitPhraseToWords(strCleanValue)
        strKey = srv.getSynonymSetIndex(strSearchTerm)
        arrSynonymSets = dTestData.plp.src.synonym
        blnSynonymMatch = False
        if strKey is not None:
            for strItemWord in arrItemWords:
                if strItemWord.lower() in arrSynonymSets[0][strKey]:
                    blnSynonymMatch = True
                    break
            return blnSynonymMatch
        else:
            return blnSynonymMatch
    
    def validateSynonyms(strItem, strSearchTerm, blnPhrase):
        """
        Objective: Validate attributes through Synonyms
        
        Params: strItem | strSearchTerm
        Returns: None
        Author: cgrapa_20231123
        """
        strItemName = strItem["strItemName"]
        strBrandName = strItem["strBrandName"]
        strCategoryName = strItem["strCategoryName"]
        arrOneWaySynonyms = dTestData.plp.src.oneWaySynonyms
        for strOneWaySynonym in arrOneWaySynonyms:
            if strOneWaySynonym["input"] == strSearchTerm:
                arrSynonyms = strOneWaySynonym["synonyms"]
                break
            else:
                arrSynonyms = []
        if arrSynonyms != []:
            blnItemNameMatch = srv.validateOneWaySynonymMatch(strItemName, arrSynonyms)
            blnBrandNameMatch = srv.validateOneWaySynonymMatch(strBrandName, arrSynonyms)
            blnCategoryNameMatch = srv.validateOneWaySynonymMatch(strCategoryName, arrSynonyms)
        else:
            blnItemNameMatch = srv.validateTwoWaySynonymMatch(strItemName, strSearchTerm)
            blnBrandNameMatch = srv.validateTwoWaySynonymMatch(strBrandName, strSearchTerm)
            blnCategoryNameMatch = srv.validateTwoWaySynonymMatch(strCategoryName, strSearchTerm)
        arrHits = [blnItemNameMatch, blnBrandNameMatch, blnCategoryNameMatch]
        return any(blnHits == True for blnHits in arrHits)
    
    def validateSearchResults(response, strSearchTerm, blnPhrase = False):
        """
        Objective: Validate Search Result Attributes
        
        Params: response | strSearchTerm | blnPhrase
        Returns: None
        Author: cgrapa_20231123
        """
        arrItems = src.getSearchResults(response)
        for strItem in arrItems:
            blnHits = srv.validateItems(strItem, strSearchTerm, blnPhrase)
            blnSynonymHits = srv.validateSynonyms(strItem, strSearchTerm, blnPhrase)
            blnTypoHits = srv.validateTypo(strItem, strSearchTerm, blnPhrase)
            arrHits = [blnHits, blnSynonymHits, blnTypoHits]
            blnNoHits = any(blnHits == True for blnHits in arrHits)
            try:
                assert blnNoHits == True, f'"{strItem["strItemName"]}" does not adhere to any search Algorithm (Keyword/Phrase: {blnHits} | Synonym: {blnSynonymHits} | Typo: {blnTypoHits}) | Search Term: "{strSearchTerm}"'
            except AssertionError as strError:
                errorLog.append(f'\n[SEARCH RESULTS] ISSUE: {strError}')
                uCommon.errorCounter()