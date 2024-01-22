import libraries.util.common as uCommon

class ct:
    """CATEGORIES"""
    def getCategoryLevel(response, strCategoryId, strCategoryFilterId):
        """
        Objective: Get Category Level
        
        Params: response | strCategoryId | strCategoryFitlerId
        Returns: L2 | L3
        Author: cgrapa_20230803
        """
        responseData = uCommon.getResponseData(response)
        arrCategories = responseData["data"]
        for strCategory in arrCategories:
            if strCategory["_id"] == strCategoryFilterId:
                if strCategory["parentId"] == strCategoryId:
                    return 'L2'
                else:
                    return 'L3'