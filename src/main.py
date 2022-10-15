import sys
from io_handler import enter_automat, draw_automat
from determinize_automat import determinize_automat, simplify_automat, delete_epsilon

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    input_filename = sys.argv[1]
    automat = enter_automat(input_filename)
    print(automat)
    draw_automat(automat, input_filename, "1_nka")

    print('----------------------------------------------------')

    automat = delete_epsilon(automat, input_filename)
    print(automat)

    print('----------------------------------------------------')

    dka_automat = simplify_automat(automat)
    print(dka_automat)
    draw_automat(dka_automat, input_filename, "4_simplify")

    dka_automat = determinize_automat(automat)
    print(dka_automat)
    draw_automat(dka_automat, input_filename, "5_dka")