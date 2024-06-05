from tqdm import tqdm
from libraries.util.response.productListing import errorLog
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import requests, allure, sys, pprint

import libraries.data.url as dUrl

strOS = 'windows'   # windows, mac

intErrorCount = 0

def getStatusCode(response):
    """
    Objective: Retrieve API status code
    
    Params: response
    Returns: response.status_code
    Author: cgrapa_20230803
    """
    return response.status_code

def getResponseData(response):
    """
    Objective: Get API response data
    
    Params: response
    Returns: responseData
    Author: cgrapa_20230803
    """
    responseData = response.json()
    return responseData

def callGet(strUrl, strHeaders, strParams = "", strAuth = ""):
    """
    Objective: GET API request
    
    Params: strUrl | strHeaders | strParams | strAuth
    Returns: response
    Author: cgrapa_20230803
    """
    response = requests.get(f'{dUrl.baseUrl}{strUrl}', headers=strHeaders, params=strParams, auth=strAuth)
    statusCode = getStatusCode(response)
    responseData = getResponseData(response)
    assert statusCode == 200, f'Get response failed with Status Code: {statusCode} | Message: {responseData["message"]}'
    return response

def callPost(strUrl, strHeaders, strPayload = "", strAuth = ""):
    """
    Objective: POST API request
    
    Params: strUrl | strHeaders | strParams | strAuth
    Returns: response
    Author: cgrapa_20230803
    """
    response = requests.post(f'{dUrl.baseUrl}{strUrl}', headers=strHeaders, json=strPayload, auth=strAuth)
    statusCode = getStatusCode(response)
    responseData = getResponseData(response)
    assert statusCode == 200, f'Post response failed with Status Code: {statusCode} | Message: {responseData["message"]}'

def callPostAndValidateResponse(strUrl, strHeaders = '', strPayload = '', strAuth = '', intRetries = 5):
    """
    Objective: POST API request and validate response code
    
    Params: strUrl | strHeaders | strPayload | strAuth
    Returns: response
    Author: cgrapa_20230803
    """
    for intRetry in range(intRetries):
        response = callPost(strUrl, strHeaders, strPayload, strAuth)
        statusCode = getStatusCode(response)
        if statusCode == 200:
            return response

def callGetAndValidateResponse(strUrl, strHeaders = '', strParams = '', strAuth = '', intRetries = 5):
    """
    Objective: GET API request and validate response code
    
    Params: strUrl | strHeaders | strParams | strAuth
    Returns: response
    Author: cgrapa_20230803
    """
    for intRetry in range(intRetries):
        response = callGet(strUrl, strHeaders, strParams, strAuth)
        statusCode = getStatusCode(response)
        if statusCode == 200:
            return response
    
def getArrayCount(strResponseData):
    """
    Objective: Get response data array count
    
    Params: strResponseData
    Returns: intArrayCount
    Author: cgrapa_20230803
    """
    intArrayCount = len(strResponseData)
    return intArrayCount

def detectDuplicates(arrData):
    """
    Objective: Detect duplicates in an array
    
    Params: arrData
    Returns: repeatedData
    Author: cgrapa_20230803
    """
    dictData = {}
    repeatedData = set()
    for data in arrData:
        if data in dictData:
            dictData[data] += 1
            repeatedData.add(data)
        else:
            dictData[data] = 1
    return repeatedData

def progressBar(strLength, strDescription):
    """
    Objective: Display terminal proggress bar
    
    Params: strLength | strDescription
    Returns: tqdm
    Author: cgrapa_20230803
    """
    return tqdm(strLength, desc=f'\033[1m{strDescription}\033[0m', unit="%", leave=True, bar_format="{desc:<60} {percentage:3.0f}%|{bar:18}| {n_fmt:>4}/{total_fmt:<4} [{elapsed}<{remaining}]")

def errorCounter():
    """
    Objective: Counts errors encountered during validation
    
    Params: None
    Returns: None
    Author: cgrapa_20230803
    """
    global intErrorCount
    intErrorCount += 1

def printErrorCount(strFunctionName):
    """
    Objective: Prints total errors encountered during validation
    
    Params: strFunctionName
    Returns: None
    Author: cgrapa_20230803
    """
    global intErrorCount
    if intErrorCount > 0:
        sys.stdout.write("\033[K")
        print("\033[1mErrors encountered: \033[31m", intErrorCount,"\n\033[0m")
        allure.attach("\n".join(errorLog), name=strFunctionName, attachment_type=allure.attachment_type.TEXT)
    else:
        sys.stdout.write("\033[K")
        print("\033[1mErrors encountered: \033[32m", intErrorCount,"\n\033[0m")
    intErrorCount = 0
    errorLog.clear()

def normalizeString(strWord):
    """
    Objective: Normalize a string
    
    Params: strWord
    Returns: strWord
    Author: cgrapa_20230803
    """
    replacements = {
        "&": "and"
    }
    for original, replacement in replacements.items():
        strWord = strWord.replace(original, replacement)
    return strWord

def validateText(strToCompare, strToCompareWith, strMsg = '', blnExact = True):
    """
    Objective: Compares 2 sets of strings
    
    Params: strToCompare | strToCompareWith | strMsg | blnExact
    Returns: None
    Author: cgrapa_20230803
    """
    if blnExact == True:
        assert normalizeString(strToCompare) == normalizeString(strToCompareWith), strMsg
    else:
        assert normalizeString(strToCompare.casefold()) == normalizeString(strToCompareWith.casefold()), strMsg
        
def findTextInArray(strToFind, arrData, strMsg = '', blnExact = True):
    """
    Objective: Finds a text in an Array
    
    Params: strToFind | arrData | strMsg | blnExact
    Returns: None
    Author: cgrapa_20230803
    """
    if blnExact == True:
        arrNormalizedData = [normalizeString(item) for item in arrData]
        assert normalizeString(strToFind) in arrNormalizedData, strMsg
    else:
        arrCasefoldedData = [item.casefold() for item in arrData]
        arrNormalizedCasefoldedData = [normalizeString(item) for item in arrCasefoldedData]
        assert normalizeString(strToFind.casefold()) in arrNormalizedCasefoldedData, strMsg
        
def sortArray(arrItems, blnReverse = False):
    """
    Objective: Sorts data in an Array
    
    Params: arrItems | blnReverse
    Returns: arrSortedItems
    Author: cgrapa_20230803
    """
    arrSortedItems = sorted(arrItems, reverse = blnReverse)
    return arrSortedItems

def joinArray(arrCollection):
    """
    Objective: Join an arrCollection - Removes '[]' when printing arrays
    
    Params: arrCollection
    Returns: arrCollection
    Author: cgrapa_20230803
    """
    return ', '.join(map(str, arrCollection))

def cleanPunctuations(strPhrase):
    """
    Objective: Clear Special Characters and Punctuations
    
    Params: strPhrase
    Returns: arrWords
    Author: cgrapa_20231123
    """
    strPunctuations = '''!()[]{};:"\\,<>./?@#$%^&*_~'''
    for strPunctuation in strPunctuations:
        strPhrase = strPhrase.replace(strPunctuation, ' ')
    return strPhrase

def splitPhraseToWords(strPhrase, blnCountWords = False):
    """
    Objective: Splits phrases to words
    
    Params: strPhrase | blnCountWords
    Returns: arrWords | len(arrWords)
    Author: cgrapa_20231123
    """
    if blnCountWords == False:
        arrWords = strPhrase.split()
        return arrWords
    else:
        arrWords = strPhrase.split()
        return len(arrWords)

def countCharacterChange(strCompareWith, strCompareTo):
    """
    Objective: Counts the number characters changed in a word
    
    Params: strCompareWith | strCompareTo
    Returns: count
    Author: cgrapa_20231123
    """
    count = 0
    for charCompareWith, charCompareTo in zip(strCompareWith, strCompareTo):
        if charCompareWith != charCompareTo:
            count += 1
    return count

def prettyPrint(dictData):
    return pprint.pprint(dictData)

def generateMongoDbConnectionString(strFilePath,strConnectionStringScheme):
    strPemFilePath = strFilePath.replace('\\', '%5C').replace(':', '%3A').replace(' ', '+')
        
    strConnectionString = (
        f"mongodb+srv://{strConnectionStringScheme}"
        "?authMechanism=MONGODB-X509"
        f"&tlsCertificateKeyFile={strPemFilePath}"
        "&authSource=%24external"
    )
    return strConnectionString