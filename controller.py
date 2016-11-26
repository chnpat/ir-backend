from model import *

x = weighting_doc()
print(x.tf_idf([0]))
y = weighting_query()
print(y.tf_idf([0]))
