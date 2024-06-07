import pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.login.manualLogin as apiManualLogin
import libraries.util.apiCall.signUp.manualSignUp as apiManualSignUp
import libraries.util.apiCall.profile.address as apiProfAddress


@pytest.mark.api()
def test_001_sign_up_success():
    apiManualSignUp.postAndVerifyUserSignUp(dTestData.rsg.strEmail, dTestData.rsg.strPassword, dTestData.rsg.strFirstName, dTestData.rsg.strLastName, dTestData.rsg.blnIsPolicyChecked)
    strAccessToken = apiManualLogin.postUserLogin(dTestData.rsg.strEmail, dTestData.rsg.strPassword)
    apiProfAddress.postAddress(strAccessToken, dTestData.add.addAddress)
    #post-test
    #apiManualSignUp.deleteNewSignedUpAcct(dTestData.rsg.strEmail)
    
    

