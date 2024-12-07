import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Notebook  # Исправленный импорт
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import string
import networkx as nx
from collections import deque

# Ваши алгоритмы
from graph import Graph  # Подключаем ваши классы и алгоритмы (в граф.py)


class SpaceExpeditionApp(tk.Tk):
    def __init__(self, graph=None):
        super().__init__()
        self.graph = graph or nx.Graph()  # Если граф не передан, создаем новый
        self.positions = {}  # Словарь для хранения позиций вершин
        self.title("Космическая экспедиция")
        self.geometry("800x600")

        # Инициализация вкладок
        self.tab_control = Notebook(self)  # Используем Notebook из ttk

        # Вкладка Космос
        self.cosmos_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.cosmos_tab, text="Космос")
        self.tab_control.pack(expand=1, fill="both")

        self.create_cosmos_tab()

        # Создание области для графа
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.cosmos_tab)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.update_graph()

    def add_edge(self, u, v, weight):
        self.graph.add_edge(u, v, weight=weight)

    def add_node(self, node):
        self.graph.add_node(node)

    def create_cosmos_tab(self):
        # Создаем основной фрейм для горизонтального разделения
        main_frame = tk.Frame(self.cosmos_tab)
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Левый блок для выбора задания и сложности
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # Блок для выбора задания
        self.task_label = tk.Label(left_frame, text="Выберите задание", font=("Helvetica", 14))
        self.task_label.pack(pady=10)

        self.task_options = ["Минимизация топлива", "Центральная база", "Объединение планет"]
        self.task_var = tk.StringVar(self)
        self.task_var.set(self.task_options[0])

        self.task_menu = tk.OptionMenu(left_frame, self.task_var, *self.task_options,
                                       command=self.update_task_description)
        self.task_menu.pack(pady=10)

        # Блок для выбора сложности
        self.difficulty_label = tk.Label(left_frame, text="Выберите сложность", font=("Helvetica", 14))
        self.difficulty_label.pack(pady=10)

        self.difficulty_options = ["Лёгкий", "Средний", "Тяжёлый"]
        self.difficulty_var = tk.StringVar(self)
        self.difficulty_var.set(self.difficulty_options[0])

        self.difficulty_menu = tk.OptionMenu(left_frame, self.difficulty_var, *self.difficulty_options)
        self.difficulty_menu.pack(pady=10)

        # Кнопка для генерации графа
        self.generate_button = tk.Button(left_frame, text="Генерировать граф", command=self.generate_and_display_graph)
        self.generate_button.pack(pady=10)

        # Кнопка для выполнения задания
        self.run_button = tk.Button(left_frame, text="Выполнить задание", command=self.run_task)
        self.run_button.pack(pady=10)

        # Средний блок для описания задания и списка рёбер
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # Блок для описания задания
        desc_frame = tk.Frame(middle_frame)
        desc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        desc_label = tk.Label(desc_frame, text="Описание задания", font=("Helvetica", 14))
        desc_label.pack(pady=5)

        desc_scrollbar = tk.Scrollbar(desc_frame, orient=tk.VERTICAL)
        self.desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=15, width=40, yscrollcommand=desc_scrollbar.set)
        desc_scrollbar.config(command=self.desc_text.yview)

        desc_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.desc_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Блок для отображения рёбер графа
        edges_frame = tk.Frame(middle_frame)
        edges_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        edges_label = tk.Label(edges_frame, text="Связи между вершинами", font=("Helvetica", 14))
        edges_label.pack(pady=5)

        edges_scrollbar = tk.Scrollbar(edges_frame, orient=tk.VERTICAL)
        self.edges_text = tk.Text(edges_frame, wrap=tk.WORD, height=15, width=40, yscrollcommand=edges_scrollbar.set)
        edges_scrollbar.config(command=self.edges_text.yview)

        self.edges_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        edges_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Правый блок для выбора вершин
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        # Заголовок для выбора вершин
        self.vertex_label = tk.Label(right_frame, text="Выберите вершины (для минимизации топлива)",
                                     font=("Helvetica", 14))
        self.vertex_label.pack(pady=10)

        # Поле для выбора начальной вершины
        self.start_var = tk.StringVar(self)
        self.start_var.set("")

        self.start_label = tk.Label(right_frame, text="Начальная вершина:")
        self.start_label.pack(pady=5)

        self.start_menu = tk.OptionMenu(right_frame, self.start_var, "")
        self.start_menu.pack(pady=5)

        # Поле для выбора конечной вершины
        self.end_var = tk.StringVar(self)
        self.end_var.set("")

        self.end_label = tk.Label(right_frame, text="Конечная вершина:")
        self.end_label.pack(pady=5)

        self.end_menu = tk.OptionMenu(right_frame, self.end_var, "")
        self.end_menu.pack(pady=5)

        # Метка для результата
        self.result_label = tk.Label(self.cosmos_tab, text="Результат: ", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

    def update_task_description(self, selected_task):
        descriptions = {
            "Минимизация топлива": """\
    Путешествуйте между планетами и найдите самый короткий маршрут, чтобы сэкономить топливо. Выберите начальную и конечную планету, и мы вычислим кратчайший путь.

    Задача:
    Используя алгоритм Дейкстры, найдите кратчайший путь от стартовой планеты к целевой.

    Алгоритм:
    Алгоритм Дейкстры (для поиска кратчайшего пути). Вы получите результат, который будет отображен на графе с выделением кратчайшего пути между выбранными вершинами.""",

            "Центральная база": """\
    Ваша задача — найти центральную базу для экспедиции, которая минимизирует время путешествия до всех других планет. Используйте алгоритм, чтобы определить, какие планеты являются наиболее удобными для центральной базы.

    Задача:
    Вычислить эксцентриситет каждой планеты, чтобы найти центральную базу. База должна быть расположена в центре космической системы.

    Алгоритм:
    Для нахождения центра графа используется алгоритм поиска эксцентриситетов и радиуса графа.""",

            "Объединение планет": """\
    Объедините все планеты в единую систему связи, используя минимальное количество топлива для построения маршрутов.

    Задача:
    Найдите минимальное остовное дерево, чтобы соединить все планеты с минимальными затратами (по весу рёбер).

    Алгоритм:
    Используется алгоритм Краскала для нахождения минимального остовного дерева."""
        }

        # Обновляем текстовое поле с описанием
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, descriptions.get(selected_task, ""))

    def update_edges_display(self, graph):
        self.edges_text.delete(1.0, tk.END)  # Очистка предыдущего содержимого
        if not graph or not graph.edges:
            self.edges_text.insert(tk.END, "Граф пуст или не сгенерирован.")
            return

        edges_set = set()
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 'нет данных')
            edge = tuple(sorted((u, v)))
            if edge not in edges_set:
                edges_set.add(edge)
                self.edges_text.insert(tk.END, f"{u} --- {v} Световых лет для перемещения: {weight}\n")

        # Проверка на изолированные вершины
        for node in graph.nodes:
            if graph.degree[node] == 0:
                self.edges_text.insert(tk.END, f"{node} недостижима. ")
                self.edges_text.insert(tk.END,
                                       "Ваш транспорт недостаточно оснащен для преодоления такого расстояния.\n")

    def generate_planet_names(self, num_names):
        prefixes = ["Zar", "Alt", "Ver", "Kor", "Lun", "Pro", "Eri", "Xen", "Gal", "Tir"]
        bases = ["nox", "mus", "dar", "lon", "mir", "pex", "quo", "vix", "tor", "lin"]
        suffixes = ["ia", "on", "ar", "us", "ix", "is", "um", "or", "as", "ae"]
        used_names = set()

        def random_index():
            return ''.join(random.choices(string.digits, k=2))  # Двухзначный индекс

        planet_names = []
        for _ in range(num_names):
            while True:
                prefix = random.choice(prefixes)
                base = random.choice(bases)
                suffix = random.choice(suffixes)
                index = random_index()
                name = f"{prefix}{base}{suffix} {index}"
                if name not in used_names:  # Уникальное имя
                    used_names.add(name)
                    planet_names.append(name)
                    break
        return planet_names

    def generate_graph(self, difficulty="easy"):
        # Определяем параметры графа в зависимости от сложности
        if difficulty == "easy":
            num_vertices = random.randint(5, 10)
            num_edges = random.randint(7, 15)
        elif difficulty == "medium":
            num_vertices = random.randint(7, 15)
            num_edges = random.randint(15, 25)
        elif difficulty == "hard":
            num_vertices = random.randint(15, 30)
            num_edges = random.randint(25, 50)
        else:
            raise ValueError("Invalid difficulty level")

        # Создаем пустой граф
        graph = nx.Graph()

        # Генерация строковых меток для вершин
        nodes = self.generate_planet_names(num_vertices)
        graph.add_nodes_from(nodes)

        # Генерация случайных рёбер
        edges = set()
        while len(edges) < num_edges:
            u, v = random.sample(nodes, 2)  # Выбираем две разные вершины
            if u != v:  # Избегаем петель
                edges.add((u, v, random.randint(1, 10)))  # Вес рёбер от 1 до 10

        # Добавляем рёбра в граф
        graph.add_weighted_edges_from(edges)

        # Генерация начальных позиций узлов (если не было сохранено)
        positions = nx.spring_layout(graph)

        return graph, positions

    def generate_and_display_graph(self):
        difficulty_map = {
            "Лёгкий": "easy",
            "Средний": "medium",
            "Тяжёлый": "hard"
        }
        difficulty = self.difficulty_var.get()
        difficulty = difficulty_map.get(difficulty, "easy")

        self.graph, self.positions = self.generate_graph(difficulty)
        self.update_graph()

        # Получаем список вершин
        nodes = list(self.graph.nodes)

        if len(nodes) >= 2:
            self.start_var.set(nodes[0])
            self.end_var.set(nodes[1])
        else:
            self.start_var.set("")
            self.end_var.set("")

        # Очистка существующих элементов в меню
        self.start_menu['menu'].delete(0, 'end')
        self.end_menu['menu'].delete(0, 'end')

        # Добавляем новые вершины в меню
        for node in nodes:
            self.start_menu['menu'].add_command(label=node, command=lambda n=node: self.start_var.set(n))
            self.end_menu['menu'].add_command(label=node, command=lambda n=node: self.end_var.set(n))


        self.update_graph()
        self.update_edges_display(self.graph)  # Обновление списка рёбер

    def run_task(self):
        task = self.task_var.get()
        if task == "Минимизация топлива":
            self.minimize_fuel_task()
        elif task == "Центральная база":
            self.find_center_task()
        elif task == "Объединение планет":
            self.minimum_spanning_tree_task()

    def reconstruct_path(self, predecessors, start, end):
        # Восстановление пути из предшественников
        path = []
        current = end

        # Пока не дошли до начальной вершины
        while current != start:
            path.append(current)

            # Проверяем, что предшественник существует и является правильным типом
            if isinstance(predecessors[current], list):
                # Если предшественник это список (например, несколько предшественников), выбираем первый
                current = predecessors[current][0]
            else:
                current = predecessors[current]

        path.append(start)  # Добавляем начальную вершину
        path.reverse()  # Переворачиваем путь, чтобы он был от start до end
        return path

    def minimize_fuel_task(self):
        # Выбираем случайные вершины из существующих в графе
        nodes = list(self.graph.nodes)
        if len(nodes) < 2:
            messagebox.showerror("Ошибка", "Граф должен содержать хотя бы две вершины.")
            return

        start_vertex = self.start_var.get()
        end_vertex = self.end_var.get()

        if start_vertex == end_vertex:
            messagebox.showerror("Ошибка", "Начальная и конечная вершины должны быть разными.")
            return

        if start_vertex not in self.graph or end_vertex not in self.graph:
            messagebox.showerror("Ошибка", f"Одна или обе вершины не найдены в графе: {start_vertex}, {end_vertex}")
            return

        try:
            if not nx.has_path(self.graph, start_vertex, end_vertex):
                result_text = f"Путь от {start_vertex} до {end_vertex} недостижим."
                self.result_label.config(text=result_text)
                self.update_graph()
                return

            # Используем функцию из networkx для нахождения кратчайшего пути и стоимости
            distances, predecessors = nx.single_source_dijkstra(self.graph, start_vertex)
            path = nx.shortest_path(self.graph, source=start_vertex, target=end_vertex, weight='weight')
            fuel_cost = nx.shortest_path_length(self.graph, source=start_vertex, target=end_vertex, weight='weight')

            result_text = f"Кратчайший путь от {start_vertex} до {end_vertex}: {' -> '.join(map(str, path))}\n" \
                          f"Общий расход топлива: {fuel_cost}"
            self.result_label.config(text=result_text)
            self.update_graph()

            for u, v in zip(path[:-1], path[1:]):
                nx.draw_networkx_edges(self.graph, self.positions, edgelist=[(u, v)], edge_color='green', width=2,
                                       ax=self.ax)
            self.canvas.draw()

        except nx.NetworkXNoPath:
            messagebox.showerror("Ошибка", f"Нет пути между {start_vertex} и {end_vertex}.")

    def find_center_task(self):
        # Преобразуем граф из NetworkX в ваш класс Graph
        graph = Graph()
        graph.from_networkx(self.graph)  # Преобразуем текущий граф NetworkX в объект Graph

        # Шаг 1: Определяем главную компоненту
        main_component, isolated_edges = graph.identify_main_component()

        # Шаг 2: Создаём подграф для главной компоненты
        subgraph = {vertex: [edge for edge in graph.adjacency_list[vertex] if edge[0] in main_component]
                    for vertex in main_component}

        # Шаг 3: Временно подменяем список смежности и находим центр
        graph.adjacency_list = subgraph
        center = graph.find_graph_center()
        graph.adjacency_list = {**graph.adjacency_list, **subgraph}  # Восстанавливаем полный граф

        # Обновляем текст с результатом
        result_text = f"Центральная база (в главной компоненте): {', '.join(center)}"
        self.result_label.config(text=result_text)

        # Шаг 4: Отрисовка графа с сохранением названий вершин и весов рёбер
        self.ax.clear()  # Очищаем ось перед новой отрисовкой
        self.ax.axis("off")  # Убираем прямоугольник вокруг графа

        # Рисуем весь граф
        nx.draw_networkx(self.graph, self.positions, ax=self.ax, with_labels=True)

        # Вершины главной компоненты (зелёные — центральные)
        nx.draw_networkx_nodes(
            self.graph,
            self.positions,
            nodelist=list(main_component),
            node_color=["green" if node in center else "blue" for node in main_component],
            ax=self.ax
        )

        # Изолированные вершины (серые)
        isolated_nodes = [node for node in self.graph.nodes if node not in main_component]
        nx.draw_networkx_nodes(self.graph, self.positions, nodelist=isolated_nodes, node_color="gray",  ax=self.ax)

        # Рёбра графа
        main_component_edges = [(u, v) for u, v, *_ in self.graph.edges if u in main_component and v in main_component]
        nx.draw_networkx_edges(self.graph, self.positions, edgelist=main_component_edges, edge_color="blue", width=2, ax=self.ax)

        isolated_edges = [(u, v) for u, v, *_ in self.graph.edges if u not in main_component or v not in main_component]
        nx.draw_networkx_edges(self.graph, self.positions, edgelist=isolated_edges, edge_color="gray", width=2, ax=self.ax)

        # Шаг 5: Перерисовка canvas
        self.canvas.draw()

    def minimum_spanning_tree_task(self):
        # Преобразуем граф из NetworkX в ваш класс Graph
        graph = Graph()
        graph.from_networkx(self.graph)  # Преобразуем текущий граф NetworkX в объект Graph

        # Теперь используем метод вашего класса для нахождения минимального остовного дерева
        mst = graph.kruskal_mst()

        # Формируем текст результата
        mst_edges_text = [f"{u} - {v} (вес {weight})" for u, v, weight in mst]
        result_text = "Минимальное остовное дерево:\n" + "\n".join(mst_edges_text)

        # Обновляем результат в интерфейсе
        self.result_label.config(text=result_text)
        self.update_graph()  # Обновим граф

        mst_edges = list(nx.minimum_spanning_edges(self.graph, data=False))
        nx.draw_networkx_edges(self.graph, self.positions, edgelist=mst_edges, edge_color='green', width=2, ax=self.ax)
        self.canvas.draw()

    def update_graph(self):
        """Обновление визуализации графа"""
        self.ax.clear()  # Очищаем предыдущую визуализацию
        self.ax.axis('off')

        # Рисуем граф с позициями
        if not self.positions:
            self.positions = nx.spring_layout(self.graph)  # Если позиции не сгенерированы, создаём их

        nx.draw(self.graph, pos=self.positions, ax=self.ax,
                with_labels=True, node_color='lightblue', edge_color='gray',
                node_size=500, font_size=10)

        # Рисуем веса рёбер, если они есть
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos=self.positions, ax=self.ax, edge_labels=edge_labels)

        self.canvas.draw()  # Перерисовываем canvas


# Запуск приложения
if __name__ == "__main__":
    graph = nx.Graph()  # Используем NetworkX Graph напрямую
    app = SpaceExpeditionApp(graph)
    app.mainloop()
