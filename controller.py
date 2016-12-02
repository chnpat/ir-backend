from model import *
from model.query import Query
from model.spliter import Spliter
from model.readcsv import CSV_Reader
import math as m

class QueryController:
    '''
    This function will be called from web service to result the list of
    retrieval result

    result:
    [('course_id1', 0.75), ('course_id2', 0.68)]
    '''
    def get_result(self, qr, method='Cosine', exp=False):
        q = Query()
        reader = CSV_Reader()
        q_dict = q.split_query(qr)
        all_d_dict = reader.get_dict("iif_weight.csv")
        result = q.retrieve(q_dict, all_d_dict, method, exp)

        if not result:
            response = []
        elif(result[0][1]) == 1 or m.isnan(result[0][1]):
            response = []
        else:
            response = result

        return response

    def get_JSON(self, tuples_list):
        spl = Spliter()
        return spl.get_JSON(tuples_list)
                
