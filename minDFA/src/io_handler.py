import os

global_counter = 1

BEGIN_CONSTANT = "--BEGIN--"
END_CONSTANT = "--END--"

START_CONSTANT = "Start:"
ACCEPTANCE_CONSTANT = "Acceptance:"
STATE_CONSTANT = "State:"

ACCEPTANCE_DELIMETER = "&"
TRANSITION_CONSTANT = "->"


def scan_file(filename):
    '''
    Reads text from a file

    Parameters:
        filename Filename

    Returns:
        text Text from file
    '''

    text = ""
    with open(filename, 'r') as file:
        text = file.readlines()
    return text


def scan_category(text):
    '''
    Reads a category and its arguments from text (categories are
    special words such as State, Start, Acceptance, ->; arguments
    categories is what is written on the line immediately after the category)

    Parameters:
        text Text

    Returns:
        text Category and its arguments
    '''

    answer = {"is_empty": True, "category": "", "args": ""}
    if len(text) == 0:
        return answer

    category = text[0].split()
    answer["is_empty"] = False
    answer["category"] = category[0]
    answer["args"] = category[1:]
    return answer


def handle_start_args(args):
    '''
    Validates the arguments of the Start category

    Parameters:
        args List with arguments

    Returns:
        Nothing
    '''

    if len(args) == 0:
        raise Exception("Doesn't set the start vertex")
    if len(args) != 1:
        raise Exception("Lots of start vertex")


def handle_acceptance_args(args):
    '''
    Validates the arguments of the Acceptance category

    Parameters:
        arhs String with arguments separated by &

    Returns:
        real_args List of arguments
    '''

    real_args = []
    next_is_vertex = True
    for i in args:
        if i != ACCEPTANCE_DELIMETER and next_is_vertex:
            real_args.append(i)
            next_is_vertex = False
        elif i == ACCEPTANCE_DELIMETER and not next_is_vertex:
            next_is_vertex = True
        else:
            raise Exception("Bad acceptance vertexes")
    if next_is_vertex:
        raise Exception("Bad acceptance vertexes")
    return real_args


def handle_state_args(args):
    '''
    Validates the arguments of the State category

    Parameters:
        args List with arguments

    Returns:
        Nothing
    '''

    if len(args) != 1:
        raise Exception("Bad states")


def handle_transition_args(args):
    '''
    Validates the arguments of the -> category

    Parameters:
        args List with arguments

    Returns:
        Nothing
    '''
    if len(args) != 2:
        raise Exception("Bad -> params")


def set_transition(automat, transition_from, transition, transition_to):
    '''
    Adds a new transition to the automat

    Parameters:
        automat Automat transitions
        transition_from The state from which the transition is made
        transition The character on which the transition is made
        transition_to The state to which the transition is made

    Returns:
        answer_automat A set of transitions containing a new transition
    '''

    answer_automat = automat

    new_item = (transition, transition_to)
    if transition_from not in answer_automat.keys():
        answer_automat[transition_from] = [new_item]
    else:
        answer_automat[transition_from].append(new_item)

    if transition_to not in answer_automat.keys():
        answer_automat[transition_to] = []
    return answer_automat


def get_alphabet_from_automat(automat):
    '''
    Gets the alphabet from the jump list

    Parameters:
        automat Jump List

    Returns:
        alphabet Alphabet
    '''

    alphabet = []
    for vertex in automat:
        for transition, vertex_to in automat[vertex]:
            if transition not in alphabet and transition != "EPS":
                alphabet.append(transition)
    alphabet.sort()
    return alphabet


def convert_text_to_automat(text):
    '''
    Text in .doa format translates into automat

    Parameters:
        text Text

    Returns:
        automat Automat
    '''

    automat = ({"automat": dict(), "start": None, "acceptance": [],
                "alphabet": []})

    # scan all before --BEGIN--
    continue_scan = True

    while continue_scan:
        category = scan_category(text)
        is_empty, category, args = (category["is_empty"],
                                    category["category"], category["args"])
        if category == BEGIN_CONSTANT:
            break
        elif category == START_CONSTANT:
            handle_start_args(args)
            automat["start"] = args[0]
        elif category == ACCEPTANCE_CONSTANT:
            automat["acceptance"] = handle_acceptance_args(args)
        text = text[1:]

    if len(automat["acceptance"]) == 0:
        raise Exception("Bad acceptance vertexes")
    if automat["start"] is None:
        raise Exception("Bad start vertex")

    # scan all after --BEGIN--
    continue_scan = True
    now_state = None

    while continue_scan:
        category = scan_category(text)
        is_empty, category, args = (category["is_empty"], category["category"],
                                    category["args"])
        if category == END_CONSTANT:
            break
        elif category == STATE_CONSTANT:
            handle_state_args(args)
            now_state = args[0]
        elif category == TRANSITION_CONSTANT:
            handle_transition_args(args)
            automat["automat"] = set_transition(automat["automat"], now_state,
                                                args[0], args[1])
        text = text[1:]

    automat["alphabet"] = get_alphabet_from_automat(automat["automat"])
    return automat


def enter_automat(input_filename):
    '''
    From the specified file gets the machine

    Parameters:
        input_filename The name of the file that describes the machine

    Returns:
        automat Automat
    '''

    return convert_text_to_automat(scan_file(input_filename))


def draw_automat(automat, automat_filename, postfix_name=""):
    '''
    Draw the automat

    Parameters:
        automat Automat
        automat_filename The name of the file in which the machine
                         was described

    Returns:
        automat Automat
    '''

    global global_counter

    automat_filepath = '/'.join(automat_filename.split('/')[:-1]) + '/'
    dot_filename = (automat_filepath + str(global_counter)
                    + "_" + postfix_name + ".dot")
    picture_filename = (automat_filepath + str(global_counter)
                        + "_" + postfix_name + ".png")
    global_counter += 1

    create_file(dot_filename)
    print_automat(automat, dot_filename)
    draw_picture(dot_filename, picture_filename)


def create_file(filename):
    '''
    Creates file

    Parameters:
        filename Filename

    Returns:
        Nothing
    '''

    os.system("echo "" > {filename}".format(filename=filename))


def print_automat(automat, filename):
    '''
    Outputs the automaton to a file in .dot format

    Parameters:
        automat Automat
        filename The name of the file where the automaton will be output

    Returns:
        Nothing
    '''

    added_vertex = []

    start = automat["start"]

    acceptance = automat["acceptance"]
    automat = automat["automat"]

    output_text = "digraph {\n"
    output_text += "\tstart [style = \"invis\"]\n"
    output_text += "\tstart -> \"{start}\"\n".format(start=start)

    for key in automat.keys():
        values = automat[key]
        line = ""
        if key not in added_vertex:
            added_vertex.append(key)
            if key not in acceptance:
                line += "\t" + "\"{vertex}\"".format(vertex=key) + "\n"
            else:
                line += "\t" + "\"{vertex}\" [shape=doublecircle]".format(
                    vertex=key
                ) + "\n"

        for value in values:
            transition, transition_to = value[0], value[1]
            if transition_to not in added_vertex:
                added_vertex.append(transition_to)
                if transition_to not in acceptance:
                    line += "\t" + "\"{vertex}\"".format(
                        vertex=transition_to
                    ) + "\n"
                else:
                    line += "\t" + "\"{vertex}\" [shape=doublecircle]".format(
                        vertex=transition_to
                    ) + "\n"
            line += "\t" + "\"{vertex_from}\" -> \"{vertex_to}\"".format(
                vertex_from=key,
                vertex_to=transition_to
                ) + "\n"
            line += "[label = \"{letter}\"]".format(letter=transition)

        output_text += line

    output_text += "}"

    with open(filename, 'w') as file:
        file.write(output_text)


def draw_picture(dot_filename, picture_filename):
    '''
    Creates an image from a given .dot file

    Parameters:
        dot_filename File name with .dot extension
        picture_filename The name of the image to be created

    Returns:
        Nothing
    '''

    os.system("dot -Tpng {dot_filename} -o {picture_filename}".format(
        dot_filename=dot_filename,
        picture_filename=picture_filename
    ))


def make_doa(automat, filename):
    '''
    Writes the automaton to a .doa formal file

    Parameters:
        automat Automat
        filename The name of the file to which the automaton will be written.

    Returns:
        Nothing
    '''

    text = "{start} {state_name}\n".format(
        start=START_CONSTANT,
        state_name=automat["start"]
    )

    text += "{acceptance} {states}\n".format(
        acceptance=ACCEPTANCE_CONSTANT,
        states=' & '.join(automat["acceptance"])
    )

    text += "{begin}\n".format(begin=BEGIN_CONSTANT)
    automat = automat["automat"]

    for vertex in automat:
        transitions = automat[vertex]
        text += "{state} {vertex}\n".format(
            state=STATE_CONSTANT,
            vertex=vertex
        )

        for letter, vertex_to in transitions:
            text += "{transition} {letter} {state}\n".format(
                transition=TRANSITION_CONSTANT,
                letter=letter,
                state=vertex_to
            )
    text += "{end}\n".format(end=END_CONSTANT)

    with open(filename, "w") as file:
        file.write(text)


def check_files_contents(filename1, filename2):
    '''
    Compares the contents of two files (required for testing)

    Parameters:
        filename1 Name of the first file
        filename2 Name of the second file

    Returns:
        is_equal True if the contents of the files match, otherwise false
    '''

    text1 = ""
    text2 = ""

    with open(filename1, "r") as file:
        text1 = file.read().strip("\n")
    with open(filename2, "r") as file:
        text2 = file.read().strip("\n")

    for i in range(len(text1)):
        if text1[i] != text2[i]:
            print("Find difference! Position i = ", i)
            print("First file has", text1[i], "on i position")
            print("Second file has", text2[i], "on i position")
            return False
    return True
