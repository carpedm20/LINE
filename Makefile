init:
	pandoc -o README.rst README.md
	vi README.rst
	python setup.py sdist upload
