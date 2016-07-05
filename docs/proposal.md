# Project specification model

## Constraints

* model must respect sections ordering (if there is any)
* model must respect spec file formatting (if there is any)
* model must be general enough to cover various languages (e.g. Go, Python, Ruby, Java)

## Facts

* model is indepedent of spec file structure
* ``%package``, ``%description`` and ``%files`` are decomposition of a spec file, not of a model
* model consists of units, each unit corresponds to a subset of a project, each subset posses files to install, dependencies to install, description, etc.
* each model unit can have its own tests (how to deduce which subset of tests belong to which unit if all tests are located under ``%check`` section?
* changelog is a history of changes of a downstream project
* program has some metadata as well (``Name``, ``Version``, etc.), basically all tags
* patch is a divergence from an upsream project, it is globally scoped, applied in ``%prep`` section in general
* interpreted (parsed) vs. uninterpreted sections, partially vs. fully evaluated models

## Model

* model consists of project units (from here on units), each unit corresponds to a subset of a project
* there is at least one unit (called main unit)
* not every unit is fully specified (``%files`` section can be missing)
* at least one unit must by fully specified
* downstream project history is distinguished unit
* information about project are part of a metadata unit

**Example of a conditional free model**:

Go project https://github.com/coreos/etcd

Metadata:

```yaml
name: etcd
version: 3.0.0
summary: A highly-available key value store for shared configuration
source0: https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
ExclusiveArch: %{ix86} x86_64 %{arm} aarch64 ppc64le
...
%provider_prefix: %{provider}.%{provider_tld}/%{project}/%{repo}
%provider: github
%provider_tld: com
%project: coreos
%repo: etcd
```

Project unit:

```yaml
name: devel
description: "golang development libraries for etcd, a highly-available key value store for shared configuration."
buildtime:
  dependencies:
    - name: golang(github.com/cheggaaa/pb)
    - name: golang(github.com/bgentry/speakeasy)
    - name: golang(github.com/boltdb/bolt)
  architecture:
    - noarch
runtime:
  dependencies:
    - name: golang(github.com/cheggaaa/pb)
      mark: ">= 1.2"
    - name: golang(github.com/bgentry/speakeasy)
    - name: golang(github.com/boltdb/bolt)
  available:
    - name: golang(%{import_path}/alarm)
      mark: %{version}-%{release}
    - name: golang(%{import_path}/auth)
      make: %{version}-%{release}
files:
  meta:
    file: deve.file-list
  list:
  - name: %license LICENSE
  - name: %doc *.md
  - name: %dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
```

History unit:

```yaml
history:
  - author: AUTHOR
  - date: Sun May 15 2016
  - mark: 3.0.0-0.1
  - comment: "Update to v3.0.0-beta0...<NL>  resolves: #1333988"
```

**Example of a model with conditionals**:

TODO

### Representation

* model must provide representation capable of including nested conditions, semantically compound blocks, non-evaluated parameters (e.g. tree)
* each element (e.g. node) in the model must be uniquely addressable (location of a list of runtime dependencies for a particular unit)

### Formatting, mutual positioning

* spec file parser generates ``%description``, ``%%package``, ``%files`` elements
* model generator generates one element for a unit specification
* model must support both approaches
* model operations must be carried with minimal changes to the original spec file, formatting and mutual positioning must be preserved
* model itself is formatting and positioning free
* formatting and positioning can be kept out of the model (with proper mapping to model elements)

**Example**:

1. spec file is parsed, parse tree is constructed
1. parse tree is broken down into specification model + formatting&positioning
1. each element in the model is given an entry in a formatting&positioning table
1. the model is updated (with possible reconstruction of the table)
1. model + formatting&positioning is converted back to a parse tree
1. spec file is renderred

**Constraints**: some updates do not have equivalent changes in formatting (e.g. what whitespaces to use with an introduction of a new unit)

## Potential analysis

* model corresponds to a upstream project snapshot in a distribution
* analysis over partially evaluated model (e.g. on what architectures/distributions can the model be applied)
* analysis over evaluated model (e.g. does all architectures provide required runtime dependencies)
* how much the model needs to be evaluted to decide if a given property holds
* using curified (partialy evaluation) models as operands
* model checking over partially evaluted models (e.g. predicate abstraction) => verification of spec files

## Vocabulary

* **raw model**: clean model with formatting and positioning information
* **clean model**: project specification model free of any formatting and positioning information
* **evaluated model**: model without any parameter (any free variable)
* **partially evaluated model**: model with at least on free parameter (including conditionals)
* **formatting**: whitespaces, comments
* **mutual positioning**: section ordering, conditional sections sharing

### Examples

* raw model is a product of spec file parsing, where whitespaces and mutual positioning has to be preserved
* clean model is a product of model generator build from data extracted from a source code (there is no formatting, no predefined mutual position of project parts)
* evaluated model is a product of substituing every macro (variable, tag, etc.) with its corresponding value (e.g. product of ``rpmspec -P name.spec``)
* partially evaluted model does not have all variables set, e.g. ``%{go_arches}`` architectures are not specified, ``%{fedora}`` is not known in advance, etc.
