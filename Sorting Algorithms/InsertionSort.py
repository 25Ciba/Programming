def insertion_sort(items):

    num_items = len(items)
    for index in range(1, num_items):
        item_to_insert = items[index]
        position = index - 1
        while position >= 0 and items[position] > item_to_insert:
            items[position + 1] = items[position]
            position = position - 1
        items[position + 1] = item_to_insert

