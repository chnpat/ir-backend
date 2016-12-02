import numpy as np
import math as m

class Similarity:
    def __init__(self):
        self.word_list = []
        self.q_list = []
        self.d_list = []

    '''
    the input of extract term function
    ----------
    q_dict = {"term1":0, "term2":0, ...}
    d_dict = {"term1":0, "term2":0, ...}
    ==========
    '''
    def extract_term(self, d_dict, q_dict):
        self.word_list = []
        self.q_list = []
        self.d_list = []
        for (k,v) in q_dict.items():
            if v != 0:
                if d_dict.has_key(k):
                    self.word_list.append(k)
                    self.q_list.append(v)
                    self.d_list.append(d_dict[k])


    def sim(self, d_dict, q_dict, method):
        self.extract_term(d_dict, q_dict)
        d_arr = np.array(self.d_list)
        q_arr = np.array(self.q_list)
        if method == "Cosine":
            return self.cos_sim(d_arr, q_arr)
        elif method == "Jaccard":
            return self.jac_sim(d_arr, q_arr)
        elif method == "Euclidean":
            return self.euc_sim(d_arr, q_arr)
        else:
            return self.man_sim(d_arr, q_arr)
        
    '''
    Cosine Similarity
    '''
    def compute_vect_norm(self, vector):
        return m.sqrt(sum([m.pow(i, 2) for i in vector]))
    
    def cos_sim(self, d_arr, q_arr):
        norm = self.compute_vect_norm(d_arr) * self.compute_vect_norm(q_arr)
        dot = np.dot(d_arr, q_arr)
        print(dot, norm)
        if norm != 0.0:
            return dot/norm
        else:
            return 0.0

    '''
    Jaccard Similarity
    '''
    def jac_sim(self, d_arr, q_arr):
        arr = np.array([d_arr, q_arr])
        part = np.sum(np.min(arr, axis = 0))
        whole = np.sum(np.max(arr, axis = 0))
        return part/whole

    '''
    Euclidean Similarity
    '''
    def euc_sim(self, d_arr, q_arr):
        diff = np.subtract(d_arr, q_arr)
        return 1 - m.sqrt(np.sum(diff**2))


    '''
    Manhattan Similarity
    '''
    def man_sim(self, d_arr, q_arr):
        return 1 - np.sum(np.abs(np.subtract(d_arr, q_arr)))
        
