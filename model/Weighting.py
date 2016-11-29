import math as m, numpy as np

class weighting_doc:
    '''
    ------------
    Term-Document Matrix is stored in dictionary format as following
    ------------
    term_doc_dict = {'course_id1': {'term1': 0, 'term2': 1}, 'course_id2': ...}
    ============
    '''
    def calculate_tf(self, term_doc_dict):
        for (doc_id, term) in term_doc_dict.items():
            for (k,v) in term.items():
                if v != 0:
                    term_doc_dict[doc_id][k] = 1 + m.log(v,2)
                else:
                    term_doc_dict[doc_id][k] = 0
        print("Term Frequency Calculation DONE!!")
        return term_doc_dict

    def calculate_idf(self, term_doc_dict, term):
        ni = 0
        for (doc_id, terms) in term_doc_dict.items():
            if term in terms.keys():
                if terms[term] != 0:
                    ni += 1
        N = len(term_doc_dict)
        return m.log((float(N)/ni),2)

    def tf_idf(self, term_doc_dict):
        term_doc_dict = self.calculate_tf(term_doc_dict)
        count = 0
        for (doc_id, terms) in term_doc_dict.items():
            print(str(count+1)+"/"+str(len(term_doc_dict)))
            for (k, v) in terms.items():
                term_doc_dict[doc_id][k] = v * self.calculate_idf(term_doc_dict, k)
            count += 1
        print("Term Weighting using TF-IDF DONE!!")
        return term_doc_dict


class weighting_query:
    '''
    ------------
    Term-Query Matrix is stored in dictionary format as following
    ------------
    term_q_dict = {'term1': 0, 'term2': 1, ...}
    ============
    '''
    
    def calculate_tf(self, term_q_dict):
        for (term, freq) in term_q_dict.items():
            if freq != 0:
                term_q_dict[term] = 1 + m.log(freq, 2)
            else:
                term_q_dict[term] = 0
        print("Term Frequency Calculation DONE!!")
        return term_q_dict

    def calculate_idf(self, term_doc_dict, term):
        return weighting_doc().calculate_idf(term_doc_dict, term)
    
    def tf_idf(self, term_q_dict, term_doc_dict):
        term_q_dict = self.calculate_tf(term_q_dict)
        for (term, tf) in term_q_dict.items():
            if term in term_doc_dict.values()[0].keys():
                term_q_dict[term] = term_q_dict[term] * self.calculate_idf(term_doc_dict, term)
            else:
                term_q_dict[term] = 0
        print("Term Weight of Query using TF-IDF DONE!!")
        return term_q_dict
