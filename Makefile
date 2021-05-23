.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: worker
worker:
	python worker.py

.PHONY: server
server:
	python main.py
