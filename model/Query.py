import re
from model.spliter import Spliter
from model.similarity import Similarity
import operator

class Query:
    def split_query(self, query):
        spl = Spliter()
        query_list = [ spl.stemmer(t) for t in re.sub(r'[^a-zA-Z0-9 \n\.]',' ',query.lower()).strip().split()]
        q_dict = spl.get_all_term()
        print(query_list)
        for q in query_list:
            if q in q_dict: 
                q_dict[q] += 1
        return q_dict

    def print_result(self, tuples):
        count = 1
        for doc, sim in tuples:
            print(str(count) + ": " + str(doc) + " | Sim = "+str(sim))
            count += 1
        
    def retrieve(self, q_dict, all_d_dict, method, expand):
        sim_dict = {}
        s = Similarity()
        for (doc_id, term_dict) in all_d_dict.items():
            sim_dict[doc_id] = round(s.sim(term_dict, q_dict, method),4)
            
        sort_sim = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sort_sim
