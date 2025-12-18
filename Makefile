# make documentation

SOURCE=$(wildcard loads/*.py)

docs: $(SOURCE)
	pip install --upgrade pdoc
	pdoc $(SOURCE) -o $@ --logo "https://github.com/eudoxys/.github/blob/main/eudoxys_logo.png?raw=true"
