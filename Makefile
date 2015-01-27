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


## Testing

lint:
	./lint.sh

test:
	./runtests.py tests


## Install / Upgrade

install:
	pip install -r requirements.txt

upgrade:
	pip install --upgrade -r requirements.txt


## Deployment

deploy_production:
	git push --tag origin master
	git push heroku master

migrate_production:
	heroku run python manage.py migrate --remote heroku

collectstatic_production:
	./manage.py collectstatic --noinput
	aws s3 sync --acl public-read renover/static s3://renover-immo/static/

# shortcuts for deploy to the production
dp: deploy_production
dmp: deploy_production migrate_production
cp: collectstatic_productio
