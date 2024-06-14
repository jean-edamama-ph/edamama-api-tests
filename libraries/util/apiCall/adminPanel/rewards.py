import libraries.data.headers as dHeaders
import libraries.data.payload as dPayload
import libraries.data.url as dUrl
import libraries.util.common as uCommon
import libraries.util.response.placeOrder as rPlaceOrder
import libraries.util.response.adminPanel.shipments as rApShipments

def putRewardsCapping(strToken, strMaxPHPCap, strMaxPercentCap):
    """
    Method: GET
    API Endpoint: /admin/rewardsCapping
    Payload: newRewardsAmountCap | newRewardsPercentageCap
    Author: abernal_20240610
    """
    response = uCommon.callPut(dUrl.ap.rewardsCap, dHeaders.withToken(strToken), dPayload.ap.updateRewardsCap(strMaxPercentCap, strMaxPHPCap))
    return response