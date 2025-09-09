# pre-commit helper targets
.PHONY: install test lint fmt ci

install:
	$(MAKE) -C automation-framework install || true
	$(MAKE) -C cloud-native-app install || true
	$(MAKE) -C ai-test-generation install || true

lint:
	$(MAKE) -C automation-framework lint || true
	$(MAKE) -C cloud-native-app lint || true
	$(MAKE) -C ai-test-generation lint || true

fmt:
	$(MAKE) -C automation-framework fmt || true
	$(MAKE) -C cloud-native-app fmt || true
	$(MAKE) -C ai-test-generation fmt || true

test:
	$(MAKE) -C automation-framework test || true
	$(MAKE) -C cloud-native-app test || true
	$(MAKE) -C ai-test-generation test || true

ci: install lint test

pre-commit-install:
	pre-commit install || true

pre-commit-run:
	pre-commit run --all-files || true
