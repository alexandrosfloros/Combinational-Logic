import itertools as it
import numpy as np

class TruthTable:
    def __init__(self, var, values):
        self.var = var
        self.values = values
        self.num = len(self.var)

class Kmap:
    def __init__(self, table):
        self.table = table
        self.mode = "sop"
        if self.table.num == 1:
            self.values = np.reshape(self.table.values, (2, 1))
            self.rows = self.table.var
            self.columns = ""
        elif self.table.num == 2:
            self.values = np.reshape(self.table.values, (2, 2))
            self.rows = self.table.var[0]
            self.columns = self.table.var[1]
        elif self.table.num == 3:
            self.values = np.reshape(self.table.values, (2, 4))
            self.values[:, [2, 3]] = self.values[:, [3, 2]]
            self.rows = self.table.var[0]
            self.columns = self.table.var[1:]
        else:
            self.values = np.reshape(self.table.values, (4, 4))
            self.values[:, [2, 3]] = self.values[:, [3, 2]]
            self.values[[2, 3], :] = self.values[[3, 2], :]
            self.rows = self.table.var[:2]
            self.columns = self.table.var[2:]

    def simplify(self):
        self.get_implicants()
        terms = []
        if all(value == "0" for value in self.table.values):
            output = "0"
        elif all(value in ("1", "X") for value in self.table.values):
            output = "1"
        else:
            if self.mode == "sop":
                for i in self.implicants:
                    terms.append("".join(i.term))
                output = " + ".join(sorted(terms, key = lambda x: x.replace("!", "")))
            else:
                for i in self.implicants:
                    if len(i.term) == 1:
                        terms.append(" + ".join(i.term))
                    else:
                        terms.append("(" + " + ".join(i.term) + ")")
                output = "".join(sorted(terms, key = lambda x: x.replace("!", "").replace("(", "").replace(")", "")))
        return output

    def get_implicants(self):
        self.groups = []
        for row in range(len(self.values)):
            for column in range(len(self.values[row])):
                if self.onexone(row, column):
                    self.add_implicant(self.onexone(row, column))
                    if self.onextwo(row, column):
                        self.add_implicant(self.onextwo(row, column))
                        if self.onexfour(row, column):
                            self.add_implicant(self.onexfour(row, column))
                            if self.twoxfour(row, column):
                                self.add_implicant(self.twoxfour(row, column))
                    if self.twoxone(row, column):
                        self.add_implicant(self.twoxone(row, column))
                        if self.fourxone(row, column):
                            self.add_implicant(self.fourxone(row, column))
                            if self.fourxtwo(row, column):
                                self.add_implicant(self.fourxtwo(row, column))
                                if self.fourxfour(row, column):
                                    self.add_implicant(self.fourxfour(row, column))
                        if self.twoxtwo(row, column):
                            self.add_implicant(self.twoxtwo(row, column))
        self.implicants = self.groups.copy()
        self.groups.sort(key = lambda i: len(i.terms))
        for i in self.groups:
            other_groups = map(set, (j.terms for j in self.implicants if i != j))
            if len(self.implicants) > 1:
                if set(i.terms).issubset(set.union(*other_groups)):
                    self.implicants.remove(i)

    def add_implicant(self, terms):
        if isinstance(terms[0], int):
            self.groups.append(Implicant(self, (terms,)))
        else:
            if not any(set(i.terms) == (set(terms)) for i in self.groups):
                self.groups.append(Implicant(self, terms))

    def onexone(self, row, column):
        if self.mode == "sop":
            if self.values[row][column] in ("1", "X"):
                return row, column
        else:
            if self.values[row][column] in ("0", "X"):
                return row, column

    def onextwo(self, row, column):
        if self.values.shape[1] > 1:
            if self.onexone(row, column) and self.onexone(row, (column + 1) % self.values.shape[1]):
                return self.onexone(row, column), self.onexone(row, (column + 1) % self.values.shape[1])

    def onexfour(self, row, column):
        if self.values.shape[1] > 3:
            if self.onextwo(row, column) and self.onextwo(row, (column + 2) % self.values.shape[1]):
                return self.onextwo(row, column) + self.onextwo(row, (column + 2) % self.values.shape[1])

    def twoxone(self, row, column):
        if self.values.shape[0] > 1:
            if self.onexone(row, column) and self.onexone((row + 1) % self.values.shape[0], column):
                return self.onexone(row, column), self.onexone((row + 1) % self.values.shape[0], column)

    def twoxtwo(self, row, column):
        if self.values.shape[0] > 1 and self.values.shape[1] > 1:
            if self.onextwo(row, column) and self.onextwo((row + 1) % self.values.shape[0], column):
                return self.onextwo(row, column) + self.onextwo((row + 1) % self.values.shape[0], column)

    def twoxfour(self, row, column):
        if self.values.shape[0] > 1 and self.values.shape[1] > 3:
            if self.twoxtwo(row, column) and self.twoxtwo(row, (column + 2) % self.values.shape[1]):
                return self.twoxtwo(row, column) + self.twoxtwo(row, (column + 2) % self.values.shape[1])

    def fourxone(self, row, column):
        if self.values.shape[0] > 3:
            if self.twoxone(row, column) and self.twoxone((row + 2) % self.values.shape[0], column):
                return self.twoxone(row, column) + self.twoxone((row + 2) % self.values.shape[0], column)

    def fourxtwo(self, row, column):
        if self.values.shape[0] > 3 and self.values.shape[1] > 1:
            if self.fourxone(row, column) and self.fourxone(row, (column + 1) % self.values.shape[1]):
                return self.fourxone(row, column) + self.fourxone(row, (column + 1) % self.values.shape[1])

    def fourxfour(self, row, column):
        if self.values.shape[0] > 3 and self.values.shape[1] > 3:
            if self.twoxfour(row, column) and self.twoxfour((row + 2) % self.values.shape[0], column):
                return self.twoxfour(row, column) + self.twoxfour((row + 2) % self.values.shape[0], column)

class Implicant:
    def __init__(self, kmap, terms):
        self.kmap = kmap
        self.terms = terms
        self.term = []
        if self.kmap.mode == "sop":
            self.get_product()
        else:
            self.get_sum()

    def get_product(self):
        self.get_common()
        if self.kmap.table.num == 1:
            if self.common[1] == "0":
                self.term.append("!" + self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append(self.kmap.rows)
        elif self.kmap.table.num == 2:
            if self.common[1] == "0":
                self.term.append("!" + self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append(self.kmap.rows)
            if self.common[3] == "0":
                self.term.append("!" + self.kmap.columns)
            elif self.common[3] == "1":
                self.term.append(self.kmap.columns)
        elif self.kmap.table.num == 3:
            if self.common[1] == "0":
                self.term.append("!" + self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append(self.kmap.rows)
            if self.common[2] == "0":
                self.term.append("!" + self.kmap.columns[0])
            elif self.common[2] == "1":
                self.term.append(self.kmap.columns[0])
            if self.common[3] == "0":
                self.term.append("!" + self.kmap.columns[1])
            elif self.common[3] == "1":
                self.term.append(self.kmap.columns[1])
        else:
            if self.common[0] == "0":
                self.term.append("!" + self.kmap.rows[0])
            elif self.common[0] == "1":
                self.term.append(self.kmap.rows[0])
            if self.common[1] == "0":
                self.term.append("!" + self.kmap.rows[1])
            elif self.common[1] == "1":
                self.term.append(self.kmap.rows[1])
            if self.common[2] == "0":
                self.term.append("!" + self.kmap.columns[0])
            elif self.common[2] == "1":
                self.term.append(self.kmap.columns[0])
            if self.common[3] == "0":
                self.term.append("!" + self.kmap.columns[1])
            elif self.common[3] == "1":
                self.term.append(self.kmap.columns[1])

    def get_sum(self):
        self.get_common()
        if self.kmap.table.num == 1:
            if self.common[1] == "0":
                self.term.append(self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append("!" + self.kmap.rows)
        elif self.kmap.table.num == 2:
            if self.common[1] == "0":
                self.term.append(self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append("!" + self.kmap.rows)
            if self.common[3] == "0":
                self.term.append(self.kmap.columns)
            elif self.common[3] == "1":
                self.term.append("!" + self.kmap.columns)
        elif self.kmap.table.num == 3:
            if self.common[1] == "0":
                self.term.append(self.kmap.rows)
            elif self.common[1] == "1":
                self.term.append("!" + self.kmap.rows)
            if self.common[2] == "0":
                self.term.append(self.kmap.columns[0])
            elif self.common[2] == "1":
                self.term.append("!" + self.kmap.columns[0])
            if self.common[3] == "0":
                self.term.append(self.kmap.columns[1])
            elif self.common[3] == "1":
                self.term.append("!" + self.kmap.columns[1])
        else:
            if self.common[0] == "0":
                self.term.append(self.kmap.rows[0])
            elif self.common[0] == "1":
                self.term.append("!" + self.kmap.rows[0])
            if self.common[1] == "0":
                self.term.append(self.kmap.rows[1])
            elif self.common[1] == "1":
                self.term.append("!" + self.kmap.rows[1])
            if self.common[2] == "0":
                self.term.append(self.kmap.columns[0])
            elif self.common[2] == "1":
                self.term.append("!" + self.kmap.columns[0])
            if self.common[3] == "0":
                self.term.append(self.kmap.columns[1])
            elif self.common[3] == "1":
                self.term.append("!" + self.kmap.columns[1])

    def get_common(self):
        self.common = ""
        for m in self.terms:
            if m[0] == 0:
                value = "00"
            elif m[0] == 1:
                value = "01"
            elif m[0] == 2:
                value = "11"
            else:
                value = "10"
            if m[1] == 0:
                value += "00"
            elif m[1] == 1:
                value += "01"
            elif m[1] == 2:
                value += "11"
            else:
                value += "10"
            if self.common == "":
                self.common = list(value)
            for c in range(len(self.common)):
                if value[c] != self.common[c]:
                    self.common[c] = "-"

def get_table(expression):
    values = np.array([], str)
    var = ""
    expression = expression.replace(" ", "").replace("*", "")
    expression = "*".join(expression)
    expression = expression.replace("!*", "!").replace("*+*", "+").replace("(*", "(").replace("*)", ")")
    for c in expression:
        if c.isalpha():
            if c not in var:
                var += c
    var = "".join(sorted(var))
    num = len(var)
    if num == 0:
        print("\nExpression needs at least one variable!")
        exit()
    elif num > 4:
        print("\nExpression cannot have more than 4 variables!")
        exit()
    for x in it.product("01", repeat = num):
        try:
            value = str(int(eval(expression.replace(var[(num - 4) % num], x[(num - 4) % num]).replace(var[(num - 3) % num], x[(num - 3) % num]).replace(var[(num - 2) % num], x[(num - 2) % num]).replace(var[num - 1], x[num - 1]).replace("0", " False ").replace("1", " True ").replace("!", " not ").replace("+", " or ").replace("*", " and "))))
        except:
            print("\nExpression is invalid!")
            exit()
        values = np.append(values, value)
    return TruthTable(var, values)

#expression = input("Input: ")
#table = get_table(expression)
#table = TruthTable("ABC", ("1", "0", "0", "X", "1", "1", "X", "X"))
#kmap = Kmap(table)
#print(kmap.simplify())
#kmap.mode = "pos"
#print(kmap.simplify())
