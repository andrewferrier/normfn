.PHONY: run

CACHE_BUST ?= $(shell date +%s)
CONTAINER ?= podman

run:
	$(CONTAINER) build -t normfn-demo \
		--build-arg CACHE_BUST=$(CACHE_BUST) \
		.
	clear
	@$(CONTAINER) run -it \
		--rm \
		--hostname normfn-demo \
		normfn-demo bash
