# A simple Makefile for building DOC and cleaning tree
# Fridolin Pokorny
# fpokorny@redhat.com

all: doc

doc:
	@epydoc --graph all -o DOC/ modules/ plugins/ examples/ specker -v && \
		echo "Documentation created, see 'DOC/' dir..."

clean:
	@echo "Cleaning tree..."
	@find -iname '*.pyc' -exec rm -f {} \;
	@rm -f ./speckerc
	@rm -rf ./DOC

