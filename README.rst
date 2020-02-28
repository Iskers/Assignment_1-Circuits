.. Copyright 2020, Oskar T. Inderberg

Assignment 1: Pumping Circuits
==============================

Pumping circuits is a script which provides design, troubleshooting and analysis of fluid circuits.

Features
--------
* Circuit design with the following parts:
    * Tanks
    * Pipes
    * Bends
    * Pumps
    * Valves
    * Filters
* Calculate the energy consumption for these circuits
* HTML study generation with adaptability for different usecases
* Validate circuits validity in a 2D-plane
* Testing with near 100% coverage

Assumptions
-----------
* Pipes can have a length of no shorter than 1 m. To change this change set function for PipeStraight.
* While the script requires pipes with the angles 0 and 90,
  it is possible to adapt for pipes with angles between requires only small changes.



Getting Started
---------------
This Python script requires at least python 3.7.

Usage
~~~~~
This script comes with a main.py file which is the base for running the deployed system. From here one can set parameters as one want.
For analisys of existing circuits import files into the data folder and load them.

.. code:: bash

    $ python3 main.py


Intro
-----
This script tries to conform to several "good pracsises" following the following principles:

    `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself/>`_

    `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it/>`_

    The Zen of Python
        >>> import this

Because these where applyed some time into the development of this script, and the resource cost of
refactoring one might find parts that do not adhere to these principles.

some change



Testing
-------

As testing and quality control of existing code is a important part of managing code, this script is developed with
the standard package unittest for testing. This gives the developer to easily and continuosly test all parts of the code
concurrently with development.

To use this feature one has to:

.. code:: bash

    $ cd /path/to/tests/
    $ unittest

As this python script is composed of several modules and data sets it is departmentalized into different folders.
Reviewing the project structure, it is composed of the folders data, tests and module, as well as a top faceing main function.
Basing the project such provides a clear overview and modularizes the project into easy accessable files without overwealming the user.






$project will solve your problem of where to start with documentation,
by providing a basic explanation of how to do it easily.

Look how easy it is to use:

    import project
    # Get your stuff done
    project.do_stuff()

Features
--------

- Be awesome
- Make things faster

Installation
------------

Install $project by running:

    install project

Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the BSD license.












pytypes is a typing toolbox w.r.t. `Something <https://www.python.org/dev/peps/pep-0484/>`_ (PEP
`526 <https://www.python.org/dev/peps/pep-0526/>`__ on the road map,
later also `544 <https://www.python.org/dev/peps/pep-0544/>`__ if it
gets accepted).

It's main features are currently

- ``@typechecked`` decorator for runtime typechecking with support for `stubfiles <https://www.python.org/dev/peps/pep-0484/#stub-files>`__ and `type comments <https://www.python.org/dev/peps/pep-0484/#suggested-syntax-for-python-2-7-and-straddling-code>`__
- ``@override`` decorator that asserts existence of a type-compatible parent method
- ``@annotations`` decorator to turn type info from stubfiles or from type comments into ``__annotations__``
- ``@typelogged`` decorator observes function and method calls at runtime and generates stubfiles from acquired type info
- service functions to apply these decorators module wide or even globally, i.e. runtime wide
- typechecking can alternatively be done in decorator-free manner (friendlier for debuggers)
- all the above decorators work smoothly with OOP, i.e. with methods, static methods, class methods and properties, even if classes are nested
- converter for stubfiles to Python 2.7 compliant form
- lots of utility functions regarding types, e.g. a Python 2.7 compliant and actually functional implementation of ``get_type_hints``
- full Python 2.7 support for all these features

An additional future goal will be integration with the Java typing system when running on Jython. Along with this, some generator utilities to produce type-safe Java bindings for Python frameworks are planned.

In wider sense, PEP 484-style type annotations can be used to build type safe interfaces to allow also other scriptming languages to call into Python code (kind of reverse FFI). In this sense the project name refers to 'ctypes', which provides Python-bindings of C.


Python 2.7, 3.5, 3.6
--------------------


:Author:
    Oskar T. Inderberg
:Version:
    1.0
:Date created: 03.02.2020
:Last updated: 14.02.2020