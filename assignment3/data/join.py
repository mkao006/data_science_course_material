import json
import sys
import MapReduce

mr = MapReduce.MapReduce()

def mapper(database):
    key = database[1]
    value = database[3:]
    transaction = [database[0]]
    mr.emit_intermediate(key, [transaction[0], database])

def reducer(key, list_of_values):
    order = [item[1] for item in list_of_values if item[0] == 'order']
    items = [item[1] for item in list_of_values if item[0] == 'line_item']
    for item in items:
        mr.emit(order[0] + item)
    

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)  
    