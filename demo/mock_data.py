# Mock data for the demo: reference product, 50 candidates, and generated keywords.


REFERENCE_PRODUCT = {
    "asin": "B0XYZ123",
    "title": "Milton Thermosteel 1000ml Insulated",
    "category": "Home & Kitchen > Water Bottles",
    "price": 899,
    "rating": 4.2,
    "reviews": 1247
}


CANDIDATE_PRODUCTS = [
    {"asin": "B0COMP001", "title": "Cello Puro Steel-X 900ml", "category": "Home & Kitchen > Water Bottles", "price": 749, "rating": 4.5, "reviews": 8932},
    {"asin": "B0COMP002", "title": "Borosil Hydra Trek 700ml", "category": "Home & Kitchen > Water Bottles", "price": 599, "rating": 4.4, "reviews": 5621},
    {"asin": "B0COMP003", "title": "Milton Atlantis 1100ml Thermosteel", "category": "Home & Kitchen > Water Bottles", "price": 1099, "rating": 4.3, "reviews": 4102},
    {"asin": "B0COMP004", "title": "Prestige PINNACLE 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 649, "rating": 4.1, "reviews": 3254},
    {"asin": "B0COMP005", "title": "Solimo Stainless Steel 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 499, "rating": 4.2, "reviews": 2876},
    {"asin": "B0COMP006", "title": "Signoraware Aqua Steel 750ml", "category": "Home & Kitchen > Water Bottles", "price": 399, "rating": 4.3, "reviews": 2541},
    {"asin": "B0COMP007", "title": "Kuber Industries Steel Bottle 1L", "category": "Home & Kitchen > Water Bottles", "price": 549, "rating": 4.4, "reviews": 1987},
    {"asin": "B0COMP008", "title": "Flair Houseware Steelo 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 449, "rating": 4.2, "reviews": 1654},
    {"asin": "B0COMP009", "title": "Nirlon Steel Bottle 800ml", "category": "Home & Kitchen > Water Bottles", "price": 349, "rating": 4.5, "reviews": 1543},
    {"asin": "B0COMP010", "title": "Pigeon Sapphire 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 599, "rating": 4.3, "reviews": 1321},
    {"asin": "B0COMP011", "title": "Local Steel Bottle", "category": "Home & Kitchen > Water Bottles", "price": 149, "rating": 3.2, "reviews": 45},
    {"asin": "B0COMP012", "title": "Roadside Plastic Bottle", "category": "Home & Kitchen > Water Bottles", "price": 49, "rating": 2.8, "reviews": 23},
    {"asin": "B0COMP013", "title": "Premium Copper Bottle 1L", "category": "Home & Kitchen > Water Bottles", "price": 2499, "rating": 4.8, "reviews": 234},
    {"asin": "B0COMP014", "title": "Designer Silver Bottle", "category": "Home & Kitchen > Water Bottles", "price": 4999, "rating": 4.9, "reviews": 87},
    {"asin": "B0COMP015", "title": "Cheap Plastic Set of 6", "category": "Home & Kitchen > Water Bottles", "price": 99, "rating": 2.1, "reviews": 12},
    {"asin": "B0COMP016", "title": "Milton Lid Replacement", "category": "Home & Kitchen > Bottle Accessories", "price": 149, "rating": 4.6, "reviews": 3421},
    {"asin": "B0COMP017", "title": "Bottle Carry Bag Sling", "category": "Home & Kitchen > Bottle Accessories", "price": 199, "rating": 4.4, "reviews": 2156},
    {"asin": "B0COMP018", "title": "Bottle Cleaning Brush Set", "category": "Home & Kitchen > Cleaning Supplies", "price": 129, "rating": 4.5, "reviews": 4532},
    {"asin": "B0COMP019", "title": "Insulated Bottle Cover Sleeve", "category": "Home & Kitchen > Bottle Accessories", "price": 179, "rating": 4.2, "reviews": 1876},
    {"asin": "B0COMP020", "title": "Sipper Cap Replacement", "category": "Home & Kitchen > Bottle Accessories", "price": 99, "rating": 4.0, "reviews": 987},
    {"asin": "B0COMP021", "title": "Wonderchef Sippy 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 799, "rating": 4.3, "reviews": 1432},
    {"asin": "B0COMP022", "title": "Amazon Basics Steel 1L", "category": "Home & Kitchen > Water Bottles", "price": 399, "rating": 4.4, "reviews": 1287},
    {"asin": "B0COMP023", "title": "Tupperware Aquasafe 1000ml", "category": "Home & Kitchen > Water Bottles", "price": 649, "rating": 4.3, "reviews": 1156},
    {"asin": "B0COMP024", "title": "Kent Stainless Steel 1L", "category": "Home & Kitchen > Water Bottles", "price": 899, "rating": 4.0, "reviews": 987},
    {"asin": "B0COMP025", "title": "Trueware Fusion 800ml", "category": "Home & Kitchen > Water Bottles", "price": 549, "rating": 4.5, "reviews": 876},
    {"asin": "B0COMP026", "title": "Homeglory Steel Bottle 1L", "category": "Home & Kitchen > Water Bottles", "price": 349, "rating": 4.2, "reviews": 765},
    {"asin": "B0COMP027", "title": "Gym Gallon Bottle 2L", "category": "Home & Kitchen > Water Bottles", "price": 449, "rating": 4.4, "reviews": 654},
    {"asin": "B0COMP028", "title": "Quench Insulated 750ml", "category": "Home & Kitchen > Water Bottles", "price": 699, "rating": 4.6, "reviews": 543},
    {"asin": "B0COMP029", "title": "Carafe Thermosteel 1L", "category": "Home & Kitchen > Water Bottles", "price": 849, "rating": 4.3, "reviews": 432},
    {"asin": "B0COMP030", "title": "Eco Vessel Steel 900ml", "category": "Home & Kitchen > Water Bottles", "price": 999, "rating": 4.1, "reviews": 321},
    {"asin": "B0COMP031", "title": "Fitness Pro Bottle 1L", "category": "Home & Kitchen > Water Bottles", "price": 450, "rating": 3.8, "reviews": 100},
    {"asin": "B0COMP032", "title": "Sports Water Sipper", "category": "Home & Kitchen > Water Bottles", "price": 449, "rating": 3.9, "reviews": 110},
    {"asin": "B0COMP033", "title": "Premium Hydration Flask", "category": "Home & Kitchen > Water Bottles", "price": 1799, "rating": 4.0, "reviews": 150},
    {"asin": "B0COMP034", "title": "Workout Jug 1.5L", "category": "Home & Kitchen > Water Bottles", "price": 1899, "rating": 4.1, "reviews": 200},
    {"asin": "B0COMP035", "title": "Basic Gym Bottle", "category": "Home & Kitchen > Water Bottles", "price": 299, "rating": 3.7, "reviews": 95},
    {"asin": "B0COMP036", "title": "New Launch Artisan Bottle", "category": "Home & Kitchen > Water Bottles", "price": 1199, "rating": 4.8, "reviews": 23},
    {"asin": "B0COMP037", "title": "Startup Brand Steel", "category": "Home & Kitchen > Water Bottles", "price": 749, "rating": 4.5, "reviews": 45},
    {"asin": "B0COMP038", "title": "Indie Craft Bottle", "category": "Home & Kitchen > Water Bottles", "price": 599, "rating": 4.3, "reviews": 67},
    {"asin": "B0COMP039", "title": "Handmade Copper Flask", "category": "Home & Kitchen > Water Bottles", "price": 1499, "rating": 4.7, "reviews": 89},
    {"asin": "B0COMP040", "title": "Boutique Steel Flask", "category": "Home & Kitchen > Water Bottles", "price": 1299, "rating": 4.4, "reviews": 99},
    {"asin": "B0COMP041", "title": "Bottle Handle Grip", "category": "Home & Kitchen > Bottle Accessories", "price": 79, "rating": 4.1, "reviews": 1234},
    {"asin": "B0COMP042", "title": "Silicone Base Protector", "category": "Home & Kitchen > Bottle Accessories", "price": 129, "rating": 4.3, "reviews": 2345},
    {"asin": "B0COMP043", "title": "Bottle Drying Stand", "category": "Home & Kitchen > Kitchen Storage", "price": 249, "rating": 4.2, "reviews": 876},
    {"asin": "B0COMP044", "title": "Bottle Holder Strap", "category": "Sports & Outdoors > Camping", "price": 149, "rating": 4.0, "reviews": 543},
    {"asin": "B0COMP045", "title": "Filter Cap Attachment", "category": "Home & Kitchen > Bottle Accessories", "price": 199, "rating": 4.4, "reviews": 432},
    {"asin": "B0COMP046", "title": "Zojirushi Cool 600ml", "category": "Home & Kitchen > Water Bottles", "price": 1299, "rating": 4.6, "reviews": 2341},
    {"asin": "B0COMP047", "title": "Tiger Steel Flask 1L", "category": "Home & Kitchen > Water Bottles", "price": 1599, "rating": 4.4, "reviews": 1876},
    {"asin": "B0COMP048", "title": "Thermos King 700ml", "category": "Home & Kitchen > Water Bottles", "price": 1799, "rating": 4.3, "reviews": 1654},
    {"asin": "B0COMP049", "title": "Stanley Classic 1L", "category": "Home & Kitchen > Water Bottles", "price": 1499, "rating": 4.4, "reviews": 1432},
    {"asin": "B0COMP050", "title": "Vacuum Flask Pro 1L", "category": "Home & Kitchen > Water Bottles", "price": 699, "rating": 4.2, "reviews": 1123},
]


GENERATED_KEYWORDS = [
    "stainless steel water bottle 1 litre",
    "vacuum insulated flask 1000ml",
    "thermosteel bottle hot cold",
    "steel sipper bottle office gym"
]
