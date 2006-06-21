#!/usr/bin/env python

import sys, commands

segfaultFile = file(sys.argv[1], "w")

lastClass = None
ret = 1
while ret != 0:
  command = "python returnedTypeCoverage.py -v5 --exclude "+sys.argv[1]
  if lastClass:
      command += " --start-from "+lastClass
  # print command
  (ret, output) = commands.getstatusoutput( command )
  if ret != 0:
    # find last args (the ones which caused the segfault)
    faultyArgs = None
    for l in reversed(output.splitlines()):
      if l.startswith('('):
        faultyArgs = l
      if faultyArgs != None :
	# find the last class
	if len(l) != 0 and l[0].isupper():
	  lastClass = l
	  break
    print faultyArgs
    segfaultFile.write(faultyArgs+"\n")
    segfaultFile.flush()
    
