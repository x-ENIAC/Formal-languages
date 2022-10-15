from enum import auto
import re
from io_handler import draw_automat, draw_automat

def get_alphabet_from_automat(automat):
    alphabet = []
    for vertex in automat:
        for transition, transition_to in automat[vertex]:
            if transition not in alphabet:
                alphabet.append(transition)
    return alphabet

def determinize_automat(automat):
    # simplify_automat(automat)
    # delete_epsilon(automat)

    start = automat["start"]
    acceptance = automat["acceptance"]
    automat = automat["automat"]

    new_automat = {"start": start, "acceptance": [], "automat": dict()}
    new_acceptance = []

    alphabet = get_alphabet_from_automat(automat)
    len_alphabet = len(alphabet)

    keys = list(automat.keys())
    # print(keys)

    for vertex in keys: # перебираем все вершины
        if vertex in automat: # если это старая, уже существующая вершина
            transitions = automat[vertex]
            all_transitions = [[] for i in range(len_alphabet)] # все переходы по всем буквам
            for transition, transition_to in transitions:
                index_of_letter = alphabet.index(transition)
                all_transitions[index_of_letter].append(transition_to)
            
            new_transitions = []
            for vertex_transition in all_transitions: # сформируем новые переходы
                if len(vertex_transition) > 0:
                    new_vertex = ','.join(sorted(vertex_transition))
                    if new_vertex not in keys:
                        keys.append(new_vertex)
                    index_of_letter = all_transitions.index(vertex_transition)
                    new_transitions.append((alphabet[index_of_letter], new_vertex))
            new_automat["automat"][vertex] = new_transitions # добавим в новый автомат
        else: # вершины не существует, она является чьей-то конкатенацией
            old_vertexes = vertex.split(',')
            new_transitions = [[] for i in range(len_alphabet)]
            for old_vertex in old_vertexes:
                if old_vertex in automat:
                    for letter, to in automat[old_vertex]:
                        new_transitions[alphabet.index(letter)].append(to)
                if old_vertex in acceptance and vertex not in new_acceptance:
                    new_acceptance.append(vertex)
            new_transitions = [','.join(i) for i in new_transitions]
            new_transitions = [(alphabet[i], new_transitions[i]) for i in range(len(new_transitions))]
            new_transitions_without_garbage = []
            for i in new_transitions:
                if i[1] != '':
                    new_transitions_without_garbage.append(i)
            new_automat["automat"][vertex] = new_transitions_without_garbage
    
    new_automat["acceptance"] = new_acceptance
    return new_automat

def remove_unattainable_vertexes(automat):
    start_vertex = automat["start"]
    vertex_queue = [start_vertex]

    for vertex in vertex_queue:
        transitions = automat["automat"][vertex]
        for transition in transitions:
            if transition[1] != "" and transition[1] not in vertex_queue:
                vertex_queue.append(transition[1])

    unattainable_vertexes = []
    keys = automat["automat"].keys()

    for vertex in keys:
        if vertex not in vertex_queue:
            unattainable_vertexes.append(vertex)
    
    for vertex in unattainable_vertexes:
        del automat["automat"][vertex]
    return automat

def simplify_automat(automat):
    automat = remove_unattainable_vertexes(automat)  

    count_of_vertexes = len(automat["automat"].keys())
    is_something_change = False

    for i in range(count_of_vertexes + 1):
        is_something_change = False
        deleted = []
        new_automat = dict()

        for vertex in automat["automat"]:
            if len(automat["automat"][vertex]) == 0 and vertex not in automat["acceptance"]: # ищем недостижимые состояния
                deleted.append(vertex)
                is_something_change = True
        if not is_something_change:
            break
        for vertex in automat["automat"]:
            if vertex not in deleted:
                new_automat[vertex] = automat["automat"][vertex]
        print("deleted_vertex", deleted)
        for deleted_vertex in deleted: # удаляем переходы в недостижимые состояния
            for vertex in new_automat:
                for transition in new_automat[vertex]:
                    if deleted_vertex == transition[1] and transition[1] != automat["start"]:
                        new_automat[vertex].remove(transition)
        
        automat["automat"] = new_automat
    return automat

def delete_epsilon(automat, input_filename):
    epsilon_queue = []
    vertex_queue = [automat["start"]]
    acceptance = automat["acceptance"]
    
    for vertex in vertex_queue: # выпишем все эпсилон-переходы
        trasitions = automat["automat"][vertex]
        for trasition in trasitions:
            if trasition[0] == 'EPS':
                eps_item = (vertex, trasition[1])
                if eps_item not in epsilon_queue:
                    epsilon_queue.append(eps_item)
                if trasition[1] in acceptance and vertex not in acceptance:
                    acceptance.append(vertex)
            if trasition[1] != "" and trasition[1] not in vertex_queue:
                vertex_queue.append(trasition[1])

    automat["acceptance"] = acceptance

    automat = construct_epsilon_closure(automat, epsilon_queue)

    draw_automat(automat, input_filename, "2_epsilon_closure")

    automat = collapse_epsilon_transitions(automat, epsilon_queue)
    automat = delete_epsilon_transitions(automat)
    
    draw_automat(automat, input_filename, "3_delete_epsilon")

    return automat

def construct_epsilon_closure(automat, epsilon_queue): # 1 ->eps-> 2 and 2 ->eps->3 => 1->eps->3
    acceptance = automat["acceptance"]
    copy_automat = automat
    automat = automat["automat"]

    is_something_change = True
    while is_something_change:
        is_something_change = False
        for vertex_from, vertex_to in epsilon_queue: # [('q3', 'q1'), ('q4', 'q5')]
            transitions = automat[vertex_to] # переходы из q1
            for transition in transitions:
                new_eps_item = (vertex_from, transition[1])
                if transition[0] == "EPS" and new_eps_item not in epsilon_queue:
                    epsilon_queue.append(new_eps_item)
                    is_something_change = True
                    automat[vertex_from].append(("EPS", transition[1]))
    
    copy_automat["automat"] = automat
    return copy_automat

def collapse_epsilon_transitions(automat, epsilon_queue):
    copy_automat = automat
    automat = automat["automat"]

    for vertex_from, vertex_to in epsilon_queue: # схлопнем переходы: ea -> a
        transitions = automat[vertex_to]
        for transition in transitions:
            if transition[0] != "EPS" and transition not in automat[vertex_from]:
                automat[vertex_from].append(transition)
    
    copy_automat["automat"] = automat
    return copy_automat

def delete_epsilon_transitions(automat): # непосредственно убирает сами эпсилон-переходы
    vertex_queue = [automat["start"]]
    copy_automat = automat
    automat = automat["automat"]

    for vertex in vertex_queue: # выпишем все эпсилон-переходы
        trasitions = automat[vertex]
        new_transitions = []
        for trasition in trasitions:
            if trasition[0] != 'EPS':
                new_transitions.append(trasition)
            if trasition[1] != "" and trasition[1] not in vertex_queue:
                vertex_queue.append(trasition[1])
        automat[vertex] = new_transitions
    
    copy_automat["automat"] = automat
    return copy_automat