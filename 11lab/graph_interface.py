import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from graph import Graph  # Ваш класс Graph
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический интерфейс для работы с графами")
        self.graph = None  # Изначально граф не выбран
        self.nx_graph = nx.Graph()  # Граф для визуализации
        self.vertex_positions = {}  # Хранение позиций вершин
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_canvas()
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
        analysis_menu.add_command(label="Решить задание 1 (полустепень захода)", command=self.solve_task1)
        analysis_menu.add_command(label="Решить задание 2 (заходящие соседи)", command=self.solve_task2)
        analysis_menu.add_command(label="Решить задание 3 (удалить непарные дуги)", command=self.solve_task3)
        analysis_menu.add_command(label="Найти все пути между вершинами (DFS)", command=self.find_all_paths)
        analysis_menu.add_command(label="Найти центр графа (BFS)", command=self.find_graph_center)
        analysis_menu.add_command(label="Найти минимальное остовное дерево (Kruskal)",
                                  command=self.find_minimum_spanning_tree)
        analysis_menu.add_command(label="Основная компонента и изолированные рёбра", command=self.show_main_component)
        analysis_menu.add_command(label="Длина кратчайшего пути и все пути", command=self.find_shortest_paths)
        analysis_menu.add_command(label="Определить N-периферию", command=self.find_n_periphery)
        analysis_menu.add_command(label="Найти отрицательные циклы", command=self.find_negative_cycles)
        analysis_menu.add_command(label="Найти максимальный поток", command=self.find_max_flow)
        menu_bar.add_cascade(label="Анализ", menu=analysis_menu)

        # Кнопка перегенерации
        regenerate_button = tk.Button(self.root, text="Перегенерировать", command=self.regenerate_graph)
        regenerate_button.pack()

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

    def randomize_positions(self):
        """Генерация случайных позиций вершин."""
        width, height = 800, 600  # Размеры окна рисования
        self.vertex_positions = {
            vertex: (random.randint(50, width - 50), random.randint(50, height - 50))
            for vertex in self.graph.adjacency_list
        }

    def regenerate_graph(self):
        """Перегенерация позиций вершин."""
        if self.graph:
            self.randomize_positions()
            self.draw_graph()
        else:
            messagebox.showerror("Ошибка", "Граф не загружен или не создан!")

    def draw_graph(self):
        """Отрисовка графа с сохранением позиций."""
        self.ax.clear()
        self.ax.set_title("Визуализация графа")
        self.ax.axis("off")

        if self.graph:
            # Преобразуем граф в объект NetworkX
            self.nx_graph = self.graph.to_networkx()

            # Используем сохраненные позиции
            nx.draw(
                self.nx_graph, pos=self.vertex_positions, ax=self.ax, with_labels=True,
                node_color="lightblue", font_weight="bold"
            )

            # Если граф взвешенный, добавляем веса рёбер
            if self.graph.weighted:
                edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
                nx.draw_networkx_edge_labels(
                    self.nx_graph, pos=self.vertex_positions, edge_labels=edge_labels,
                    ax=self.ax, font_size=8, label_pos=0.5
                )

        self.canvas.draw()

    def load_graph(self):
        filename = filedialog.askopenfilename(title="Выберите файл графа")
        if filename:
            try:
                self.graph = Graph()
                self.graph.load_from_file(filename)
                if not self.vertex_positions:
                    self.randomize_positions()
                self.draw_graph()
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
            in_degree = self.graph.vertices_with_lower_indegree(vertex)
            messagebox.showinfo("Результат", f"Вершины с полустепенью захода менье, чем у {vertex}: {in_degree}")

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
        self.graph.remove_non_reciprocal_edges()
        self.update_graph_visualization()
        messagebox.showinfo("Результат", "Непарные дуги удалены.")

    def find_all_paths(self):
        if not self.ensure_graph_loaded():
            return
        u = simpledialog.askstring("Все пути (DFS)", "Введите начальную вершину:")
        v = simpledialog.askstring("Все пути (DFS)", "Введите конечную вершину:")
        if u and v:
            paths = self.graph.dfs_all_paths(u, v)
            messagebox.showinfo("Результат", f"Все пути от {u} до {v}: {paths}")

    def find_graph_center(self):
        if not self.ensure_graph_loaded():
            return
        center = self.graph.find_graph_center()
        messagebox.showinfo("Результат", f"Центр графа: {center}")

    def find_minimum_spanning_tree(self):
        if not self.ensure_graph_loaded():
            return
        mst = self.graph.kruskal_mst()
        messagebox.showinfo("Результат", f"Минимальное остовное дерево: {mst}")

    def show_main_component(self):
        if not self.ensure_graph_loaded():
            return
        main_component, isolated_edges = self.graph.identify_main_component()
        print(f"Основная компонента: {main_component}\nИзолированные рёбра: {isolated_edges}")

    def find_shortest_paths(self):
        if not self.ensure_graph_loaded():
            return

        u = simpledialog.askstring("Кратчайшие пути", "Введите начальную вершину:")
        if not u:
            return

        v = simpledialog.askstring("Кратчайшие пути", "Введите конечную вершину:")
        if not v:
            return

        try:
            paths, length = self.graph.find_all_shortest_paths(u, v)
            if paths:
                result = "\n".join([f"{' -> '.join(path)}" for path in paths])
                messagebox.showinfo("Результат", f"Длина: {length}\nПуть:\n{result}")
            else:
                messagebox.showinfo("Результат", f"Путь из {u} в {v} не существует.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при поиске кратчайших путей: {e}")

    def find_n_periphery(self):
        if not self.ensure_graph_loaded():
            return

        source = simpledialog.askstring("N-периферия", "Введите начальную вершину:")
        if source is None:
            return

        n = simpledialog.askinteger("N-периферия", "Введите значение N:")
        if n is None:
            return

        try:
            periphery = self.graph.find_n_periphery(source, n)
            messagebox.showinfo("Результат", f"N-периферия для вершины {source} при N={n}:\n{periphery}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при поиске N-периферии: {e}")

    def find_negative_cycles(self):
        if not self.ensure_graph_loaded():
            return
        try:
            all_cycles = set()  # Используем множество для хранения уникальных циклов
            for start in self.graph.adjacency_list:
                cycles = self.graph.bellman_ford(start)
                for cycle in cycles:
                    # Преобразуем цикл в кортеж с сортировкой для уникальности
                    normalized_cycle = tuple(sorted(cycle))
                    all_cycles.add(normalized_cycle)

            if all_cycles:
                result = "\n".join([f"Цикл: {cycle}" for cycle in all_cycles])
                messagebox.showinfo("Результат", f"Найдены отрицательные циклы:\n{result}")
            else:
                messagebox.showinfo("Результат", "Отрицательных циклов не найдено.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при поиске циклов: {e}")

    def find_max_flow(self):
        if not self.ensure_graph_loaded():
            return
        source = simpledialog.askstring("Максимальный поток", "Введите начальную вершину (источник):")
        if not source:
            return
        sink = simpledialog.askstring("Максимальный поток", "Введите конечную вершину (сток):")
        if not sink:
            return

        source = source.strip()
        sink = sink.strip()

        try:
            max_flow_value = self.graph.edmonds_karp_max_flow(source, sink)
            if max_flow_value is not None:
                messagebox.showinfo("Результат", f"Максимальный поток от {source} до {sink}: {max_flow_value}")
            else:
                messagebox.showerror("Ошибка", "Алгоритм применим только к ориентированным графам.")
        except ValueError as ve:
            messagebox.showerror("Ошибка", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при вычислении максимального потока: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
