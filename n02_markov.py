import re


def find_word(query, list_of_strings):
    pattern = re.compile(r"\b" + query + r"\b", flags=re.IGNORECASE)
    return [s for s in list_of_strings if pattern.search(s)]


def find_words(query_list, list_of_strings):
    results = []
    for s in list_of_strings:
        for query in query_list:
            if re.search(r"\b" + query + r"\b", s, flags=re.IGNORECASE):
                results.append(s)
                break;
    return results


if __name__ == '__main__':
    data_directory = "sentence_data"

    file_path = data_directory + "/" + "60.txt"

    with open(file_path, "r") as f:
        sentences = f.readlines()
        no_sentences = find_words(["no", "never", "not", "nope"], sentences)
        # print(sentences)
        for sentence in no_sentences:
            print(sentence, end="")
