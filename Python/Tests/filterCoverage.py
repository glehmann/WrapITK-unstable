#!/usr/bin/env python

import commands, sys, re

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
excludeSet = set(["UnaryFunctorImageFilter",
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
filterFiles = commands.getoutput("find /usr/include/InsightToolkit -name 'itk*Filter.h'").splitlines()
filters = set([f.split('/')[-1][len('itk'):-len('.h')] for f in filterFiles]) - excludeSet
fDict = {}
for filterFile in filterFiles :
            d = filterFile.split('/')[4]
	    f = filterFile.split('/')[-1][len('itk'):-len('.h')]
	    fDict[f] = d
			    
# get filter from wrapper files
wrappersFiles = commands.getoutput("find -name 'wrap_itk*Filter*.cmake'").splitlines()
wrappers = set([f.split('/')[-1][len('wrap_itk'):-len('.cmake')].split('_')[0] for f in wrappersFiles])

nonWrapped = filters - wrappers
for f in sorted(nonWrapped) :
	print '%s (%s) is not wrapped' % (f, fDict[f])

print

print
print '%i filters' % len(filters)
print '%i wrapped filters' % len(wrappers)
print '%i non wrapped filters' % len(nonWrapped)
print '%f%% covered' % (len(wrappers) / float(len(filters)) * 100)
