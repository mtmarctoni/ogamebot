.ONESHELL:
.DEFAULT_GOAL := run

# Variables editable to your environment
VENV            := venv
PYTHON_VERSION  := 3.12
DATA_DIR        := database
SNAPSHOT_PATTERN := empire_snapshot_*.json
SNAPSHOT_LATEST := empire_snapshot_latest.json
FB_SESSION_FILE := fb_session.json

# Internal variables
PYTHON    		:= python${PYTHON_VERSION}
PIP     		:= pip${PYTHON_VERSION}
PYTHON_GLOBAL   := $(shell which $(PYTHON))
PIP_GLOBAL      := $(shell which ${PIP})
PYTHON_VENV     := $(VENV)/bin/${PYTHON}
PIP_VENV        := $(VENV)/bin/${PIP}
ACTIVATE_VENV   := . $(VENV)/bin/activate &&

# Detect OS and set APPDATA dynamically
UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
    APPDATA_PATH := $(HOME)/Library/Application Support
else
    APPDATA_PATH := $(HOME)/.config
endif

# Declare PHONY targets
.PHONY: install run clean-session clean-db nuke deploy

# 1. Create venv if it doesn't exist
$(VENV)/bin/activate:
	$(PYTHON_GLOBAL) -m venv $(VENV)

# 2. Install dependencies (depends on venv)
install: $(VENV)/bin/activate
	$(ACTIVATE_VENV) $(PIP_VENV) install -r requirements.txt
	$(ACTIVATE_VENV) $(PYTHON_VENV) -m playwright install

# 3. Run the app (depends on install)
run: install
	$(ACTIVATE_VENV) $(PYTHON_VENV) main.py &
	$(ACTIVATE_VENV) $(PYTHON_VENV) config_gui.py

clean-session:
	rm -f $(FB_SESSION_FILE)

clean-db:
	cd $(DATA_DIR) && ls -t $(SNAPSHOT_PATTERN) | grep -v '^$(SNAPSHOT_LATEST)$$' | tail -n +2 | xargs -I {} rm -- {}

# Deploy target to automate pulling, installing, and running
deploy:
	git pull
	make install
	make run
	
# Completely remove the environment
nuke:
	rm -rf $(VENV)
