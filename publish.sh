rm -rf build dist
python -m build

python -m twine upload --verbose dist/*
