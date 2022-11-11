import os


def find_word(query, list_of_strings):
    return [s for s in list_of_strings if query in s]


def find_words(query_list, list_of_strings):
    results = []
    for s in list_of_strings:
        for query in query_list:
            if query in s:
                results.append(s)
            break;


if __name__ == '__main__':
    print("hello")
