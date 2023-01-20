from io_handler import draw_automat, draw_automat


def determinize_automat(automat, input_filename):
    '''
    From NFA makes DFA.

    Parameters:
        automat NFA
        input_filename The name of the file that contains the description of
                        the NFA (required for intermediate rendering of
                        automat)

    Returns:
        automat DFA
    '''

    automat = simplify_automat(automat)
    automat = delete_epsilon(automat, input_filename)

    start = automat["start"]
    acceptance = automat["acceptance"]
    alphabet = automat["alphabet"]
    automat = automat["automat"]

    new_automat = {"acceptance": [], "automat": dict()}
    new_automat["alphabet"] = alphabet
    new_automat["start"] = start
    new_acceptance = [i for i in acceptance]

    len_alphabet = len(alphabet)

    keys = list(automat.keys())

    for vertex in keys:  # iterate over all vertices
        if vertex in automat:  # if it's an old, existing node
            transitions = automat[vertex]
            # all_transitions are all transitions across all letters
            all_transitions = [[] for i in range(len_alphabet)]
            for i in range(len(transitions)):
                transition, transition_to = transitions[i]
                index_of_letter = alphabet.index(transition)
                all_transitions[index_of_letter].append(transition_to)
            new_transitions = []
            for i in range(len(all_transitions)):  # create new transitions
                vertex_transition = all_transitions[i]
                if len(vertex_transition) > 0:
                    new_vertex = ','.join(sorted(vertex_transition))
                    if new_vertex not in keys:
                        keys.append(new_vertex)
                    new_transitions.append((alphabet[i], new_vertex))
            # add new transitions to the new automat
            new_automat["automat"][vertex] = new_transitions
        else:  # top does not exist, it is someone's concatenation
            old_vertexes = vertex.split(',')
            new_transitions = [[] for i in range(len_alphabet)]
            for old_vertex in old_vertexes:
                if old_vertex in automat:
                    for i in range(len(automat[old_vertex])):
                        letter, to = automat[old_vertex][i]
                        index_of_letter = alphabet.index(letter)
                        # we exclude states of the form q1,q1,q1,q1,q2, etc.
                        if to not in new_transitions[index_of_letter]:
                            new_transitions[index_of_letter].append(to)
                if old_vertex in acceptance and vertex not in new_acceptance:
                    new_acceptance.append(vertex)
            new_transitions = [','.join(sorted(i)) for i in new_transitions]
            for new_vertex in new_transitions:
                if new_vertex not in keys:
                    keys.append(new_vertex)

            new_transitions = ([(alphabet[i], new_transitions[i])
                                for i in range(len(new_transitions))])
            new_transitions_without_garbage = []
            for i in new_transitions:
                if i[1] != '':
                    new_transitions_without_garbage.append(i)
            new_automat["automat"][vertex] = new_transitions_without_garbage

    new_automat["acceptance"] = new_acceptance
    new_automat = simplify_automat(new_automat)
    return new_automat


def remove_unattainable_vertexes(automat):
    '''
    Removes unreachable states from the automat

    Parameters:
         automat Automat

    Returns:
         automat An automat containing no unreachable states
    '''

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
    '''
    Removes states from the automat that are unreachable terminal states

    Parameters:
        automat Automat

    Returns:
        automat An automat that does not contain states from which it is
                impossible come to some terminal state
     '''

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

    for i in range(count_of_vertexes):
        if not acceptance_is_reachable[i]:
            del automat[vertexes[i]]

    copy_automat["automat"] = automat
    copy_automat = remove_non_existent_vertexes_from_transitions(copy_automat)
    return copy_automat


def remove_non_existent_vertexes_from_transitions(automat):
    '''
    Removes from the automat transitions leading or originating from
    non-existent states

    Parameters:
        automat Automat

    Returns:
        automat Automat without transitions that contain
                non-existent states
    '''

    copy_automat = automat
    automat = automat["automat"]
    old_acceptance = copy_automat["acceptance"]
    new_acceptance = []

    vertexes = sorted(list(automat.keys()))
    is_reachable = [False for i in vertexes]
    is_reachable[vertexes.index(copy_automat["start"])] = True

    for vertex in vertexes:
        transitions = automat[vertex]
        count_transitions = len(transitions)
        correct_transitions = []

        for i in range(count_transitions):
            vertexZz = transitions[i][1]
            if vertexZz in vertexes:
                correct_transitions.append(transitions[i])
                vertex_index = vertexes.index(vertexZz)
                is_reachable[vertex_index] = True

        vertex_index = vertexes.index(vertex)
        if len(correct_transitions) > 0 or is_reachable[vertex_index]:
            automat[vertex] = correct_transitions
        else:
            del automat[vertex]

    for vertex in old_acceptance:
        if vertex in automat:
            new_acceptance.append(vertex)

    copy_automat["automat"] = automat
    copy_automat["acceptance"] = new_acceptance
    return copy_automat


def simplify_automat(automat):
    '''
    Simplifies the machine with three actions:
    - removes unreachable states
    - removes those states from which it is impossible to end
    - removes transitions that contain nonexistent states

    Parameters:
        automat Automat

    Returns:
        automat Simplified automat
    '''

    automat = remove_unattainable_vertexes(automat)
    automat = remove_vertexes_without_reachable_acceptance(automat)
    automat = remove_non_existent_vertexes_from_transitions(automat)

    return automat


def delete_epsilon(automat, input_filename):
    '''
    Removes epsilon transitions according to the following algorithm:
    - an epsilon-closure of the automat is done (i.e. if there were transitions
        q1->eps->q2 and q2->eps->q3, then the transition q1->eps->q3 is added);
    - further transitions of the form q1->eps->q2, q2->a->q3 are considered, where
        a - an arbitrary character of the alphabet. A transition is added to the machine
        q1->a->q3;
    - after which epsilon transitions are directly removed from the machine

    Parameters:
        automat Automat
        input_filename The name of the file that contains the description of
                        the NFA (required for intermediate rendering
                        of automat)
    Returns:
        automat Automat without epsilon transitions
    '''

    epsilon_queue = []
    vertex_queue = [automat["start"]]
    acceptance = automat["acceptance"]

    for vertex in vertex_queue:  # write out all epsilon transitions
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
    automat = remove_non_existent_vertexes_from_transitions(automat)

    draw_automat(automat, input_filename, "delete_epsilon")

    return automat


def construct_epsilon_closure(automat, epsilon_queue):
    '''
    Makes an epsilon closure of the automat: if transitions existed
     q1->eps->q2 and q2->eps->q3, then the transition q1->eps->q3 is added);

    Parameters:
        automat Automat
        epsilon_queue List of epsilon transitions (if there was a transition
                        q3 ->eps->q1, then the list will store ('q3', 'q1'))

    Returns:
        automat Automat with epsilon closure
    '''

    acceptance = automat["acceptance"]
    copy_automat = automat
    automat = automat["automat"]

    is_something_change = True
    while is_something_change:
        is_something_change = False
        for vertex_from, vertex_to in epsilon_queue:
            # q0 ->eps-> q1, q1 - acceptance => q0 - acceptance
            if vertex_from not in acceptance:
                acceptance.append(vertex_from)
            transitions = automat[vertex_to]
            for transition in transitions:
                new_eps_item = (vertex_from, transition[1])
                if (transition[0] == "EPS" and
                        new_eps_item not in epsilon_queue):
                    epsilon_queue.append(new_eps_item)
                    is_something_change = True
                    automat[vertex_from].append(("EPS", transition[1]))

    copy_automat["automat"] = automat
    copy_automat["acceptance"] = acceptance
    return copy_automat


def collapse_epsilon_transitions(automat, epsilon_queue):
    '''
    It does the following: considers transitions of the form q1->eps->q2, q2->a->q3, where
    a - an arbitrary character of the alphabet. Adds a transition to the automat
    q1->a->q3

    Parameters:
        automat Automat
        epsilon_queue List of epsilon transitions

    Returns:
        automat Automat with additional transitions
    '''

    copy_automat = automat
    automat = automat["automat"]

    for vertex_from, vertex_to in epsilon_queue:  # collapse transitions: ea -> a
        transitions = automat[vertex_to]
        for transition in transitions:
            if (transition[0] != "EPS" and
                    transition not in automat[vertex_from]):
                automat[vertex_from].append(transition)

    copy_automat["automat"] = automat
    return copy_automat


def delete_epsilon_transitions(automat):
    '''
    Removes epsilon transitions from the automat

    Parameters:
        automat Automat

    Returns:
        automat Automat without epsilon transitions
    '''

    vertex_queue = [automat["start"]]
    copy_automat = automat
    automat = automat["automat"]

    for vertex in vertex_queue:
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
    '''
    Makes a full DFA from a DFA by adding a sink vertex

    Parameters:
        automat DFA

    Returns:
        automat Full DFA
    '''

    copy_automat = automat
    alphabet = automat["alphabet"]
    automat = automat["automat"]

    automat["stock"] = [(i, "stock") for i in alphabet]
    states = sorted(list(automat.keys()))

    for vertex in states:
        transitions = automat[vertex]
        all_letters = [letter for letter, to in transitions]

        for letter in alphabet:
            if letter not in all_letters:
                automat[vertex].append((letter, "stock"))

    copy_automat["automat"] = automat
    return copy_automat
