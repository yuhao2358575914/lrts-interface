import os

path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path2 =os.path.dirname(os.path.abspath(__file__))
path3=os.path.abspath(__file__)
print(path3)
print(path2)

print(path1)
