import numpy as np
import utils


#X = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Chandrika_Data_X1.csv', delimiter=",")
X = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Peter_data_X1.csv', delimiter=",")
#y = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/chandrika_Y.csv', delimiter=",")
y = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Peter_data_Y.csv', delimiter=",")
#z = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Chandrika_Testdata1_X1.csv', delimiter=",")
z = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Peter_test_X1.csv', delimiter=",")
#w = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Chandrika_Testdata_Y.csv', delimiter=",")
w = np.genfromtxt ('/Users/chandrikasharma/documents/AI Project Data/Peter_test_y.csv', delimiter=",")
z1 = np.nan_to_num(z)
w1 = np.nan_to_num(w)
X1 = np.nan_to_num(X)
counter = 0
import pdb; pdb.set_trace()
from sklearn import svm

lin_clf = svm.LinearSVC()
lin_clf.fit(X1, y) 


new_array = []
for i in range(len(z1)):
    
    new_array = np.append(new_array, lin_clf.predict([z1[i]]))
print new_array

for j in range(len(w1)):
    if w1[j] == new_array[j]:
        counter = counter + 1
Percentage = (counter*1.0/len(w1))*100
print "Percentage", Percentage

