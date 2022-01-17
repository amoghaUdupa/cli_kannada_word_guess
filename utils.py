import re
import pickle
import random
import argparse

# Regex to separate out the aksharas in a pada, copy pasta from:
# https://github.com/vinayakakv/akshara_tokenizer
swara = '[\u0c85-\u0c94\u0ce0\u0ce1]'
vyanjana = '[\u0c95-\u0cb9\u0cde]'
halant = '\u0ccd'
vowel_signs = '[\u0cbe-\u0ccc]'
anuswara = '\u0c82'
visarga = '\u0c83'
letters_re = re.compile('(?:({swara})|((?:{vyanjana}{halant})*)({vyanjana})(?:({vowel_signs})|({halant}))?)({anuswara}|{visarga})?'
                        .format(swara=swara, vyanjana=vyanjana, vowel_signs=vowel_signs, halant=halant, anuswara=anuswara, visarga=visarga))

def split_str(in_str):
     return letters_re.findall(in_str)

def count(in_str):
    return len(split_str(in_str))

# returns the main swara/vyanjana at each pos
def get_skeleton(in_str):
    matches = split_str(in_str)
    ret_letters = []
    for letter_splits in matches:
        if letter_splits[0]:
            ret_letters.append(letter_splits[0])
        elif letter_splits[1]:
            ret_letters.append(letter_splits[1][0])
        elif letter_splits[2]:
            ret_letters.append(letter_splits[2])

    return ret_letters

# Returns the letter at each pos
def get_all(in_str):
    matches = split_str(in_str)
    ret_letters = ["".join(match) for match in matches]
    return ret_letters


# Courtesy https://github.com/alar-dict/data
data = None
wc_dict = {}
with open("assets/alar.pkl", "rb") as f:
    data = pickle.load(f)
data = set(data)
for entry in data:
    c = count(entry)
    if c in wc_dict:
        wc_dict[c] += [entry]
    else:
        wc_dict[c] = [entry]
del data

def in_dict(in_str, c):
    return (in_str in wc_dict[c])

def get_random(length):
    random_index = random.randrange(len(wc_dict[length]))
    return wc_dict[length][random_index]

# Evaluates user and returns a value for each position
# 3 [GREEN] - correct position of the correct vyanjana+ottakshara+swara
# 2 [BLUE] - correct position of the vyanjana, wrong ottakshara or swara
# 1 [YELLOW] - correct vyanjana but wrong position
# 0 [] - just wrong
def evaluate(in_ref, in_user, easy):
    ret_mask = [0 for x in range(count(in_ref))]

    assert(count(in_ref) == count(in_user))

    letters_ref = get_skeleton(in_ref)
    letters_user = get_skeleton(in_user)

    for idx,letter in enumerate(letters_user):
        if letter in letters_ref:
            ret_mask[idx] += 1

    if in_dict(in_user, count(in_ref)) or easy:
        for idx,(x,y) in enumerate(zip(list(get_all(in_ref)), list(get_all(in_user)))):
            if x == y:
                ret_mask[idx] += 1;
        for idx,(x,y) in enumerate(zip(get_skeleton(in_ref), get_skeleton(in_user))):
            if x == y:
                ret_mask[idx] += 1;
    else:
        return False, ret_mask
    return True ,ret_mask


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ಅಕ್ಷರಗಳನ್ನು ಎಣಿಸಿ')
    parser.add_argument('--word', type=str, dest='word', action='store',
                        help='Input word')
    args = parser.parse_args()
    count, letters_skeleton = get_skeleton(args.word)
    count, letters_all = get_all(args.word)
    print (letters_skeleton)
    print (letters_all)
