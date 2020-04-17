to_sort = ['p', 'a', 'n', 'd', 'r', 'e', 'q', 'w', 't', 'y', 'u', 'i', 'o', 's', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x',
           'c', 'v', 'b', 'm', 'f', 'a', 'c']


def counting_sort(l):

    range_el = max(l) + 1
    occur = [0] * range_el
    final = [0] * (len(l))

    for i in range(len(l)):
        occur[l[i]] += 1

    for i in range(1, len(occur)):
        occur[i] = occur[i - 1] + occur[i]

    for e in l:
        final[occur[e]-1] = e
        occur[e] -= 1

    return final


def sort_char(char_list):

    to_sort_int = [(ord(x) - 97) for x in char_list]
    result = counting_sort(to_sort_int)
    result = [chr(x + 97) for x in result]
    return result


print(sort_char(to_sort))


def prettify(ordered_list_int):
    result = []
    for num in ordered_list_int:
        num = str(num)
        stringa = ""
        for i in range(1,len(num), 2):
            if (num[i-1])+str(num[i]) == "00":
                continue
            elif (num[i-1])+str(num[i]) == "01":
                stringa += " "
            else:
                stringa += chr(int(str(num[i-1])+str(num[i]))+86)
        result.append(stringa)

    return result


def prep_input(list_strings):

    m = len(max(list_strings, key=len))
    out = []
    list_strings = [x.lower() for x in list_strings]

    for word in list_strings:
        s = ""
        for letter in word:
            if letter == " ":
                s += '01'
            else:
                s += str(ord(letter)-86)
        if len(word) < m:
            s = s.ljust((len(word) + (m-len(word)))*2, '0')

        out.append(s)

    out = [int(x) for x in out]

    return out


def counting_sort_snd(l, digit):

    occur = [0] * 10
    final = [0] * (len(l)+1)

    for i in range(len(l)):
        occur[(l[i] // digit) % 10] += 1

    for i in range(1, len(occur)):
        occur[i] = occur[i - 1] + occur[i]

    for e in reversed(l):
        final[occur[(e // digit) % 10] - 1] = e
        occur[(e // digit) % 10] -= 1

    for i in range(len(l)):
        l[i] = final[i]


def radix_sort(l):

    range_el = max(l)
    digit = 1

    while range_el / digit > 0:
        counting_sort_snd(l, digit)
        digit *= 10


def my_algorithm(to_sort):

    print(to_sort)
    prepped_list = prep_input(to_sort)

    radix_sort(prepped_list)
    result = prettify(prepped_list)

    return result


input_test = ["buono", "cattivo", "vestaglia", "oak hill", "zara", "bua", "bacini", "oak"]

print(my_algorithm(input_test))
