# Spec Model Proposal

This document is meant to describe an abstract model of a spec file. Its use in in ...

## Abstract model of a package specification

The model itself is not meant to contain information about position of sections or
ordering of individual lists (build-time dependencies, install-time dependencies,
provided packages, etc.).

Each spec model can consists of various sections (some of which are mandatory, some are optional).
Each section can consists of various blocks (list of dependencies, building script, description, etc.)
The spec model is meant to describe a structure and mutual releationship of individual components.
In general, spec model consists of a list of packages, `build` section, `prep` section and `install` section.
Each package consists of `package`, `description` and `files` section which are inseparable.
It does not make sense to have one section without the other.

There can be various repensentations of the model such as spec file, json, yaml or xml.
Every representation has its assumptions.
A spec file models a package as three sections.
Json can model a package as a one unit.
Spec file parser is aware that each package definition consists of three sections.
On the other hand, tarball parser see a tarball as a collection of source codes.
In order to accomodate different views for each parser and specific representation,
the model is constructed to be as much assumption-free as possible.

## Definition of the model

Model of a package specification (or spec model) consists of:

* metadata (name, version, release, ..., + user defined macros/variables) TODO(jchaloup): complete the list
* non-empty list of packages (name, summary, description, list of built-time deps, list of install-time deps, list of provides, list of files to package, ...) TODO(jchaloup): what about installation script?
* non-empty prep section
* build section (can be empty)
* non-empty install section
* check section (can be empty)
* non-empty changelog

Spec file package and subpackage are treated identically.

## Model manipulations

In order to provide various use cases, the following operations of manipulation with the model are provided:

* add new package
* remove a package
* update a list of dependencies (built-time, run-time) for a given package
* update a list of provided entities for a given package
* add new section (e.g. postun, preun, postinstall, etc.)
* get a list of all packages

## Application of the model

The aim is to provide:

* abstract model of a package specification with an API for automatic modification of the model
* support for other tools that want to abtract from direct manipulation with a specific representation.

## Use cases

* Spec file translator (https://github.com/gofed/gofed/issues/56). Combine a spec file with an instruction file (describing what needs to be changed) and generate new spec file with changes applied. This can be usefull for update of spec files between different branches (e.g. regenereate spec file without devel subpackage)

* Generate partial list of dependencies for projects with docker or k8s as a dependency (https://github.com/gofed/gofed/issues/55). Some projects are not kept up-to-date very frequently or it is impossible to built from them as they break API. It can be automatically detected which dependencies are better to bundle and generate spec file accordingly.

* Create a multi spec file generator (https://github.com/gofed/gofed/issues/49). New projects can depend on other projects not yet packaged in a distribution. Thus it is usefull to provide a way to generate various spec models from a downloaded tarballs without a user intervention. In some situations generated models will have to be updated accordingly to newly discovered dependencies.

* Implement golang spec file regenerator (https://github.com/gofed/gofed/issues/47). Usefull for clean-ups. Some spec files can contain whitespaces or incomplete package definitions which can be removed. Or lists are not formatted properly.

* Other application can be automatic updates of a list of depedencies, list of tests, list of files. Or to regenerate a list of devel packages (merge or split some devel subpackages, etc.)


