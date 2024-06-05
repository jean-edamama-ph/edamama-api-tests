import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon

def addAddress(strAccessToken, strFname, strLname, strFullName, strPhoneNum, strRegionName, strRegionId, strCityName, strCityId, strCityRegionId, strZipCode, strBarangayName, strBarangayId,
                    strBarangayCityId, strLandmark, strBuildingNumber, strCountry, boolIsDefault):
    """
    Method: POST
    API Endpoint: /users/address
    Payload: strToken | strFname | strLname | strFullName | strPhoneNum | strRegionName | strRegionId | strCityName | strCityId | strCityRegionId | strZipCode | strBarangayName 
            | strBarangayId | strBarangayCityId | strLandmark | strBuildingNumber | strCountry | boolIsDefault               
    Author: jatregenio_20240605
    """
    
    response = uCommon.callPost(dUrl.prf.address, dHeaders.withToken(strAccessToken),dPayload.prf.userAddress(strFname, strLname, strFullName, strPhoneNum, strRegionName, strRegionId, strCityName, strCityId, strCityRegionId, strZipCode, strBarangayName, strBarangayId,
                    strBarangayCityId, strLandmark, strBuildingNumber, strCountry, boolIsDefault))
    return response