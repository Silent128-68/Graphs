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
        existing_edge = next(((i, w) for i, (neighbor, *w) in enumerate(self.adjacency_list[u]) if neighbor == v),
                             None)

        if existing_edge:
            if overwrite:
                index, _ = existing_edge
                if self.weighted:
                    self.adjacency_list[u][index] = (v, weight)
                else:
                    self.adjacency_list[u][index] = (v,)  # Для невзвешенного графа
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
            existing_reverse_edge = next(
                ((i, w) for i, (neighbor, *w) in enumerate(self.adjacency_list[v]) if neighbor == u), None)
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

    # Задание 1: Вершины с меньшей полустепенью захода
    def vertices_with_lower_indegree(graph, target_vertex):
        if target_vertex not in graph.adjacency_list:
            print(f"Вершина {target_vertex} не существует в графе.")
            return []

        indegrees = {vertex: 0 for vertex in graph.adjacency_list}

        for vertex, neighbors in graph.adjacency_list.items():
            for neighbor, *_ in neighbors:
                indegrees[neighbor] += 1

        target_indegree = indegrees[target_vertex]
        result = [vertex for vertex, indegree in indegrees.items() if indegree < target_indegree]

        print(f"Вершины с полустепенью захода меньше, чем у {target_vertex}: {result}")
        return result

    # Задание 2: Соседи, входящие в вершину
    def incoming_neighbors(graph, target_vertex):
        if target_vertex not in graph.adjacency_list:
            print(f"Вершина {target_vertex} не существует в графе.")
            return []

        incoming = []
        for vertex, neighbors in graph.adjacency_list.items():
            if any(neighbor == target_vertex for neighbor, *_ in neighbors):
                incoming.append(vertex)

        print(f"Вершины, которые направлены на {target_vertex}: {incoming}")
        return incoming

    # Задание 3: Удаление дуг без обратных
    def remove_non_reciprocal_edges(graph):
        reciprocal_graph = Graph(directed=True, weighted=graph.weighted)

        for vertex in graph.adjacency_list:
            reciprocal_graph.add_vertex(vertex)

        for vertex in graph.adjacency_list:
            for neighbor, *edge_data in graph.adjacency_list[vertex]:
                # Проверяем, существует ли обратное ребро
                if neighbor in graph.adjacency_list and any(v == vertex for v, *_ in graph.adjacency_list[neighbor]):
                    if graph.weighted:
                        reciprocal_graph.add_edge(vertex, neighbor, weight=edge_data[0])
                    else:
                        reciprocal_graph.add_edge(vertex, neighbor)

        print("Построен новый граф с удалением непарных дуг.")
        return reciprocal_graph

    # Задание 4: Все пути из u в v с помощью DFS
    def dfs_all_paths(self, u, v, path=None, all_paths=None):
        if path is None:
            path = []
        if all_paths is None:
            all_paths = []

        path.append(u)

        if u == v:
            all_paths.append(list(path))
        else:
            for neighbor, *_ in self.adjacency_list.get(u, []):
                if neighbor not in path:
                    self.dfs_all_paths(neighbor, v, path, all_paths)

        path.pop()
        return all_paths

    # Задание 5: Нахождение центра графа (эксцентриситеты и радиус графа)
    def bfs_eccentricity(self, start):
        from collections import deque

        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        distances[start] = 0

        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            current_distance = distances[vertex]

            for neighbor, *_ in self.adjacency_list[vertex]:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = current_distance + 1
                    queue.append(neighbor)

        eccentricity = max(distances.values())
        return eccentricity

    def find_graph_center(self):
        eccentricities = {vertex: self.bfs_eccentricity(vertex) for vertex in self.adjacency_list}
        radius = min(eccentricities.values())
        center = [vertex for vertex, ecc in eccentricities.items() if ecc == radius]

        return center
