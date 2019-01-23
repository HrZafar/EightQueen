import random


def insertionSort(alist):
    for i in range(1, len(alist)):
        key = alist[i]
        j = i - 1
        while j >= 0 and key['fitness'] > alist[j]['fitness']:
            alist[j + 1] = alist[j]
            j -= 1
        alist[j + 1] = key
    return alist


def fitness(x):
    fitness = 0
    board = x
    for i in range(len(board)):
        check = True
        j = 1
        while i + j < len(board) and check == True:
            if board[i + j] == board[i] + j:
                check = False
            j += 1
        j = 1
        while i - j > -1 and check == True:
            if board[i - j] == board[i] + j:
                check = False
            j += 1
        j = 1
        while i + j < len(board) and check == True:
            if board[i + j] == board[i] - j:
                check = False
            j += 1
        j = 1
        while i - j > -1 and check == True:
            if board[i - j] == board[i] - j:
                check = False
            j += 1
        if check == True:
            fitness += 1
    return fitness


def gen_individuals(n, b):
    list = []
    for i in range(b):
        dict = {}
        list1 = random.sample(range(0, n), n)
        dict['board'] = list1
        dict['fitness'] = fitness(list1)
        list.append(dict)
    return list


def select_boards(n):
    p1 = random.randint(0, n - 1)
    p2 = random.randint(0, n - 1)
    while p1 == p2:
        p2 = random.randint(0, n - 1)
    return p1, p2


def mutation(child):
    probability = random.randint(1, 100)
    if probability > 25:
        a, b = select_boards(len(child))
        temp = child[a]
        child[a] = child[b]
        child[b] = temp
    return child


def crossover(list, p1, p2):
    ch = []
    child = {}
    for i in range(round(len(list[p1]['board']) / 2)):
        ch.append(list[p1]['board'][i])
    j = i + 1
    while i < len(list[p2]['board']) - 1:
        k = 0
        while k < len(ch):
            if list[p2]['board'][j] == ch[k]:
                j += 1
                k = 0
                if j == len(list[p2]['board']):
                    j = 0
            else:
                k += 1
        if k == len(ch):
            ch.append(list[p2]['board'][j])
            i += 1
    ch = mutation(ch)
    child['board'] = ch
    child['fitness'] = fitness(ch)
    return child


def gen_childs(list, p1, p2):
    return crossover(list, p1, p2), crossover(list, p2, p1)


file = open('max_fitness.txt', 'a')
check = False
generations = 0
solution = []
n = 8
boards = 25
child_boards = 20
childs = []
generation = gen_individuals(n, boards)
i = 0
while check == False and i < len(generation):
    if generation[i]['fitness'] == n:
        check = True
        solution = generation[i]['board']
    i += 1
while check == False and generations < 200:
    generations += 1
    for j in range(int(child_boards / 2)):
        board1, board2 = select_boards(boards)
        childs.extend(gen_childs(generation, board1, board2))
    generation_1 = generation + childs
    generation_1 = insertionSort(generation_1)
    for k in range(len(generation)):
        generation[k] = generation_1[k]
        # print(generations, generation[k]['fitness'], generation[k])
        if generation[k]['fitness'] == n:
            check = True
            solution = generation[k]['board']
if generations == 200:
    generations = ''
    solution = ''
file.write('n=')
file.write(str(n))
file.write('; iterations=')
file.write(str(generations))
file.write('; solution=')
file.write(str(solution))
file.write("\n")
file.close()
