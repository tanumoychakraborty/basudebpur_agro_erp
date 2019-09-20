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
    
    
def clearDictionary(a, replace=None):
    if replace is None:
        if type(a) is list:
            for child in a:
                for k, v in dict(child).items():
                            if v is None:
                                del child[k]
                            elif type(v) is list:
                                for line in child[k]:
                                    for k1, v1 in dict(line).items():
                                        if v1 is None:
                                            del line[k1]
                                    
        else:
            for k, v in dict(a).items():
                            if v is None:
                                del a[k]
                            elif type(v) is list:
                                for line in a[k]:
                                    for k1, v1 in dict(line).items():
                                        if v1 is None:
                                            del line[k1]
    else:
        if type(a) is list:
            for child in a:
                for k, v in dict(child).items():
                            if v is None:
                                child[k] = replace
                            elif type(v) is list:
                                for line in child[k]:
                                    for k1, v1 in dict(line).items():
                                        if v1 is None:
                                            line[k1] = replace
                                    
        else:
            for k, v in dict(a).items():
                            if v is None:
                                a[k] = replace
                            elif type(v) is list:
                                for line in a[k]:
                                    for k1, v1 in dict(line).items():
                                        if v1 is None:
                                            line[k1] = replace
    
    return a