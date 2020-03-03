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
* HTML study generation with adaptability for different use cases
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
some change

Usage
~~~~~
This script comes with a main.py file which is the base for running the deployed system. From here one can set parameters as one want.
For analysis of existing circuits import files into the data folder and load them.

.. code:: bash

    $ python3 main.py


Intro
-----
This script tries to conform to several "good practises" following the following principles:

    `DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself/>`_

    `YAGNI <https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it/>`_

    The Zen of Python
        >>> import this

Because these where applied some time into the development of this script, and the resource cost of
refactoring one might find parts that do not adhere to these principles.

some change



Testing
-------

As testing and quality control of existing code is a important part of managing code, this script is developed with
the standard package unittest for testing. This gives the developer to easily and continuously test all parts of the code
concurrently with development.

To use this feature one has to:

.. code:: bash

    $ cd /path/to/tests/
    $ unittest

As this python script is composed of several modules and data sets it is departmentalized into different folders.
Reviewing the project structure, it is composed of the folders data, tests and module, as well as a top facing main function.
Basing the project such provides a clear overview and modularize's the project into easy accessible files without overwhelming the user.



Modularisation
--------------

Compared to many other projects this project is modularized in quite a degree. This is an attempt to create files which can be copied and pasted to
new projects when needed. For example file_handler.py and

.. literalinclude:: module.file_handler.py
    :linenos:
    :language: python
    :lines: 1, 3-5
    :start-after: 3
    :end-before: 5


Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.

We have a mailing list located at: project@google-groups.com


Python 2.7, 3.5, 3.6
--------------------


:Author:
    Oskar T. Inderberg
:Version:
    1.0
:Date created: 03.02.2020
:Last updated: 14.02.2020