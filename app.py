from dex_collect import Klayswap_crawler, klayswap_crawler
from chain_collect import Klatnscope_crawler
import os

if __name__ == "__main__" :
    
    #test
    # token_list = ['wemix']
    
    klayswap_crawler = Klayswap_crawler()
    
    token_list = klayswap_crawler.main()
    
    print(token_list)
    
    klaytnscope = Klatnscope_crawler()
    
    klaytnscope.main(token_list)
