<h1 align='center'>Amazon Product Scraper</h1>

## Description
This project is a web scraper built using the Scrapy Python framework that allows you to scrape product information from Amazon and store it in a MySQL database. The scraper is highly customizable, allowing you to specify the product, brand, and price range you are interested in. It also comes with various pipelines to process and clean the scraped data before saving it to the database.

## Table of Contents

- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Customization](#customization)
- [Pipelines](#pipelines)
- [Database Schema](#database-schema)
- [Important Notes](#important-notes)
- [License](#license)
- [Author](#author)

## Requirements
- Python 3.6+
- MySQL

## Installation
1. Clone the repository
2. Create a virtual environment (optional but recommended).
3. Install the required Python packages using pip:
    
        pip install scrapy mysql-connector-python

## Configuration
1. Modify the `pipelines.py` file to set up your MySQL database connection. Replace the following parameters with your database credentials:
```
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = '',         # Enter your MySQL username
            password = '',     # Enter your MySQL password
            database = ''      # Enter your MySQL database name
        )
```
2. You need to enable fake browser headers from ScrapeOps to prevent being blocked by Amazon's anti-scraping measures. To do this, sign up for a ScrapeOps API key and set it as the value of `SCRAPEOPS_API_KEY` in the `settings.py` file.
```
SCRAPEOPS_API_KEY = 'your_scrapeops_api_key' # Insert your ScrapeOps API key
```

## Usage
1. Open a terminal and navigate to the project directory.
2. Run the following command to start the scraper:

        scrapy crawl amazonspider

3. The scraper will prompt you for the product name, specific brand (optional), and price range (optional) you want to scrape. Enter the details as requested.

## Customization
The scraper is designed to be highly customizable. You can modify the following parameters in `amazonspider.py` to suit your specific requirements:

- `CONCURRENT_REQUESTS`: The number of concurrent requests made to Amazon. Increase this value to speed up the scraping process.
- `DOWNLOAD_DELAY`: A small delay (in seconds) between requests to avoid overwhelming the server. Adjust this value to be more considerate to Amazon's servers
- `ITEM_PIPELINES`: A dictionary that defines the pipelines and their order of execution. You can customize the order or add/remove pipelines according to your needs.

## Pipelines
The scraper uses several pipelines to process and clean the scraped data before saving it to the MySQL database:

1. `BrandCheckPipeline`: Filters products based on a specific brand provided by the user.
2. `AmazonItemPipeline`: Cleans and formats fields from the scraped item.
3. `PriceRangeCheckPipeline`: Filters products based on the price range provided by the user.
4. `ProductCheckPipeline`: Ensures that the product name contains the search term provided by the user.
5. `DuplicateCheckPipeline`: Checks and removes duplicate items based on their name, brand, price, rating, and number of reviews.
6. `SaveToMySQLPipeline`: Saves the processed item to the MySQL database.

You can modify or extend these pipelines to implement custom data processing or another saving logic.

## Database Schema
The scraper creates a table in the MySQL database for each search term provided by the user. The schema of the table is as follows:

| Column      | Data Type | Description                                  |
| ----------- | --------- | -------------------------------------------- |
| id          | INT       | Primary key and auto-incremented ID          |
| date        | DATE      | Date when the product was scraped            |
| name        | VARCHAR   | Name of the product                          |
| brand       | VARCHAR   | Brand of the product                         |
| price       | DECIMAL   | Price of the product                         |
| available   | BOOLEAN   | Indicates if the product is available or not |
| rating      | DECIMAL   | Product rating (0-5)                         |
| num_reviews | INT       | The number of reviews for the product        |
| url         | VARCHAR   | The URL of the product on Amazon             |


## Important Notes

- Web scraping may violate the terms of service of the website being scraped. Be sure to review Amazon's terms of service before using this scraper to avoid potential legal issues.
- Avoid excessive scraping and implement reasonable rate-limiting to avoid causing strain on the server.

## License
This project is under the [MIT License](https://chat.openai.com/c/LICENSE).

## Author
| [<img src="https://avatars.githubusercontent.com/u/105685220?v=4" width=115><br><sub>Pedro Vinicius Messetti</sub>](https://github.com/pedromessetti) |
| :---------------------------------------------------------------------------------------------------------------------------------------------------: |

If you have any questions or need further assistance, feel free to contact me at [pedromessetti@gmail.com](pedromessetti@gmail.com).