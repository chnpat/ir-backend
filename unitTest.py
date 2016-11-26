from model import *

term_doc_dict = {"1":{"Hello":1, "World":0, "Python":1},
                 "2":{"Hello":1, "World":1, "Python":1},
                 "3":{"Hello":2, "World":0, "Python":3}}

term_q_dict = {"Hello":1, "World":0, "Python":1}

weight_doc = weighting_doc()
weight_q = weighting_query()

print(weight_doc.tf_idf(term_doc_dict))
print(weight_q.tf_idf(term_q_dict, term_doc_dict))
