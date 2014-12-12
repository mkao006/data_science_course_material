import sys
import MapReduce
import json

mr = MapReduce.MapReduce()

def mapper(records):
    key = records[0]
    value = records[1]
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    for v in list_of_values:
        if v not in mr.intermediate.keys():
            mr.emit((key, v))
            mr.emit((v, key))
        else:
            if key not in mr.intermediate[v]:
                mr.emit((key, v))
                mr.emit((v, key))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)  