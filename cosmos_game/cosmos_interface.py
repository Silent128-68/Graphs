import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Notebook  # Исправленный импорт
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
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
        # Выбор задания
        self.task_label = tk.Label(self.cosmos_tab, text="Выберите задание", font=("Helvetica", 14))
        self.task_label.pack(pady=10)

        self.task_options = ["Минимизация топлива", "Центральная база", "Объединение планет"]
        self.task_var = tk.StringVar(self)
        self.task_var.set(self.task_options[0])  # По умолчанию выбрано первое задание

        self.task_menu = tk.OptionMenu(self.cosmos_tab, self.task_var, *self.task_options)
        self.task_menu.pack(pady=10)

        # Выбор сложности
        self.difficulty_label = tk.Label(self.cosmos_tab, text="Выберите сложность", font=("Helvetica", 14))
        self.difficulty_label.pack(pady=10)

        self.difficulty_options = ["Лёгкий", "Средний", "Тяжёлый"]
        self.difficulty_var = tk.StringVar(self)
        self.difficulty_var.set(self.difficulty_options[0])  # По умолчанию выбрано лёгкое

        self.difficulty_menu = tk.OptionMenu(self.cosmos_tab, self.difficulty_var, *self.difficulty_options)
        self.difficulty_menu.pack(pady=10)

        # Кнопка для генерации графа
        self.generate_button = tk.Button(self.cosmos_tab, text="Генерировать граф",
                                         command=self.generate_and_display_graph)
        self.generate_button.pack(pady=10)

        # Кнопка для выполнения задания
        self.run_button = tk.Button(self.cosmos_tab, text="Выполнить задание", command=self.run_task)
        self.run_button.pack(pady=10)

        self.result_label = tk.Label(self.cosmos_tab, text="Результат: ", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

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
        nodes = [f"Node_{i}" for i in range(num_vertices)]
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
        # Преобразуем строку сложности на русский в формат, используемый в методе generate_graph
        difficulty_map = {
            "Лёгкий": "easy",
            "Средний": "medium",
            "Тяжёлый": "hard"
        }
        difficulty = self.difficulty_var.get()
        difficulty = difficulty_map.get(difficulty, "easy")  # По умолчанию используем "easy"
        # Генерация графа по выбранной сложности
        self.graph, self.positions = self.generate_graph(difficulty)
        # Обновляем визуализацию
        self.update_graph()

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

        start_vertex = random.choice(nodes)
        end_vertex = random.choice(nodes)

        # Если начальная и конечная вершины одинаковы, пробуем снова
        while start_vertex == end_vertex:
            end_vertex = random.choice(nodes)

        if start_vertex not in self.graph or end_vertex not in self.graph:
            messagebox.showerror("Ошибка", f"Одна или обе вершины не найдены в графе: {start_vertex}, {end_vertex}")
            return

        # Используем функцию из networkx для нахождения кратчайшего пути и стоимости
        distances, predecessors = nx.single_source_dijkstra(self.graph, start_vertex)

        # Проверим, что предшественники (predecessors) имеют правильный формат
        if not isinstance(predecessors, dict):
            messagebox.showerror("Ошибка", "Некорректный формат предшественников.")
            return

        # Восстановление пути из предшественников
        path = self.reconstruct_path(predecessors, start_vertex, end_vertex)
        fuel_cost = distances[end_vertex]

        result_text = f"Кратчайший путь от {start_vertex} до {end_vertex}: {' -> '.join(path)}\n" \
                      f"Общий расход топлива: {fuel_cost}"
        self.result_label.config(text=result_text)
        self.update_graph()  # Обновим граф

    def find_center_task(self):
        # Преобразуем граф из NetworkX в ваш класс Graph
        graph = Graph()
        graph.from_networkx(self.graph)  # Преобразуем текущий граф NetworkX в объект Graph

        # Теперь используем методы вашего класса для поиска центра
        center = graph.find_graph_center()

        result_text = f"Центральная база: {', '.join(center)}"
        self.result_label.config(text=result_text)
        self.update_graph()  # Обновим граф

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

    def update_graph(self):
        """Обновление визуализации графа"""
        self.ax.clear()
        self.ax.axis("off")

        # Используем сохраненные позиции вершин
        pos = self.positions

        # Собираем веса рёбер
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')

        # Отображение графа с использованием NetworkX и matplotlib
        nx.draw(self.graph, with_labels=True, ax=self.ax, node_color="lightblue", font_weight="bold", pos=pos)

        # Отображение меток рёбер с весами
        nx.draw_networkx_edge_labels(self.graph, pos=pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()


# Запуск приложения
if __name__ == "__main__":
    graph = nx.Graph()  # Используем NetworkX Graph напрямую
    app = SpaceExpeditionApp(graph)
    app.mainloop()
