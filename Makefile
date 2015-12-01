all: doc

doc:
	epydoc --graph all -o DOC/ modules/ specker -v

