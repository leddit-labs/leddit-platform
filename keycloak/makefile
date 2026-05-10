.PHONY: setup start stop reset logs

setup:
	@bash scripts/init-keycloak.sh

start:
	docker compose up -d

stop:
	docker compose down

reset:
	docker compose down -v
	cd terraform && rm -f terraform.tfstate* .terraform.lock.hcl

logs:
	docker compose logs -f keycloak