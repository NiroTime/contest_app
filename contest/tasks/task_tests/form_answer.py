def container_with_most_water(height):    i = 0    j = len(height) - 1    max_val = 0    while i != j:        if height[i] > height[j]:            cur_max = height[j] * (j - i)            j -= 1        else:            cur_max = height[i] * (j - i)            i += 1        max_val = max(max_val, cur_max)    return max_val