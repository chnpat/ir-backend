from model import *
import math as m

class controller:
    '''
    This function will be called from web service to result the list of
    retrieval result

    result:
    [('course_id1', 0.75), ('course_id2', 0.68)]
    '''
    def get_result(self, qr, method, exp):
        q = query()
        reader = CSV_Reader()
        q_dict = q.split_query(qr)
        all_d_dict = reader.get_dict("iif_weight.csv")
        result = q.retrieve(q_dict, all_d_dict, method, exp)
        if(result[0][1]) == 1 or m.isnan(result[0][1]):
            return []
        else:
            return result

    def get_JSON(self, tuples_list):
        spl = Spliter()
        return spl.get_JSON(tuples_list)
                
