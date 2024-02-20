import allure, pytest

import libraries.data.testData as dTestData
import libraries.util.apiCall.productListing.category as apiCategory
import libraries.util.apiCall.productListing.curated as apiCurated
import libraries.util.apiCall.productListing.search as apiSearch
import libraries.util.apiCall.productListing.ds as apiDs

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Diapering')
def test_AUTO_937_Category_Listing_Diapering():
    apiCategory.validateCategoriesPlp(dTestData.plp.diapering)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Fashion')
def test_AUTO_937_Category_Listing_Fashion():
    apiCategory.validateCategoriesPlp(dTestData.plp.fashion)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Food and Nutrition')
def test_AUTO_937_Category_Listing_Food_and_Nutrition():
    apiCategory.validateCategoriesPlp(dTestData.plp.foodAndNutrition)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Nursery')
def test_AUTO_937_Category_Listing_Nursery():
    apiCategory.validateCategoriesPlp(dTestData.plp.nursery)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Feeding and Mealtime')
def test_AUTO_937_Category_Listing_Feeding_and_Mealtime():
    apiCategory.validateCategoriesPlp(dTestData.plp.feedingAndMealtime)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Mama')
def test_AUTO_937_Category_Listing_Mama():
    apiCategory.validateCategoriesPlp(dTestData.plp.mama)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Baby Gear')
def test_AUTO_937_Category_Listing_Baby_Gear():
    apiCategory.validateCategoriesPlp(dTestData.plp.babyGear)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Home and Living')
def test_AUTO_937_Category_Listing_Home_and_Living():
    apiCategory.validateCategoriesPlp(dTestData.plp.homeAndLiving)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Toys and Learning')
def test_AUTO_937_Category_Listing_Toys_and_Learning():
    apiCategory.validateCategoriesPlp(dTestData.plp.toysAndLearning)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Bath and Body')
def test_AUTO_937_Category_Listing_Bath_and_Body():
    apiCategory.validateCategoriesPlp(dTestData.plp.bathAndBody)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Furmama')
def test_AUTO_937_Category_Listing_Furmama():
    apiCategory.validateCategoriesPlp(dTestData.plp.furmama)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Beauty and Wellness')
def test_AUTO_937_Category_Listing_Beauty_and_Wellness():
    apiCategory.validateCategoriesPlp(dTestData.plp.beautyAndWellness)

@pytest.mark.api()
@allure.step('Verify if products displayed through search follow search result requirements including Filtering and Sorting')
def test_AUTO_938_Atlas_Search_Results_Validation():
    strSearchTerm = dTestData.plp.src.searchTerm
    apiSearch.validateSearchPlp(strSearchTerm)

@pytest.mark.api()
@allure.step('Verify if products displayed through search follow search result requirements including Filtering and Sorting - Multiple Search Terms')
def test_AUTO_938_Atlas_Search_Filter_Validation_Multiple_Search_Terms():
    arrTop30SearchTerms = dTestData.plp.src.top30SearchTerms
    for strSearchTerm in arrTop30SearchTerms:
        apiSearch.validateSearchPlp(strSearchTerm)

@pytest.mark.api()
@allure.step('Verify if products displayed through curated PLPs are valid')
def test_AUTO_000_Curated_Products_PLP_Validation():
    apiCurated.validateCuratedPlp()

@pytest.mark.api()
@allure.step('Verify if products displayed through DS PLPs are valid')
def test_AUTO_000_DS_PLP_Validation():
    apiDs.validateDsPlp()