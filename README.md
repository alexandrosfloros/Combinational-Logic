# Features

Main Features:

* Creating truth table from input expression
* Creating Karnaugh map from input truth table
* Evaluating implicants from input Karnaugh map
* Obtaining minimized SOP and POS expressions

Other Features:

* Flexible choice of variables
* Flexible parsing of expression input
* Flexible editing of inputs
* Support for up to 4 variables

# How to Use

## Execution

The file used to run the project is ``main.py``.

## Boolean Expression

An input Boolean expression of up to 4 variables can be inserted to be parsed and converted to a truth table. Any letters from the English alphabet, lowercase and uppercase, can be used. The expression may also use the following characters: ``!``, ``+``, ``*``, ``(`` and ``)``. If there are two or more letters next to each other (e.g., ``AB``), the program reads that as a product. Any spaces appearing in the expression are ignored.

## Truth Table

A truth table can be filled in to be converted to a Karnaugh map. The variables and minterms can either be chosen manually or, alternatively, obtained from the previous expresion. The output of each of the different rows can be ``0``, ``1`` or ``X``, the latter of which corresponds to the "don't care term".

## Karnaugh Map

A Karnaugh map can be filled in to be solved. The variables and minterms can either be chosen manually or, alternatively, obtained from the previous truth table. The value of each of the different cells can be ``0``, ``1`` or ``X``. Once the Karnaugh map is solved, the SOP (sum of products) and POS (product of sums) minimized expressions can be viewed, as well as the implicants they consist of. The latter ones are highlighted in the Karnaugh map.
