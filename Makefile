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

# Default goal
.DEFAULT_GOAL := run

# 1. Create venv if it doesn't exist
$(VENV)/bin/activate:
	$(PYTHON_GLOBAL) -m venv $(VENV)

# 2. Install dependencies (depends on venv)
install: $(VENV)/bin/activate
	$(PIP_VENV) install -r requirements.txt
	$(PYTHON_VENV) -m playwright install

# 3. Run the app (depends on install)
run: $(VENV)/bin/activate
	export APPDATA="$$HOME/Library/Application Support"; \
	$(PYTHON_VENV) main.py

clean-session:
	rm -f $(FB_SESSION_FILE)

clean-db:
	cd $(DATA_DIR) && ls -t $(SNAPSHOT_PATTERN) | grep -v '^$(SNAPSHOT_LATEST)$$' | tail -n +2 | xargs -I {} rm -- {}

# Completely remove the environment
nuke:
	rm -rf $(VENV)