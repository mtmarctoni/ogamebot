PYTHON := python3.10
PIP := pip3.10
DATA_DIR := data
SNAPSHOT_PATTERN := empire_snapshot_*.json
SNAPSHOT_LATEST := empire_snapshot_latest.json
FB_SESSION_FILE := fb_session.json

run:
	$(PYTHON) main.py

install:
	$(PIP) install -r requirements.txt
	$(PYTHON) -m playwright install

clean:
	rm -f $(FB_SESSION_FILE)

clean-db:
	cd $(DATA_DIR) && ls -t $(SNAPSHOT_PATTERN) | grep -v '^$(SNAPSHOT_LATEST)$$' | tail -n +2 | xargs -I {} rm -- {}