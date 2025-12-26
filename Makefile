# Variables
VENV            := venv
PYTHON          := $(VENV)/bin/python3
PIP             := $(VENV)/bin/pip
DATA_DIR        := data
SNAPSHOT_PATTERN := empire_snapshot_*.json
SNAPSHOT_LATEST := empire_snapshot_latest.json
FB_SESSION_FILE := fb_session.json

# Default goal
.DEFAULT_GOAL := run

# 1. Create venv if it doesn't exist
$(VENV)/bin/activate:
	python3 -m venv $(VENV)

# 2. Install dependencies (depends on venv)
install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt
	$(PYTHON) -m playwright install

# 3. Run the app (depends on install)
run: $(VENV)/bin/activate
	export APPDATA="$$HOME/Library/Application Support"; \
	$(PYTHON) main.py

clean:
	rm -f $(FB_SESSION_FILE)

clean-db:
	cd $(DATA_DIR) && ls -t $(SNAPSHOT_PATTERN) | grep -v '^$(SNAPSHOT_LATEST)$$' | tail -n +2 | xargs -I {} rm -- {}

# Completely remove the environment
nuke:
	rm -rf $(VENV)