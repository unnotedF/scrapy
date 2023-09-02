# Scrapy settings for amazonscraper project

BOT_NAME = "amazonscraper"

SPIDER_MODULES = ["amazonscraper.spiders"]
NEWSPIDER_MODULE = "amazonscraper.spiders"

SCRAPEOPS_API_KEY = 'your_scrapeops_api_key' # Insert your ScrapeOps API key
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = "https://headers.scrapeops.io/v1/browser-headers"
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32 # Increase number of concurrent requests
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOAD_DELAY = 0.15 # Small delay between requests to avoid server overwhelming

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 28800  # Cache for 8 hours
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "amazonscraper.middlewares.AmazonSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'amazonscraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 100,
    #"amazonscraper.middlewares.AmazonDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
