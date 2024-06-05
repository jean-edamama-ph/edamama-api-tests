from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import libraries.data.testData as dTestData
import libraries.util.common as uCommon

def verifyUserAccount(strEmail):
    """ 
    Objective: Make the user account as email and mobile verified
    
    param strEmail
    returns: None
    Author: jatregenio_20240604
    """
    strConnectionString = uCommon.generateMongoDbConnectionString(dTestData.md.strPemFilePath, dTestData.md.strConnectionStringScheme)
    searchCriteria = {"email": strEmail}
    editOperation = {"$set": {
                        "isEmailVerified": True,
                        "type": "verified"
                        }
                     }
    try:
        client = MongoClient(strConnectionString)
        db = client[dTestData.md.strDatabaseName]
        collection = db['users']
        editResult = collection.update_one(searchCriteria, editOperation)
        assert editResult.matched_count > 0, f"Email: {strEmail}, was not found on DB"
    except ConnectionFailure as e:
        raise RuntimeError(f"Connection failed: {e}\nPLEASE MAKE SURE AWS VPN IS RUNNING AND CONNECTED")
    finally:
        client.close()
        
def deleteUserAccount(strEmail):
    """ 
    Objective: Hard delete user account
    
    param strEmail
    returns: None
    Author: jatregenio_20240605
    """
    strConnectionString = uCommon.generateMongoDbConnectionString(dTestData.md.strPemFilePath, dTestData.md.strConnectionStringScheme)
    searchCriteria = {"email": strEmail}
    try:
        client = MongoClient(strConnectionString)
        db = client[dTestData.md.strDatabaseName]
        collection = db['users']
        deleteOneResult = collection.delete_one(searchCriteria)
        assert deleteOneResult.deleted_count == 1, f"Expected to delete 1 document, but deleted {deleteOneResult.deleted_count}."
    except ConnectionFailure as e:
        raise RuntimeError(f"Connection failed: {e}\nPLEASE MAKE SURE AWS VPN IS RUNNING AND CONNECTED")
    finally:
        client.close()