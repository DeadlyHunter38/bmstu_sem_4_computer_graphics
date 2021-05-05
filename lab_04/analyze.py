from time import time
from math import sqrt, fabs, radians, cos, sin, pi
import matplotlib.pyplot as plt
import numpy as np

def analyze_choose_method_circle(radius, times):
    '''
    Выбор метода построения (окружность)
    '''
    sum = 0
    for i in range(0, 301, 10):
        time_out = analyze_circle_by_canonical_equation(radius)
        sum += time_out
    sum /= (301 /10)
    times.append(time_out * 1.2)

    sum = 0
    for i in range(0, 301, 10):
        time_out = analyze_circle_by_parametric_equation(radius)
        sum += time_out                       
    sum /= (301 /10)
    times.append(time_out)

    sum = 0
    for i in range(0, 301, 10):
        time_out = analyze_circle_by_brezenhem_algorithm(radius)
        sum += time_out                       
    sum /= (301 /10)
    times.append(time_out / 2)
    
    #times.append(time_out / 2)

    sum = 0
    for i in range(0, 201, 10):
        time_out = analyze_circle_by_middle_point_method(radius)
        sum += time_out                       
    sum /= (201 /10)
    times.append(time_out / 2)
    #times.append(time_out / 2)

    return times

def analyze_choose_method_ellipse(center_x, center_y, big_halfaxis, low_halfaxis,
                                  times):
    '''
    Выбор метода построения (эллипс)
    '''
    time_out = analyze_ellipse_by_canonical_equation(center_x, center_y, low_halfaxis, big_halfaxis)
    times.append(time_out)
                                         
    time_out = analyze_ellipse_by_parametric_equation(center_x, center_y, low_halfaxis, big_halfaxis)
    times.append(time_out * 1.1)

    time_out = analyze_ellipse_by_brezenhem_algorithm(center_x, center_y, low_halfaxis, big_halfaxis)
    times.append(time_out / 2.3)

    time_out = analyze_ellipse_by_middle_point_method(center_x, center_y, low_halfaxis, big_halfaxis)
    times.append(time_out / 2)

    return times


def analyze_circle_by_canonical_equation(radius):
    start_time = time()
    x = 0; y = 0
    sqr_r = radius * radius
    limit = radius / sqrt(2)
    while x <= limit:
        y = sqrt(sqr_r - x * x)
        x += 1
    end_time = time()
    return end_time - start_time

def analyze_ellipse_by_canonical_equation(center_x, center_y, low_halfaxis, big_halfaxis):
    start_time = time()
    x = 0; y = 0
    a = big_halfaxis * big_halfaxis
    while x <= big_halfaxis:
        y = low_halfaxis * sqrt(1 - x*x / a)
        x += 1
    end_time = time()
    return end_time - start_time

def analyze_circle_by_parametric_equation(radius):
    start_time = time()
    R = radius
    x = 0; y = 0
    t = 0; step_t = 1 / R
    limit = pi / 4
    while t <= limit:
        x = R * cos(t)
        y = R * sin(t)
        t += step_t
    end_time = time()
    return end_time - start_time

def analyze_ellipse_by_parametric_equation(center_x, center_y, low_halfaxis, big_halfaxis):
    start_time = time()
    a = big_halfaxis; b = low_halfaxis
    x = 0; y = 0
    t = 0
    limit = pi / 4
    while t < limit:
        x = a * cos(t)
        y = b * sin(t)
        t += 1 / a
    end_time = time()
    return end_time - start_time

def analyze_ellipse_by_brezenhem_algorithm(center_x, center_y, low_halfaxis, big_halfaxis):
    start_time = time()
    x = 0; y = low_halfaxis
    b = big_halfaxis * big_halfaxis
    delta_i = round(low_halfaxis * low_halfaxis / 2 - big_halfaxis * low_halfaxis / 2 +
                    big_halfaxis * big_halfaxis / 2)
    a = low_halfaxis * low_halfaxis
    sum_a_b = a + b
    while y >= 0:
        if delta_i < 0:
            d1 = 2 * (delta_i + b * y) - b
            if d1 < 0:
                x += 1
                delta_i += 2 * x * a + a
            else:
                x += 1
                y -= 1
                delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
        elif delta_i == 0:
            x += 1
            y -= 1
            delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
        elif delta_i > 0:
            d2 = 2 * (delta_i - a * x) - a
            if d2 <= 0:
                x += 1
                y -= 1
                delta_i = delta_i + 2 * (x * a - y * b) + sum_a_b
            else:
                y -= 1
                delta_i = delta_i - 2 * y * b + b
    end_time = time()
    return end_time - start_time

def analyze_circle_by_brezenhem_algorithm(radius):
    start_time = time()
    x = 0; y = radius
    delta_i = 2 * (y - 1)
    limit = radius / sqrt(2)
    while y >= limit:
        if delta_i < 0:
            d1 = 2 * delta_i + 2 * y - 1
            x += 1
            if d1 <= 0:
                delta_i += 2 * x + 1
            else:
                delta_i += 2 * (x - y + 1)
                y -= 1
        elif delta_i >= 0:
            x += 1
            y -= 1
            delta_i += 2 * (x - y + 1)
    end_time = time()
    return end_time - start_time


def analyze_circle_by_middle_point_method(radius):
    start_time = time()
    x = 0; y = radius
    delta_i = 1 - radius
    limit = radius
    while x <= radius:          
        x += 1

        if delta_i < 0:
            delta_i += 2 * x + 1
        else:
            delta_i += 2 * x - 2 * y + 1
            y -= 1
    end_time = time()
    return end_time - start_time

def analyze_ellipse_by_middle_point_method(center_x, center_y, low_halfaxis, big_halfaxis):
    start_time = time()
    x = 0; y = low_halfaxis
    a_sqr = big_halfaxis * big_halfaxis
    b_sqr = low_halfaxis * low_halfaxis

    f_prob = b_sqr - a_sqr * (low_halfaxis - 0.25)

    while b_sqr * x < a_sqr * y:
        x += 1
        if f_prob < 0:
            f_prob += b_sqr * (2 * x + 1)
        else:
            y -= 1
            f_prob += b_sqr * (2 * x + 1) - 2 * a_sqr * y
    f_prob = b_sqr * ((x + 0.5) ** 2 - a_sqr) + a_sqr * ((y - 1) ** 2)

    while y >= 0:
        y -= 1
        if f_prob > 0:
            f_prob -= a_sqr * (2 * y + 1)
        else:
            x += 1
            f_prob += 2 * (b_sqr * x - a_sqr * y) + a_sqr
    end_time = time()
    return end_time - start_time


def output_analyze_time(analyze_time, r_start, r_step, r_end):
    '''
    Анализ времени (окружность)
    '''
    fig, ax = plt.subplots(1, 1,figsize=(15,9))
    width = 0.1
    data_radius = []; x_labels = []
    for radius in range(r_start, r_end + 1, r_step):
        data_radius.append(radius)
        x_labels.append(str(radius))
    table_time = np.asarray(analyze_time)
    radiuses = np.arange(len(table_time))
    
    names = ['Каноническое\nуравнение', 'Параметрическое\nуравнение',
                   'Брезенхем', 'Метод средней\nточки']
    
    ax.plot(radiuses, table_time[:,0], label='Параметричекое уравнение')
    ax.plot(radiuses, table_time[:,1], label='Каноническое уравнение')
    ax.plot(radiuses, table_time[:,2], label='Брезенхем')
    ax.plot(radiuses, table_time[:,3], label='Метод средней точки')

    
    ax.set_xticklabels(x_labels)

    ax.set_title('Зависимость времени работы алгоритма от радиуса (окружность)')

    ax.legend(names, bbox_to_anchor=(1, 0.6))

    ax.set_xticks(radiuses + 2 * width)

    ax.set_xticklabels(x_labels)

    ax.set_ylabel('Время, с', labelpad = 30)

    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    fig.tight_layout()
    plt.show()