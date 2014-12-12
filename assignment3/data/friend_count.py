import sys
import MapReduce
import json

mr = MapReduce.MapReduce()


def mapper(records):
    keys = records[0]
    values = records[1]
    mr.emit_intermediate(keys, values)
    
def reducer(key, list_of_values):
    number_of_friends = 0
    for friends in list_of_values:
        number_of_friends += 1
    mr.emit((key, number_of_friends))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)  