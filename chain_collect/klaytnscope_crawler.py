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
        
        self.chain = "klaytn"
        
    def main(self,token_list) :
    
        result = self.set_token_info(token_list)
        
        return result
        
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
            
    def set_token_info(self,token_list) :
        
        self.tokens = self.set_tokens()
        
        print(self.tokens)
        
        new_token_list = self.check_token_copy(token_list)
        
        n = 0
        
        for token in new_token_list :
            
            n += 1
            
            self.token = token
            
            tokenDict = self.parse_token_info()
            self.tokens.update({self.token : tokenDict})
            
            self.save_token(self.tokens)
            
            if n > 10 :
                break
    
    def parse_token_info(self) :
        """scroll down token list
            "MOOI" : {
                "id" : 1,
                "name" : "MOOI",
                "symbol" : "MOOI",
                "contract" : "0x4b734a4d5bf19d89456ab975dfb75f02762dda1d",
                "decimal" : 18,
                "info" : false
            },
        """
        
        # result = {}
        
        # for token in token_list :
            
        self.load_token_info()
        
        check = self.check_token_info()
        
        if not check :
            return self.safe_token()
            
        try :
            token_detail = self.get_token_detail()
        except :
            token_detail = None
        try :
            token_name = self.get_token_name()
        except :
            token_name = None            
        try :
            token_symbol = self.get_token_symbol()
        except :
            token_symbol = None      
        try :
            token_contract = self.get_token_contract()
        except :
            token_contract = None
        try :
            self.get_token_image()
        except :
            None

        tokenDict = {
            
            "name" : token_name,
            "symbol" : token_symbol,
            "contract" : {
                self.chain : token_contract
            },
            "detail" : token_detail,
            
        }
            
        token = self.deep_extend(self.safe_token(), tokenDict)

        return token
    
    def load_token_info(self) :

        tokenPage = f'https://scope.klaytn.com/search/tokens-nft-account?key={self.token}'
        
        self.driver.get(tokenPage)
        
    def check_token_info(self) :
        
        try :
            for i in range(1,10) :
                
                self.i = i
                
                token_symbol = self.get_token_symbol()
                
                if self.token == token_symbol :
                    break

            if self.token == token_symbol :
                return True
            else :
                return False
        except :
            return False
        
    def check_token_copy(self,token_list) :
        
        tokens = self.set_tokens()
        
        old_token_list = list(tokens.keys())
        
        new_token_list = list(set(token_list) - set(old_token_list))
        
        print(f"new token : {new_token_list}")
        
        return new_token_list
        
    @retry
    def get_token_detail(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//a[@href]")))
        
        token_detail = elem.get_attribute("href")
        
        return token_detail
    
    @retry
    def get_token_image(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//img[@src]")))
        
        token_image = elem.get_attribute("src")
        
        self.driver.get(token_image)
        
        self.driver.save_screenshot(f"token_icons/{self.token}.png")

    
    @retry
    def get_token_name(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[1]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_name = elem.get_attribute("innerText")
             
        return token_name
    
    @retry
    def get_token_symbol(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[2]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_symbol = elem.get_attribute("innerText")
             
        return token_symbol
    
    @retry
    def get_token_contract(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
    
    @retry
    def get_token_contract(self) :
        
        elem = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
        