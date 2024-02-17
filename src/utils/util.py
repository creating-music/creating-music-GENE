def divide_chunk(list_dividend, division_size):
    def __divide_chunk(l, n):
        for i in range(0, len(l), n):
            yield l[i : i+n]

    return list(__divide_chunk(list_dividend, division_size))

def divide_chunk_into(list_dividend, num):
    division_size = len(list_dividend) // num
    division_res = len(list_dividend) % num

    if (division_res != 0):
        raise Exception('Not equally divisible.')

    return divide_chunk(list_dividend, division_size)
