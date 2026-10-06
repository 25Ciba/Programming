def merge(left, right):

    merged = [] 
    index_left = 0 
    index_right = 0 

    while index_left < len(left) and index_right < len(right):
        if left[index_left] < right[index_right]:
            merged.append(left[index_left])
            index_left += 1
        else:
            merged.append(right[index_right])
            index_right += 1
    while index_left < len(left):
        merged.append(left[index_left])
        index_left += 1
    while index_right < len(right):
        merged.append(right[index_right])
        index_right += 1
    return merged