class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on various criteria like cuisine type, location, and rating.
    
    Attributes:
        database (RestaurantDatabase): An instance of RestaurantDatabase that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize RestaurantBrowsing with a reference to a restaurant database.
        
        Args:
            database (RestaurantDatabase): The database object containing restaurant information.
        """
        self.database = database

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants based on their cuisine type.
        
        Args:
            cuisine_type (str): The type of cuisine to filter by (e.g., "Italian").
        
        Returns:
            list: A list of restaurants that match the given cuisine type.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        Search for restaurants based on their location.
        
        Args:
            location (str): The location to filter by (e.g., "Downtown").
        
        Returns:
            list: A list of restaurants that are located in the specified area.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants based on their minimum rating.
        
        Args:
            min_rating (float): The minimum acceptable rating to filter by (e.g., 4.0).
        
        Returns:
            list: A list of restaurants that have a rating greater than or equal to the specified rating.
        """
        return [restaurant for restaurant in self.database.get_restaurants() 
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None,rating=None, delivery_speed=None):
        """
        Search for restaurants based on multiple filters: cuisine type, location, and/or rating.
        
        Args:
            cuisine_type (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            min_rating (float, optional): The minimum acceptable rating to filter by.
        
        Returns:
            list: A list of restaurants that match all specified filters.
        """
        results = self.database.get_restaurants()  # Start with all restaurants

        if cuisine_type:
            results = [restaurant for restaurant in results 
                       if restaurant['cuisine'].lower() == cuisine_type.lower()]

        # Filter by location
        if location:
            results = [restaurant for restaurant in results if restaurant['location'].lower() == location.lower()]

        # Filter by rating
        if rating is not None:
            results = [r for r in results if r["rating"] >= rating]

        # Filter by delivery speed
        if delivery_speed is not None:
            results = [r for r in results if r.get("delivery_speed") and r["delivery_speed"] <= delivery_speed]

        return results


class RestaurantDatabase:
    """
    A simulated in-memory database that stores restaurant information.
    
    Attributes:
        restaurants (list): A list of dictionaries, where each dictionary represents a restaurant with
                            fields like name, cuisine, location, rating, price range, and delivery status.
    """

    def __init__(self):
        # 示例数据，包含餐厅名称、菜系、位置、评分和配送速度
        self.restaurants = [
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "New York", "rating": 4.5, "delivery_speed": 30},
            {"name": "Sushi World", "cuisine": "Japanese", "location": "San Francisco", "rating": 4.7,
             "delivery_speed": 40},
            {"name": "Burger Shack", "cuisine": "American", "location": "Los Angeles", "rating": 4.2,
             "delivery_speed": 25},
            {"name": "Taco Stand", "cuisine": "Mexican", "location": "Chicago", "rating": 3.9, "delivery_speed": 20},
            {"name": "Vegan Delight", "cuisine": "Vegan", "location": "Austin", "rating": 4.8, "delivery_speed": 35},
            {"name": "Dim Sum House", "cuisine": "Chinese", "location": "Seattle", "rating": 4.6, "delivery_speed": 50},
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.0,
             "delivery_speed": 30},  # 添加意大利餐厅
            {"name": "Sushi Express", "cuisine": "Japanese", "location": "Downtown", "rating": 4.2,
             "delivery_speed": 30}  # 添加 Downtown 餐厅
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants in the database.
        
        Returns:
            list: A list of dictionaries, where each dictionary contains restaurant information.
        """
        return self.restaurants


class RestaurantSearch:
    """
    A class that interfaces with RestaurantBrowsing to perform restaurant searches based on user input.
    
    Attributes:
        browsing (RestaurantBrowsing): An instance of RestaurantBrowsing used to perform searches.
    """

    def __init__(self, browsing):
        """
        Initialize the RestaurantSearch with a reference to a RestaurantBrowsing instance.
        
        Args:
            browsing (RestaurantBrowsing): An instance of the RestaurantBrowsing class.
        """
        self.browsing = browsing

    def search_restaurants(self, cuisine=None, location=None, rating=None):
        """
        Search for restaurants using multiple optional filters: cuisine, location, and rating.
        
        Args:
            cuisine (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            rating (float, optional): The minimum rating to filter by.
        
        Returns:
            list: A list of restaurants that match the provided search criteria.
        """
        results = self.browsing.search_by_filters(cuisine_type=cuisine, location=location, min_rating=rating)
        return results


# Unit tests for RestaurantBrowsing class
import unittest

class TestRestaurantBrowsing(unittest.TestCase):

    def setUp(self):
        self.database = RestaurantDatabase()
        self.browsing = RestaurantBrowsing(self.database)

    def test_search_by_cuisine(self):
        results = self.browsing.search_by_cuisine("Italian")
        self.assertEqual(len(results), 2)  # 现在意大利餐厅有2个
        self.assertTrue(all([restaurant['cuisine'] == "Italian" for restaurant in results]))

    def test_search_by_location(self):
        results = self.browsing.search_by_location("Downtown")
        self.assertEqual(len(results), 2)  # 现在Downtown有2个餐厅
        self.assertTrue(all([restaurant['location'] == "Downtown" for restaurant in results]))

    def test_search_by_rating(self):
        results = self.browsing.search_by_rating(4.0)
        self.assertEqual(len(results), 7)  # 评分>=4.0的餐厅有7个
        self.assertTrue(all([restaurant['rating'] >= 4.0 for restaurant in results]))

    def test_search_by_filters(self):
        # 现在搜索Downtown的Italian餐厅，且评分大于等于4.0
        results = self.browsing.search_by_filters(cuisine_type="Italian", location="Downtown", rating=4.0)
        self.assertEqual(len(results), 1)  # 只有一个符合条件
        self.assertEqual(results[0]['name'], "Italian Bistro")  # 结果应为"Italian Bistro"


if __name__ == '__main__':
    unittest.main()
