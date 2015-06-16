# These targets are not files
.PHONY: contribute travis test lint coverage

clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov violations.txt

todo:
	# Look for areas of the code that need updating when some event has taken place
	grep --exclude-dir=components -rnH TODO reqs
	grep --exclude-dir=components -rnH TODO accounting
	grep --exclude-dir=components -rnH TODO tests

publish:
	git push --tag origin master
	rm -rf dist/*
	python setup.py sdist
	twine upload dist/*


## Testing

lint:
	./lint.sh

test:
	./runtests.py tests

coverage:
	coverage run ./runtests.py --with-xunit tests
	coverage xml -i

# This target is run on Travis.ci. We lint, test and build.
# We don't call 'install' first as that is run as a separate part
# of the Travis build process.
travis: lint coverage


## Install / Upgrade

install:
	pip install -r requirements.txt

upgrade:
	pip install --upgrade -r requirements.txt
