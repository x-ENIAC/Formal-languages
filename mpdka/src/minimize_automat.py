from determinize_automat import determinize_automat, simplify_automat
from io_handler import draw_automat


def minimize_automat(automat):
    '''
    Минимизирует ПДКА алгоритмом, разобранном на семинарах и лекциях (с
    использованием классов эквивалентности состояний)

    Parameters:
        automat ПДКА

    Returns:
        automat Минимальный ПДКА
    '''

    copy_automat = automat
    acceptance = automat["acceptance"]
    alphabet = automat["alphabet"]
    automat = automat["automat"]

    len_alphabet = len(alphabet)

    vertexes = sorted(list(automat.keys()))
    count_of_vertexes = len(vertexes)

    previous_classes = [0 for i in range(count_of_vertexes)]

    for i in range(count_of_vertexes):  # строим нулевой класс эквивалентности
        if vertexes[i] in acceptance:
            previous_classes[i] = 1

    transitioins = ([[0 for i in range(len_alphabet)]
                    for i in range(count_of_vertexes)])

    for _ in range(count_of_vertexes + 1):
        transitioins = ([[0 for i in range(len_alphabet)]
                        for i in range(count_of_vertexes)])
        now_classes = [0 for i in range(count_of_vertexes)]

        for i in range(count_of_vertexes):
            vertex = vertexes[i]
            for letter, vertex_to in automat[vertex]:
                letter_index = alphabet.index(letter)
                vertex_to_index = vertexes.index(vertex_to)
                transitioins[i][letter_index] = (
                    previous_classes[vertex_to_index]
                )

        existed_classes = []

        # формируем новый класс эквивалентности
        for i in range(count_of_vertexes):
            now_class = [previous_classes[i]] + transitioins[i]
            if now_class not in existed_classes:
                existed_classes.append(now_class)
            now_classes[i] = existed_classes.index(now_class)

        if check_two_classes_on_equal(previous_classes, now_classes):
            automat = create_automat_by_classes(copy_automat, transitioins,
                                                now_classes)
            return automat

        previous_classes = now_classes.copy()

    raise Exception("Something wrong in minimize")


def check_two_classes_on_equal(class_1, class_2):
    '''
    Проверяет два списка классов эквивалентности состояний на идентичность

    Parameters:
        class_1 Первый список классов эквивалентности состояний
        class_2 Второй список классов эквивалентности состояний

    Returns:
        is_equal True, если списки идентачны; False, если нет
    '''

    copy_class_1 = sorted(class_1)
    copy_class_2 = sorted(class_2)

    if copy_class_1 == copy_class_2:
        return True
    return False


def create_automat_by_classes(automat, transitioins, classes):
    '''
    По классам эквивалентности вершин создаёт автомат

    Parameters:
        automat Старый автомат, на основе которого
                сформировали классы эквивалентности
        transitioins Переход из одного состояния в другие по каждому
                     символу алфавита
        classes Классы эквивалентности состояний

    Returns:
        automat Автомат, построенный на основе классов эквивалентности
                и переходов между ними
    '''

    old_start, old_acceptance = automat["start"], automat["acceptance"]
    keys = sorted(list(automat["automat"].keys()))
    old_start_class = classes[keys.index(old_start)]
    old_acceptance_classes = [classes[keys.index(i)] for i in old_acceptance]

    new_transitions, new_classes = (
        remove_repetitions_from_transitions_and_classes(transitioins, classes)
    )

    count_of_classes = len(new_classes)

    alphabet = automat["alphabet"]
    len_alphabet = len(alphabet)

    zero_state_string = "q{i}".format(i=new_classes[0])
    new_automat = {zero_state_string: []}
    new_start = None
    new_acceptance = []

    for i in range(len_alphabet):
        vertex_to = "q{j}".format(j=new_transitions[0][i])
        new_automat[zero_state_string].append((alphabet[i], vertex_to))

    if old_start_class == new_classes[0]:
        new_start = zero_state_string
    if new_classes[0] in old_acceptance_classes:
        new_acceptance.append(zero_state_string)

    for i in range(1, count_of_classes):
        vertex_from = "q{j}".format(j=new_classes[i])
        for j in range(len_alphabet):
            letter = alphabet[j]
            vertex_to = "q{k}".format(k=new_transitions[i][j])
            if vertex_from not in new_automat:
                new_automat[vertex_from] = [(letter, vertex_to)]
            elif (letter, vertex_to) not in new_automat[vertex_from]:
                new_automat[vertex_from].append((letter, vertex_to))
        if old_start_class == new_classes[i] and new_start is None:
            new_start = vertex_from
        if new_classes[i] in old_acceptance_classes:
            new_acceptance.append(vertex_from)

    new_automat = {"automat": new_automat}
    new_automat["alphabet"] = alphabet
    new_automat["acceptance"] = new_acceptance
    new_automat["start"] = new_start

    return new_automat


def remove_repetitions_from_transitions_and_classes(transitions, classes):
    '''
    Удаляет дубликаты из списка классов эквивалентности (т.е. эквивалентные
    состояния)

    Parameters:
        transitions Переход из одного состояния в другие по каждому
                     символу алфавита
        classes Классы эквивалентности состояний

    Returns:
        new_transitions Переходы, соответствующие new_classes
        new_classes Неэквивалентные состояния
    '''

    new_transitions = [transitions[0]]
    new_classes = [classes[0]]
    count_classes = len(classes)

    for i in range(1, count_classes):
        if classes[i] == classes[i - 1]:
            continue
        new_classes.append(classes[i])
        new_transitions.append(transitions[i])

    return new_transitions, new_classes
