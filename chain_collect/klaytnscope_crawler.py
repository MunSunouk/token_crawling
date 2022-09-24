from base import Crawler
import time
from datetime import datetime
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Klatnscope_crawler(Crawler):

    def __init__(self):
        super().__init__()
        
    def retry(method):
        @wraps(method)
        def retry_method(self, *args):
            for i in range(self.retries):
                
                print('{} - {} - Attempt {}'.format(datetime.now(), method.__name__, i))
                time.sleep(self.retriesTime)
                try:
                    return method(self, *args)
                except :
                    if i == self.retries - 1:
                        raise

        return retry_method
        
    def main(self,token_list) :
    
        result = self.get_token_info(token_list)
        
        return result
    
    def get_token_info(self,token_list) :
        """scroll down token list"""
        
        result = []
        
        for token in token_list :
            
            self.load_token_info(token)
            
            token_detail = self.get_token_detail()
            token_image = self.get_token_image(token)
            token_name = self.get_token_name()
            token_symbol = self.get_token_symbol()
            token_contract = self.get_token_contract()
            
            result.append((token_detail,token_image,token_name,token_symbol,token_contract))
            
        return result
    
    @retry
    def load_token_info(self,token) :

        tokenPage = f'https://scope.klaytn.com/search/tokens-nft-account?key={token}'
        
        self.driver.get(tokenPage)
        
    @retry
    def get_token_detail(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//a[@href]")))
        
        token_detail = elem.get_attribute("href")
        
        return token_detail
    
    @retry
    def get_token_image(self,token) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//img[@src]")))
        
        token_image = elem.get_attribute("src")
        
        with open(f'{token}.png', 'wb') as file:
            file.write(token_image.screenshot_as_png)
        
        return token_image
    
    @retry
    def get_token_name(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//div[1]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_name = elem.get_attribute("innerText")
             
        return token_name
    
    @retry
    def get_token_symbol(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//div[2]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_symbol = elem.get_attribute("innerText")
             
        return token_symbol
    
    @retry
    def get_token_contract(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
    
    @retry
    def get_token_contract(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[1]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
        