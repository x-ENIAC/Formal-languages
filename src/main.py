import sys
from io_handler import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    input_filename = sys.argv[1]
    automat = enter_automat(input_filename)
    draw_automat(automat, input_filename)
