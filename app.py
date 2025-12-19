
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import db
import models


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cardiac + Diabetic Food Database")
        self.geometry("980x520")
        self.minsize(900, 480)

        self.selected_name = None

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        actions = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Actions", menu=actions)
        actions.add_command(label="Set Serving Size…", command=self.set_serving_size_for_selected)
        actions.add_separator()
        actions.add_command(label="Refresh", command=self.refresh_list)
        actions.add_command(label="Clear Form", command=self.clear_form)

        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=2)
        outer.rowconfigure(0, weight=1)

        left = ttk.Frame(outer)
        right = ttk.Frame(outer)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right.grid(row=0, column=1, sticky="nsew")
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)
        right.columnconfigure(1, weight=1)

        ttk.Label(left, text="Foods").grid(row=0, column=0, sticky="w")

        self.search_var = tk.StringVar()
        e = ttk.Entry(left, textvariable=self.search_var)
        e.grid(row=1, column=0, sticky="ew", pady=(6, 8))
        e.bind("<KeyRelease>", lambda _: self.refresh_list())

        self.food_list = tk.Listbox(left, height=20)
        self.food_list.grid(row=2, column=0, sticky="nsew")
        self.food_list.bind("<<ListboxSelect>>", lambda _: self.on_select())

        btns_left = ttk.Frame(left)
        btns_left.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        btns_left.columnconfigure(0, weight=1)
        btns_left.columnconfigure(1, weight=1)
        ttk.Button(btns_left, text="Refresh", command=self.refresh_list).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(btns_left, text="Clear", command=self.clear_form).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(right, text="Food Info", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.serving_var = tk.StringVar()
        self.carbs_var = tk.StringVar()
        self.gi_var = tk.StringVar()
        self.ginote_var = tk.StringVar()
        self.sodium_var = tk.StringVar()
        self.sodium_status_var = tk.StringVar()
        self.calories_var = tk.StringVar()

        r = 1
        r = self._field(right, r, "Name", self.name_var)
        r = self._field(right, r, "Category", self.category_var)
        r = self._field(right, r, "Serving Size", self.serving_var)
        r = self._field(right, r, "Carbs (g)", self.carbs_var)
        r = self._field(right, r, "Glycemic Index", self.gi_var)
        r = self._field(right, r, "GI Note", self.ginote_var)
        r = self._field(right, r, "Sodium (mg)", self.sodium_var)

        ttk.Label(right, text="Sodium Status").grid(row=r, column=0, sticky="w", pady=6)
        ttk.Combobox(right, textvariable=self.sodium_status_var, values=["Low", "Medium", "High", "Unknown"], state="readonly").grid(row=r, column=1, sticky="ew", pady=6)
        r += 1

        r = self._field(right, r, "Calories", self.calories_var)

        btns = ttk.Frame(right)
        btns.grid(row=r, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)
        ttk.Button(btns, text="Add", command=self.on_add).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(btns, text="Update", command=self.on_update).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(btns, text="Delete", command=self.on_delete).grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self.refresh_list()

    def _field(self, parent, r, label, var):
        ttk.Label(parent, text=label).grid(row=r, column=0, sticky="w", pady=6)
        ttk.Entry(parent, textvariable=var).grid(row=r, column=1, sticky="ew", pady=6)
        return r + 1

    def refresh_list(self):
        names = [row[0] for row in models.get_all_foods()]
        q = self.search_var.get().strip().lower()
        if q:
            names = [n for n in names if q in n.lower()]
        self.food_list.delete(0, tk.END)
        for n in names:
            self.food_list.insert(tk.END, n)

    def clear_form(self):
        self.selected_name = None
        for v in [self.name_var, self.category_var, self.serving_var, self.carbs_var, self.gi_var, self.ginote_var, self.sodium_var, self.sodium_status_var, self.calories_var]:
            v.set("")
        self.food_list.selection_clear(0, tk.END)

    def on_select(self):
        sel = self.food_list.curselection()
        if not sel:
            return
        name = self.food_list.get(sel[0])
        row = models.find_food_info(name)
        if row is None:
            messagebox.showwarning("Not found", "That food no longer exists.")
            self.refresh_list()
            return

        self.selected_name = row[1]
        self.name_var.set(row[1] or "")
        self.category_var.set(row[2] or "")
        self.carbs_var.set("" if row[3] is None else str(row[3]))
        self.gi_var.set("" if row[4] is None else str(row[4]))
        self.ginote_var.set(row[5] or "")
        self.sodium_var.set("" if row[6] is None else str(row[6]))
        self.sodium_status_var.set(row[7] or "")
        self.calories_var.set("" if row[8] is None else str(row[8]))
        self.serving_var.set(row[9] or "")

    def _float_or_none(self, s, field):
        s = (s or "").strip()
        if s == "":
            return None
        try:
            return float(s)
        except ValueError:
            raise ValueError(f"{field} must be a number (or blank).")

    def _read_form(self):
        name = self.name_var.get().strip()
        if not name:
            raise ValueError("Name is required.")
        return (
            name,
            self.category_var.get().strip(),
            self._float_or_none(self.carbs_var.get(), "Carbs"),
            self._float_or_none(self.gi_var.get(), "Glycemic Index"),
            self.ginote_var.get().strip(),
            self._float_or_none(self.sodium_var.get(), "Sodium"),
            self.sodium_status_var.get().strip(),
            self._float_or_none(self.calories_var.get(), "Calories"),
            self.serving_var.get().strip(),
        )

    def on_add(self):
        try:
            name, category, carbs, gi, ginote, sodium, sodium_status, calories, serving_size = self._read_form()
            models.add_food(name, category, carbs, gi, ginote, sodium, sodium_status, calories, serving_size)
            self.refresh_list()
            self._select_name_in_list(name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_update(self):
        if not self.selected_name:
            messagebox.showerror("Error", "Select a food first.")
            return
        try:
            name, category, carbs, gi, ginote, sodium, sodium_status, calories, serving_size = self._read_form()
            models.update_food(self.selected_name, name, category, carbs, gi, ginote, sodium, sodium_status, calories, serving_size)
            self.selected_name = name
            self.refresh_list()
            self._select_name_in_list(name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_delete(self):
        if not self.selected_name:
            messagebox.showerror("Error", "Select a food first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete '{self.selected_name}'?"):
            return
        try:
            models.delete_food(self.selected_name)
            self.clear_form()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_serving_size_for_selected(self):
        if not self.selected_name:
            messagebox.showerror("Error", "Select a food first.")
            return
        new_size = simpledialog.askstring("Serving Size", f"Serving size for {self.selected_name}:", initialvalue=self.serving_var.get())
        if new_size is None:
            return
        try:
            row = models.find_food_info(self.selected_name)
            if row is None:
                messagebox.showerror("Error", "Food not found.")
                self.refresh_list()
                return
            models.update_food(self.selected_name, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], new_size.strip())
            self.serving_var.set(new_size.strip())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _select_name_in_list(self, name):
        for i in range(self.food_list.size()):
            if self.food_list.get(i) == name:
                self.food_list.selection_clear(0, tk.END)
                self.food_list.selection_set(i)
                self.food_list.see(i)
                self.on_select()
                return

