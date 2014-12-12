import sys
import MapReduce
import json

mr = MapReduce.MapReduce()

def mapper(dna_sequence):
    char = dna_sequence[1]
    value = char[0:len(char) - 10]
    mr.emit_intermediate(1, value)

def reducer(key, list_of_values):
    for v in list(set(list_of_values)):
        mr.emit(v)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)        
        