from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

import libraries.data.testData as dTestData
import libraries.data.url as dUrl
import libraries.page.sellerCenter as pSellerCenter
import libraries.util.common as uCommon
import libraries.util.response.sellerCenter.login as rLoginSC

def inputCredentialsAndSignIn(page, strUsername, strPassword):
    """
    Objective: Input login credentials and sign in
    
    Params: page | strUsername | strPassword
    Returns: redirectUri
    Author: cgrapa_20240605
    """
    uCommon.setElemText(page, pSellerCenter.sc.usernameTxt, strUsername)
    uCommon.setElemText(page, pSellerCenter.sc.passwordTxt, strPassword)
    uCommon.clickElem(page, pSellerCenter.sc.signinBtn)
    redirectUri = uCommon.getUriWithAuthCode(page, dUrl.lgn.sc.redirectUri)
    return redirectUri

def getAuthCode(redirectUri):
    """
    Objective: Get authorization code
    
    Params: redirectUri
    Returns: authCode
    Author: cgrapa_20240605
    """
    parsedUrl = urlparse(redirectUri)
    authCode = parse_qs(parsedUrl.query).get('code')[0]
    return authCode

def postOAuth2Token(strTokenUrl, strAuthCode, strRedirectUri, strClientID):
    """
    Method: POST
    API Endpoint: strTokenUrl
    Author: cgrapa_20240605
    """
    response = uCommon.callPostOAuth2(strTokenUrl, strAuthCode, strRedirectUri, strClientID)
    return response

def loginOAuth2(strEmail, strPassword):
    """
    Objective: Login to Seller Center with OAuth2.0 verification
    
    Params: strEmail | strPassword
    Returns: accessToken
    Author: cgrapa_20240605
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        authUrl = f'{dUrl.lgn.sc.authBaseUrl}?response_type=code&client_id={dTestData.lgn.sc.clientID}&redirect_uri={dUrl.lgn.sc.redirectUri}'
        page.goto(authUrl)
        redirectUri = inputCredentialsAndSignIn(page, strEmail, strPassword)
        authCode = getAuthCode(redirectUri)
        browser.close()
    response = postOAuth2Token(dUrl.lgn.sc.tokenUrl, authCode, dUrl.lgn.sc.redirectUri, dTestData.lgn.sc.clientID)
    dictData = rLoginSC.getAccessTokenAndRefreshTokenSC(response)
    return dictData