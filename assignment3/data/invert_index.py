import MapReduce
import sys
import json

mr = MapReduce.MapReduce()
    
def mapper(record):
    key = record[0]
    value = record[1]
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)    

def reducer(key, list_of_values):
    total = []
    for v in list_of_values:
      total.append(v)
    mr.emit((key, list(set(total))))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)  