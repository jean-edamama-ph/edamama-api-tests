import allure, pytest

import libraries.data.testData as dTestData

import libraries.util.apiCall.productListing as apiProductListing

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Diapering')
def test_AUTO_937_Category_Listing_Diapering():
    apiProductListing.validateCategoriesPlp(dTestData.plp.diapering)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Fashion')
def test_AUTO_937_Category_Listing_Fashion():
    apiProductListing.validateCategoriesPlp(dTestData.plp.fashion)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Food and Nutrition')
def test_AUTO_937_Category_Listing_Food_and_Nutrition():
    apiProductListing.validateCategoriesPlp(dTestData.plp.foodAndNutrition)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Nursery')
def test_AUTO_937_Category_Listing_Nursery():
    apiProductListing.validateCategoriesPlp(dTestData.plp.nursery)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Feeding and Mealtime')
def test_AUTO_937_Category_Listing_Feeding_and_Mealtime():
    apiProductListing.validateCategoriesPlp(dTestData.plp.feedingAndMealtime)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Mama')
def test_AUTO_937_Category_Listing_Mama():
    apiProductListing.validateCategoriesPlp(dTestData.plp.mama)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Baby Gear')
def test_AUTO_937_Category_Listing_Baby_Gear():
    apiProductListing.validateCategoriesPlp(dTestData.plp.babyGear)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Home and Living')
def test_AUTO_937_Category_Listing_Home_and_Living():
    apiProductListing.validateCategoriesPlp(dTestData.plp.homeAndLiving)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Toys and Learning')
def test_AUTO_937_Category_Listing_Toys_and_Learning():
    apiProductListing.validateCategoriesPlp(dTestData.plp.toysAndLearning)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Bath and Body')
def test_AUTO_937_Category_Listing_Bath_and_Body():
    apiProductListing.validateCategoriesPlp(dTestData.plp.bathAndBody)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Furmama')
def test_AUTO_937_Category_Listing_Furmama():
    apiProductListing.validateCategoriesPlp(dTestData.plp.furmama)

@pytest.mark.api()
@allure.step('Verify if search results will be Filtered and Sorted By correctly - Beauty and Wellness')
def test_AUTO_937_Category_Listing_Beauty_and_Wellness():
    apiProductListing.validateCategoriesPlp(dTestData.plp.beautyAndWellness)