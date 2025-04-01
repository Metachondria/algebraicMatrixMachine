import tkinter as tk
from tkinter import ttk, messagebox
from matrix import MatrixonRings

class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        self.matrix1_entries = []
        self.matrix2_entries = []

        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Экран приветствия с выбором размеров матриц"""
        self.clear_screen()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="Matrix Calculator", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        # Выбор размеров матриц
        size_frame = tk.Frame(frame, bg="#f0f0f0")
        size_frame.pack(pady=10)

        tk.Label(size_frame, text="Matrix 1 size:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.rows1 = ttk.Combobox(size_frame, values=[1, 2, 3, 4, 5], width=3, state="readonly")
        self.rows1.current(0)
        self.rows1.grid(row=0, column=1)
        tk.Label(size_frame, text="x", bg="#f0f0f0").grid(row=0, column=2)
        self.cols1 = ttk.Combobox(size_frame, values=[1, 2, 3, 4, 5], width=3, state="readonly")
        self.cols1.current(0)
        self.cols1.grid(row=0, column=3)

        tk.Label(size_frame, text="Matrix 2 size:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=10)
        self.rows2 = ttk.Combobox(size_frame, values=[1, 2, 3, 4, 5], width=3, state="readonly")
        self.rows2.current(0)
        self.rows2.grid(row=1, column=1)
        tk.Label(size_frame, text="x", bg="#f0f0f0").grid(row=1, column=2)
        self.cols2 = ttk.Combobox(size_frame, values=[1, 2, 3, 4, 5], width=3, state="readonly")
        self.cols2.current(0)
        self.cols2.grid(row=1, column=3)

        ttk.Button(frame, text="Next", command=self.create_input_screen).pack(pady=20)

    def create_input_screen(self):
        """Экран ввода матриц"""
        try:
            self.size1 = (int(self.rows1.get()), int(self.cols1.get()))
            self.size2 = (int(self.rows2.get()), int(self.cols2.get()))
        except:
            messagebox.showerror("Error", "Invalid matrix size")
            return

        self.clear_screen()

        # Основной контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Левая панель (матрицы)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        # Правая панель (настройки и результат)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="y", padx=20)

        # Создаем матрицы
        self.create_matrix_container(left_frame, "Matrix 1", self.size1, self.matrix1_entries)
        self.create_matrix_container(left_frame, "Matrix 2", self.size2, self.matrix2_entries)

        # Панель управления
        control_frame = ttk.LabelFrame(right_frame, text="Operations")
        control_frame.pack(fill="x", pady=10)

        # Выбор кольца
        tk.Label(control_frame, text="Ring:").grid(row=0, column=0, padx=5, pady=5)
        self.ring_var = tk.StringVar(value="float")
        ttk.Radiobutton(control_frame, text="Float", variable=self.ring_var, value="float").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(control_frame, text="Boolean", variable=self.ring_var, value="bool").grid(row=0, column=2, padx=5)

        # Выбор операции
        tk.Label(control_frame, text="Basic operations:").grid(row=1, column=0, padx=5, pady=5)
        self.op_var = tk.StringVar(value="add")
        ttk.Radiobutton(control_frame, text="Add", variable=self.op_var, value="add").grid(row=1, column=1, padx=5)
        ttk.Radiobutton(control_frame, text="Multiply", variable=self.op_var, value="multiply").grid(row=1, column=2, padx=5)

        # Кнопки
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        ttk.Button(button_frame, text="Back", command=self.create_welcome_screen).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Calculate", command=self.perform_operation).pack(side="left", padx=5)

        # Дополнительные операции
        ttk.Label(control_frame, text="Advanced:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Floyd-Warshall (Matrix 1)",
                  command=lambda: self.perform_floyd(1)).grid(row=3, column=1, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Floyd-Warshall (Matrix 2)",
                  command=lambda: self.perform_floyd(2)).grid(row=4, column=1, columnspan=2, pady=5)

        # Результат
        self.result_frame = ttk.LabelFrame(right_frame, text="Result")
        self.result_frame.pack(fill="both", expand=True, pady=10)

    def perform_floyd(self, matrix_num):
        """Выполняет алгоритм Флойда-Уоршелла для выбранной матрицы"""
        try:
            # Получаем данные матрицы
            if matrix_num == 1:
                entries = self.matrix1_entries[0]
                size = self.size1
            else:
                entries = self.matrix2_entries[0]
                size = self.size2

            # Проверяем что матрица квадратная
            if size[0] != size[1]:
                raise ValueError("Matrix must be square for Floyd-Warshall algorithm")

            matrix = self.get_matrix_data(entries, is_bool=False)

            # Создаем матрицу с операциями min и +
            mat = MatrixonRings(matrix, add_op=min, mul_op=lambda a, b: a + b)
            result = mat.find_shortest()

            # Отображаем результат
            self.create_matrix_view(self.result_frame, result.matrix, f"Floyd-Warshall Result (Matrix {matrix_num})")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_matrix_container(self, parent, title, size, entries_list):
        """Контейнер для отображения одной матрицы"""
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Создаем сетку Entry
        entries = []
        for i in range(size[0]):
            row = []
            for j in range(size[1]):
                entry = ttk.Entry(frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            entries.append(row)
        entries_list.append(entries)

        # Добавляем валидацию для булевых значений
        if "Matrix 1" in title:
            for row in entries:
                for entry in row:
                    entry.config(validate="key", validatecommand=(self.root.register(self.validate_input), '%P'))

    def create_matrix_view(self, parent, matrix, title):
        """Создает красивое отображение матрицы"""
        for widget in parent.winfo_children():
            widget.destroy()

        parent.config(text=title)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                value = matrix[i][j]
                if isinstance(value, bool):
                    text = "T" if value else "F"
                    bg = "#d4edda" if value else "#f8d7da"
                else:
                    text = f"{value:.2f}" if isinstance(value, float) else str(value)
                    bg = "white"

                label = tk.Label(parent, text=text, bg=bg, relief="groove", padx=10, pady=5)
                label.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")

    def perform_operation(self):
        """Выполняет операцию и отображает результат"""
        try:
            # Получаем данные матриц
            m1 = self.get_matrix_data(self.matrix1_entries[0], self.ring_var.get() == "bool")
            m2 = self.get_matrix_data(self.matrix2_entries[0], self.ring_var.get() == "bool")

            # Создаем объекты MatrixonRings
            if self.ring_var.get() == "bool":
                add_op = lambda a, b: a or b
                mul_op = lambda a, b: a and b
            else:
                add_op = lambda a, b: a + b
                mul_op = lambda a, b: a * b

            mat1 = MatrixonRings(m1, add_op, mul_op)
            mat2 = MatrixonRings(m2, add_op, mul_op)

            # Выполняем операцию
            if self.op_var.get() == "add":
                result = mat1 + mat2
            else:
                result = mat1.matmul(mat2)

            # Отображаем результат
            self.create_matrix_view(self.result_frame, result.matrix, "Operation Result")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_matrix_data(self, entries, is_bool=False):
        """Получает данные из полей ввода"""
        matrix = []
        for row in entries:
            new_row = []
            for entry in row:
                value = entry.get().strip()
                if is_bool:
                    if value.lower() in ('t', 'true', '1'):
                        new_row.append(True)
                    elif value.lower() in ('f', 'false', '0'):
                        new_row.append(False)
                    else:
                        raise ValueError(f"Invalid boolean value: {value}")
                else:
                    try:
                        new_row.append(float(value))
                    except:
                        raise ValueError(f"Invalid number: {value}")
            matrix.append(new_row)
        return matrix

    def clear_screen(self):
        """Очищает текущий экран"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def validate_input(self, value):
        """Валидация ввода для булевых значений"""
        if self.ring_var.get() == "bool":
            return value.lower() in ('t', 'f', 'true', 'false', '0', '1', '')
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()