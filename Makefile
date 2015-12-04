# A simple Makefile for building DOC and cleaning tree
# Fridolin Pokorny
# fpokorny@redhat.com

all: doc

doc:
	@epydoc --graph all -o DOC/ modules/ plugins/ examples/ specker check.py -v && \
		echo "Documentation created, see 'DOC/' dir..."

check:
	@echo "Performing checks..."
	@LC_ALL="C" ./check.py

clean:
	@echo "Cleaning tree..."
	@find -iname '*.pyc' -exec rm -f {} \;
	@rm -f ./speckerc
	@rm -rf ./DOC

