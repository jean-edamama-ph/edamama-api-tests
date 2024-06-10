categories = ''

curatedTypesSpotlight = {
                        "forSpotlight": True
                        }





class sc:
    """SELLER CENTER"""
    
    # change this portion to def if vendorID needs to be dynamic
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