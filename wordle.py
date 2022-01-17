import sys
import argparse
from utils import *

bcolors= {
     2 : '\033[94m', # BLUE
     3 : '\033[92m', # GREEN
     1 : '\033[93m', # YELLOW
     0 : '\033[0m'   # END
}

def test():
    b, mask = evaluate("ನಿಘಂಟು", "ನಿಘಂಟ")
    print(b, mask)
    b, mask = evaluate("ಸ್ವಯಂಚಾಲಿತ", "ಸ್ವಯಂಸೇವಕ")
    print(b, mask)
    b, mask =evaluate("ಹಳೆಗನ್ನಡ", "ಹೊಸಗನ್ನಡ")
    print(b, mask)

def play(length, easy=False):
    print( str(length)+" ಅಕ್ಷರದ "+"ಪದ ನೀಡಿ")
    REF = get_random(length)
    with open("result", "w") as f:
        f.write(REF)
    while True:
        in_user = input()
        try: 
            b, mask = evaluate(REF, in_user, easy)
            if not b:
                print("ಪದ ನಿಘಂಟಿನಲ್ಲಿಲ್ಲ, ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ")
                continue
            out = ""
            letters_user = get_all(in_user)
            for letter , val in zip(letters_user,mask):
                if val > 0:
                    out += bcolors[val]
                out += letter
                if val > 0:
                    out += bcolors[0]
            sys.stdout.write("\033[F")
            print(out)
        except AssertionError:
            print(str(length)+" ಅಕ್ಷರದ "+"ಪದ ನೀಡಿ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cli Kannada Wordle')
    parser.add_argument('--length', type=int, dest='length', action='store',
                        default=4,help='Length of input word')
    parser.add_argument('--easy',  action='store_true',
                        help='Easy mode, no dictionary look up')
    args = parser.parse_args()
    play(args.length, args.easy)
