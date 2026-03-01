ENV=dev

venv:
	python3 -m venv venv \
		&& . venv/bin/activate \
		&& pip install -q -r requirements.txt

.PHONY: check-fmt
check-fmt:
	find $(MODULE) -type f -name '*.tf' -or -name '*.tfvars' -or -name '*.tftest.hcl' | xargs -n1 terraform fmt -check -diff

clean:
	rm -rf venv
