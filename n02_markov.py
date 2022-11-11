def find_word(query, list_of_strings):
    return [s for s in list_of_strings if query in s]


def find_words(query_list, list_of_strings):
    results = []
    for s in list_of_strings:
        for query in query_list:
            if query in s:
                results.append(s)
                break;
    return results


if __name__ == '__main__':
    data_directory = "sentence_data"

    file_path = data_directory + "/" + "60.txt"

    with open(file_path, "r") as f:
        sentences = f.readlines()[100:110]
        no_sentences = find_words(["devil", "himself"], sentences)
        print(sentences)
        print(no_sentences)



