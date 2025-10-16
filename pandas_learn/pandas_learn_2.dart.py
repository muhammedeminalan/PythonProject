import  pandas as pd
import numpy as np

#series
my_dict = {'a': 1, 'b': 2, 'c': 3}
print(pd.Series(my_dict))

numpy_array = np.arange(0,8)
print(pd.Series(numpy_array))
numpy_array2 = np.array(['a', 'b', 'c', 'd'])
print(pd.Series(numpy_array2))

