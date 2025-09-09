# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

SHELL := bash

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

PROJECTS = numpy scipy pandas scikit-learn scikit-image networkx astropy sunpy
ISSUE_DATA = $(patsubst %, devstats-data/%_issues.json, $(PROJECTS))
PR_DATA = $(patsubst %, devstats-data/%_PRs.json, $(PROJECTS))
REPORTS = $(patsubst %, _generated/%/index.md, $(PROJECTS))

$(REPORTS) : $(ISSUE_DATA) $(PR_DATA)

devstats-data :
	mkdir devstats-data

devstats-data/%_issues.json : | devstats-data
	(cd devstats-data && \
	export URL=$(shell curl -s https://api.github.com/repos/scientific-python/devstats-data/releases/latest | jq -r '.assets[] | select(.name | contains ("devstats-$*.")) | .browser_download_url') && \
	curl -L $$URL | tar xJmf -)

devstats-data/%_PRs.json : devstats-data/%_issues.json

_generated/%/index.md:
	devstats template -o _template $*
	devstats publish -t _template -o _generated $*
	ln -sf $(PWD)/devstats-data _generated/$*

html : $(REPORTS)
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

clean:
	rm -rf _build _template _generated

.PHONY: help clean

## Catch-all target: route all unknown targets to Sphinx using the new
## "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
