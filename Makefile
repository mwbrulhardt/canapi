clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf

package:
	  rm -rf dist
	  python3 setup.py sdist
	  python3 setup.py bdist_wheel

test-release: package
	  python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: package
	  python3 -m twine upload dist/*
