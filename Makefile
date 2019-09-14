clean:
	rm -rf *.egg-info
	rm -rf dist

test:
	coverage run testing.py
	coverage report

html:
	coverage run testing.py
	coverage html
	open ./coverage_html_report/index.html

publish:
	python setup.py sdist bdist_wheel
	twine upload -s dist/*

.PHONY: clean publish test html
