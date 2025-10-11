import numpy as np

my_numpy_list=np.arange(0,20)
print(my_numpy_list)
print(my_numpy_list[4])
print(my_numpy_list[0:5])

my_list=np.arange(0,20)

my_numpy_list[0:5]=-10
print(my_numpy_list)

other_list=np.arange(0,15)
print(other_list)
sliced_list=other_list[0:5]
print(sliced_list)
