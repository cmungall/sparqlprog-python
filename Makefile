test:
	python -m unittest tests/test_*.py

# TODO: manually increment version in setup.py, run . bump.sh, then this
release: cleandist
	python setup.py sdist bdist_wheel
	twine upload dist/*

cleandist:
	rm dist/* || true
