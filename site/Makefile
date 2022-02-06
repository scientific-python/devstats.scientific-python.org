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

_generated/numpy.md: analysis_template.md
	python tools/generate_from_template.py numpy

_generated/scipy.md: analysis_template.md
	python tools/generate_from_template.py scipy

_generated/matplotlib.md: analysis_template.md
	python tools/generate_from_template.py matplotlib

_generated/pandas.md: analysis_template.md
	python tools/generate_from_template.py pandas

_generated/scikit-learn.md: analysis_template.md
	python tools/generate_from_template.py scikit-learn

_generated/scikit-image.md: analysis_template.md
	python tools/generate_from_template.py scikit-image

_generated/networkx.md: analysis_template.md
	python tools/generate_from_template.py networkx

html : _generated/numpy.md _generated/scipy.md _generated/matplotlib.md _generated/pandas.md _generated/scikit-learn.md _generated/scikit-image.md _generated/networkx.md
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

clean: 
	rm -rf _build _generated

.PHONY: help clean

## Catch-all target: route all unknown targets to Sphinx using the new
## "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
