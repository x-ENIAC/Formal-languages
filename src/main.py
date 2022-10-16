import sys
from io_handler import enter_automat, draw_automat
from determinize_automat import determinize_automat, simplify_automat, delete_epsilon, full_determinize
from minimize_automat import minimize_automat

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    input_filename = sys.argv[1]
    automat = enter_automat(input_filename)
    print("nka:", automat)
    draw_automat(automat, input_filename, "nka")

    # print('----------------------------------------------------')

    dka_automat = determinize_automat(automat, input_filename)
    print("dka_automat:", dka_automat)
    draw_automat(dka_automat, input_filename, "dka")

    pdka_automat = full_determinize(dka_automat)
    print("pdka_automat:", pdka_automat)
    draw_automat(pdka_automat, input_filename, "pdka")

    # print('----------------------------------------------------')

    mpdka_automat = minimize_automat(pdka_automat, input_filename)
    print("mpdka_automat:", mpdka_automat)
    draw_automat(mpdka_automat, input_filename, "mpdka")