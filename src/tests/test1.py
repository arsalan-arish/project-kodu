lst = [[0,0], [1,1]]
print(lst)
for num in lst:
    num.append(5)
print(lst)


#* In a foreach loop in python, the variable infront of 'num' only holds reference to the object
#* inside that iterable. If that object is mutable and you mutate it, it will mutate the object 
#* inside the iterable too. If that object is immutable, then reassigning the reference variable
#* will only reassign to the that variable itself and definitely not the object inside that iterable