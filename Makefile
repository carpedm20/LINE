init:
	pandoc -o README.rst README.md
	vi README.rst
	vi docs/conf.py
	#python setup.py sdist upload
