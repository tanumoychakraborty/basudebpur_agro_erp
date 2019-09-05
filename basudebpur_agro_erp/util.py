'''
Created on 05-Sep-2019

@author: tanumoy
'''


def isFloat(a):
    try:
        float(a)
        return True
    except ValueError:
        return False
    
    
def clearDictionary(a):
    for k, v in dict(a).items():
                if v is None:
                    del a[k]
                elif type(v) is list:
                    for line in a[k]:
                        for k1, v1 in dict(line).items():
                            if v1 is None:
                                del line[k1]
                                
    return a