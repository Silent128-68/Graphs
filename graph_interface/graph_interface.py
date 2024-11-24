import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from graph import Graph  # Ваш класс Graph
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический интерфейс для работы с графами")
        self.graph = None  # Изначально граф не выбран
        self.nx_graph = nx.Graph()  # Граф для визуализации
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_canvas()

        # Вопрос пользователю: загрузить граф или создать новый
        self.ask_initial_action()

    def ask_initial_action(self):
        choice = messagebox.askyesnocancel(
            "Выбор действия",
            "Вы хотите загрузить граф из файла?\nНажмите 'Да' для загрузки, 'Нет' для создания нового графа."
        )
        if choice is True:
            self.load_graph()
        elif choice is False:
            self.create_new_graph()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Загрузить граф из файла", command=self.load_graph)
        file_menu.add_command(label="Сохранить граф в файл", command=self.save_graph)
        file_menu.add_command(label="Создать новый граф", command=self.create_new_graph)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Редактировать"
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Добавить вершину", command=self.add_vertex)
        edit_menu.add_command(label="Добавить ребро", command=self.add_edge)
        edit_menu.add_command(label="Удалить вершину", command=self.remove_vertex)
        edit_menu.add_command(label="Удалить ребро", command=self.remove_edge)
        menu_bar.add_cascade(label="Редактировать", menu=edit_menu)

        # Меню "Анализ"
        analysis_menu = tk.Menu(menu_bar, tearoff=0)
        analysis_menu.add_command(label="Основная компонента и изолированные рёбра", command=self.show_main_component)
        analysis_menu.add_command(label="Длина кратчайшего пути и все пути", command=self.find_shortest_paths)
        analysis_menu.add_command(label="Определить N-периферию", command=self.find_n_periphery)
        analysis_menu.add_command(label="Найти отрицательные циклы", command=self.find_negative_cycles)
        # Новые функции
        analysis_menu.add_command(label="Решить задание 1 (полустепень захода)", command=self.solve_task1)
        analysis_menu.add_command(label="Решить задание 2 (заходящие соседи)", command=self.solve_task2)
        analysis_menu.add_command(label="Решить задание 3 (удалить непарные дуги)", command=self.solve_task3)
        analysis_menu.add_command(label="Найти все пути между вершинами (DFS)", command=self.find_all_paths)
        analysis_menu.add_command(label="Найти центр графа (BFS)", command=self.find_graph_center)
        analysis_menu.add_command(label="Найти минимальное остовное дерево (Kruskal)",
                                  command=self.find_minimum_spanning_tree)
        menu_bar.add_cascade(label="Анализ", menu=analysis_menu)

        self.root.config(menu=menu_bar)

    def create_canvas(self):
        self.ax.clear()
        self.ax.set_title("Визуализация графа")
        self.ax.axis("off")

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graph_visualization(self):
        self.ax.clear()
        self.ax.set_title("Визуализация графа")
        self.ax.axis("off")

        if self.graph:
            # Преобразуем ваш граф в объект NetworkX
            self.nx_graph = self.graph.to_networkx()
            pos = nx.spring_layout(self.nx_graph)

            # Рисуем вершины и ребра
            nx.draw(
                self.nx_graph, pos, ax=self.ax, with_labels=True,
                node_color="lightblue", font_weight="bold"
            )

            # Если граф взвешенный, добавляем веса рёбер
            if self.graph.weighted:
                edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
                nx.draw_networkx_edge_labels(
                    self.nx_graph, pos, edge_labels=edge_labels,
                    ax=self.ax, font_size=8, label_pos=0.5
                )

        self.canvas.draw()

    def load_graph(self):
        filename = filedialog.askopenfilename(title="Выберите файл графа")
        if filename:
            try:
                self.graph = Graph()
                self.graph.load_from_file(filename)
                self.update_graph_visualization()
                print(f"Граф загружен из файла: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить граф: {e}")

    def save_graph(self):
        if not self.ensure_graph_loaded():
            return
        filename = filedialog.asksaveasfilename(title="Сохранить граф в файл")
        if filename:
            try:
                self.graph.save_to_file(filename)
                print(f"Граф сохранён в файл: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить граф: {e}")

    def create_new_graph(self):
        directed = messagebox.askyesno("Тип графа", "Граф ориентированный?")
        weighted = messagebox.askyesno("Тип графа", "Граф взвешенный?")
        self.graph = Graph(directed=directed, weighted=weighted)
        self.nx_graph.clear()
        self.update_graph_visualization()
        print("Создан новый граф.")

    def ensure_graph_loaded(self):
        if self.graph is None:
            messagebox.showerror("Ошибка", "Сначала загрузите граф или создайте новый!")
            return False
        return True

    def add_vertex(self):
        if not self.ensure_graph_loaded():
            return
        vertex = simpledialog.askstring("Добавить вершину", "Введите имя вершины:")
        if vertex:
            self.graph.add_vertex(vertex)
            self.update_graph_visualization()
            print(f"Добавлена вершина: {vertex}")

    def add_edge(self):
        if not self.ensure_graph_loaded():
            return
        u = simpledialog.askstring("Добавить ребро", "Введите первую вершину:")
        v = simpledialog.askstring("Добавить ребро", "Введите вторую вершину:")
        if self.graph.weighted:
            weight = simpledialog.askfloat("Добавить ребро", "Введите вес ребра:")
        else:
            weight = None
        if u and v:
            success = self.graph.add_edge(u, v, weight)
            if success:
                self.update_graph_visualization()
                print(f"Добавлено ребро: {u} -> {v} (Вес: {weight})")
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить ребро.")

    def remove_vertex(self):
        if not self.ensure_graph_loaded():
            return
        vertex = simpledialog.askstring("Удалить вершину", "Введите имя вершины:")
        if vertex:
            self.graph.remove_vertex(vertex)
            self.update_graph_visualization()
            print(f"Удалена вершина: {vertex}")

    def remove_edge(self):
        if not self.ensure_graph_loaded():
            return
        u = simpledialog.askstring("Удалить ребро", "Введите первую вершину:")
        v = simpledialog.askstring("Удалить ребро", "Введите вторую вершину:")
        if u and v:
            self.graph.remove_edge(u, v)
            self.update_graph_visualization()
            print(f"Удалено ребро: {u} -> {v}")

    def solve_task1(self):
        if not self.ensure_graph_loaded():
            return
        vertex = simpledialog.askstring("Полустепень захода", "Введите вершину:")
        if vertex:
            in_degree = self.graph.in_degree(vertex)
            messagebox.showinfo("Результат", f"Полустепень захода вершины {vertex}: {in_degree}")

    def solve_task2(self):
        if not self.ensure_graph_loaded():
            return
        vertex = simpledialog.askstring("Заходящие соседи", "Введите вершину:")
        if vertex:
            neighbors = self.graph.incoming_neighbors(vertex)
            messagebox.showinfo("Результат", f"Заходящие соседи вершины {vertex}: {', '.join(neighbors)}")

    def solve_task3(self):
        if not self.ensure_graph_loaded():
            return
        self.graph.remove_unpaired_edges()
        self.update_graph_visualization()
        messagebox.showinfo("Результат", "Непарные дуги удалены.")

    def find_all_paths(self):
        if not self.ensure_graph_loaded():
            return
        u = simpledialog.askstring("Все пути (DFS)", "Введите начальную вершину:")
        v = simpledialog.askstring("Все пути (DFS)", "Введите конечную вершину:")
        if u and v:
            paths = self.graph.find_all_paths(u, v)
            messagebox.showinfo("Результат", f"Все пути от {u} до {v}: {paths}")

    def find_graph_center(self):
        if not self.ensure_graph_loaded():
            return
        center = self.graph.find_center()
        messagebox.showinfo("Результат", f"Центр графа: {center}")

    def find_minimum_spanning_tree(self):
        if not self.ensure_graph_loaded():
            return
        mst = self.graph.kruskal_mst()
        messagebox.showinfo("Результат", f"Минимальное остовное дерево: {mst}")

    def show_main_component(self):
        if not self.ensure_graph_loaded():
            return
        main_component, isolated_edges = self.graph.find_main_component_and_isolated_edges()
        print(f"Основная компонента: {main_component}\nИзолированные рёбра: {isolated_edges}")

    def find_shortest_paths(self):
        if not self.ensure_graph_loaded():
            return
        u = simpledialog.askstring("Кратчайшие пути", "Введите начальную вершину:")
        v = simpledialog.askstring("Кратчайшие пути", "Введите конечную вершину:")
        if u and v:
            paths, length = self.graph.find_shortest_paths_and_length(u, v)
            print(f"Длина: {length}\nПути: {paths}")

    def find_n_periphery(self):
        if not self.ensure_graph_loaded():
            return
        n = simpledialog.askinteger("N-периферия", "Введите значение N:")
        if n is not None:
            periphery = self.graph.find_n_periphery(n)
            print(f"N-периферия: {periphery}")

    def find_negative_cycles(self):
        if not self.ensure_graph_loaded():
            return
        cycles = self.graph.find_negative_cycles()
        print(f"Отрицательные циклы: {cycles}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
