all: doc

doc:
	epydoc --graph all -o DOC/ modules/ plugins/ examples/ specker -v

