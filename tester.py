def solution(n):
    print(n)
    str_n = str(n)
    
    len_str = len(str_n)
    
    print(len_str % 2)

    if len_str % 2 !=0:
        return False
        
    half_length     = len_str //2
    first_half      = str_n[:half_length]
    second_half     = str_n[half_length:]
    print(first_half)
    print(second_half)
    
    sum_first_half      = sum(int(digit) for digit in first_half)
    sum_second_half     = sum(int(digit) for digit in second_half)
    
    return sum_first_half == sum_second_half
    
    
number = 1230
print(solution(number))
