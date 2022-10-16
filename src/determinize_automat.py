from ast import copy_location
from copy import copy
from enum import auto
from itertools import count
from operator import index
import re
from io_handler import draw_automat, draw_automat

def determinize_automat(automat, input_filename):
    simplify_automat(automat)
    delete_epsilon(automat, input_filename)

    start = automat["start"]
    acceptance = automat["acceptance"]
    alphabet = automat["alphabet"]
    automat = automat["automat"]

    new_automat = {"start": start, "acceptance": [], "automat": dict(), "alphabet": alphabet}
    new_acceptance = [i for i in acceptance]

    
    len_alphabet = len(alphabet)

    keys = list(automat.keys())

    for vertex in keys: # перебираем все вершины
        if vertex in automat: # если это старая, уже существующая вершина
            transitions = automat[vertex]
            print(vertex, transitions)
            all_transitions = [[] for i in range(len_alphabet)] # все переходы по всем буквам
            for i in range(len(transitions)):
                transition, transition_to = transitions[i]
                index_of_letter = alphabet.index(transition)
                all_transitions[index_of_letter].append(transition_to)
            new_transitions = []
            for i in range(len(all_transitions)): # сформируем новые переходы
                vertex_transition = all_transitions[i]
                if len(vertex_transition) > 0:
                    new_vertex = ','.join(sorted(vertex_transition))
                    if new_vertex not in keys:
                        keys.append(new_vertex)
                    new_transitions.append((alphabet[i], new_vertex))
            new_automat["automat"][vertex] = new_transitions # добавим в новый автомат
        else: # вершины не существует, она является чьей-то конкатенацией
            old_vertexes = vertex.split(',')
            new_transitions = [[] for i in range(len_alphabet)]
            for old_vertex in old_vertexes:
                if old_vertex in automat:
                    for i in range(len(automat[old_vertex])):
                        letter, to = automat[old_vertex][i]
                        index_of_letter = alphabet.index(letter)
                        new_transitions[index_of_letter].append(to)
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

def remove_unattainable_vertexes(automat): # удаляет недостижимые вершины
    start_vertex = automat["start"]
    copy_automat = automat
    automat = automat["automat"]

    unattainable_vertexes = []
    keys = list(automat.keys())
    is_visited = [False for i in range(len(keys))]

    
    vertex_queue = [start_vertex]

    for vertex in vertex_queue:
        if vertex not in keys:
            unattainable_vertexes.append(vertex)
            continue
        is_visited[keys.index(vertex)] = True
        transitions = automat[vertex]
        for transition in transitions:
            if transition[1] != "" and transition[1] not in vertex_queue:
                vertex_queue.append(transition[1])
        
        # print(is_visited)
        # print([True for i in range(len(keys))])
        # if is_visited != [True for i in range(len(keys))]:
        #     for i in vertex_queue:
        #         if i not in unattainable_vertexes:
        #             unattainable_vertexes.append(i)
        #     vertex_queue = []

    keys = automat.keys()

    for vertex in keys:
        if vertex not in vertex_queue:
            unattainable_vertexes.append(vertex)
    
    for vertex in unattainable_vertexes:
        if vertex in automat:
            del automat[vertex]
    
    keys = automat.keys()
    
    acceptance = copy_automat["acceptance"]
    new_acceptance = []
    for vertex in acceptance:
        if vertex in keys:
            new_acceptance.append(vertex)

    copy_automat["acceptance"] = new_acceptance
    copy_automat["automat"] = automat

    return copy_automat

def remove_vertexes_without_reachable_acceptance(automat):
    copy_automat = automat
    acceptance = automat["acceptance"]
    automat = automat["automat"]
    
    vertexes = sorted(list(automat.keys()))
    count_of_vertexes = len(vertexes)

    acceptance_is_reachable = [False for i in range(count_of_vertexes)]

    for i in range(count_of_vertexes):
        is_visited = [False for i in range(count_of_vertexes)]
        vertexes_queue = [vertexes[i]]

        for vertex_from in vertexes_queue:
            is_visited[vertexes.index(vertex_from)] = True
            if vertex_from in acceptance:
                acceptance_is_reachable[i] = True
            transitions = automat[vertex_from]
            for letter, vertex_to in transitions:
                if vertex_to not in vertexes_queue:
                    vertexes_queue.append(vertex_to)

    print("acceptance_is_reachable:", acceptance_is_reachable)

    for i in range(count_of_vertexes):
        if not acceptance_is_reachable[i]:
            del automat[vertexes[i]]

    copy_automat["automat"] = automat
    return copy_automat

def remove_non_existent_vertexes_from_transitions(automat):
    copy_automat = automat
    automat = automat["automat"]
    
    vertexes = sorted(list(automat.keys()))

    for vertex_to in vertexes:
        transitions = automat[vertex_to]
        count_transitions = len(transitions)
        correct_transitions = []

        for i in range(count_transitions):
            # print(transitions[i])
            if transitions[i][1] in vertexes:
                correct_transitions.append(transitions[i])
        
        automat[vertex_to] = correct_transitions

    copy_automat["automat"] = automat
    return copy_automat

def simplify_automat(automat):
    automat = remove_unattainable_vertexes(automat)  # убрали недостижимые
    automat = remove_vertexes_without_reachable_acceptance(automat) # убрали те, из которых нельзя дойти до терминальной
    automat = remove_non_existent_vertexes_from_transitions(automat)

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

    draw_automat(automat, input_filename, "epsilon_closure")

    automat = collapse_epsilon_transitions(automat, epsilon_queue)
    automat = delete_epsilon_transitions(automat)
    
    draw_automat(automat, input_filename, "delete_epsilon")

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

def full_determinize(automat):
    copy_automat = automat
    alphabet = automat["alphabet"]
    automat = automat["automat"]
    
    alphabet_size = len(alphabet)
    automat["stock"] = [(i, "stock") for i in alphabet]
    print(alphabet)
    print(automat["stock"])

    for vertex in automat:
        transitions = automat[vertex]
        if len(transitions) == alphabet_size:
            continue
        all_letters = [letter for letter, to in transitions]
        
        for letter in alphabet:
            if letter not in all_letters:
                automat[vertex].append((letter, "stock"))

    copy_automat["automat"] = automat
    return copy_automat