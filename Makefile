.PHONY: install test lint fmt ci

install:
	$(MAKE) -C automation-framework install || true
	$(MAKE) -C cloud-native-app install || true
	$(MAKE) -C ai-testing install || true

lint:
	$(MAKE) -C automation-framework lint || true
	$(MAKE) -C cloud-native-app lint || true
	$(MAKE) -C ai-testing lint || true

fmt:
	$(MAKE) -C automation-framework fmt || true
	$(MAKE) -C cloud-native-app fmt || true
	$(MAKE) -C ai-testing fmt || true

test:
	$(MAKE) -C automation-framework test || true
	$(MAKE) -C cloud-native-app test || true
	$(MAKE) -C ai-testing test || true

ci: install lint test
