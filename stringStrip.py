# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:01:50 2022

@author: A02234125
"""

stringTest = "ghfe-gh"

def alphaStrip(string):
    
    out = ""
    
    for i in range(len(string)):
        
        if string[i].isalpha():
            out = out+string[i]
            
    return(out)

out = alphaStrip(stringTest)

print(out)