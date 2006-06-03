#!/usr/bin/env python

import sys, re, itk, os
from sys import argv

# python 2.3 compatibility
if sys.version < '2.4' :
        # set compatibility
        import sets
        set = sets.Set

        def sorted(iterable, cmp=None, key=None, reverse=False) :
	    i = list(iterable)
	    if key :
		d = {}
		for v in iterable :
		    k = key(v)
		    if not d.has_key(k) :
			d[k] = []
		    d[k].append(v)
		keys = d.keys()
		keys.sort(cmp)
		i = []
		for k in keys :
		    i += d[k]
	    else :
		i.sort(cmp)
	    if reverse :
		i.reverse()
	    return i

# declares filter which will not be wrapped
excluded = set([
  "UnaryFunctorImageFilter",
  "ReconstructionImageFilter",
  "PadImageFilter",
  "ObjectMorphologyImageFilter",
  "MovingHistogramDilateImageFilter",
  "MovingHistogramErodeImageFilter",
  "MovingHistogramImageFilter",
  "MovingHistogramMorphologicalGradientImageFilter",
  "MovingHistogramMorphologyImageFilter",
  "MorphologyImageFilter",
  "FFTWRealToComplexConjugateImageFilter",
  "FFTWComplexConjugateToRealImageFilter",
  "FFTRealToComplexConjugateImageFilter",
  "FFTComplexConjugateToRealImageFilter",
  "SCSLComplexConjugateToRealImageFilter",
  "SCSLRealToComplexConjugateImageFilter",
  "BinaryMorphologyImageFilter",
  "BinaryFunctorImageFilter",
  "TernaryFunctorImageFilter",
  "ShiftScaleInPlaceImageFilter",
  "FastIncrementalBinaryDilateImageFilter",
  "BasicMorphologicalGradientImageFilter",
  "TwoOutputExampleImageFilter",
  "NaryFunctorImageFilter",
  "NonThreadedShrinkImageFilter",
  "RegionGrowImageFilter",
  "ConnectedComponentFunctorImageFilter",
  "BasicDilateImageFilter",
  "BasicErodeImageFilter",
  "BasicErodeImageFilter",
  "AdaptImageFilter",
  ])


# get filters from sources
headers = sum([ f for p,d,f in os.walk(argv[1]) ], [])
filters = set([f[len('itk'):-len('.h')] for f in headers if f.endswith("Filter.h")]) - excluded

# get filter from wrapper files
# remove filters which are not in the toolkit (external projects, PyImageFilter, ...)
wrapped = set([a for a in dir(itk) if a.endswith("Filter")]).intersection(filters)

nonWrapped = filters - wrapped

for f in sorted(nonWrapped) :
	print '%s is not wrapped' % f

print

print
print '%i filters' % len(filters)
print '%i wrapped filters' % len(wrapped)
print '%i non wrapped filters' % len(nonWrapped)
print '%f%% covered' % (len(wrapped) / float(len(filters)) * 100)
