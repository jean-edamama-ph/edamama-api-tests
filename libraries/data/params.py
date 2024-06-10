categories = ''

curatedTypesSpotlight = {
                        "forSpotlight": True
                        }





class sc:
    """SELLER CENTER"""

    def shipments (strVendorId):
        return {
                "limit": 1,
                "page": 1,
                "generalStatus": 1,
                "vendorId": strVendorId
            }
    def searchOrderNum (strOrderId, strVendorId):
        return {
                "limit": 1,
                "page": 1,
                "generalStatus": 1,
                "search": strOrderId,
                "vendorId": strVendorId
        }





class asc:
    """ADMIN PANEL | SELLER CENTER"""
    def print(strPrintType):
        return {
            "printType": strPrintType
        }