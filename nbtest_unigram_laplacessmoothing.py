import sys
from math import log
import json
import os
from collections import OrderedDict
from operator import itemgetter

test_data = {}
predict_data = {}
list_positive_negative = []
POS = []
NEG = []
pos_to_neg = dict()
neg_to_pos = dict()
top_p_n = []
top_n_p = []


def printtopN(toptwenty):
    count = 0
    for key, value in toptwenty.items():
        count = count + 1
        print(key, value, '\n')
        if count == 20:
            break


def main(model_file_path, input_dir, predication_file):
    test_file_names = []
    print(input_dir)
    with open(model_file_path) as f:
        try:
            model_data = json.load(f)
            # index2 = yaml.load(f)
        except ValueError:
            mode_data = []

    positive_term_freq = model_data[1]
    negative_term_freq = model_data[0]

    for key, value in list(positive_term_freq.items()):
        values = log(value)
        pos_to_neg[key] = values - log(negative_term_freq.get(key))

    for key, value in list(negative_term_freq.items()):
        values = log(value)
        neg_to_pos[key] = values - log(positive_term_freq.get(key))

    newA = OrderedDict(reversed(sorted(list(pos_to_neg.items()), key=itemgetter(1))))

    newB = OrderedDict(reversed(sorted(list(neg_to_pos.items()), key=itemgetter(1))))

    for dirName, subdirList, fileList in os.walk(input_dir):
        for fname in fileList:
            test_file_names.append(dirName + "/" + fname)
    print(test_file_names)
    for i in test_file_names:
        input_file = open(i, 'r')

        test_data[i] = input_file.read().replace('\n', ' ')
        c = 0
        cumulative_probabilityP = 0.0
        cumulative_probabilityN = 0.0
        words = test_data[i].split()

        for k in words:
            cumulative_probabilityP += log(positive_term_freq.get(k, 1))
            cumulative_probabilityN += log(negative_term_freq.get(k, 1))

        predict_data[i] = [cumulative_probabilityP, cumulative_probabilityN]
        if cumulative_probabilityP > cumulative_probabilityN:
            POS.append(i)
        else:
            NEG.append(i)

    file1 = open(predication_file, 'w')
    file1.write('{:>5}\t{:>5}\t{:>2}\n'.format("file-name", "pos-score", "neg-score"))
    for key, value in predict_data.items():
        sentence_rev = " ".join(reversed(str(key).split('/')))
        file1.write('{:>5}\t{:>5}\t{:>2}\t'.format(sentence_rev.split()[0], value[0], value[1]))
        file1.write("\n")


if __name__ == '__main__':
    model_file_path = sys.argv[1]
    input_dir = sys.argv[2]
    predication_file = sys.argv[3]
    main(model_file_path, input_dir, predication_file)
