def quick_sort(items, start, end):
    
    if start >= end:
        return
    else:
        pivot_value = items[start] 
        low_mark = start + 1 
        high_mark = end 
        finished = False
        while finished == False:
            while low_mark <= high_mark and items[low_mark] <= pivot_value:
                low_mark = low_mark + 1                              
            while items[high_mark] >= pivot_value and high_mark >= low_mark:
                high_mark = high_mark - 1
            if low_mark < high_mark:
                temp = items[low_mark]
                items[low_mark] = items[high_mark]
                items[high_mark] = temp
            else:
                finished = True
        temp = items[start]
        items[start] = items[high_mark]
        items[high_mark] = temp
        quick_sort(items, start, high_mark - 1)
        quick_sort(items, high_mark + 1, end)
    return items