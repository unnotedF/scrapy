from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from collections import defaultdict
import mysql.connector
import re


class SaveToMySQLPipeline:
    def __init__(self):
        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = '',         # Enter your MySQL username
            password = '',     # Enter your MySQL password
            database = ''      # Enter your MySQL database name
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        # Create table if it does not exist
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {item.get('search_term').replace(' ', '_')} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                name VARCHAR(255),
                brand VARCHAR(20),
                price DECIMAL(10,2),
                available BOOLEAN,
                rating DECIMAL(2,1),
                num_reviews INT,
                url VARCHAR(255)
            )
        """)
        self.conn.commit()

        # Insert item into table
        self.cur.execute("""
            INSERT INTO {} (date, name, brand, price, available, rating, num_reviews, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """.format(item.get('search_term').replace(' ', '_')), (
            item.get('date'),
            item.get('name'),
            item.get('brand'),
            item.get('price'),
            item.get('available'),
            item.get('rating'),
            item.get('num_reviews'),
            item.get('url')
        ))
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


class DuplicateCheckPipeline:
    def __init__(self):
        self.seen_items = defaultdict(set)
    def process_item(self, item, spider):
        item_key = (item.get('name'), item.get('brand'), item.get('price'), item.get('rating'),  item.get('num_reviews'))
        if item_key in self.seen_items[spider.name]:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.seen_items[spider.name].add(item_key)
            return item


class ProductCheckPipeline:
    def process_item(self, item, spider):
        if item.get('search_term') not in item.get('name'):
            raise DropItem(f"Item {item.get('name')} does not contain the search term")
        else:
            return item


class BrandCheckPipeline:
    def process_item(self, item, spider):
        if item.get('specific_brand') == None:
            return item
        elif item.get('specific_brand') not in item.get('brand'):
            raise DropItem(f"Item {item.get('name')} does not contain the specific brand")
        else:
            return item
        

class PriceRangeCheckPipeline:
    def process_item(self, item, spider):
        if item.get('min_price') == None or item.get('max_price') == None:
            return item
        elif item.get('price') < item.get('min_price') or item.get('price') > item.get('max_price'):
            raise DropItem(f"Item {item.get('name')} is not in the price range")
        else:
            return item


class AmazonItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Remove all whitespaces from name, brand and rating fields
        to_strip = [field for field in adapter.field_names() if field in ['name', 'brand', 'rating']]
        for field in to_strip:
            adapter[field] = adapter.get(field).strip()

        # Clean name field
        name = adapter.get('name')
        name = name.lower()
        # Uncomment to remove brand from name
        #brand = adapter.get('brand')
        #if brand.lower() in name:
        #    name = name.replace(brand.lower(), "").strip()
        # Uncomment to remove paranthesis from name
        #if "(" in name and ")" in name:
        #    name = re.sub(r'\([^)]*\)', '', name).strip()
        if "[" in name and "]" in name:
            name = re.sub(r'\[[^)]*\]', '', name).strip()
        if ", " in name:
            if name[0] == "," or name[1] == ",":
                name = name[:2].split(",")[0].strip()
            if ", " in name:
                name = name.split(",")[0].strip()
        if "with" in name:
            name = name.split("with")[0].strip()
        if "and" in name:
            name = name.split(" and ")[0].strip()
        if " - " in name:
            name = name.split(" -")[0].strip()
        name = name.replace(",","").replace(":", "").strip()
        adapter['name'] = name[:255]

        # Clean brand field
        brand = adapter.get('brand')
        brand = brand.lower()
        if "visit the" in brand:
            brand = brand.replace("visit the ", "").replace(" store", "")
        if "brand:" in brand:
            brand = brand.replace("brand:", "")
        if " " in brand and brand[1] != " " and brand[2] != " ":
            brand = brand.split(" ")[0]
        adapter['brand'] = brand

        # Check if the price is 0 and set available to False
        if adapter['price'] == "0":
            adapter['available'] = False

        # Clean and converts price, rating and num_reviews field
        item['price'] = float(re.sub(r'[^\d.]', '', adapter.get('price')))
        item['rating'] = float(adapter.get('rating').split(" ")[0])
        item['num_reviews'] = int(re.sub(r'[^\d.]', '', adapter.get('num_reviews')))

        # Limit url to 255 characters
        adapter['url'] = adapter.get('url')[:255]

        return item
