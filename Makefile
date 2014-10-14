# These targets are not files
.PHONY: contribute travis test lint coverage

install:
	pip install -r requirements.txt
	python setup.py develop

sync:
	python manage.py migrate

lint:
	./lint.sh

test:
	./runtests.py tests

coverage:
	coverage run ./runtests.py --with-xunit
	coverage html -i

# This target is run on Travis.ci. We lint, test and build the sandbox/demo sites as well
# as testing migrations apply correctly. We don't call 'install' first as that is run
# as a separate part of the Travis build process.
travis: lint coverage

clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov violations.txt

todo:
	# Look for areas of the code that need updating when some event has taken place
	grep --exclude-dir=components -rnH TODO reqs
	grep --exclude-dir=components -rnH TODO accounting
	grep --exclude-dir=components -rnH TODO tests
