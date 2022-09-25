import json
from pathlib import Path
import os

class Token(object) :

    def __init__(self) :

        self.name = None
        self.symbol = None
        self.contract = None
        self.detail = None
        
    def set_token(self) -> dict :
        '''
        get balance of token in wallet

        Returns
        -------
        "oUSDT" : {
            "id" : 2,
            "name" : "Orbit Bridge Klaytn USD Tether",
            "symbol" : "oUSDT",
            "contract" : {
                "klaytn" : "0xcee8faf64bb97a73bb51e115aa89c17ffa8dd167",
                "polygon" : "0x957da9EbbCdC97DC4a8C274dD762EC2aB665E15F"
            },
            "decimal" : 6,
            "detail" : None,
            "info" : "https://bridge.orbitchain.io/"
        }
        '''
    
        tokenDictPath = os.path.join("list", "token_list.json")
        
        if Path(tokenDictPath).exists() :
            with open(tokenDictPath, "rt", encoding="utf-8") as f:
                tokenDict = json.load(f)
        else :
            print("tokenDictPath doesnt exist")
            return {}

        return tokenDict
    
    def save_token(self,tokens) :
        
        tokenDictPath = os.path.join("list", "token_list.json")
        
        if Path(tokenDictPath).exists() :
            with open(tokenDictPath, 'w', encoding="utf-8") as f:     
                json.dump(tokens, f, indent=4)
                
        else :
            print("tokenDictPath doesnt exist")
            

