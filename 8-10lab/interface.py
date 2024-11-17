from graph import Graph

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
        print("10. Решить задание 1 (полустепень захода)")
        print("11. Решить задание 2 (заходящие соседи)")
        print("12. Решить задание 3 (удалить непарные дуги)")
        print("13. Найти все пути между вершинами (DFS)")
        print("14. Найти центр графа (BFS)")
        print("15. Найти минимальное остовное дерево (Kruskal)")
        print("16. Показать основную компоненту и изолированные рёбра")
        print("17. Найти длину кратчайшего пути и вывести все такие пути")
        print("18. Определить N-периферию")
        print("19. Найти отрицательные циклы")
        print("20. Выйти")

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
            target_vertex = input("Введите вершину для задания 1: ").strip()
            graph.vertices_with_lower_indegree(target_vertex)

        elif choice == '11':
            target_vertex = input("Введите вершину для задания 2: ").strip()
            graph.incoming_neighbors(target_vertex)

        elif choice == '12':
            reciprocal_graph = graph.remove_non_reciprocal_edges()
            reciprocal_graph.display_adjacency_list()
            graph = reciprocal_graph

        elif choice == '13':
            start = input("Введите начальную вершину: ").strip()
            end = input("Введите конечную вершину: ").strip()
            paths = graph.dfs_all_paths(start, end)
            if paths:
                print(f"Все пути из {start} в {end}:")
                for path in paths:
                    print(f"Путь: {' -> '.join(path)}")
            else:
                print(f"Пути из {start} в {end} не найдены.")

        elif choice == '14':
            center_vertices = graph.find_graph_center()
            if center_vertices:
                print("Центральные вершины графа:")
                print(", ".join(center_vertices))
            else:
                print("Центральные вершины не найдены.")


        elif choice == '15':
            main_component, isolated_edges = graph.identify_main_component()
            mst = graph.kruskal_mst()
            if mst:
                print("Минимальное остовное дерево для основной компоненты графа:")
                edges_in_main_component = [
                    (u, v, weight) for u, v, weight in mst
                    if u in main_component and v in main_component
                ]
                for u, v, weight in edges_in_main_component:
                    print(f"{u} - {v} (Вес: {weight})")
                if isolated_edges:
                    print("\nИзолированные рёбра (не связанные с основной компонентой):")
                    for u, v, weight in isolated_edges:
                        if graph.weighted:
                            print(f"{u} - {v} (Вес: {weight})")
                        else:
                            print(f"{u} - {v}")
            else:
                print("Минимальное остовное дерево не найдено.")

        elif choice == '16':
            main_component, isolated_edges = graph.identify_main_component()

            if main_component:
                print("\nОсновная компонента графа (вершины):")
                print(", ".join(main_component))
            else:
                print("\nОсновная компонента отсутствует.")

            if isolated_edges:
                print("\nИзолированные рёбра (не связанные с основной компонентой):")
                for u, v, weight in isolated_edges:
                    if graph.weighted:
                        print(f"{u} - {v} (Вес: {weight})")
                    else:
                        print(f"{u} - {v}")
            else:
                print("\nИзолированные рёбра отсутствуют.")


        elif choice == '17':
            start = input("Введите начальную вершину для алгоритма Дейкстры: ").strip()
            end = input("Введите конечную вершину для поиска кратчайшего пути: ").strip()
            distances, predecessors = graph.dijkstra(start)
            if end not in distances or distances[end] == float('inf'):
                print(f"Путь из {start} в {end} не существует.")
            else:
                print(f"Кратчайшее расстояние из {start} в {end}: {distances[end]}")
                print("Все кратчайшие пути из", start, "в", end)
                paths = graph.find_all_shortest_paths(start, end)
                for path in paths:
                    print(" -> ".join(path))


        elif choice == '18':
            source = input("Введите начальную вершину для поиска N-периферии: ").strip()
            try:
                N = int(input("Введите значение N: ").strip())
            except ValueError:
                print("Ошибка: N должно быть числом.")
                continue

            n_periphery = graph.find_n_periphery(source, N)
            if n_periphery:
                print(f"N-периферия для вершины {source} с N={N}:")
                print(", ".join(n_periphery))
            else:
                print(f"Для вершины {source} нет вершин, удаленных на расстояние больше {N}.")


        elif choice == '19':
            start = input("Введите начальную вершину для алгоритма Форда-Беллмана: ").strip()
            negative_cycles = graph.bellman_ford(start)
            if negative_cycles:
                print("Найдены отрицательные циклы в графе:")
                for cycle in negative_cycles:
                    print(" -> ".join(cycle))
            else:
                print("Отрицательные циклы не обнаружены.")

        elif choice == '20':
            print("Выход из программы.")
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
