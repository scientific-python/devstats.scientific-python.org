# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

_generated/numpy.md:
	devstats publish numpy

_generated/scipy.md:
	devstats publish scipy

_generated/matplotlib.md:
	devstats publish matplotlib

_generated/pandas.md:
	devstats publish pandas

_generated/scikit-learn.md:
	devstats publish scikit-learn

_generated/scikit-image.md:
	devstats publish scikit-image

_generated/networkx.md:
	devstats publish networkx

_generated/astropy.md:
	devstats publish astropy

_generated/sunpy.md:
	devstats publish sunpy

html : _generated/numpy.md _generated/scipy.md _generated/matplotlib.md _generated/pandas.md _generated/scikit-learn.md _generated/scikit-image.md _generated/networkx.md _generated/astropy.md _generated/sunpy.md
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

clean: 
	rm -rf _build _generated

.PHONY: help clean

## Catch-all target: route all unknown targets to Sphinx using the new
## "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
