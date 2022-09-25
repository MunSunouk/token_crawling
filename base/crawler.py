from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from base.token import Token
import json

class Crawler:

    def __init__(self):
        super().__init__()

        self.retries = 3

        self.retriesTime = 3

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        self.wait = WebDriverWait(driver = self.driver, timeout = self.retriesTime)
        
    @staticmethod
    def set_tokens():
        return Token().set_token()
    
    @staticmethod
    def safe_token():
        return Token().__dict__
    
    @staticmethod
    def save_token(tokens):
        return Token().save_token(tokens)
    
    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict): 
                if not isinstance(result, dict):
                    result = {}          
                for key in arg:             
                    result[key] = Crawler.deep_extend(result[key] if key in result else None, arg[key])                 
            else:
                result = arg
        return result
        
    
        