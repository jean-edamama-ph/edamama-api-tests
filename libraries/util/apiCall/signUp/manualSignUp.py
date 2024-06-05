import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.guestToken as rGuestToken
import libraries.util.mongoDB.userAccount as mUserAccount

def postUserSignUp(strEmail, strPassword, strFname, strLname, boolIsPolicyChecked):
    """
    Method: POST
    API Endpoint: /users/signup
    Payload: strEmail | strPassword | strFname | strLname | boolIsPolicyChecked
    Author: jatregenio_20240604
    """
    
    response = uCommon.callPost(dUrl.rsg.userSignUp, dHeaders.withToken(), dPayload.rsg.userSignUp(strEmail, strPassword, strFname, strLname, boolIsPolicyChecked))
    return response

def postAndVerifyUserSignUpViaEmail(strEmail, strPassword, strFname, strLname, boolIsPolicyChecked):
    postUserSignUp(strEmail, strPassword, strFname, strLname, boolIsPolicyChecked)
    mUserAccount.verifyUserAccount(strEmail)
    
def deleteNewSignedUpAcct(strEmail):
    mUserAccount.deleteUserAccount(strEmail)
    