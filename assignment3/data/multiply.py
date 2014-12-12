import sys
import MapReduce
import json



mr = MapReduce.MapReduce()

def mapper(vector):
    if vector[0] == "a":
        for col_num in range(5):
            mr.emit_intermediate((vector[1], col_num), \
                                 [('a', vector[2]), vector[3]])
    elif vector[0] == "b":
        for row_num in range(5):
            mr.emit_intermediate((row_num, vector[2]), \
                                 [('b', vector[1]), vector[3]])


def reducer(key, list_of_values):
    indexa = [items[0][1] for items in list_of_values\
              if items[0][0] == 'a']
    indexb = [items[0][1] for items in list_of_values\
              if items[0][0] == 'b']
    intersection_index = list(set(indexa).intersection(indexb))

    value = 0
    for index in intersection_index:
        aval = [items[1] for items in list_of_values\
                if items[0][0] == 'a' and items[0][1] == index]
        bval = [items[1] for items in list_of_values\
                if items[0][0] == 'b' and items[0][1] == index]
        value += aval[0] * bval[0]
        
    mr.emit((key[0], key[1], value))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)  
    