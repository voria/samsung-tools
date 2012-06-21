PEP8_OPTIONS ?= --max-line-length=120 --exclude=build/*

# Set to false to skip all download steps
ONLINE = true
ifeq ($(ONLINE),true)
	WGET_OPTIONS = --timestamp
else
	WGET_OPTIONS = --no-clobber
endif

BUILD_DIRECTORY ?= build

FIND = /usr/bin/find
GIT = /usr/bin/git
LN = /usr/bin/ln
MAKE = /usr/bin/make
MKDIR = /usr/bin/mkdir
PYTHON = /usr/bin/python
TAR = /usr/bin/tar
VENV = /usr/bin/virtualenv
WGET = /usr/bin/wget $(WGET_OPTIONS)
XARGS = /usr/bin/xargs

# Use METHOD=git to check only files in the Git index or working tree
METHOD = find
ifeq ($(METHOD),git)
	python_files_run = $(GIT) ls-files -z '*.py' | $(XARGS) -0
else ifeq ($(METHOD),find)
	python_files_run = $(FIND) . -type f -name '*.py' -exec printf '%s\0' {} + | $(XARGS) -0
endif

PYTHON_VERSION ?= $(shell $(PYTHON) --version | cut -d ' ' -f 2 | cut -d '.' -f 1-3)
PYTHON_NAME ?= Python-$(PYTHON_VERSION)
PYTHON_SOURCE_DIRECTORY ?= $(PYTHON_BUILD_DIRECTORY)/$(PYTHON_NAME)
PYTHON_PREFIX ?= $(realpath $(PYTHON_BUILD_DIRECTORY))/$(PYTHON_NAME)-install
PYTHON_TARBALL ?= $(PYTHON_NAME).tgz
PYTHON_TARBALL_PATH ?= $(PYTHON_BUILD_DIRECTORY)/$(PYTHON_TARBALL)
PYTHON_DOWNLOAD_URL ?= https://www.python.org/ftp/python/$(PYTHON_VERSION)/$(PYTHON_TARBALL)
PYTHON_MAKEFILE ?= $(PYTHON_SOURCE_DIRECTORY)/Makefile
PYTHON_SOURCE_EXECUTABLE ?= $(PYTHON_SOURCE_DIRECTORY)/python
PYTHON_EXECUTABLE ?= $(PYTHON_PREFIX)/bin/python$(python_short_version)

VENV_VERSION ?= $(shell $(VENV) --version)
VENV_NAME ?= virtualenv-$(VENV_VERSION)
VENV_SOURCE_DIRECTORY ?= $(VENV_BUILD_DIRECTORY)/$(VENV_NAME)
VENV_TARBALL ?= $(VENV_NAME).tar.gz
VENV_TARBALL_PATH ?= $(VENV_BUILD_DIRECTORY)/$(VENV_TARBALL)
VENV_DOWNLOAD_URL ?= https://pypi.python.org/simple/virtualenv/
VENV_EXECUTABLE ?= $(VENV_SOURCE_DIRECTORY)/virtualenv.py

VENV_DIRECTORY ?= $(PYTHON_BUILD_DIRECTORY)/virtualenv-$(PYTHON_VERSION)

pep8_executable = $(VENV_DIRECTORY)/bin/pep8

PYTHON_BUILD_DIRECTORY ?= $(BUILD_DIRECTORY)/python
python_version_numbers = $(wordlist 1,3,$(subst ., ,$(PYTHON_VERSION)))
python_version_major = $(word 1,$(python_version_numbers))
python_version_minor = $(word 2,$(python_version_numbers))
python_version_patch = $(word 3,$(python_version_numbers))
python_short_version = $(python_version_major).$(python_version_minor)

VENV_BUILD_DIRECTORY ?= $(PYTHON_BUILD_DIRECTORY)/virtualenv

.PHONY: python-pep8
python-pep8: $(VENV_DIRECTORY) $(pep8_executable)
	. $(VENV_DIRECTORY)/bin/activate && $(python_files_run) $(pep8_executable) $(PEP8_OPTIONS)

$(PYTHON_TARBALL_PATH): $(PYTHON_BUILD_DIRECTORY)
	$(WGET) --directory-prefix $(PYTHON_BUILD_DIRECTORY) $(PYTHON_DOWNLOAD_URL)

# Two targets in one to work around 1-second resolution on Make timestamps
$(PYTHON_MAKEFILE): $(PYTHON_TARBALL_PATH)
	$(TAR) --extract --gzip --directory $(dir $(PYTHON_TARBALL_PATH)) --file $(PYTHON_TARBALL_PATH)
	cd $(PYTHON_SOURCE_DIRECTORY) && ./configure --prefix $(PYTHON_PREFIX)

$(PYTHON_SOURCE_EXECUTABLE): $(PYTHON_MAKEFILE)
	$(MAKE) -C $(PYTHON_SOURCE_DIRECTORY)

$(PYTHON_EXECUTABLE): $(PYTHON_SOURCE_EXECUTABLE)
	$(MAKE) -C $(PYTHON_SOURCE_DIRECTORY) install

$(VENV_TARBALL_PATH): $(VENV_BUILD_DIRECTORY)
	$(WGET) --accept=$(VENV_TARBALL) --directory-prefix $(VENV_BUILD_DIRECTORY) --no-directories --recursive $(VENV_DOWNLOAD_URL)

$(VENV_SOURCE_DIRECTORY): $(VENV_TARBALL_PATH)
	$(TAR) --extract --gzip --directory $(dir $(VENV_TARBALL_PATH)) --file $(VENV_TARBALL_PATH)

$(VENV_EXECUTABLE): $(VENV_SOURCE_DIRECTORY)

$(VENV_DIRECTORY): $(PYTHON_EXECUTABLE) $(VENV_EXECUTABLE)
	$(VENV_EXECUTABLE) --python=$(PYTHON_EXECUTABLE) $(VENV_DIRECTORY)

.PHONY: $(pep8_executable)
$(pep8_executable): $(VENV_DIRECTORY)
	. $(VENV_DIRECTORY)/bin/activate && pip install pep8

.PHONY: clean-python
clean-python: clean-python-build clean-python-virtualenv

.PHONY: clean-python-build
clean-python-build:
	$(RM) -r $(PYTHON_BUILD_DIRECTORY)

.PHONY: clean-python-virtualenv
clean-python-virtualenv:
	$(RM) -r $(VENV_DIRECTORY)

$(PYTHON_BUILD_DIRECTORY) $(VENV_BUILD_DIRECTORY):
	$(MKDIR) --parent $@
