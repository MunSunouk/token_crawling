from dex_collect import Klayswap_crawler
from chain_collect import Klatnscope_crawler

if __name__ == "__main__" :
    
    test_list = ['wemix']
    
    klaytnscope = Klatnscope_crawler()
    
    elem_text = klaytnscope.main(test_list)
    
    print(elem_text)