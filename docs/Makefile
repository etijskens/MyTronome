# Minimal makefile for Sphinx documentation
# Execute this file as from the project`s directory as:
#  > cd path/to/project/docs        # where the Makefile is located
#  > source ../.venv/bin/activate   # activate the project's virtual environment
#  (.venv) > make                   # to generate help
#  (.venv) > make html              # to generate documentation in html format
#  (.venv) > make latexpdf          # to generate documentation in pfd format

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = MyTronome
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile deps venv

# Verify that the right virtual environment is activated
venv:
	@if [ "$$VIRTUAL_ENV" == "" ]; then echo "ERROR: .venv not activated: expecting '`realpath ../.venv`' to be activated."; exit 1; fi
	@if [ "$$VIRTUAL_ENV" -ef "../.venv/" ]; then : ; else echo "ERROR: wrong .venv: expecting '`realpath ../.venv`'"; exit 1; fi
	@echo "Virtual environment ok."

# Install the necessary dependendies for documenting the project.
# (see https://unix.stackexchange.com/questions/153763/dont-stop-makeing-if-a-command-fails-but-check-exit-status)
deps:
ifdef VSC_HOME
	$(warning "VSC_HOME is set: $(VSC_HOME).")
	$(error "The cluster ($(VSC_INSTITUTE_CLUSTER)) is not suitable for building documentation. Use a desktop machine instead")
endif

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile deps
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
