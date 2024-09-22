class Graph:
    def __init__(self, directed=False, adjacency_list=None):
        if adjacency_list is None:
            self.adjacency_list = {}
        else:
            self.adjacency_list = {v: list(adj) for v, adj in adjacency_list.items()}
        self.directed = directed

    def load_from_file(self, filename):
        """Загрузка графа из файла с указанием типа графа (ориентированный или неориентированный)."""
        with open(filename, 'r') as file:
            first_line = file.readline().strip().lower()  # Читаем первую строку для типа графа
            if first_line == 'directed':
                self.directed = True
            elif first_line == 'undirected':
                self.directed = False
            else:
                raise ValueError("Первой строкой файла должно быть 'directed' или 'undirected'.")

            for line in file:
                parts = line.split()
                if len(parts) == 2:  # Обработка рёбер без весов
                    u, v = parts
                    self.add_edge(u, v)
                elif len(parts) == 3:  # Обработка рёбер с весами
                    u, v, weight = parts
                    self.add_edge(u, v, float(weight))
                elif len(parts) == 1:  # Изолированные вершины
                    u = parts[0]
                    if u not in self.adjacency_list:
                        self.add_vertex(u)

    def copy(self):
        """Конструктор-копия (создаёт глубокую копию графа)."""
        return Graph(self.directed, self.adjacency_list)

    def display_adjacency_list(self):
        for vertex in self.adjacency_list:
            edges = ', '.join(f"{adj} ({weight})" if weight != 1 else adj
                              for adj, weight in self.adjacency_list[vertex])
            print(f"{vertex}: {edges if edges else ''}")

    def add_vertex(self, vertex):
        """Добавить вершину."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
        else:
            print(f"Вершина {vertex} уже существует.")

    def add_edge(self, u, v, weight=1):
        """Добавить ребро в граф. Если граф неориентированный, добавляем симметричное ребро."""
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []

        # Проверяем, не существует ли уже ребро u -> v
        if not any(neighbor == v for neighbor, _ in self.adjacency_list[u]):
            self.adjacency_list[u].append((v, weight))

        # Если граф неориентированный и ребро не петля, добавляем обратное ребро v -> u
        if not self.directed and u != v:
            if not any(neighbor == u for neighbor, _ in self.adjacency_list[v]):
                self.adjacency_list[v].append((u, weight))

    def remove_vertex(self, vertex):
        """Удалить вершину."""
        if vertex in self.adjacency_list:
            # Удаляем все рёбра, связанные с этой вершиной
            self.adjacency_list.pop(vertex)
            for adj in self.adjacency_list:
                self.adjacency_list[adj] = [(v, w) for v, w in self.adjacency_list[adj] if v != vertex]
        else:
            print(f"Вершина {vertex} не существует.")

    def remove_edge(self, u, v):
        """Удалить ребро."""
        if u in self.adjacency_list and v in [x[0] for x in self.adjacency_list[u]]:
            self.adjacency_list[u] = [(x, w) for x, w in self.adjacency_list[u] if x != v]
            if not self.directed:
                self.adjacency_list[v] = [(x, w) for x, w in self.adjacency_list[v] if x != u]
        else:
            print(f"Ребро {u}-{v} не существует.")

    def save_to_file(self, filename):
        """Сохранение графа в файл, включая вершины без рёбер."""
        with open(filename, 'w') as file:
            for vertex in self.adjacency_list:
                # Если у вершины нет смежных вершин, все равно выводим её
                if not self.adjacency_list[vertex]:
                    file.write(f"{vertex}\n")
                else:
                    for (neighbor, weight) in self.adjacency_list[vertex]:
                        if self.directed or (neighbor, vertex) not in self.adjacency_list[neighbor]:
                            # Для взвешенных графов добавляем вес ребра
                            if weight != 1:
                                file.write(f"{vertex} {neighbor} {weight}\n")
                            else:
                                file.write(f"{vertex} {neighbor}\n")

    def __str__(self):
        """Вывод графа в виде строки с указанием весов рёбер, включая петли."""
        result = ""
        for vertex in self.adjacency_list:
            result += f"{vertex}: "
            edges = []
            for (adj, weight) in self.adjacency_list[vertex]:
                edges.append(f"{adj} ({weight})")  # Включаем вес, если есть
            result += ", ".join(edges) + "\n"
        return result

    def edges(self):
        """Вернуть список рёбер."""
        edge_list = []
        seen_edges = set()
        for vertex in self.adjacency_list:
            for (neighbor, weight) in self.adjacency_list[vertex]:
                # Добавляем рёбра только один раз для неориентированного графа
                if self.directed or (neighbor, vertex) not in seen_edges:
                    edge_list.append((vertex, neighbor, int(weight) if weight == 1 else weight))
                seen_edges.add((vertex, neighbor))
        return edge_list

# Пример работы консольного интерфейса
def console_interface():
    graph = Graph()
    print("Добро пожаловать в систему работы с графом!")
    initial_choice = input("Введите '1' для загрузки из файла или '2' для работы с пустым графом: ").strip()

    if initial_choice == '1':
        filename = input("Введите имя файла с графом: ")
        try:
            graph.load_from_file(filename)
            print(f"Граф из файла {filename} загружен. Вот его содержимое:")
            graph.display_adjacency_list()
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Создан пустой граф.")
    elif initial_choice == '2':
        print("Создан пустой граф.")

    while True:
        print("\nМеню:")
        print("1. Добавить вершину")
        print("2. Добавить ребро")
        print("3. Удалить вершину")
        print("4. Удалить ребро")
        print("5. Показать граф")
        print("6. Показать рёбра графа")
        print("7. Сохранить в файл")
        print("8. Создать копию графа")
        print("9. Загрузить граф из файла")
        print("10. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            vertex = input("Введите имя вершины: ")
            graph.add_vertex(vertex)

        elif choice == '2':
            u = input("Введите первую вершину: ")
            v = input("Введите вторую вершину: ")
            weight = input("Введите вес (по умолчанию 1): ") or 1
            graph.add_edge(u, v, float(weight) if '.' in str(weight) else int(weight))

        elif choice == '3':
            vertex = input("Введите имя вершины для удаления: ")
            graph.remove_vertex(vertex)

        elif choice == '4':
            u = input("Введите первую вершину: ")
            v = input("Введите вторую вершину: ")
            graph.remove_edge(u, v)

        elif choice == '5':
            print("\nТекущий граф:")
            graph.display_adjacency_list()

        elif choice == '6':
            print("\nСписок рёбер:")
            print(graph.edges())

        elif choice == '7':
            filename = input("Введите имя файла для сохранения: ")
            graph.save_to_file(filename)
            print(f"Граф сохранён в файл {filename}.")

        elif choice == '8':
            copy_graph = graph.copy()
            print("\nСоздана копия графа. Вот её содержимое:")
            copy_graph.display_adjacency_list()

        elif choice == '9':
            filename = input("Введите имя файла для загрузки графа: ")
            try:
                graph.load_from_file(filename)  # Вызываем метод на экземпляре
                print(f"Граф из файла {filename} загружен. Вот его содержимое:")
                graph.display_adjacency_list()
            except FileNotFoundError:
                print(f"Файл {filename} не найден.")

        elif choice == '10':
            break

        else:
            print("Некорректный ввод.")

    print("Завершение работы.")

if __name__ == "__main__":
    console_interface()  # Запуск консольного интерфейса
