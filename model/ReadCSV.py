import os

class CSV_Reader:
    def __init__(self):
        self.term_list = []
        self.doc_list = []
        
    def get_dict(self, csv_file_name):
        result_dict = {}
        if os.path.isfile(csv_file_name): 
            csv_file = open(csv_file_name)
            self.term_list += [str(t) for t in csv_file.readline().split(',')[1:-1]]
            for line in csv_file:
                doc_id, word_freq_list = line.split(',')[:1], [float(i) for i in line.split(',')[1:-1]]
                self.doc_list += doc_id
                result_dict[doc_id[0]] = dict(zip(self.term_list, word_freq_list))
            csv_file.close()
        return result_dict

    def save_dict(self, weight_dict, csv_file_name):
        outfile = open(csv_file_name, 'w')
        if len(self.term_list) > 0:
            outfile.write('Document')
            for word in self.term_list:
                outfile.write(',' + word)
            outfile.write('\n')
            for doc in self.doc_list:
                outfile.write(doc)
                for term in self.term_list:
                    outfile.write(','+str(weight_dict[doc][term]))
                outfile.write('\n')
        outfile.close()

            
            
