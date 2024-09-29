class Graph:
    def __init__(self, directed=False, adjacency_list=None, weighted=False):
        if adjacency_list is None:
            self.adjacency_list = {}
        else:
            self.adjacency_list = {v: list(adj) for v, adj in adjacency_list.items()}
        self.directed = directed
        self.weighted = weighted  # Атрибут для определения взвешенности графа

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Определяем тип графа (направленный/ненаправленный) и взвешенный/невзвешенный
        header = lines[0].strip().lower().split()
        self.directed = header[0] == 'directed'
        self.weighted = header[1] == 'weighted'

        # Используем словарь для хранения графа
        self.graph = {}
        all_vertices = set()

        for i, line in enumerate(lines[1:]):
            parts = line.strip().split()

            if len(parts) == 1:
                vertex = parts[0]
                all_vertices.add(vertex)
                self.graph.setdefault(vertex, [])
                continue

            if self.weighted:
                u, v, weight = parts[0], parts[1], float(parts[2])
                all_vertices.update([u, v])
                self.graph.setdefault(u, []).append((v, weight))
                if not self.directed:
                    if u != v:
                        self.graph.setdefault(v, []).append((u, weight))
            else:
                u, v = parts[0], parts[1]
                all_vertices.update([u, v])
                self.graph.setdefault(u, []).append((v, None))
                if not self.directed:
                    if u != v:
                        self.graph.setdefault(v, []).append((u, None))

        # Обеспечиваем наличие всех вершин, включая обособленные
        for vertex in all_vertices:
            if vertex not in self.graph:
                self.graph[vertex] = []

        # Копируем данные из self.graph в self.adjacency_list для дальнейшего использования
        self.adjacency_list = self.graph.copy()

        # Вывод содержимого графа:
        print(f"Граф из файла '{filename}' загружен. Вот его содержимое:")
        for vertex, edges in self.graph.items():
            if edges:
                if self.weighted:
                    edges_str = ', '.join(f"{v} (вес: {weight})" for v, weight in edges)
                else:
                    edges_str = ', '.join(v for v, _ in edges)
                print(f"{vertex}: {edges_str}")
            else:
                if self.directed:
                    has_incoming = any(vertex in [v for v, _ in adj] for adj in self.graph.values())
                    if has_incoming:
                        print(f"{vertex}: нет исходящих рёбер")
                    else:
                        print(f"{vertex}: нет рёбер")
                else:
                    print(f"{vertex}: нет рёбер")

        # Вывод типа графа:
        graph_type = "Ориентированный" if self.directed else "Неориентированный"
        weight_type = "Взвешенный" if self.weighted else "Невзвешенный"
        print(f"Тип графа: {graph_type}, {weight_type}")

    def display_adjacency_list(self):
        for vertex in self.adjacency_list:
            if self.weighted:
                edges = ', '.join(f"{adj} ({weight})" for adj, weight in self.adjacency_list[vertex])
            else:
                edges = ', '.join(str(adj) for adj, *_ in self.adjacency_list[vertex])
            print(f"{vertex}: {edges if edges else ''}")

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
        else:
            print(f"Вершина {vertex} уже существует.")

    def add_edge(self, u, v, weight=None, overwrite=False):
        # Проверяем существование обеих вершин
        if u not in self.adjacency_list or v not in self.adjacency_list:
            print(f"Ошибка: Вершины '{u}' и/или '{v}' не существуют.")
            return False

        # Определяем вес ребра
        if self.weighted:
            if weight is None:
                print("Ошибка: Для взвешенного графа необходимо указать вес ребра.")
                return False
        else:
            weight = None  # В невзвешенном графе вес не хранится

        # Проверяем существование ребра
        if self.weighted:
            existing_edge = next(((i, w) for i, (neighbor, w) in enumerate(self.adjacency_list[u]) if neighbor == v),
                                 None)
        else:
            existing_edge = next((i for i, (neighbor,) in enumerate(self.adjacency_list[u]) if neighbor == v), None)

        if existing_edge:
            if overwrite:
                index, _ = existing_edge
                if self.weighted:
                    self.adjacency_list[u][index] = (v, weight)
                else:
                    self.adjacency_list[u][index] = (v,)
                print(f"Ребро {u}-{v} обновлено.")
            else:
                print(f"Ребро {u}-{v} уже существует.")
                return False  # Указывает, что ребро уже существует и не было перезаписано
        else:
            if self.weighted:
                self.adjacency_list[u].append((v, weight))
                print(f"Ребро {u}-{v} добавлено с весом {weight}.")
            else:
                self.adjacency_list[u].append((v,))
                print(f"Ребро {u}-{v} добавлено.")

        if not self.directed and u != v:
            existing_reverse_edge = next(((i, w) for i, (neighbor, w) in enumerate(self.adjacency_list[v]) if neighbor == u), None)
            if existing_reverse_edge:
                if overwrite and self.weighted:
                    index, _ = existing_reverse_edge
                    self.adjacency_list[v][index] = (u, weight)
            else:
                if self.weighted:
                    self.adjacency_list[v].append((u, weight))
                else:
                    self.adjacency_list[v].append((u,))
        return True  # Указывает, что ребро было успешно добавлено или обновлено

    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            # Удаляем все рёбра, связанные с этой вершиной
            self.adjacency_list.pop(vertex)
            for adj in self.adjacency_list:
                if self.weighted:
                    self.adjacency_list[adj] = [(v, w) for v, w in self.adjacency_list[adj] if v != vertex]
                else:
                    self.adjacency_list[adj] = [v for v, *_ in self.adjacency_list[adj] if v != vertex]
        else:
            print(f"Вершина {vertex} не существует.")

    def remove_edge(self, u, v):
        if u in self.adjacency_list:
            if self.weighted:
                original_length = len(self.adjacency_list[u])
                self.adjacency_list[u] = [(x, w) for x, w in self.adjacency_list[u] if x != v]
                if len(self.adjacency_list[u]) < original_length:
                    print(f"Ребро {u}-{v} удалено.")
                else:
                    print(f"Ребро {u}-{v} не существует.")
            else:
                original_length = len(self.adjacency_list[u])
                self.adjacency_list[u] = [x for x, *_ in self.adjacency_list[u] if x != v]
                if len(self.adjacency_list[u]) < original_length:
                    print(f"Ребро {u}-{v} удалено.")
                else:
                    print(f"Ребро {u}-{v} не существует.")

            if not self.directed:
                if self.weighted:
                    self.adjacency_list[v] = [(x, w) for x, w in self.adjacency_list[v] if x != u]
                else:
                    self.adjacency_list[v] = [x for x, *_ in self.adjacency_list[v] if x != u]
        else:
            print(f"Вершина {u} не существует.")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            type_line = ""
            if self.directed and self.weighted:
                type_line = "directed weighted"
            elif self.directed and not self.weighted:
                type_line = "directed unweighted"
            elif not self.directed and self.weighted:
                type_line = "undirected weighted"
            else:
                type_line = "undirected unweighted"
            file.write(f"{type_line}\n")
            for vertex in self.adjacency_list:
                if not self.adjacency_list[vertex]:
                    file.write(f"{vertex}\n")
                else:
                    for edge in self.adjacency_list[vertex]:
                        if self.directed or (not self.directed and vertex < edge[0]):
                            if self.weighted:
                                file.write(f"{vertex} {edge[0]} {edge[1]}\n")
                            else:
                                file.write(f"{vertex} {edge[0]}\n")

    def __str__(self):
        # Вывод графа в виде строки с указанием весов рёбер, включая петли
        result = ""
        for vertex in self.adjacency_list:
            result += f"{vertex}: "
            if self.weighted:
                edges = ", ".join(f"{adj} ({weight})" for adj, weight in self.adjacency_list[vertex])
            else:
                edges = ", ".join(adj for adj, *_ in self.adjacency_list[vertex])
            result += f"{edges}\n"
        return result

    def edges(self):
        edge_list = []
        seen_edges = set()
        for vertex in self.adjacency_list:
            for edge in self.adjacency_list[vertex]:
                neighbor = edge[0]
                weight = edge[1] if self.weighted else None
                if self.directed:
                    edge_repr = (vertex, neighbor, weight) if self.weighted else (vertex, neighbor)
                    edge_list.append(edge_repr)
                else:
                    # Для неориентированного графа избегаем дублирования ребер
                    edge_key = tuple(sorted([vertex, neighbor]))
                    if edge_key not in seen_edges:
                        edge_repr = (vertex, neighbor, weight) if self.weighted else (vertex, neighbor)
                        edge_list.append(edge_repr)
                        seen_edges.add(edge_key)
        return edge_list


def console_interface():
    print("Добро пожаловать в систему работы с графом!")
    initial_choice = input("Введите '1' для загрузки из файла или '2' для создания нового графа: ").strip()

    if initial_choice == '1':
        filename = input("Введите имя файла с графом: ").strip()
        try:
            graph = Graph()  # Инициализируем граф перед загрузкой
            graph.load_from_file(filename)
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден. Создан пустой граф.")
            # Запрашиваем тип графа при создании пустого графа
            graph = create_new_graph()
        except ValueError as ve:
            print(f"Ошибка при загрузке графа: {ve}")
            # Запрашиваем тип графа при создании пустого графа
            graph = create_new_graph()
    elif initial_choice == '2':
        graph = create_new_graph()
    else:
        print("Некорректный выбор. Создан пустой граф.")
        graph = Graph()

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

        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            vertex = input("Введите имя вершины: ").strip()
            graph.add_vertex(vertex)

        elif choice == '2':
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            if graph.weighted:
                while True:
                    weight_input = input("Введите вес ребра: ").strip()
                    try:
                        weight = float(weight_input)
                        break
                    except ValueError:
                        print("Неверный формат веса. Пожалуйста, введите число.")
            else:
                weight = None

            # Проверяем, существует ли уже ребро
            edge_exists = False
            if graph.weighted:
                edge_exists = any(neighbor == v for neighbor, _ in graph.adjacency_list.get(u, []))
            else:
                edge_exists = any(neighbor == v for neighbor, *_ in graph.adjacency_list.get(u, []))

            if edge_exists:
                overwrite_choice = input(f"Ребро {u}-{v} уже существует. Хотите перезаписать его? (да/нет): ").strip().lower()
                if overwrite_choice in ['да', 'д', 'yes', 'y']:
                    success = graph.add_edge(u, v, weight=weight, overwrite=True)
                    if not success:
                        print("Не удалось перезаписать ребро.")
                else:
                    print("Добавление ребра отменено.")
            else:
                success = graph.add_edge(u, v, weight=weight)
                if not success:
                    print("Не удалось добавить ребро.")

        elif choice == '3':
            vertex = input("Введите имя вершины для удаления: ").strip()
            graph.remove_vertex(vertex)

        elif choice == '4':
            u = input("Введите первую вершину: ").strip()
            v = input("Введите вторую вершину: ").strip()
            graph.remove_edge(u, v)

        elif choice == '5':
            print("\nТекущий граф:")
            graph.display_adjacency_list()
            # Отображаем тип графа
            graph_type = []
            graph_type.append("Ориентированный" if graph.directed else "Неориентированный")
            graph_type.append("Взвешенный" if graph.weighted else "Невзвешенный")
            print(f"Тип графа: {', '.join(graph_type)}")

        elif choice == '6':
            print("\nСписок рёбер:")
            for edge in graph.edges():
                if graph.weighted:
                    print(f"{edge[0]} - {edge[1]} (Вес: {edge[2]})")
                else:
                    print(f"{edge[0]} - {edge[1]}")

        elif choice == '7':
            filename = input("Введите имя файла для сохранения: ").strip()
            graph.save_to_file(filename)
            print(f"Граф сохранён в файл '{filename}'.")

        elif choice == '8':
            copy_graph = graph.copy()
            print("\nСоздана копия графа. Вот её содержимое:")
            copy_graph.display_adjacency_list()
            graph_type = []
            graph_type.append("Ориентированный" if copy_graph.directed else "Неориентированный")
            graph_type.append("Взвешенный" if copy_graph.weighted else "Невзвешенный")
            print(f"Тип графа копии: {', '.join(graph_type)}")

        elif choice == '9':
            filename = input("Введите имя файла для загрузки графа: ").strip()
            try:
                graph.load_from_file(filename)
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден.")
            except ValueError as ve:
                print(f"Ошибка при загрузке графа: {ve}")

        elif choice == '10':
            break

        else:
            print("Некорректный ввод.")

    print("Завершение работы.")


def create_new_graph():
    # Запрашиваем тип графа у пользователя
    while True:
        directed_input = input("Граф ориентированный? (да/нет): ").strip().lower()
        if directed_input in ['да', 'д', 'yes', 'y']:
            directed = True
            break
        elif directed_input in ['нет', 'н', 'no', 'n']:
            directed = False
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    while True:
        weighted_input = input("Граф взвешенный? (да/нет): ").strip().lower()
        if weighted_input in ['да', 'д', 'yes', 'y']:
            weighted = True
            break
        elif weighted_input in ['нет', 'н', 'no', 'n']:
            weighted = False
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

    graph = Graph(directed=directed, weighted=weighted)
    print("Создан новый граф.")
    graph_type = []
    graph_type.append("Ориентированный" if graph.directed else "Неориентированный")
    graph_type.append("Взвешенный" if graph.weighted else "Невзвешенный")
    print(f"Тип графа: {', '.join(graph_type)}")
    return graph


if __name__ == "__main__":
    console_interface()
