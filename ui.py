import string
import tkinter as tk
from tkinter import ttk
from logic import *

class Interface:
    def __init__(self, master):
        self.alphabet = ("",) + tuple(string.ascii_letters)

        self.table_dig_list = []
        self.table_min_list = []
        self.binary = []

        for x in it.product("01", repeat = 4):
            self.binary.append(x)

        self.master = master
        self.master.title("Combinational Logic")
        self.master.geometry("475x700")
        self.master.resizable(True, True)
        self.master.iconbitmap("logo.ico")

        self.input_expression = ttk.Frame(master)
        self.input_expression_buttons = ttk.Frame(self.input_expression)
        self.main_frame = ttk.Frame(master)
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side = "left", padx = 5)
        self.table = ttk.Frame(self.left_frame)
        self.table_buttons = ttk.Frame(self.left_frame)
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side = "right", padx = 5, expand = "true", fill = tk.Y)
        self.kmap = ttk.Frame(self.right_frame)
        self.kmap_buttons = ttk.Frame(self.right_frame)
        self.simplified_expression = ttk.Frame(master)

        self.input_expression_title = ttk.Label(master, text = "Input Expression")
        self.input_expression_title.pack()
        self.input_expression.pack()
        self.main_frame.pack()

        self.input_expression_entry = ttk.Entry(self.input_expression, width = 40)
        self.input_expression_entry.pack()
        self.input_expression_scrollbar = ttk.Scrollbar(self.input_expression, orient = "horizontal", command = self.input_expression_entry.xview)
        self.input_expression_entry.config(xscrollcommand = self.input_expression_scrollbar.set)
        self.input_expression_scrollbar.pack(expand = "true", fill = tk.X)
        self.input_expression_buttons.pack(pady = 5)

        self.fill_table_button = ttk.Button(self.input_expression_buttons, text = "Fill Table", command = self.fill_table)
        self.fill_table_button.grid(row = 0, column = 0, padx = 2)
        self.clear_entry_button = ttk.Button(self.input_expression_buttons, text = "Clear Entry", command = lambda: self.input_expression_entry.delete(0, "end"))
        self.clear_entry_button.grid(row = 0, column = 1, padx = 2)

        self.table_title = ttk.Label(self.left_frame, text = "Truth Table")
        self.table_title.pack()
        self.table.pack()
        self.table_buttons.pack(pady = 5)

        self.table_var_combobox1 = ttk.Combobox(self.table, values = self.alphabet, state = "readonly", width = 2)
        self.table_var_combobox1.bind("<<ComboboxSelected>>", self.change_table_var)
        self.table_var_combobox1.grid(row = 0, column = 0, padx = 1)
        self.table_var_combobox2 = ttk.Combobox(self.table, values = self.alphabet, state = "readonly", width = 2)
        self.table_var_combobox2.bind("<<ComboboxSelected>>", self.change_table_var)
        self.table_var_combobox2.grid(row = 0, column = 1, padx = 1)
        self.table_var_combobox3 = ttk.Combobox(self.table, values = self.alphabet, state = "readonly", width = 2)
        self.table_var_combobox3.bind("<<ComboboxSelected>>", self.change_table_var)
        self.table_var_combobox3.grid(row = 0, column = 2, padx = 1)
        self.table_var_combobox4 = ttk.Combobox(self.table, values = self.alphabet, state = "readonly", width = 2)
        self.table_var_combobox4.bind("<<ComboboxSelected>>", self.change_table_var)
        self.table_var_combobox4.grid(row = 0, column = 3, padx = 1)

        self.min_label = ttk.Button(self.table, text = "m", state = "disabled", width = 4)
        self.min_label.grid(row = 0, column = 4)
        self.num_label = ttk.Button(self.table, text = "n", state = "disabled", width = 4)
        self.num_label.grid(row = 0, column = 5, padx = 2, pady = 2)

        for i in range(16):
            table_dig_row = []
            for j in range(4):
                dig = ttk.Button(self.table, state = "disabled", width = 4)
                dig.grid(row = i + 1, column = j)
                table_dig_row.append(dig)

                if i < 10:
                    ttk.Button(self.table, text = f"0{i}", state = "disabled", width = 4).grid(row = i + 1, column = 5)
                else:
                    ttk.Button(self.table, text = f"{i}", state = "disabled", width = 4).grid(row = i + 1, column = 5)

            self.table_dig_list.append(table_dig_row)
            min = ttk.Button(self.table, width = 4)
            min.grid(row = i + 1, column = 4)
            min.bind("<Button-1>", self.change_table_min)
            self.table_min_list.append(min)
        
        self.fill_kmap_button = ttk.Button(self.table_buttons, text = "Fill Kmap")
        self.fill_kmap_button.grid(row = 0, column = 0, padx = 2)
        self.clear_table_button = ttk.Button(self.table_buttons, text = "Clear Table", command = self.clear_table)
        self.clear_table_button.grid(row = 0, column = 1, padx = 2)

        self.kmap_title = ttk.Label(self.right_frame, text = "Karnaugh Map")
        self.kmap_title.pack()
        self.kmap.pack()
        self.kmap_buttons.pack(pady = 5)

        self.kmap_var_row_combobox1 = ttk.Combobox(self.kmap, state = "readonly", width = 2)
        self.kmap_var_row_combobox1.grid(row = 5, column = 0, pady = 1)
        self.kmap_var_row_combobox2 = ttk.Combobox(self.kmap, state = "readonly", width = 2)
        self.kmap_var_row_combobox2.grid(row = 5, column = 1, pady = 1)

        self.kmap_var_column_combobox1 = ttk.Combobox(self.kmap, state = "readonly", width = 2)
        self.kmap_var_column_combobox1.grid(row = 0, column = 5, padx = 1)
        self.kmap_var_column_combobox2 = ttk.Combobox(self.kmap, state = "readonly", width = 2)
        self.kmap_var_column_combobox2.grid(row = 1, column = 5, padx = 1)

        self.kmap_row_bit_label00 = ttk.Button(self.kmap, text = "00", state = "disabled", width = 4)
        self.kmap_row_bit_label00.grid(row = 1, column = 0, padx = 2)
        self.kmap_row_bit_label01 = ttk.Button(self.kmap, text = "01", state = "disabled", width = 4)
        self.kmap_row_bit_label01.grid(row = 2, column = 0, padx = 2)
        self.kmap_row_bit_label11 = ttk.Button(self.kmap, text = "11", state = "disabled", width = 4)
        self.kmap_row_bit_label11.grid(row = 3, column = 0, padx = 2)
        self.kmap_row_bit_label10 = ttk.Button(self.kmap, text = "10", state = "disabled", width = 4)
        self.kmap_row_bit_label10.grid(row = 4, column = 0, padx = 2)

        self.kmap_column_bit_label00 = ttk.Button(self.kmap, text = "00", state = "disabled", width = 4)
        self.kmap_column_bit_label00.grid(row = 0, column = 1, pady = 2)
        self.kmap_column_bit_label01 = ttk.Button(self.kmap, text = "01", state = "disabled", width = 4)
        self.kmap_column_bit_label01.grid(row = 0, column = 2, pady = 2)
        self.kmap_column_bit_label11 = ttk.Button(self.kmap, text = "11", state = "disabled", width = 4)
        self.kmap_column_bit_label11.grid(row = 0, column = 3, pady = 2)
        self.kmap_column_bit_label10 = ttk.Button(self.kmap, text = "10", state = "disabled", width = 4)
        self.kmap_column_bit_label10.grid(row = 0, column = 4, pady = 2)

        for i in range(4):
            for j in range(4):
                ttk.Button(self.kmap, text = "0", width = 4).grid(row = i + 1, column = j + 1)
        
        self.evaluate_button = ttk.Button(self.kmap_buttons, text = "Evaluate")
        self.evaluate_button.grid(row = 0, column = 0, padx = 2)
        self.clear_kmap_button = ttk.Button(self.kmap_buttons, text = "Clear Kmap")
        self.clear_kmap_button.grid(row = 0, column = 1, padx = 2)

        self.implicants_display = ttk.Notebook(self.right_frame)
        self.implicants_display.pack()
        self.sop_table = ttk.Treeview(self.implicants_display, columns = ("implicants"), show = "headings", height = 10)
        self.sop_table.heading("implicants", text = "Implicants")
        self.sop_table.column("implicants", width = 180)
        self.sop_table.pack()
        self.pos_table = ttk.Treeview(self.implicants_display, columns = ("implicants"), show = "headings", height = 10)
        self.pos_table.heading("implicants", text = "Implicants")
        self.pos_table.column("implicants", width = 180)
        self.pos_table.pack()
        self.implicants_display.add(self.sop_table, text = "SOP")
        self.implicants_display.add(self.pos_table, text = "POS")

        self.simplified_expression_title = ttk.Label(master, text = "Simplifed Expression")
        self.simplified_expression_title.pack()
        self.simplified_expression.pack()

        self.sop_label = ttk.Label(self.simplified_expression, text = "SOP")
        self.sop_label.grid(row = 0, column = 0)
        self.pos_label = ttk.Label(self.simplified_expression, text = "POS")
        self.pos_label.grid(row = 3, column = 0)
        self.sop_output_expression = ttk.Entry(self.simplified_expression, state = "readonly", width = 40)
        self.sop_output_expression.grid(row = 0, column = 1)
        self.sop_scrollbar = ttk.Scrollbar(self.simplified_expression, orient = "horizontal", command = self.sop_output_expression.xview)
        self.sop_output_expression.config(xscrollcommand = self.sop_scrollbar.set)
        self.sop_scrollbar.grid(row = 1, column = 1, sticky = "ew")
        self.pos_output_expression = ttk.Entry(self.simplified_expression, state = "readonly", width = 40)
        self.pos_output_expression.grid(row = 3, column = 1)
        self.pos_scrollbar = ttk.Scrollbar(self.simplified_expression, orient = "horizontal", command = self.pos_output_expression.xview)
        self.pos_output_expression.config(xscrollcommand = self.pos_scrollbar.set)
        self.pos_scrollbar.grid(row = 4, column = 1, sticky = "ew")
        self.sop_input_button = ttk.Button(self.simplified_expression, text = "Set Input")
        self.sop_input_button.grid(row = 0, column = 2, padx = 5)
        self.pos_input_button = ttk.Button(self.simplified_expression, text = "Set Input")
        self.pos_input_button.grid(row = 3, column = 2, padx = 5)

    def fill_table(self):
        table = get_table(self.input_expression_entry.get())
        self.clear_table()
        if len(table.var) == 1:
            self.table_var_combobox4.set(table.var)
        elif len(table.var) == 2:
            self.table_var_combobox3.set(table.var[0])
            self.table_var_combobox4.set(table.var[1])
        elif len(table.var) == 3:
            self.table_var_combobox2.set(table.var[0])
            self.table_var_combobox3.set(table.var[1])
            self.table_var_combobox4.set(table.var[2])
        else:
            self.table_var_combobox1.set(table.var[0])
            self.table_var_combobox2.set(table.var[1])
            self.table_var_combobox3.set(table.var[2])
            self.table_var_combobox4.set(table.var[3])

        count = 0
        for min in self.table_min_list[:2 ** table.num]:
            min.configure(text = table.values[count])
            count += 1
        
        self.update_table()

    def update_table(self):
        mins = []
        vars = self.table_var_combobox1.get() + self.table_var_combobox2.get() + self.table_var_combobox3.get() + self.table_var_combobox4.get()
        
        for min in self.table_min_list[:2 ** len(vars)]:
            if min["text"] == "":
                min.configure(text = "0")
            mins.append(min["text"])
        
        table = TruthTable(vars, mins)
        count = 0

        for row in self.table_dig_list:
            for i in range(4):
                row[i].configure(text = self.binary[count][i])
            count += 1

        if self.table_var_combobox4.get() == "":
            self.clear_table()
        elif self.table_var_combobox3.get() == "":
            self.table_var_combobox1.set("")
            self.table_var_combobox2.set("")
            for row in self.table_dig_list[2:]:
                for dig in row:
                    dig.configure(text = "")
            for min in self.table_min_list[2:]:
                min.configure(text = "")
            for row in self.table_dig_list[:2]:
                row[0].configure(text = "")
                row[1].configure(text = "")
                row[2].configure(text = "")
        elif self.table_var_combobox2.get() == "":
            self.table_var_combobox1.set("")
            for row in self.table_dig_list[4:]:
                for dig in row:
                    dig.configure(text = "")
            for min in self.table_min_list[4:]:
                min.configure(text = "")
            for row in self.table_dig_list[:4]:
                row[0].configure(text = "")
                row[1].configure(text = "")
        elif self.table_var_combobox1.get() == "":
            for row in self.table_dig_list[8:]:
                for dig in row:
                    dig.configure(text = "")
            for min in self.table_min_list[8:]:
                min.configure(text = "")
            for row in self.table_dig_list[:8]:
                row[0].configure(text = "")

    def change_table_var(self, event):
        self.update_table()
    
    def change_table_min(self, event):
        if event.widget["text"] != "":
            if event.widget["text"] == "0":
                event.widget.configure(text = "1")
            elif event.widget["text"] == "1":
                event.widget.configure(text = "X")
            else:
                event.widget.configure(text = "0")

        self.update_table()
    
    def fill_kmap(self):
        pass

    def clear_table(self):
        self.table_var_combobox1.set("")
        self.table_var_combobox2.set("")
        self.table_var_combobox3.set("")
        self.table_var_combobox4.set("")

        for row in self.table_dig_list:
            for dig in row:
                dig.configure(text = "")
        for min in self.table_min_list:
            min.configure(text = "")

    def evaluate(self):
        pass

    def clear_kamp(self):
        pass

    def sop_input(self):
        pass

    def pos_input(self):
        pass

    def set_table(self):
        pass

    def set_kmap(self):
        pass