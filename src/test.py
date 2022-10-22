from io_handler import enter_automat, draw_automat, make_doa
from io_handler import check_files_contents
from determinize_automat import remove_unattainable_vertexes
from determinize_automat import remove_vertexes_without_reachable_acceptance
from determinize_automat import remove_non_existent_vertexes_from_transitions
from determinize_automat import delete_epsilon, full_determinize
from determinize_automat import simplify_automat, determinize_automat
from minimize_automat import minimize_automat
from minimize_automat import remove_repetitions_from_transitions_and_classes


def test_remove_unattainable_vertexes():
    name = "remove_unattainable_vertexes"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = remove_unattainable_vertexes(automat)
    draw_automat(new_automat, filename, name)
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_remove_vertexes_without_reachable_acceptance():
    name = "remove_vertexes_without_reachable_acceptance"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = remove_vertexes_without_reachable_acceptance(automat)
    draw_automat(new_automat, filename, name)
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_remove_non_existent_vertexes_from_transitions():
    name = "remove_non_existent_vertexes_from_transitions"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    del automat["automat"]["q4"]

    new_automat = remove_non_existent_vertexes_from_transitions(automat)
    draw_automat(new_automat, filename, name)
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_delete_epsilon():
    name = "delete_epsilon"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = delete_epsilon(automat, filename)
    draw_automat(new_automat, filename, "delete_epsilon")
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_full_determinize():
    name = "full_determinize"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = full_determinize(automat)
    draw_automat(new_automat, filename, "full_determinize")
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_simplify_automat():
    name = "simplify_automat"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = simplify_automat(automat)
    draw_automat(new_automat, filename, "simplify_automat")
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_determinize_automat():
    name = "determinize_automat"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = determinize_automat(automat, filename)
    draw_automat(new_automat, filename, "determinize_automat")
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_minimize_automat():
    name = "minimize_automat"
    filename = "test/{name}/1.doa".format(name=name)
    test_filename_answer = "test/{name}/answer.doa".format(name=name)
    filename_real_answer = "test/{name}/real_answer.doa".format(name=name)

    automat = enter_automat(filename)
    draw_automat(automat, filename, "automat")

    new_automat = minimize_automat(automat, filename)
    draw_automat(new_automat, filename, "minimize_automat")
    make_doa(new_automat, test_filename_answer)

    assert check_files_contents(filename_real_answer, test_filename_answer)


def test_remove_repetitions_from_transitions_and_classes():
    transitions = [[4, 0], [4, 0], [2, 3], [2, 3], [3, 3],
                           [3, 3], [3, 3], [1, 1]]
    classes = [0, 0, 1, 1, 2, 3, 3, 4]

    correct_transitions = [[4, 0], [2, 3], [3, 3], [3, 3], [1, 1]]
    correct_classes = [0, 1, 2, 3, 4]

    new_transitions, new_classes = (
        remove_repetitions_from_transitions_and_classes(
            transitions, classes
        )
    )

    assert (sorted(correct_classes) == sorted(new_classes) and
            sorted(correct_transitions) == sorted(new_transitions))
