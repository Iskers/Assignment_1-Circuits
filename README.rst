.. Copyright 2020, Oskar T. Inderberg

******************************
Assignment 1: Pumping Circuits
******************************

Pumping circuits is a program which provides design, troubleshooting and analysis of fluid circuits.

Getting Started
===============
This Python program requires at least python 3.7.

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
* HTML study generation with adaptability for different use cases
* Validate circuits validity in a 2D-plane
* Testing with near 100% coverage

Assumptions
------------
* Pipes can have a length of no shorter than 1 m. To change this change set function for PipeStraight.
* While the program requires pipes with the angles 0 and 90,
  it is possible to adapt for pipes with angles between requires only small changes.


Usage
-----
This project comes with a main.py file which is the base for running the deployed system. From here one can set
parameters as one want. For analysis of existing circuits import files into the data folder and load them.

.. code:: bash

    $ python main.py


Pumping Circuits
================
This program tries to conform to several "good practises" following the following principles:

    `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_

    `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it>`_

    The Zen of Python
        >>> import this

Because these where applied some time into the development of this program, and the resource cost of
refactoring one might find parts that do not adhere to these principles.

Core Modules
------------
Most big functionality, which is not private should be documented in their docstrings.

General conventions
~~~~~~~~~~~~~~~~~~~

Most classes are initialized with a init function. This takes in arguments and initializes a object, assigning
member variables with their given value. Private member variables are named with the following convention
``_variable_name``, public variables are named without the leading underscore ``variable_name``.

Classes in this project use `properties <https://docs.python.org/3/library/functions.html?highlight=property#property>`_
as opposed to setter and getter functions. Properties function as setter and getter functions, but are accessed with
``some_object.property_name`` in the same way manipulating private member variables without accessing them directly.

Some classes have representations defined using the magic methods ``__repr__`` or ``__str__``. These are mostly used
for printing classes, but are also useful in debugging.

The classes Circuit and FileHandler can be used as
`context managers <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ in which a certain context is
created when using the with statement. See the docstrings for the __enter__ methods explain their uses.



parts.py
~~~~~~~~
This module contains the parts of the circuit. The ``class Part`` is abstract class for all other parts used. It
contains a name which is a property shared by all parts, used with ``Part.name``.

It also contains two different
`factory methods <https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)>`_, which use arguments or
keyword arguments to initialize and return objects.

All sub part classes are structured with the following pattern:
    1. Initialization
        * Initializing private member variables
    2. Representation
    3. Properties
    4. Factory functions
    5. Calculation functions

Representation is used to give a clear picture of how objects look like in circuit. This can be used for printing a
part object or a circuit canvas.

Factory functions are used by the factory methods to instance new objects which have different arguments than the
initializer.

Calculation functions are functions used by the class CircuitCalculator.py to calculate losses of pressure or
return the objects specific ZETA value. While it would be preferred to contain these functions in the class
CircuitCalculator it was simpler to add it to the parts for easy iteration.

circuit.py
~~~~~~~~~~


Testing
-------

As testing and quality control of existing code is a important part of managing code, this program is developed with
the standard package unittest for testing. This gives the developer to easily and continuously test all parts of the
code concurrently with development.

To use this feature one has to:

.. code:: bash

    $ cd /path/to/project-dir/
    $ python -m unittest

Testing during this projects development is done using the packages unittest and coverage. Coverages gives the
developer an overview of what lines of code has been run. The tests developed have tried to give 100% coverage to
ensure that all lines have been tested and gives the expected response.

Modularisation
--------------

As this python program is composed of several modules and data sets it is departmentalized into different folders.
Reviewing the project structure, it is composed of the folders data, tests and module, as well as a top facing
main function. Basing the project such provides a clear overview and modularize's the project into easy accessible
files without overwhelming the user.

This is an attempt to create files which can be copied and pasted to new projects when needed. For example
*file_handler.py* and *parser.py* are meant to be easily adapted for new projects. Furthermore modularizing classes
which dont share inheritance seemed like a useful standard.

.. Compared to many other projects this project is modularized in quite a degree.

Documentation, docstrings and annotations
------------------------------------------

In an attempt to develop this project in a more realistic manner, close to a real world open-source project I have
tried to use the conventions of creating a README and use `docstrings <https://www.python.org/dev/peps/pep-0257/>`_
and `annotations <https://www.python.org/dev/peps/pep-3107/>`_.

Discovering these conventions during development has led to some inconsistencies in the project.

.. include:: module/file_handler.py
    :code: python
    :start-line: 1
    :end-line: 10



Afterthoughts
~~~~~~~~~~~~~
I should have decided on some conventions in the start of the project and kept to them. Refactoring and changing
conventions midway was very time consuming and with

Consistency is key. After learning about new


:Author:
    Oskar T. Inderberg
:Version:
    1.0
:Date created: 03.02.2020
:Last updated: 03.03.2020