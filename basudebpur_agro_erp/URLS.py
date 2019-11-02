'''
Created on 08-Dec-2018

@author: tanumoy
'''
from basudebpur_agro_erp.endpoints import API

ACCESS_RIGHT = API+'/api/access-right'
PURCHASE_TRANSACTION = API+'/api/purchase_trx/'
SALES_TRANSACTION = API+'/api/sales_trx/'
RECEIPT = API+'/api/receipt/'
RECEIPT_SEARCH = API+ '/api/receipt?'
PURCHASE_ORDER_TYPE = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_TYPE'
SALES_ORDER_TYPE = API + '/api/common_lookups?lookupName=SALES_ORDER_TYPE'
PURCHASE_ORDER_HEADER_STATUS = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_HEADER_STATUS'
PURCHASE_ORDER_LINES_STATUS = API + '/api/common_lookups?lookupName=PURCHASE_ORDER_LINES_STATUS'
SALES_ORDER_HEADER_STATUS = API + '/api/common_lookups?lookupName=SALES_ORDER_HEADER_STATUS'
UNIT_OF_MEASURE = API + '/api/common_lookups?lookupName=UNIT_OF_MEASURE'
ITEM_LIST = API + '/api/inventory_items?OperationType=ITEM_LIST'
ITEM_DETAILS = API + '/api/inventory_items?item_id='
RECEIPT_LINE_STATUS = API + '/api/common_lookups?lookupName=RECEIPT_LINE_STATUS'
RECEIPT_HEADER_STATUS = API + '/api/common_lookups?lookupName=RECEIPT_HEADER_STATUS'
SUPPLIER_TYPE = API + '/api/common_lookups?lookupName=SUPPLIER_TYPE'
SUPPLIER_LIST = API + '/api/supplier_master?OperationType=SUPPLIER_LIST'
SUPPLIER_SEARCH = API + '/api/supplier_master?OperationType=SUPPLIER_MASTER_SEARCH'
SUPPLIER = API + '/api/supplier_master'
CUSTOMER_TYPE = API + '/api/common_lookups?lookupName=CUSTOMER_TYPE'
CUSTOMER_LIST = API + '/api/customer_master?OperationType=CUSTOMER_LIST'
CUSTOMER = API + '/api/customer_master'
CUSTOMER_SEARCH = API + '/api/customer_master?OperationType=CUSTOMER_MASTER_SEARCH'
CREATE_CHALLAN = API + '/api/challan'