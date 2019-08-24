'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.endpoints import API

ACCESS_RIGHT = API+'/api/access-right'
PURCHASE_TRANSACTION = API+'/api/purchase_trx/'
RECEIPT = API+'/api/receipt/'
RECEIPT_SEARCH = API+ '/api/receipt?'
PURCHASE_ORDER_TYPE = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_TYPE'
PURCHASE_ORDER_HEADER_STATUS = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_HEADER_STATUS'
PURCHASE_ORDER_LINES_STATUS = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_LINES_STATUS'
UNIT_OF_MEASURE = API + '/api/common_lookups?lookupName=UNIT_OF_MEASURE'
ITEM_LIST = API + '/api/inventory_items?OperationType=ITEM_LIST'
SUPPLIER_TYPE = API + '/api/common_lookups?lookupName=SUPPLIER_TYPE'
RECEIPT_LINE_STATUS = API + '/api/common_lookups?lookupName=RECEIPT_LINE_STATUS'
SUPPLIER_LIST = API + '/api/supplier_master?OperationType=SUPPLIER_LIST'
SUPPLIER_SEARCH = API + '/api/supplier_master?OperationType=SUPPLIER_MASTER_SEARCH'
SUPPLIER = API + '/api/supplier_master'
CREATE_CHALLAN = API + '/api/challan'