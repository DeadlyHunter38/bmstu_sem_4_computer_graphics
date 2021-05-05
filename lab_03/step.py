from math import trunc, fabs, radians, cos, sin

def analyze_step_digital_differential_analyzer(x_start, y_start, x_end, y_end, flag_table):
    '''
    Цифровой дифференциальный анализатор
    '''
    max_step_stair = 0; max_len_stair = 0
    len_stair = 0

    l = 0; dx = 0; dy = 0
    if abs(x_end - x_start) >= abs(y_end - y_start):
        l = abs(x_start - x_end)
    else:
        l = abs(y_start - y_end)
    dx = (x_end - x_start) / l
    dy = (y_end - y_start) / l
    x = x_start; y = y_start
    for i in range (int(l) + 1):
        last_x = x; last_y = y
        x_draw = round(x); y_draw = round(y)
        x += dx; y += dy
        new_x = x; new_y = y
        
        if fabs(int(new_x) - int(last_x)) != 0 and int(new_y) - int(last_y) == 0:
            len_stair += 1

        if fabs(int(new_x) - int(last_x)) != 0 and int(new_y) - int(last_y) != 0:
            max_step_stair += 1
            if len_stair > max_len_stair:
                max_len_stair = len_stair
            len_stair = 1

    return max_step_stair, max_len_stair

def analyze_step_by_brezenham_with_float_data(x_start, y_start, x_end, y_end, flag_table):
    '''
    Алгоритм Брезенхема с действительными данными
    '''
    max_step_stair = 0; max_len_stair = 0
    len_stair = 0

    dx = x_end - x_start; dy = y_end - y_start
    sx = sign(dx); sy = sign(dy)
    dx = abs(dx); dy = abs(dy)
    if dx > dy:
        flag_exchange = 0
    else:
        dx, dy = dy, dx
        flag_exchange = 1
    m = dy / dx
    f = m - 0.5

    x_temp = x_start; y_temp = y_start
    for i in range(int(dx) + 1):
        if f > 0:
            if flag_exchange == 1:
                x_temp += sx
                len_stair += 1
            else:
                y_temp += sy
                max_step_stair += 1
                if len_stair > max_len_stair:
                    max_len_stair = len_stair
                len_stair = 0
            f -= 1
        if f <= 0:
            if flag_exchange == 1:
                y_temp += sy
                max_step_stair += 1
                if len_stair > max_len_stair:
                    max_len_stair = len_stair
                len_stair = 0
            else:
                x_temp += sx
                len_stair += 1
        f += m
    return max_step_stair, max_len_stair


def analyze_step_by_brezenham_with_int_data(x_start, y_start, x_end, y_end, flag_table):
    '''
    Алгоритм Брезенхема с целочисленными данными
    '''
    max_step_stair = 0; max_len_stair = 0
    len_stair = 0

    dx = x_end - x_start; dy = y_end - y_start
    sx = sign(dx); sy = sign(dy)
    dx = abs(dx); dy = abs(dy)
    if dx > dy:
        flag_exchange = 0
    else:
        dx, dy = dy, dx
        flag_exchange = 1
    m = dy/dx
    f = 2 * dy - dx

    x_temp = x_start; y_temp = y_start
    for i in range(int(dx) + 1):
        if f >= 0:
            if flag_exchange == 1:
                x_temp += sx
                len_stair += 1
            else:
                y_temp += sy
                max_step_stair += 1
                if len_stair > max_len_stair:
                    max_len_stair = len_stair
                len_stair = 0
            f -= 2 * dx
        if f < 0:
            if flag_exchange == 1:
                y_temp += sy
                max_step_stair += 1
                if len_stair > max_len_stair:
                    max_len_stair = len_stair
                len_stair = 0
            else:
                x_temp += sx
                len_stair += 1
        f += 2 * dy
    return max_step_stair, max_len_stair

def analyze_step_by_brezenham_with_step_removal(x_start, y_start, x_end, y_end, flag_table):
    '''
    Алгоритм Брезенхема с устранением ступенчатости
    '''
    max_step_stair = 0; max_len_stair = 0
    len_stair = 0

    # Количество уровней интенсивности
    I = 255
    dx = x_end - x_start; dy = y_end - y_start
    sx = sign(dx); sy = sign(dy)
    dx = abs(dx); dy = abs(dy)
    if dx != 0:
        m = dy/dx
    else:
        m = 0
    
    if dx > dy:
        flag_exchange = 0
    else:
        dx, dy = dy, dx
        flag_exchange = 1
        if m != 0:
            m = 1 / m
    f = I / 2
    x_temp = x_start; y_temp = y_start
    m *= I
    w = I - m

    for i in range (int(dx)):          
        if f <= w:
            if flag_exchange == 0:
                x_temp += sx
                len_stair += 1
            if flag_exchange == 1:
                y_temp += sy
                max_step_stair += 1
                if len_stair > max_len_stair:
                    max_len_stair = len_stair
                len_stair = 1
            f += m
        else:
            x_temp += sx; y_temp += sy; f-= w
            max_step_stair += 1
            if len_stair > max_len_stair:
                max_len_stair = len_stair
            len_stair = 1
    return max_step_stair, max_len_stair

def analyze_step_by_vu(x_start, y_start, x_end, y_end, flag_table):
    '''
    Алгоритм Ву
    '''
    max_step_stair = 0; max_len_stair = 0
    prev_step = 0; cur_step = 0
    len_stair = 0
    last_y = 0; new_y = 0

    dx = x_end - x_start
    dy = y_end - y_start

    flag_exchange = 0
    if abs(dx) < abs(dy):
        flag_exchange = 1
        x_start, y_start = y_start, x_start
        x_end, y_end = y_end, x_end
        dx, dy = dy, dx
    
    if x_end < x_start:
        x_start, x_end = x_end, x_start
        y_start, y_end = y_end, y_start
    
    m = 0
    if dx != 0:
        m = dy / dx
    
    y = y_start; x = x_start
    last_x = x; last_y = y
    new_x = x; new_y = y
    I = 255

    while x <= x_end:
        if flag_exchange:
            sign_y = sign(y)
        else:
            sign_y = sign(y)

        last_y = y
        y += m; x += 1
        new_y = y
        if int(new_y) > int(last_y):
            max_step_stair += 1
            if len_stair > max_len_stair:
                max_len_stair = len_stair
            len_stair = 1
        else:
            len_stair += 1
    return max_step_stair, max_len_stair
        

def sign(x):
    value = 0
    if x > 0:
        value = 1
    elif x == 0:
        value = 0
    else:
        value = -1
    return value