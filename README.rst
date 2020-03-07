.. Copyright 2020, Oskar T. Inderberg

==============================
Assignment 1: Pumping Circuits
==============================

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
This project comes with a *main.py* file which is the base for running the deployed system. From here one can set
parameters as one want. For analysis of existing circuits import files into the data folder and load them.

.. code:: bash

    $ pip install -r requirements.txt
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

Most big functionality, which is not private should be documented in their docstrings.

General conventions
--------------------

Most classes are initialized with a init function. This takes in arguments and initializes a object, assigning
member variables with their given value. Private member variables are named with the following convention
``_variable_name``, public variables are named without the leading underscore ``variable_name``. Private and public
member functions also follow this convention.

Classes in this project use `properties <https://docs.python.org/3/library/functions.html?highlight=property#property>`_
as opposed to setter and getter functions. Properties function as setter and getter functions, but are accessed with
``some_object.property_name`` in the same way manipulating private member variables without accessing them directly.

Some classes have representations defined using the magic methods ``__repr__`` or ``__str__``. These are mostly used
for printing classes, but are also useful in debugging.

The classes Circuit and FileHandler can be used as
`context managers <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ in which a certain context is
created when using the with statement. See the docstrings for the __enter__ methods explain their uses.

@typechecked a decorator from the package ``pytypes``, which checks that the arguments in functions follow the
annotations.

Trailing underscores are used when naming conflicts with pythons built in functions.

File specifics
---------------

main.py
~~~~~~~
This is the file to be run by regular users for analysing circuits. It is run by using one of its two functions. One is
run purely by user input the other is run by editing the function and running it in main. Custom ranges and velocities
can be set here as well. By altering the default function one can input custom ranges if specific velocity studies need
to be calculated. In addition one can set ranges for the plot studies if the ranges dont fit the desired purpose.

For example:

.. code:: python

    page_generator.default_page_generation(circuit, base_velocity=10, height_range=(1, 100, 90),
                                                       efficiency_range=(0.1, 1, 90), velocity_range=(1, 10, 1),
                                                       diameter_range=(0.1, 1, 10))

Remember, pipes have a minimum length of 1 m. That means that the height range cant be lower than the amount of
vertical pipes. ``velocity_range`` works is a regular for loop range, the others have a different step type. The last
argument is the amount of steps and not the step size. ``base_velocity`` is used for calculating the core attributes.

This method can also be used for ``page_generator.export_circuit_study_in_HTML()`` as they accept those same arguments.

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

Factory functions are used by the factory methods to instance new objects which have different arguments than the
initializer.

Calculation functions are functions used by the class CircuitCalculator to calculate losses of pressure or
return the objects specific ZETA value. While it would be preferred to contain these functions in the class
CircuitCalculator it was simpler to add it to the parts for easy iteration.

circuit.py
~~~~~~~~~~
Overall class representing a circuit. Canvas is the most important variable. This contains a chronological list of
parts. Items in the canvas can be accessed through ``some_circuit[index]``.

Circuit can, as previously mentioned be used in a context where one can alter it and then it reverts back when leaving
the context. This is useful in *study_.py* because here we want to alter a circuit do some studies and then return
the original for final alterations.

Some of a circuits properties are independent of the amount of parts in it. Such properties are efficiency and inside
diameter. They can therefore be defined for the entire circuit. Additionally their setters must alter parts in the
circuit in order to represent the circuit correctly.

.. todo add section for canvascreator

parser.py
~~~~~~~~~
This file contains parser class which can be used for parsing different file types. It should be used by calling
its member function ``parse`` which uses *file_handler.py* and *path_finder.py* as well as the package ElementTree to
parse both tsv and xml formats.

circuit_control.py
~~~~~~~~~~~~~~~~~~
This file contains the ``CircuitControl`` class which is used to control circuits for faults. It is used by initializing
a class instance and then called with the function ``control_circuit`` which takes in a circuit and raises an exception
if a rule is broken. If no rule is broken it returns ``True``.

circuit_calculator.py
~~~~~~~~~~~~~~~~~~~~~
This file holds two classes. The first ``CircuitFormulas`` contains all the formulas used for the different calculations
used on a circuit. The second ``CircuitCalculator`` is the class used for retrieving the different calculations.
Modularizing the functions in such a way makes it easy to alter functions if needed and the calculator class remains
readable. One might want to change the function names in ``CircuitFormulas`` to make it more simple and flat.

study\_.py
~~~~~~~~~~
This file holds the class ``Study`` which, after initialized, can be called with a study function. A study function
utilizes the classes private functions to perform some studies on a circuit. A circuit should be designed and controlled
before using these functions. If one is to create new studies they should be created as public member functions to be
called from this class.

page_generator.py
~~~~~~~~~~~~~~~~~
This file is used for generating HTML reports for studies of circuits.

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
    :start-line: 0
    :end-line: 100
    :literal:


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
:Last updated: 04.03.2020