from determinize_automat import determinize_automat, simplify_automat
from io_handler import draw_automat

def minimize_automat(automat, input_filename):
    copy_automat = automat
    acceptance = automat["acceptance"]
    alphabet = automat["alphabet"]
    automat = automat["automat"]

    len_alphabet = len(alphabet)

    vertexes = sorted(list(automat.keys()))
    count_of_vertexes = len(vertexes)

    previous_classes = [0 for i in range(count_of_vertexes)]

    for i in range(count_of_vertexes): # строим нулевой класс эквивалентности
        if vertexes[i] in acceptance:
            previous_classes[i] = 1
    
    # print("previous_classes", previous_classes)
    transitioins = [[0 for i in range(len_alphabet)] for i in range(count_of_vertexes)]
    
    for _ in range(count_of_vertexes + 1): # максимум может формировать классы N раз
        transitioins = [[0 for i in range(len_alphabet)] for i in range(count_of_vertexes)]
        now_classes = [0 for i in range(count_of_vertexes)]

        for i in range(count_of_vertexes):
            vertex = vertexes[i]
            for letter, vertex_to in automat[vertex]:
                letter_index = alphabet.index(letter)
                vertex_to_index = vertexes.index(vertex_to)
                transitioins[i][letter_index] = previous_classes[vertex_to_index]
        
        # print("transitioins:", transitioins)

        existed_classes = []
        for i in range(count_of_vertexes):  # формируем новый класс эквивалентности
            now_class = [previous_classes[i]] + transitioins[i]
            if now_class not in existed_classes:
                existed_classes.append(now_class)
            now_classes[i] = existed_classes.index(now_class)
        
        if check_two_classes_on_equal(previous_classes, now_classes):
            # print("FIND!!! Step:", _)
            automat = create_automat_by_classes(copy_automat, transitioins, now_classes)
            return automat

        # print("now_classes:", now_classes)
        previous_classes = now_classes.copy()

    raise Exception("Something wrong in minimize")

def check_two_classes_on_equal(class_1, class_2):
    copy_class_1 = sorted(class_1)
    copy_class_2 = sorted(class_2)

    if copy_class_1 == copy_class_2:
        return True
    return False

def create_automat_by_classes(automat, transitioins, classes):
    old_start, old_acceptance = automat["start"], automat["acceptance"]
    keys = sorted(list(automat["automat"].keys()))
    old_start_class = classes[keys.index(old_start)]
    old_acceptance_classes = [classes[keys.index(i)] for i in old_acceptance]

    new_transitions, new_classes = remove_repetitions_from_transitions_and_classes(transitioins, classes)
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
    
    if old_start_class == new_classes[0]: # если нулевая вершина была стартовой
        new_start = zero_state_string

    for i in range(1, count_of_classes):
        vertex_from = "q{j}".format(j=new_classes[i])
        for j in range(len_alphabet):
            letter = alphabet[j]
            vertex_to = "q{k}".format(k=new_transitions[i][j])
            if vertex_from not in new_automat:
                new_automat[vertex_from] = [(letter, vertex_to)]
            else:
                new_automat[vertex_from].append((letter, vertex_to))
        if old_start_class == new_classes[i] and new_start == None:
            new_start = vertex_from
        if new_classes[i] in old_acceptance_classes:
            new_acceptance.append(vertex_from)

    new_automat = {"start": new_start, "acceptance": new_acceptance, "automat": new_automat, "alphabet": alphabet}
    
    return new_automat

def remove_repetitions_from_transitions_and_classes(transitions, classes):
    new_transitions = [transitions[0]]
    new_classes = [classes[0]]
    count_classes = len(classes)

    for i in range(1, count_classes):
        if classes[i] == classes[i - 1]:
            continue
        new_classes.append(classes[i])
        new_transitions.append(transitions[i])

    return new_transitions, new_classes
