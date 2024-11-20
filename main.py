import sys

#массив полосочек
already = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
)

#определяется чей сейчас ход
def sign(cnt):
    return 'X' if cnt % 2 == 0 else 'O'

#определяется какая фигура - соперник текущей
def ansign(char):
    return 'X' if char == 'O' else 'O'

#перебор
def bforce(field, cnt, to_add, we_won, amount, right_move):
    move = sign(cnt)
    anmove = ansign(move)
    #проверяем что мы уже выиграли
    for i in already:
        tmp = field[i[0] // 3][i[0] % 3] + field[i[1] // 3][i[1] % 3] + field[i[2] // 3][i[2] % 3]      #создаём строку-визуализацию полоски
        if tmp == anmove * 3:
            amount[to_add] += 1
            if anmove == right_move:
                we_won[to_add] += 1
            return
    #проверяем ситуацию на ничью
    if cnt == 9:
        amount[to_add] += 1
        we_won[to_add] += 1
        return
    #проверяем что мы можем одним ходом завершить партию
    for i in already:
        tmp = field[i[0] // 3][i[0] % 3] + field[i[1] // 3][i[1] % 3] + field[i[2] // 3][i[2] % 3]      #создаём строку-визуализацию полоски
        if tmp == '.' + move * 2:
            field[i[0] // 3] = field[i[0] // 3][:i[0] % 3] + move + field[i[0] // 3][i[0] % 3 + 1:]
            bforce(field, cnt + 1, to_add, we_won, amount, right_move)
            field[i[0] // 3] = field[i[0] // 3][:i[0] % 3] + '.' + field[i[0] // 3][i[0] % 3 + 1:]
            return
        elif tmp == move + '.' + move:
            field[i[1] // 3] = field[i[1] // 3][:i[1] % 3] + move + field[i[1] // 3][i[1] % 3 + 1:]
            bforce(field, cnt + 1, to_add, we_won, amount, right_move)
            field[i[1] // 3] = field[i[1] // 3][:i[1] % 3] + '.' + field[i[1] // 3][i[1] % 3 + 1:]
            return
        elif tmp == move * 2 + '.':
            field[i[2] // 3] = field[i[2] // 3][:i[2] % 3] + move + field[i[2] // 3][i[2] % 3 + 1:]
            bforce(field, cnt + 1, to_add, we_won, amount, right_move)
            field[i[2] // 3] = field[i[2] // 3][:i[2] % 3] + '.' + field[i[2] // 3][i[2] % 3 + 1:]
            return
    #ничего не нашли и расставляем фишки дальше перебирая все пустые клетки
    for i in range(3):
        for j in range(3):
            if field[i][j] == '.':
                field[i] = field[i][:j] + move + field[i][j + 1:]       #на место каждой пустой ячейки по очереди подставляем фишку
                bforce(field, cnt + 1, to_add, we_won, amount, right_move)       #запускаемся от получившегося поля рекурсивно
                field[i] = field[i][:j] + '.' + field[i][j + 1:]        #удаляем фишку

while 1:
    print("Введите поле для крестиков-ноликов без пробелов в следующем формате:")        #инструкции для пользователя
    print("X - крестик")
    print("O - нолик")
    print(". - пустое пространство")
    print("Поле для ввода должно быть 3x3. Пример:\nXO.\nOX.\n...")
    print("-------------")
    field = [""] * 3
    cnt = 0
    cnt_x, cnt_o = 0, 0
    #вводим поле и считаем количество крестиков и ноликов (как вместе так и по-отдельности)
    for i in range(3):
        field[i] = input()
        for j in range(3):
            if field[i][j] != '.':
                cnt += 1
                if field[i][j] == 'X':
                    cnt_x += 1
                else:
                    cnt_o += 1
    print("-------------")
    if cnt_o > cnt_x or abs(cnt_x - cnt_o) >= 2:
        print('\033[91m' + "Неверный формат ввода. Количество крестиков и ноликов не соответствует правилам.")
        print("Программа завершается для повторения." + '\033[0m')
        print("-----------------------")
        continue
    move = sign(cnt)
    anmove = ansign(move)
    #определяем не закончена ли уже партия на момент ввода
    flag = True
    if cnt == 9:
        print("Партия уже закончена. Дальнейшие ходы делать невозможно.")
        flag = False
    if not flag:
        break
    for i in already:
        tmp = field[i[0] // 3][i[0] % 3] + field[i[1] // 3][i[1] % 3] + field[i[2] // 3][i[2] % 3]      #создаём строку-визуализацию полоски
        if tmp == move * 3 or tmp == anmove * 3:
            print("Партия уже закончена. Дальнейшие ходы делать невозможно.")
            flag = False
            break
    if not flag:
        break
    #проверяем можно ли за один ход победить
    for i in already:
        tmp = field[i[0] // 3][i[0] % 3] + field[i[1] // 3][i[1] % 3] + field[i[2] // 3][i[2] % 3]      #создаём строку-визуализацию полоски
        if tmp == '.' + move * 2:
            field[i[0] // 3] = field[i[0] // 3][:i[0] % 3] + move + field[i[0] // 3][i[0] % 3 + 1:]      #ставим фишку
            print(*field, sep='\n')        #вывод
            flag = False
            break
        elif tmp == move + '.' + move:
            field[i[1] // 3] = field[i[1] // 3][:i[1] % 3] + move + field[i[1] // 3][i[1] % 3 + 1:]      #ставим фишку
            print(*field, sep='\n')        #вывод
            flag = False
            break
        elif tmp == move * 2 + '.':
            field[i[2] // 3] = field[i[2] // 3][:i[2] % 3] + move + field[i[2] // 3][i[2] % 3 + 1:]      #ставим фишку
            print(*field, sep='\n')        #вывод
            flag = False
            break
    if not flag:
        break
    #создаём 2 словаря где ключ и значение - номер ячейки и количество партий
    we_won = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}       #количество партий где мы победили
    amount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}       #количество партий в целом
    #запускаем перебор всех вариантов
    for i in range(3):
        for j in range(3):
            if field[i][j] == '.':
                field[i] = field[i][:j] + move + field[i][j + 1:]       #на место каждой пустой ячейки по очереди подставляем фишку
                bforce(field, cnt + 1, i * 3 + j, we_won, amount, move)       #запускаемся от получившегося поля рекурсивно
                field[i] = field[i][:j] + '.' + field[i][j + 1:]        #удаляем фишку
    #выбираем самый наилучший результат
    ans_i, ans_j = -1, -1
    for i in range(3):
        for j in range(3):
            if field[i][j] != '.':
                continue
            if ans_i == -1 and ans_j == -1 or we_won[i * 3 + j] / amount[i * 3 + j] > we_won[ans_i * 3 + ans_j] / amount[ans_i * 3 + ans_j]:        #сравниваем вероятности не проигрыша
                ans_i = i
                ans_j = j
    field[ans_i] = field[ans_i][:ans_j] + move + field[ans_i][ans_j + 1:]
    #вывод ответа
    print(*field, sep='\n')
    break
input("\nНажмите на Enter для выхода")
