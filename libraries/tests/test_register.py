import pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.signUp.manualSignUp as apiManualSignUp
import libraries.util.apiCall.profile.address as apiProfAddress


@pytest.mark.api()
def test_001_sign_up_success():
    apiManualSignUp.postAndVerifyUserSignUpViaEmail(dTestData.rsg.strEmail, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.boolIsPolicyChecked)
    strAccessToken = apiManualLogin.postUserLogin(dTestData.rsg.strEmail, dTestData.rsg.strPassword)
    apiProfAddress.addAddress(strAccessToken, dTestData.add.addAddress["firstName"], dTestData.add.addAddress["lastName"], dTestData.add.addAddress["fullName"], dTestData.add.addAddress["phoneNumber"],
                              dTestData.add.addAddress["regionName"], dTestData.add.addAddress["regionId"], dTestData.add.addAddress["cityName"], dTestData.add.addAddress["cityId"],
                              dTestData.add.addAddress["cityRegionId"], dTestData.add.addAddress["zipCode"], dTestData.add.addAddress["barangayName"], dTestData.add.addAddress["barangayId"],
                              dTestData.add.addAddress["barangayCityId"], dTestData.add.addAddress["landmark"], dTestData.add.addAddress["buildingNumber"], dTestData.add.addAddress["country"],
                              dTestData.add.addAddress["isDefault"])
    #post-test
    apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail)
    
    

