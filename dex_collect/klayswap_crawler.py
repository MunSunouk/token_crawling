from base import Crawler
import time
from datetime import datetime
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Klayswap_crawler(Crawler):

    def __init__(self):
        super().__init__()
        
        self.swapPage = 'https://klayswap.com/exchange/swap'
        
        self.connect_network()
        
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

    @retry
    def connect_network(self) :

        self.driver.get(self.swapPage)
        
    def main(self) :
        
        self.click_token_icon()
        result = self.load_token_list()
        
        return result
        
    @retry
    def click_token_icon(self) :
        
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        click_from_icon = self.wait.until(EC.presence_of_element_located((By.XPATH,f'//section[contains(@class,"exchange-swap-page")]/article[1]//div[contains(@class,"ic-wrap")]')))

        self.driver.execute_script("arguments[0].click();", click_from_icon)
        
    @retry
    def load_token_list(self) :
        """scroll down token list"""
        
        j = 1
        result = []
        
        try :
            while True:
                ele = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//section[@class='ps']/div[{j}]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
                token = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//section[@class='ps']/div[{j}]//div[@class='text-symbol']/p[2]"))).get_attribute('innerText')
                result.append(token)
                j = j + 1

                # #below code is just in case you want to break from infinite loop
                # if j > 50:
                #     break
        except :
            return result