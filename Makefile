# make documentation

SOURCE=$(wildcard loads/*.py)

LOGO="https://github.com/eudoxys/.github/blob/main/eudoxys_logo.png?raw=true"

docs: $(SOURCE)
	pip install --upgrade pdoc
	pdoc $(SOURCE) -o $@ --logo $(LOGO) --mermaid
