SHELL := /bin/bash
OS := $(shell uname -s)

PY := python3
VENV := .venv
ACT := source $(VENV)/bin/activate

.PHONY: install dev run service test build-flipper flash-flipper clean

install:
	@if [ "$(OS)" = "Darwin" ]; then ./scripts/install_macos.sh; \
	elif [ "$(OS)" = "Linux" ]; then ./scripts/install_linux.sh; \
	else powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1; fi

dev:
	$(PY) -m venv $(VENV); \
	$(ACT) && pip install -r requirements.txt && pip install -e .[dev]

run:
	$(PY) -m venv $(VENV); \
	$(ACT) && pip install -r requirements.txt >/dev/null; \
	$(ACT) && PYTHONPATH=src \
	python src/main.py run --profile $${PROFILE:-demo_indoor} --device $${DEVICE:-file} \
	$${FREQ:+--freq $$FREQ} $${SR:+--sample-rate $$SR} $${HOST:+--host $$HOST} $${IQ:+--iq $$IQ}

service:
	sudo cp system/spectrumd.service /etc/systemd/system/spectrumd.service; \
	sudo mkdir -p /etc/spectrumd; \
	sudo cp system/spectrumd.env /etc/spectrumd/spectrumd.env; \
	sudo systemctl daemon-reload; \
	sudo systemctl enable spectrumd; \
	sudo systemctl start spectrumd; \
	sudo systemctl status --no-pager spectrumd

build-flipper:
	./scripts/setup_flipper_toolchain.sh && make -C flipper/app

flash-flipper:
	@echo "Copy the built .fap to your Flipper's apps folder using qFlipper or mass storage."

test:
	$(PY) -m venv $(VENV); \
	$(ACT) && pip install -r requirements.txt >/dev/null; \
	$(ACT) && PYTHONPATH=src pytest -q

clean:
	rm -rf $(VENV) build dist __pycache__ .pytest_cache logs/*.jsonl
