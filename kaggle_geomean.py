from __future__ import division
from collections import defaultdict
from glob import glob
import sys
import math

glob_files = sys.argv[1]
loc_outfile = sys.argv[2]
method = "average"
weights="uniform"

if method == "average":
    combined_row_predictions = {}
with open(loc_outfile,"wb") as outfile:
    for file_idx, glob_file in enumerate( glob(glob_files) ):
        print "parsing:", glob_file
        # sort glob_file by first column, ignoring the first line
        lines = open(glob_file).readlines()
        lines = [lines[0]] + sorted(lines[1:])
        for line_idx, line in enumerate( lines ):
  #        print "{0}, {1}".format(file_idx, line_idx)

          # add headings
          if file_idx == 0 and line_idx == 0:
              outfile.write(line)
              continue

          row_predictions = line.strip().split(",")

          # initialise multiplication
          if file_idx == 0 and line_idx > 0:
              combined_row_predictions[row_predictions[0]] = [ float(math.log(1)) for i in range(len(row_predictions[1:])) ]

          if line_idx > 0:
              current_total = combined_row_predictions[row_predictions[0]]
              combined_row_predictions[row_predictions[0]] = [a+math.log(float(b)) for a,b in zip(current_total, row_predictions[1:])]
              
    for k,v in combined_row_predictions.iteritems():
        csv_predictions = ",".join(map(str, [math.exp(prediction * 1/(file_idx+1)) for prediction in combined_row_predictions[k]]))
        outfile.write("{0},{1}\n".format(k,csv_predictions))
print("wrote to %s"%loc_outfile)
