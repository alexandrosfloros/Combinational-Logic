# Motivation

The idea behind this project came during my revision for a digital electronics exam. Quite often, the problems encountered involved tedious, time-consuming calculations and observations, which often had to be checked multiple times to ensure there were no errors. After successfully making a script to read Boolean expressions and build a truth table, this small experimental project expanded to a user-friendly application with multiple functionalities, accepting a variety of user inputs. Unfortunately, it was finished shortly after the exams had ended!

# Features

Main Features:

* Creating truth table from input expression
* Creating Karnaugh map from input truth table
* Evaluating implicants from input Karnaugh map
* Obtaining minimised SOP and POS expressions

Other Features:

* Flexible choice of variables
* Flexible parsing of expression input
* Flexible editing of inputs
* Support for up to 4 variables
* Robust to problematic inputs

# How to Use

## Execution

The file used to run the project is ``main.py``.

## Boolean Expression

An input Boolean expression of up to 4 variables can be inserted to be parsed and converted to a truth table. Any letters from the English alphabet, lowercase and uppercase, can be used. The expression may also use the following characters: ``+``, ``*``, ``(`` and ``)``. If there are two or more letters next to each other (e.g. ``AB``), the program reads that as a product. Any spaces appearing in the expression are ignored.

## Truth Table

A truth table can be filled in to be converted to a Karnaugh map. The variables and minterms can either be chosen manually or, alternatively, obtained from the previous expresion. The output of each of the different rows can be ``0``, ``1`` or ``X``, the latter of which corresponds to the "don't care term". The number of variables may also be adjusted to be less than 4.

## Karnaugh Map

A Karnaugh map can be filled in to be solved. The variables and minterms can either be chosen manually or, alternatively, obtained from the previous truth table. The value of each of the different cells can be ``0``, ``1`` or ``X``. The number of variables may also be adjusted to be less than 4. Once the Karnaugh map is solved, the SOP (sum of products) and POS (product of sums) minimised expressions can be viewed, as well as the implicants they consist of. The latter ones are highlighted in the Karnaugh map.
