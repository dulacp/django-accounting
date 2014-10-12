# These targets are not files
.PHONY: contribute ci test lint

install:
	pip install --upgrade -r reqs/dev.txt

sync:
	python manage.py migrate

lint:
	./lint.sh

test:
	./runtests.py tests

coverage:
	coverage run ./runtests.py --with-xunit
	coverage html -i

ci: install lint
	# Run continous tests and generate lint reports
	./runtests.py --with-coverage --with-xunit
	coverage xml -i

clean:
	# Remove files not in source control
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov violations.txt

todo:
	# Look for areas of the code that need updating when some event has taken place
	grep --exclude-dir=components -rnH TODO reqs
	grep --exclude-dir=components -rnH TODO accounting
	grep --exclude-dir=components -rnH TODO tests
