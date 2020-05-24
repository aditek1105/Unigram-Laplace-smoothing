import glob
import json
import sys


def updated_dict(dict, resdict):
    for i in list(dict):
        if resdict[i] < 5:
            del dict[i]
    return dict


def freq_count(dict, resdict):
    total_count = 0
    for key, value in list(dict.items()):
        if resdict[key] < 5:
            del dict[key]
        else:
            total_count += dict[key]
    return total_count


def convert_file_to_list(path):
    lst = []
    for i in path:
        file_temp = open(i, 'r')
        lst.append(file_temp.read())
    return lst


def store_dict_of_freq(lst):
    words_dict = {}
    for i in lst:
        words = i.split()
        for k in words:
            words_dict[k] = words_dict.get(k, 0) + 1
    return words_dict


def store_total_words_freq(dict_1, dict_2):
    total_words = {}
    total_words = dict_1.copy()
    for i in list(dict_2.keys()):
        total_words[i] = total_words.get(i, 0) + dict_2[i]
    return total_words


def normal_smoothing_pos(positive_words_dict, total_positive_count, total_words_len):
    pos_words_prob = {}
    for i in list(positive_words_dict.keys()):
        pos_words_prob[i] = (positive_words_dict[i] + 1) / (total_positive_count + total_words_len)
    return pos_words_prob


def normal_smoothing_neg(negative_words_dict, total_negative_count, total_words_len):
    neg_words_prob = {}
    for i in list(negative_words_dict.keys()):
        neg_words_prob[i] = (negative_words_dict[i] + 1) / (total_negative_count + total_words_len)
    return neg_words_prob


def main(inputdir, output):
    total_words = {}

    negative_list = []
    positive_list = []
    negative_words_dict = {}
    positive_words_dict = {}
    total_words = {}
    neg_words_prob = {}
    pos_words_prob = {}
    total_negative_count = 0
    total_positive_count = 0

    neg_train_file_names = glob.glob(inputdir + '/neg/*.txt')
    pos_train_file_names = glob.glob(inputdir + '/pos/*.txt')
    negative_list = convert_file_to_list(neg_train_file_names)
    positive_list = convert_file_to_list(pos_train_file_names)

    negative_words_dict = store_dict_of_freq(negative_list)
    positive_words_dict = store_dict_of_freq(positive_list)

    total_words = store_total_words_freq(negative_words_dict, positive_words_dict)

    for i in list(total_words.keys()):
        positive_words_dict[i] = positive_words_dict.get(i, 0)
        negative_words_dict[i] = negative_words_dict.get(i, 0)

    total_negative_count = freq_count(negative_words_dict, total_words)
    negative_words_dict = updated_dict(negative_words_dict, total_words)
    total_positive_count = freq_count(positive_words_dict, total_words)
    positive_words_dict = updated_dict(positive_words_dict, total_words)

    total_words = store_total_words_freq(negative_words_dict, positive_words_dict)


    total_words_len = total_words.__len__()

    neg_words_prob = normal_smoothing_neg(negative_words_dict, total_negative_count, total_words_len)
    pos_words_prob = normal_smoothing_pos(positive_words_dict, total_positive_count, total_words_len)

    all_words_prob_list = [neg_words_prob, pos_words_prob]
    model_file = open(output, "w")
    json.dump(all_words_prob_list, model_file)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_model = sys.argv[2]
    main(input_dir, output_model)
