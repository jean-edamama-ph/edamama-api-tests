import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.mongoDB.userAccount as mUserAccount
import libraries.util.apiCall.profile.address as apiCallProfAddress
import libraries.util.apiCall.login.manualLogin as apiCallManualLogin

def postUserSignUp(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked):
    """
    Method: POST
    API Endpoint: /users/signup
    Payload: strEmail | strPassword | strFname | strLname | blnIsPolicyChecked
    Author: jatregenio_20240604
    """
    
    response = uCommon.callPost(dUrl.rsg.userSignUp, dHeaders.withToken(), dPayload.rsg.userSignUp(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked))
    return response

def postAndVerifyUserSignUp(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked):
    """
    Objective: Register and verify newly signed up account
    Param: strEmail | strPassword | strFname | strLname | blnIsPolicyChecked
    Author: jatregenio_20240604
    """
    postUserSignUp(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked)
    mUserAccount.verifyUserAccount(strEmail)
    
def deleteRegisteredAcct(strEmail):
    """
    Objective: Register and verify newly signed up account
    Param: strEmail | strPassword | strFname | strLname | blnIsPolicyChecked
    Author: jatregenio_20240604
    """
    mUserAccount.deleteUserAccount(strEmail)

def postAndVerifyAndAddAddressToNewSignedUpAcct(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked, dictAddress):
    """
    Objective: Register and verify newly signed up account then add address
    Param: strEmail | strPassword | strFname | strLname | blnIsPolicyChecked
    Author: jatregenio_20240604
    """
    postAndVerifyUserSignUp(strEmail, strPassword, strFname, strLname, blnIsPolicyChecked, )
    strAccessToken = apiCallManualLogin.postUserLogin(strEmail, strPassword)
    apiCallProfAddress.postAddress(strAccessToken, dictAddress)
    return strAccessToken
    