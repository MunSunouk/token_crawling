from base import Crawler
import time
from datetime import datetime
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import asyncio

class Klatnscope_crawler(Crawler):

    def __init__(self):
        super().__init__()
        
        self.chain = "klaytn"
        
    def main(self,token_list) :
    
        asyncio.run(self.set_token_info(token_list))
        
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
                        return None

        return retry_method
            
    async def set_token_info(self,token_list) :
        
        self.tokens = self.set_tokens()
        
        new_token_list = self.check_token_copy(token_list)
        
        n = 0
        
        for token in new_token_list :
            
            n += 1
            
            self.token = token
            
            tokenDict = await self.parse_token_info()
            self.tokens.update({self.token : tokenDict})
            
            self.save_token(self.tokens)
            
            if n > 10 :
                break
    
    async def parse_token_info(self) :
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
            
        await self.load_token_info()
        
        check = await self.check_token_info()
        
        if not check :
            return self.safe_token()
            
        result = await asyncio.gather(self.get_token_name(),
                                      self.get_token_symbol(),
                                      self.get_token_contract(),
                                      self.get_token_detail(),
                                      self.get_token_image()
                                      )
        
        return result

        # tokenDict = {
            
        #     "name" : result[0],
        #     "symbol" : result[1],
        #     "contract" : {
        #         self.chain : result[2]
        #     },
        #     "detail" : result[3],
            
        # }
            
        # token = self.deep_extend(self.safe_token(), tokenDict)

        # return token
    
    async def load_token_info(self) :

        tokenPage = f'https://scope.klaytn.com/search/tokens-nft-account?key={self.token}'
        
        await self.driver.get(tokenPage)
        
    async def check_token_info(self) :
        
        try :
            for i in range(1,10) :
                
                self.i = i
                
                token_symbol = await self.get_token_symbol()
                
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
        
        tokens_list = list(tokens.keys())
        
        new_token_list = list(set(token_list) - set(tokens_list))
        
        return new_token_list
        
    async def get_token_detail(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//a[@href]")))
        
        token_detail = elem.get_attribute("href")
        
        return token_detail
    
    async def get_token_image(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//img[@src]")))
        
        token_image = elem.get_attribute("src")
        
        self.driver.get(token_image)
        
        self.driver.save_screenshot(f"asset/{self.chain}/{self.token}.png")

    async def get_token_name(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[1]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_name = elem.get_attribute("innerText")
             
        return token_name
    
    async def get_token_symbol(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[2]//span[@class='ValueWithKeyword--highlighted']")))
        
        token_symbol = elem.get_attribute("innerText")
             
        return token_symbol
    
    async def get_token_contract(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
    
    async def get_token_contract(self) :
        
        elem = await self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='Table__tbody']/div/div[{self.i}]//div[3]")))
        
        token_contract = elem.get_attribute("innerText")
             
        return token_contract
        