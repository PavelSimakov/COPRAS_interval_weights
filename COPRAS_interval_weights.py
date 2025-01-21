import tkinter as tk
from tkinter import ttk
from pathlib import *
from tkinter.messagebox import showinfo

import numpy as np
import pandas as pd

import itertools
from tabulate import tabulate

index_matrix_DMM = []
index_matrix_WDMM = []
index_matrix_qualities = []


def enter_weights(window):
    window.grab_release()
    window.destroy()
    weights_decision_making_matrices()


def bring_best_alternatives(window):
    window.grab_release()
    window.destroy()
    monte_carlo_method()


def change_number_columns():
    # Обновление метки, чтобы отобразить выбранное значение
    value_label_for_columns.config(text="Выбрано критериев: " + spinbox_for_columns.get())


def change_number_rows():
    # Обновление метки, чтобы отобразить выбранное значение
    value_label_for_rows.config(text="Выбрано альтернатив: " + spinbox_for_rows.get())


def decision_making_matrices():
    columns = int(spinbox_for_columns.get())
    rows = int(spinbox_for_rows.get())

    window_DMM = tk.Toplevel()
    window_DMM.title("Матрица принятия решений")
    if columns <= 3 and rows <= 3:
        window_DMM.geometry('450x85')
    elif columns >= 7 and rows >= 7:
        window_DMM.geometry(str(columns * 95) + 'x' + str(rows * 25))
    elif columns == rows:
        window_DMM.geometry(str(columns * 109 + 60) + 'x' + str(rows * 25))
    else:
        window_DMM.geometry(str(columns * columns + 810) + 'x' + str(rows * rows + 140))
    window_DMM.iconbitmap(Path.cwd() / '4.ico')
    window_DMM.grab_set()  # захватываем пользовательский ввод

    # Создаю индекс для каждой переменной в массиве
    entries = []

    for i in range(columns):
        index_matrix_DMM.append([])
        entries.append([])
        for j in range(rows):
            index_matrix_DMM[i].append(tk.StringVar())
            entries[i].append(tk.Entry(window_DMM, textvariable=index_matrix_DMM[i][j], width=7))
            entries[i][j].place(x=i * 50, y=j * 23)

    lbl_DMM = tk.Label(window_DMM, text="Введите элементы матрицы принятия решений")
    lbl_DMM.place(x=columns * 55, y=rows * 8)

    btn_DMM = tk.Button(window_DMM, text="Ввести веса принятия решений", command=lambda: enter_weights(window_DMM))
    btn_DMM.place(x=columns * 55, y=(rows * 8) + 30)


def weights_decision_making_matrices():
    columns = int(spinbox_for_columns.get())

    window_WDMM = tk.Toplevel()
    window_WDMM.title("Веса матрицы принятия решений")
    if columns <= 3:
        window_WDMM.geometry('750x85')
    elif columns >= 5:
        window_WDMM.geometry(str((columns * columns * 3) + 850) + 'x' + str(85))
    else:
        window_WDMM.geometry(str(columns * 210) + 'x' + str(85))
    window_WDMM.iconbitmap(Path.cwd() / '1.ico')
    window_WDMM.grab_set()  # захватываем пользовательский ввод

    # Создаю индекс для каждой переменной в массиве
    entries = []

    # Положительные и отрицательные качества
    positive_negative_qualities = []

    for i in range(columns):
        index_matrix_WDMM.append([])
        index_matrix_WDMM[i].append(tk.StringVar())
        entries.append([])
        entries[i].append(tk.Entry(window_WDMM, textvariable=index_matrix_WDMM[i], width=7))
        entries[i][0].place(x=i * 50, y=0)

        index_matrix_qualities.append([])
        index_matrix_qualities[i].append(tk.StringVar())
        positive_negative_qualities.append([])
        positive_negative_qualities[i].append(tk.Entry(window_WDMM, textvariable=index_matrix_qualities[i], width=7))
        positive_negative_qualities[i][0].place(x=i * 50, y=20)

    lbl_WDMM = tk.Label(window_WDMM, text="Введите диапазон веса для каждого критерия через : (Пример- 4:6)")
    lbl_WDMM.place(x=columns * 55, y=0)

    lbl_qualities = tk.Label(window_WDMM, text="Под каждым критерием укажите его нужно максимизировать 1 "
                                               "или минимизировать -1")
    lbl_qualities.place(x=columns * 55, y=20)

    btn_WDMM = tk.Button(window_WDMM, text="Вывести лучшие альтернативы",
                         command=lambda: bring_best_alternatives(window_WDMM))
    btn_WDMM.place(x=columns * 55, y=50)


def normalize_matrix(decision_matrix):
    return decision_matrix / decision_matrix.sum(axis=0)


def weighted_normalized_matrix(normalized_matrix, weights):
    return normalized_matrix * weights


def calculate_sums(weighted_matrix, beneficial_criteria, non_beneficial_criteria):
    S_plus = weighted_matrix[:, beneficial_criteria].sum(axis=1)  # Sum for beneficial criteria
    S_minus = weighted_matrix[:, non_beneficial_criteria].sum(axis=1)  # Sum for non-beneficial criteria

    return S_plus, S_minus


def calculate_utility(S_plus, S_minus, S_minus_min):
    Q = S_plus + ((np.sum(S_minus))/(S_minus * np.sum(1 / S_minus)))

    return Q / np.max(Q)


def method_COPRAS(matrix, weights, types):
    # Шаг 1: Нормализация матрицы принятия решений
    normalized_matrix = normalize_matrix(matrix)

    # Шаг 2: Применение весов к нормализованной матрице принятия решений
    weighted_matrix = weighted_normalized_matrix(normalized_matrix, weights)

    # Шаг 3: Определение положительных и отрицательных критериев
    beneficial_criteria = [i for i, t in enumerate(types) if t == 1]
    non_beneficial_criteria = [i for i, t in enumerate(types) if t == -1]

    # Шаг 4: Расчет суммы S+ (положительные) и S- (отрицательные)
    S_plus, S_minus = calculate_sums(weighted_matrix, beneficial_criteria, non_beneficial_criteria)

    # Шаг 5: Вычисление минимального значения S- (для отрицательных критериев)
    S_minus_min = S_minus.min()

    # Шаг 6: Рассчитайте относительную значимость (полезность) каждой альтернативы.
    N = calculate_utility(S_plus, S_minus, S_minus_min)

    # Ранжирование альтернатив в соответствии с убывающими значениями оценочного балла (N).
    ind = np.arange(1, np.shape(matrix)[0] + 1)
    s = pd.Series(N, index=ind)

    # Альтернатива с наивысшим N - лучший выбор среди возможных альтернатив.
    sorted_df = s.sort_values(ascending=False)

    return sorted_df


def monte_carlo_method():
    AS = []
    columns = int(spinbox_for_columns.get())
    rows = int(spinbox_for_rows.get())

    number_repetitive_iterations = 5
    number_alternatives_compared = 3

    AS_previous = []
    for i in range(number_alternatives_compared + 1):
        AS_previous.append(5)

    assessments_COPRAS = np.array([[]])

    # Интервальные веса
    interval_weights = []
    cartesian_product_interval_weights = []

    iteration = number_iterations.get()
    if iteration == "Auto":
        iteration = 8
        # Включаю проверку
        number_repetitive_solutions = 0
    else:
        iteration = int(number_iterations.get())
        # Выключаю проверку
        number_repetitive_solutions = number_repetitive_iterations * 2

    for w in range(columns):
        temporary_i_w = []
        for w1 in np.random.uniform(float(index_matrix_WDMM[w][0].get().split(":")[0]),
                                    float(index_matrix_WDMM[w][0].get().split(":")[1]), iteration):
            temporary_i_w.append(w1)
        interval_weights.append(temporary_i_w)

    # Декартово произведение
    for element in itertools.product(*interval_weights):
        cartesian_product_interval_weights.append(element)

    cartesian_product_interval_weights = np.array(cartesian_product_interval_weights)

    # Одномерный массив преобразуй в двумерный
    cartesian_product_interval_weights = np.reshape(cartesian_product_interval_weights, (-1, columns))


    # Построение матрицы принятия решений
    matrix = []

    for r in range(rows):
        matrix.append([])
        for c in range(columns):
            matrix[r].append(float(index_matrix_DMM[c][r].get()))

    matrix = np.array(matrix)


    # Положительные и отрицательные качества
    types = []

    for t in range(columns):
        types.append(int(index_matrix_qualities[t][0].get()))

    types = np.array(types)


    for i in np.arange(len(cartesian_product_interval_weights)):

        # Остановка для итераций, при выборе Auto
        if number_repetitive_solutions != number_repetitive_iterations:

            AS_temporary = []
            AS_previous_temporary = []

            # Вес критерия
            weights = cartesian_product_interval_weights[i]

            AS = method_COPRAS(matrix, weights, types)

            if len(AS) >= number_alternatives_compared and len(AS_previous) >= number_alternatives_compared:
                for a in np.arange(1, number_alternatives_compared + 1):
                    AS_temporary.append(float("{:.5f}".format(AS[a])))
                    AS_previous_temporary.append(float("{:.5f}".format(AS_previous[a])))

                if AS_temporary == AS_previous_temporary:
                    number_repetitive_solutions += 1

            AS_previous = AS

            # Лучшая альтернатива
            assessments_COPRAS = np.append(assessments_COPRAS, [[AS[AS == AS.max()].index]])

        assessments_COPRAS_count = np.unique(assessments_COPRAS, return_counts=True)

    # Отображение результата
    alternative = np.array([[]])
    estimation = np.array([[]])

    for i in range(len(AS[assessments_COPRAS_count[0]])):
        alternative = np.append(alternative, assessments_COPRAS_count[0][i])
        estimation = np.append(estimation, assessments_COPRAS_count[1][i] / cartesian_product_interval_weights.shape[0])

    solution = pd.DataFrame({'alternative': alternative, 'estimation': list(estimation)},
                            columns=['alternative', 'estimation'])
    solution = solution.sort_values(by='estimation', ascending=False)

    if len(solution) == 1:
        showinfo(title="Сильное решение", message=tabulate(solution, headers='keys', tablefmt='presto'))
    else:
        showinfo(title="Лучшие альтернативы", message=tabulate(solution, headers='keys', tablefmt='presto'))


# Начало программы (Start of the program)

main_window = tk.Tk()
main_window.title("COPRAS с интервальными весами")
main_window.geometry('400x185')
main_window.iconbitmap(Path.cwd() / '2.ico')

lbl = tk.Label(main_window, text="Размер матрицы принятия решений")
lbl.pack()

spinbox_for_columns = ttk.Spinbox(main_window, from_=1, to=10, command=change_number_columns)
spinbox_for_columns.place(x=80, y=40, width=40)
spinbox_for_columns.insert(1, "1")

value_label_for_columns = tk.Label(main_window, text="Выбрано критериев: 1")
value_label_for_columns.place(x=200, y=40)

spinbox_for_rows = ttk.Spinbox(main_window, from_=1, to=10, command=change_number_rows)
spinbox_for_rows.place(x=80, y=70, width=40)
spinbox_for_rows.insert(1, "1")

value_label_for_rows = tk.Label(main_window, text="Выбрано альтернатив: 1")
value_label_for_rows.place(x=200, y=70)

btn = tk.Button(main_window, text="Ввести значение матрицы принятия решений", command=decision_making_matrices)
btn.place(x=73, y=110)

languages = ["Auto", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
number_iterations = tk.StringVar()

lbl_number_iterations = tk.Label(main_window, text="Количество итераций")
lbl_number_iterations.place(x=10, y=150)

spinbox = ttk.Spinbox(textvariable=number_iterations, values=languages)
spinbox.place(x=168, y=150, width=50)
number_iterations.set("Auto")

main_window.mainloop()
