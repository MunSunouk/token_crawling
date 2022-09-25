from dex_collect import Klayswap_crawler, klayswap_crawler
from chain_collect import Klatnscope_crawler
import os
import asyncio

if __name__ == "__main__" :
    
    #test
    token_list = ['wemix']
    
    # klayswap_crawler = Klayswap_crawler()
    
    # token_list = klayswap_crawler.main()
    
    klaytnscope = Klatnscope_crawler()
    
    # klaytnscope.main(token_list)
    
    klaytnscope.token = token_list[0]
    
    result = asyncio.run(klaytnscope.parse_token_info())
    
    print(result)
    
    
