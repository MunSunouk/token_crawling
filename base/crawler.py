from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

class Crawler:

    def __init__(self):
        super().__init__()

        self.retries = 5

        self.retriesTime = 10

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        self.wait = WebDriverWait(driver = self.driver, timeout = self.retriesTime)