from tkinter import *
from tkinter import ttk
from math import sqrt, acos
import tkinter.messagebox as box
import copy

FONT_1 = 'Times New Roman'
SIZE_1 = 14
SHIFT_X = 697; SHIFT_Y = 372
SHIFT_POINT = 6
count_polygones = 0; old_count_polygones = 0
number_coord = 0; number_action = 0
pressed = False
actions = [1, 2, 3, 4, 5, 6]
#создание списка контуров
list_of_x = []; list_of_y = []; old_list_x = []; old_list_y = []
old_x = 0; old_y = 0; old_location = 0
id_points = []; id_lines = []
id_center = [] #ось х, у, точка центра


def start_input_new_polygone(window, list_of_x, list_of_y):
    global count_polygones, number_action
    number_action = actions[0]
    count_polygones += 1
    label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))
    label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)
    list_of_x.append([]); list_of_y.append([])

def input_coordinates(ep_x, ep_y, table, list_of_x, list_of_y, count_polygons):
    print(count_polygons)
    if (list_of_x == []):
        text = 'Необходимо создать многоугольник.\n'
        box.showerror('Ошибка', text)
    else:
        try:
            global number_coord, number_action
            number_action = actions[1]
            x = float(ep_x.get()); y = float(ep_y.get())
            number_coord += 1
            list_of_x[count_polygons - 1].append(x); list_of_y[count_polygons - 1].append(y)
            string = ''
            string += ' '+str(number_coord)+"\t"+str(count_polygones)+"\t\t\t"+str(x)+"\t\t\t"+str(y)
            table.insert('', 'end', text="0", 
                        values=string)
        except ValueError:
            text = 'Некорректные входные данные.\n'
            box.showerror('Ошибка', text)

def delete_coordinate(window, ep_number, table, list_of_x, list_of_y, table_size, type_del):
    print(table_size)
    signal_in = 1
    if (type_del == 1):
        #Получаем id первого выделенного элемента
        try:
            selected_item = table.selection()[0]
        except IndexError:
            text = "Пустая таблица или не выбрана точка."
            box.showerror('Ошибка', text)
            signal_in = 0
    elif type_del == 2:
        low_board = ep_number

    if (signal_in == 1):
        global number_coord, number_action
        number_action = actions[2]
        number_coord -= 1; low_board = 0
        if (type_del == 1):
            # Получаем значения в выделенной строке
            value_id = table.item(selected_item, option="values")
            low_board = int(value_id[0])
            table.delete(selected_item)
        elif (type_del == 2):
            low_board = ep_number
        location = 0
        start_i = 0; start_j = 0
        global old_list_x, old_list_y, old_count_polygones, count_polygones
        old_count_polygones = copy.deepcopy(count_polygones)
        old_list_x = copy.deepcopy(list_of_x)
        old_list_y = copy.deepcopy(list_of_y)
        exit_flag = False
        for i in range(len(list_of_x)):
            for j in range(len(list_of_x[i])):
                if (location == low_board - 1):
                    del(list_of_x[i][j]); del(list_of_y[i][j])
                    start_i = i; start_j = j
                    exit_flag = True
                location += 1
            if exit_flag == True:
                break

        #проверка на пустые многоугольники
        for i in range(len(list_of_x)):
            if (list_of_x[i] == []):
                list_of_x.pop(i); list_of_y.pop(i)
                count_polygones -= 1
                label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))
                label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)

        #удаление всех элементов после выделенного
        temp_id = low_board; temp_count = 0
        for record in table.get_children():
            if temp_count >= low_board - 1:
                table.delete(record)
            temp_count += 1

        #обновление всех удаленных элементов
        temp_count = 0
        for i in range(len(list_of_x)):
            for j in range(len(list_of_x[i])):
                if temp_count >= temp_id - 1:
                    table.insert('', 'end', text="0", 
                        values=str(temp_count + 1)+"\t\t\t"+str(count_polygones)+"\t\t\t"+str(list_of_x[i][j])+"\t\t\t"+str(list_of_y[i][j]))
                temp_count += 1 

def delete_all(window, table):
    global list_of_x
    if list_of_x == []:
        text = "Необходимо заполнить таблицу"
        box.showerror('Ошибка', text)
    else:
        i = 0
        global list_of_y, count_polygones, old_count_polygones, number_coord, number_action, old_list_x, old_list_y
        number_action = actions[3]
        for record in table.get_children():
            table.delete(record)
        old_count_polygones = copy.deepcopy(count_polygones)
        old_list_x = copy.deepcopy(list_of_x)
        old_list_y = copy.deepcopy(list_of_y)
        list_of_x = []; list_of_y = []; count_polygones = 0; number_coord = 0
        label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))
        label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)
    return

def print_matrix(matrix):
    for i in range (len(matrix)):
        for j in range (len(matrix[0])):
            print(matrix[i][j])
    print()

def find_min_distance(list_x1, list_y1, size_matrix):  
    begin_coord = 0; end_coord = 1
    min = 0; temp_min = 0
    min = sqrt((list_x1[0] - list_x1[1]) ** 2 + (list_y1[0] - list_y1[1]) ** 2)
    for i in range(1, size_matrix - 1):
        temp_min = sqrt((list_x1[i] - list_x1[i + 1]) ** 2 + (list_y1[i] - list_y1[i + 1]) ** 2)
        if temp_min < min:
            begin_coord = i; end_coord = i + 1

    value = sqrt((list_x1[size_matrix - 1] - list_x1[0]) ** 2 + (list_y1[size_matrix - 1] - list_y1[0]) ** 2)
    if (value <= min):
        min = value
        begin_coord = 0; end_coord = size_matrix - 1
    
    return begin_coord, end_coord

def add_coord(graph, table, ep_x, ep_y, ep_number):
    try:
        global list_of_x, list_of_x, old_list_x, old_list_y
        number = int(ep_number.get())
        x = int(ep_x.get()); y = int(ep_y.get())
        temp_count = 0; flag_out = 0
        for i in range(len(list_of_x)):
            if temp_count == number - 1:
                list_of_x[i].append(x)
                list_of_y[i].append(y)
                flag_out = 1
                break
            temp_count += 1
            if flag_out == 1:
                break
        for record in table.get_children():
            table.delete(record)

        temp_count = 0
        for i in range(len(list_of_x)):
            for j in range(len(list_of_x[i])):
                table.insert('', 'end', 
                    values=str(temp_count + 1)+"\t\t\t"+str(i + 1)+"\t\t\t"+str(list_of_x[i][j])+"\t\t\t"+str(list_of_y[i][j]))
                temp_count += 1

    except ValueError:
            text = 'Некорректные входные данные.\n'
            box.showerror('Ошибка', text)

def compare_matrix(matrix_1, matrix_2, angles_1, angles_2):
    array_1 = []; array_2 = []
    flag_in = 1
    for i in range(len(matrix_1) - 1):
        array_1.append(matrix_1[i][i + 1])
        array_2.append(matrix_2[i][i + 1])
    array_1.append(matrix_1[0][len(matrix_1) - 1])
    array_2.append(matrix_2[0][len(matrix_2) - 1])

    array_1.sort()
    array_2.sort()
    k = array_1[0] / array_2[0] 
    for i in range(1, len(array_1)):
        if (array_1[i] / array_2[i]) != k:
            flag_in = 0
            break
    if (flag_in == 1):
        angles_1.sort(); angles_2.sort()
        for i in range(0, len(array_1)):
            if (angles_1[i] != angles_2[i]):
                flag_in = 0
                break
    return flag_in

def create_distanse_matrix(list_x, list_y):  
    size_matrix = len(list_x)
    matrix = [[0] * size_matrix for j in range (size_matrix)]

    begin_coord, end_coord = find_min_distance(list_x, list_y, size_matrix)

    j = 0
    for i in range(begin_coord, size_matrix - 1):
        matrix[j][j + 1] = sqrt((list_x[i] - list_x[i + 1]) ** 2 + (list_y[i] - list_y[i + 1]) ** 2)
        j += 1
    if (begin_coord == 0):
        matrix[0][size_matrix - 1] = sqrt((list_x[size_matrix - 1] - list_x[0]) ** 2 + (list_y[size_matrix - 1] - list_y[size_matrix - 1]) ** 2)
        if (len(list_x) > 3):
            matrix[0][size_matrix - 1] = sqrt((list_x[begin_coord] - list_x[size_matrix - 1]) ** 2 + (list_y[begin_coord] - list_y[size_matrix - 1]) ** 2)
    else:
        matrix[j][j + 1] = sqrt((list_x[size_matrix - 1] - list_x[0]) ** 2 + (list_y[size_matrix - 1] - list_y[0]) ** 2)
        j += 1
        for i in range(begin_coord - 1):
            matrix[j][j + 1] = sqrt((list_x[i] - list_x[i + 1]) ** 2 + (list_y[i] - list_y[i + 1]) ** 2)
            j += 1
        matrix[0][size_matrix - 1] = sqrt((list_x[begin_coord - 1] - list_x[begin_coord]) ** 2 + (list_y[begin_coord - 1] - list_y[begin_coord]) ** 2)

    return matrix

def define_angle(list_x, list_y):
    angles = []
    size = len(list_x)
    for i in range(size - 2):
        a = sqrt((list_x[i] - list_x[i + 1]) ** 2 + (list_y[i] - list_y[i + 1]) ** 2)
        b = sqrt((list_x[i + 1] - list_x[i + 2]) ** 2 + (list_y[i + 1] - list_y[i + 2]) ** 2)
        c = sqrt((list_x[i] - list_x[i + 2]) ** 2 + (list_y[i] - list_y[i + 2]) ** 2)
        angle = acos((a * a + b * b - c * c) / (2 * a * b))
        angles.append(angle)
    a = sqrt((list_x[size - 2] - list_x[size - 1]) ** 2 + (list_y[size - 2] - list_y[size - 1]) ** 2)
    b = sqrt((list_x[size - 1] - list_x[0]) ** 2 + (list_y[size - 1] - list_y[0]) ** 2)
    c = sqrt((list_x[size - 2] - list_x[0]) ** 2 + (list_y[size - 2] - list_y[0]) ** 2)
    angle = acos((a * a + b * b - c * c) / (2 * a * b))
    angles.append(angle)

    a = sqrt((list_x[size - 1] - list_x[0]) ** 2 + (list_y[size - 1] - list_y[0]) ** 2)
    b = sqrt((list_x[0] - list_x[1]) ** 2 + (list_y[0] - list_y[1]) ** 2)
    c = sqrt((list_x[size - 1] - list_x[1]) ** 2 + (list_y[size - 1] - list_y[1]) ** 2)
    angle = acos((a * a + b * b - c * c) / (2 * a * b))
    angles.append(angle)
    return angles 
    
def draw_polygon(graph, list_of_x, list_of_y):
    #перевод введенных координат в масштаб экрана
    A = 8.342 * 3; B = 3
    SHIFT_ZOOM_X = 0; SHIFT_ZOOM_Y = 0 #сдвиг масштаба на экране
    result_list_x = []; result_list_y = []

    for i in range(0, len(list_of_x)):
        result_list_x.append(list_of_x[i] * A)
        result_list_y.append(list_of_y[i] * (-1) * A)
    
    global id_points, id_lines
    size_polygon = len(result_list_x)
    temp_id_points = 0; temp_id_lines = 0
    for i in range(size_polygon - 1):
        temp_id_lines = graph.create_line(result_list_x[i] + SHIFT_X + B, result_list_y[i] + SHIFT_Y + B, result_list_x[i + 1] + SHIFT_X + B,
                          result_list_y[i + 1] + B + SHIFT_Y, fill='blue', width=4)
        id_lines.append(temp_id_lines)
        temp_id_points = graph.create_oval(result_list_x[i] + SHIFT_X, result_list_y[i] + SHIFT_Y, result_list_x[i] + SHIFT_X + SHIFT_POINT, 
                            result_list_y[i] + SHIFT_Y + SHIFT_POINT, fill='blue', activefill='yellow')
        id_points.append(temp_id_points)
    temp_id_lines = graph.create_line(result_list_x[size_polygon - 1] + SHIFT_X + B, result_list_y[size_polygon - 1] + SHIFT_Y + B,
                        result_list_x[0] + SHIFT_X + B, result_list_y[0] + SHIFT_Y + B, fill='blue', width=4)
    id_lines.append(temp_id_lines)
    temp_id_points = graph.create_oval(result_list_x[size_polygon - 1] + SHIFT_X, result_list_y[size_polygon - 1] + SHIFT_Y, result_list_x[size_polygon - 1] + SHIFT_X  + SHIFT_POINT, 
                        result_list_y[size_polygon - 1] + SHIFT_Y + SHIFT_POINT, fill='blue', activefill='yellow')
    id_points.append(temp_id_points)

def find_empty_polygon(list_of_x):
    signal_empty = 0
    size_list = len(list_of_x)
    for i in range(size_list):
        if list_of_x[i] == []:
            signal_empty = 1
            break
    return signal_empty

def find_not_polygon(list_of_x):
    signal_not_polygon = 0
    size_list = len(list_of_x); size_i = 0
    for i in range(size_list):
        size_i = len(list_of_x[i])
        if (size_i == 1 or size_i == 2):
            signal_not_polygon = 1
            break
    return signal_not_polygon

def edit_coord(window, table, ep_x, ep_y):
    try:
        global list_of_x, list_of_y, old_list_x, old_list_y, number_action, old_count_polygones
        number_action = 5
        selected_item = table.selection()[0]
        x = float(ep_x.get()); y = float(ep_y.get())
        value_id = table.item(selected_item, option="values")
        low_board = int(value_id[0]) - 1
        old_list_x = copy.deepcopy(list_of_x)
        old_list_y = copy.deepcopy(list_of_y)
        old_count_polygones = copy.deepcopy(count_polygones)

        recover_coord(table, list_of_x, list_of_y, low_board, x, y)
    except IndexError:
        text = "Пустая таблица или не выбрана точка."
        box.showerror('Ошибка', text)
        signal_in = 0
    except ValueError:
        text = 'Некорректные входные данные.\n'
        box.showerror('Ошибка', text)

def create_output_result(list_of_x, list_of_y):
    output_res = ''
    size_list = len(list_of_x)
    for i in range(size_list - 1):
        output_res += ' (' + str(list_of_x[i]) + ';' + str(list_of_y[i]) + '),'
    output_res += ' (' + str(list_of_x[size_list - 1]) + ';' + str(list_of_y[size_list - 1]) + ');'
    return output_res

def delete_old_result(graph):
    global id_lines, id_points
    for i in id_lines:
        graph.delete(i)
    for i in id_points:
        graph.delete(i)
    id_lines = []; id_points = []

def find_solution(graph, result_canvas, list_of_x, list_of_y, table, table_size):
    try:
        if (len(list_of_x) < 2):
            text = 'Необходимо количество многоугольников больше одного.\n'
            box.showerror('Ошибка', text)
        elif (find_empty_polygon(list_of_x) == 1):
            text = 'Присутствует пустой многоугольник.\nВведите данные заново.'
            box.showerror('Ошибка', text)
        elif (find_not_polygon(list_of_x) == 1):
            text = 'Присутствует не многоугольник.\nВведите данные заново.'
            box.showerror('Ошибка', text)
        else:
            global number_action
            delete_old_result(graph)
            number_action = actions[4]
            matrix_1 = [[]]; matrix_2 = [[]]; angles_1 = []; angles_2 = []
            result_matrix_x1 = [[]]; result_matrix_x2 = [[]]; result_matrix_y1 = []; result_matrix_y2 = []
            start = 0; end = 0; min_polygon = 0
            for i in range(len(list_of_x) - 1):
                size_matrix_1 = len(list_of_x[i]); 
                for j in range(i + 1, len(list_of_x)):
                    size_matrix_2 = len(list_of_x[j])
                    if size_matrix_1 == size_matrix_2:
                        matrix_1 = create_distanse_matrix(list_of_x[i], list_of_y[i])
                        angles_1 = define_angle(list_of_x[i], list_of_y[i])
                        matrix_2 = create_distanse_matrix(list_of_x[j], list_of_y[j])
                        angles_2 = define_angle(list_of_x[j], list_of_y[j])
                        if (compare_matrix(matrix_1, matrix_2, angles_1, angles_2) == 1 and size_matrix_1 > min_polygon):
                            start = i; end = j; min_polygon = size_matrix_1
            if start != end:
                result_matrix_x1 = list_of_x[i]; result_matrix_x2 = list_of_x[i + 1]
                result_matrix_y1 = list_of_y[i]; result_matrix_y2 = list_of_y[i + 1]
                draw_polygon(graph, list_of_x[start], list_of_y[start])
                draw_polygon(graph, list_of_x[end], list_of_y[end])
                output_res_start = ''; output_res_end = ''
                output_res_start = create_output_result(list_of_x[start], list_of_y[start])
                output_res_end = create_output_result(list_of_x[end], list_of_y[end])
                label_result_start = Label(result_canvas, text="Номер первого многоугольника и его координаты: N = " +
                                    str(start + 1) + " " + output_res_start, font=(FONT_1, SIZE_1), background='white',
                                    justify='left')
                label_result_end = Label(result_canvas, text="Номер первого многоугольника и его координаты: N = " +
                                    str(end + 1) + " " + output_res_end, font=(FONT_1, SIZE_1), background='white',
                                    justify='left')
                label_result_start.place(relx=0.01, rely=0.05, relheight = 0.2, relwidth = 1)
                label_result_end.place(relx=0.01, rely=0.25, relheight = 0.2, relwidth = 1)
            else:
                text = "Нет многоугольников, удовлетворяющих условию."
                box.showinfo('Вывод', text)
    except NameError:
        text = 'Необходимо создать и заполнить многоугольник.\n'
        box.showerror('Ошибка', text)
    
def print_info():
    window = Tk()
    FONT_ = 'Times New Roman'
    SIZE = 14
    window.title('Справка')
    window.geometry('900x600')
    text = ('Условие задачи:\n' +
            'Будем называть два многоугольника подобными, если существует взаимно-однозначное\n' +
            'отображение сторон этих двух фигур такое, что соответствующие стороны\n' +
            'пропорциональны с коэффициентом пропорциональности k, а углы, образованные двумя\n' +
            'соответствующими сторонами, равны.\n\n' +
            'Найти два подобных N-угольника, где N – максимально возможное.\n' +
            'Многоугольники задаются на плоскости координатами вершин контуров. Вершины в\n' +
            'контуре перечисляются в порядке обхода против часовой стрелки. Считать, что две\n' +
            'величины равны с точностью до двух знаков после запятой.\n\n\n' +
            'Справка по работе с программой:\n' +
            '1. Добавление новой координаты:\n' + 
            '\t1.1. Введите координаты в соответствующие поля и нажмите "Ввести координаты"\n' +
            '\t1.2. Вещественные координаты вводятся через "."\n' 
            '2. Создание нового многоугольника: нажмите "Новый многоугольник"\n' + 
            '3. Удаление координаты: выберите соответствующую координату из таблицы и нажмите\n "Удалить координату"\n' +
            '4. Масштабирование в координатной плоскости: наведите курсор на часть экрана координатной плоскости\n' +
            'и прокрутите колесиком мыши.\n' + 
            '5. Вывод результата: под графиком будет отображена информация о координатах полученных N угольников.\n'+
            '6. Кнопка "отмена": применяется только к последнему действию, кроме "найти решение".\n' + 
            '7. Изменение координаты: выберите в таблице желаемую координату и нажмите "изменить координату"\n')
    label_1 = Label(window, text = text, font=(FONT_1, SIZE_1), justify = 'left')
    label_1.place(relx = 0.01, rely= 0.001, relwidth = 1, relheight = 0.93)
    window.mainloop()
    
def zoom_more(event, window):
    window.scale("all", event.x, event.y, 1.1, 1.1)

def zoom_less(event, window):
    window.scale("all", event.x, event.y, 0.9, 0.9)

def move_start(event, window):
    global pressed
    pressed = not pressed
    window.scan_mark(event.x, event.y)

def move_move(event, window):
    if pressed:
        window.scan_dragto(event.x, event.y, gain=1)

def click_on_circle(event, window, id):
    window.itemconfig(id, fill='yellow')
    label = Label(window, text="(0,0)", font=(FONT_1, SIZE_1), justify = 'center', width = 100, bg ='blue')
    label.place(x=697, y=447)
    window.after(1000, in_focus(event, graph, id))

def recover_coord(table, list_of_x, list_of_y, low_board, x, y):
    temp_count = 0; exit_flag = False
    for i in range(len(list_of_x)):
        for j in range(len(list_of_x[i])):
            if temp_count == low_board:
                list_of_x[i].pop(j); list_of_y[i].pop(j)
                list_of_x[i].insert(j, x); list_of_y[i].insert(j, y)
                exit_flag = True
            temp_count += 1
        if exit_flag == True:
            break
	
    for record in table.get_children():
        table.delete(record)

    temp_count = 0
    for i in range(len(list_of_x)):
        for j in range(len(list_of_x[i])):
            table.insert('', 'end', 
                values=str(temp_count + 1)+"\t\t\t"+str(i + 1)+"\t\t\t"+str(list_of_x[i][j])+"\t\t\t"+str(list_of_y[i][j]))
            temp_count += 1

def recover_all(window, table, old_list_x, old_list_y, type_del):
    global list_of_x, list_of_y, count_polygones, old_count_polygones
    list_of_x = copy.deepcopy(old_list_x)
    list_of_y = copy.deepcopy(old_list_y)

    if type_del == 1:
        for record in table.get_children():
            table.delete(record)

    temp_count = 0
    for i in range(len(list_of_x)):
        for j in range(len(list_of_x[i])):
            table.insert('', 'end', 
                values=str(temp_count + 1)+"\t\t\t"+str(i + 1)+"\t\t\t"+str(list_of_x[i][j])+"\t\t\t"+str(list_of_y[i][j]))
            temp_count += 1
    count_polygones = copy.deepcopy(old_count_polygones)
    label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))
    label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)

def cancel_action(window, graph_window, table_window, result_window, table, old_location, old_x, old_y):
    global number_action, count_polygones
    if (number_action == 0):
        text = 'Еще не было выполнено ни одного действия.'
        box.showerror('Ошибка', text)
    #команда "новый многоугольник"
    elif (number_action == 1):
        list_of_x.pop(count_polygones - 1); list_of_y.pop(count_polygones - 1)
        count_polygones -= 1; number_action = 0
        label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))
        label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)
    #Команда "ввести координаты"
    elif (number_action == 2):
        delete_coordinate(window, number_coord, table, list_of_x, list_of_y, count_polygones, 2)
        number_action = 0
    #Команда "удалить координату"
    elif (number_action == 3):
        recover_all(window, table, old_list_x, old_list_y, 1)
        number_action = 0
    #Команда "Удалить всю таблицу"
    elif (number_action == 4):
        recover_all(window, table, old_list_x, old_list_y, 0)
        number_action = 0
    #Команда "Изменить координаты"
    elif (number_action == 5):
        recover_all(window, table, old_list_x, old_list_y, 1)
        number_action = 0

def create_coordinate_plane(graph):
    #отрисовка сетки и центра координат
    GRID_COUNT = 150
    SQUARE_SIZE = 25
    #ось х
    for j in range(-100, GRID_COUNT):
        graph.create_line(j*SQUARE_SIZE,-2500,j*SQUARE_SIZE,3725)
    #ось у
    for j in range(-100, GRID_COUNT):
        graph.create_line(-2500, j*SQUARE_SIZE, 3725,j*SQUARE_SIZE)
    
    #ось х
    graph.create_line(-2500, 375, 3725, 375, fill='red', width=3)

    #ось у
    graph.create_line(700, -2500, 700, 3725, fill='red', width=3)

    #центр координат
    center_x = SHIFT_X; center_y = SHIFT_Y
    oval_id = graph.create_oval(center_x, center_y, center_x + SHIFT_POINT, center_y + SHIFT_POINT, fill="#ff0000",
                                activefill="yellow")

#общая функция обработки
def main():
    window = Tk()
    window.title("Лабораторная работа №1")
    window.geometry('1920x920')

    #запрет на расширение экраан по горизонтали и вертикали
    window.resizable(width=True, height=True)

    #текстовое поле
    label_param = Label(text="Параметры", font=(FONT_1, SIZE_1))
    label_x = Label(text="x", font=(FONT_1, SIZE_1 + 2))
    label_y = Label(text="y", font=(FONT_1, SIZE_1 + 2))
    label_count_polygon = Label(text="Создано\nмногоугольников:", font=(FONT_1, SIZE_1), justify = 'left')
    label_input = Label(window, text=str(count_polygones), font=(FONT_1, SIZE_1))

    label_param.place(relx=0.74, rely=0.01, relheight=0.035, relwidth=0.09)
    label_x.place(relx=0.72, rely=0.05, relheight=0.035, relwidth=0.09)
    label_y.place(relx=0.72, rely=0.09, relheight=0.035, relwidth=0.09)
    label_count_polygon.place(relx=0.84, rely=0.0001, relheight=0.05, relwidth=0.15)
    label_input.place(relx=0.97, rely=0.025, relheight=0.025, relwidth=0.01)
    #переменные, принимающие введенные значения
    ep_x = StringVar()
    ep_y = StringVar()
    ep_number = StringVar()
    ep_number_polygon = StringVar()

    #текстовый ввод данных
    entry_x = Entry(window, width=20, font=(FONT_1, SIZE_1), textvariable=ep_x, bd=2)
    entry_y = Entry(window, width=20, font=(FONT_1, SIZE_1), textvariable=ep_y, bd=2)
    entry_count = Entry(window, width=10, font=(FONT_1, SIZE_1), textvariable=ep_number_polygon, bd=2)

    entry_x.place(relx=0.78, rely=0.05, relheight=0.035, relwidth=0.09)
    entry_y.place(relx=0.78, rely=0.09, relheight=0.035, relwidth=0.09)
    entry_count.place(relx=0.875, rely=0.05, relheight=0.035, relwidth=0.03)
    
    #Объединение нескольких виджетов
    table_frame = Frame(window, bg='white')
    graph_frame = Frame(window, bg='white')
    result_frame = Frame(window, bg='white')

    table_frame.place(relx=0.75, rely=0.21, relheight=0.70, relwidth=0.235)
    graph_frame.place(relx = 0.001, rely = 0.01, relheight = 0.83, relwidth = 0.745)
    result_frame.place(relx = 0.001, rely = 0.85, relheight = 0.15, relwidth = 0.745)

    #полосы прокрутки
    scroll_x_table = Scrollbar(table_frame, orient="horizontal")
    scroll_y_table = Scrollbar(table_frame, orient=VERTICAL)
 
    #создание координат на экране
    graph = Canvas(graph_frame, width=1400, height = 900, bg='white')

    scroll_x_graph = Scrollbar(graph_frame, orient="horizontal")
    scroll_y_graph = Scrollbar(graph_frame, orient="vertical")

    scroll_x_graph.pack(side=BOTTOM, fill=X)
    scroll_y_graph.pack(side=RIGHT, fill=Y)

    scroll_x_graph.config(command=graph.xview)
    scroll_y_graph.config(command=graph.yview)

    #координаты изменяются относительно graph_frame
    graph.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
    graph.config(xscrollcommand=scroll_x_graph.set, yscrollcommand=scroll_y_graph.set)

    create_coordinate_plane(graph)

    graph.bind("<B1-Motion>", lambda e, f=graph: move_move(e, f))
    graph.bind("<Button-1>", lambda e, f=graph: move_start(e, f))
    graph.bind("<Button-4>", lambda e, f=graph: zoom_more(e, f))
    graph.bind("<Button-5>", lambda e, f=graph: zoom_less(e, f))

    #таблица, выведенная на экран (содержит значения координат)
    table_columns = ("N", "polygon", "x", "y")
    table = ttk.Treeview(table_frame, show="headings", height = 55,
                         columns=table_columns, xscrollcommand=scroll_x_table.set, yscrollcommand=scroll_y_table.set)

    scroll_x_table.pack(side=BOTTOM, fill=X)
    scroll_y_table.pack(side=RIGHT, fill=Y)

    scroll_x_table.config(command=table.xview)
    scroll_y_table.config(command=table.yview)
    
    table["columns"]=("N", "polygon", "x","y")
    table.column("N", width=50, minwidth=50, stretch=NO,  anchor='center')
    table.column("polygon", width=80, minwidth=50, stretch=NO, anchor='center')
    table.column("x", width=150, minwidth=100, stretch=NO,  anchor='center')
    table.column("y", width=150, minwidth=100, stretch=NO,  anchor='center')
    table.heading("N", text=table_columns[0])
    table.heading("polygon", text=table_columns[1])
    table.heading("x", text=table_columns[2])
    table.heading("y", text=table_columns[3])
    table.pack()
    
    #результат - координаты точек
    result_canvas = Canvas(result_frame, width=1400, height = 900, bg='white')
    
    scroll_x_result = Scrollbar(result_frame, orient="horizontal")
    scroll_y_result = Scrollbar(result_frame, orient="vertical")
    scroll_x_result.pack(side=BOTTOM, fill=X)
    scroll_y_result.pack(side=RIGHT, fill=Y)
    scroll_x_result.config(command=result_canvas.xview)
    scroll_y_result.config(command=result_canvas.yview)

    result_canvas.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
    result_canvas.config(xscrollcommand=scroll_x_result.set, yscrollcommand=scroll_y_result.set)

    #кнопки
    button_new_polygon = Button(text="Новый\nмногоугольник", font=(FONT_1, SIZE_1), width=20, justify=CENTER,
                      command=lambda: start_input_new_polygone(window, list_of_x, list_of_y))
    button_input = Button(text="Ввести\nкоординаты", font=(FONT_1, SIZE_1), width=20, justify=CENTER,
                      command=lambda: input_coordinates(ep_x, ep_y, table, list_of_x, list_of_y, count_polygones))
    button_delete = Button(text="Удалить\nкоординату", font=(FONT_1, SIZE_1), width=10, justify=CENTER,
                      command=lambda: delete_coordinate(window, ep_number, table, list_of_x, list_of_y, count_polygones, 1))
    button_delete_all = Button(text="Удалить\nвсю таблицу", font=(FONT_1, SIZE_1), width=10, justify=CENTER,
                      command=lambda: delete_all(window, table))
    button_solution = Button(text="Найти\nрешение", font=(FONT_1, SIZE_1), width=10, justify=CENTER,
                      command=lambda: find_solution(graph, result_canvas, list_of_x, list_of_y, table, count_polygones))
    button_edit = Button(text="Изменить\nкоординату", font=(FONT_1, SIZE_1), width=20, justify=CENTER,
                      command=lambda: edit_coord(graph, table, ep_x, ep_y))
    button_add = Button(text="Добавить\nкоординату", font=(FONT_1, SIZE_1), width=20, justify=CENTER,
                      command=lambda: add_coord(graph, table, ep_x, ep_y, ep_number_polygon))
                      
    button_new_polygon.place(relx=0.75, rely=0.13, relheight=0.067, relwidth=0.075)
    button_edit.place(relx=0.83, rely=0.13, relheight=0.067, relwidth=0.075)
    button_input.place(relx=0.91, rely=0.13, relheight=0.067, relwidth=0.075)
    button_delete.place(relx=0.75, rely=0.915, relheight=0.067, relwidth=0.075)
    button_delete_all.place(relx=0.83, rely=0.915, relheight=0.067, relwidth=0.075)
    button_solution.place(relx=0.91, rely=0.915, relheight=0.067, relwidth=0.075)
    button_add.place(relx=0.91, rely=0.05, relheight=0.067, relwidth=0.075)

    #создание меню
    main_menu = Menu(window, font=(FONT_1, SIZE_1))
    file_menu = Menu(window, font=(FONT_1, SIZE_1), tearoff=0)
    window.config(menu=main_menu)
    main_menu.add_cascade(label='Файл', menu=file_menu)
    main_menu.add_command(label='Справка', command=print_info)
    file_menu.add_command(label='Отменить',
                          command=lambda: cancel_action(window, graph, table, result_canvas, table, old_location, old_x, old_y))

    window.mainloop()

if __name__ == "__main__":
	main()
