from collections import deque
import random
import copy
import sys
import loading_pc
import os


def move(new_list, from_, to):

    temp = new_list[from_].pop()
    for _i in range(0,4):
        if len(new_list[from_])>0 and abs(int(temp) - int(new_list[from_][-1]))<3 and len(new_list[to])<3:
            temp = new_list[from_].pop()
            new_list[to].append(temp)
    new_list[to].append(temp)
    return new_list

def possible_moves(table, boxes):
    pos=[]
    for i in range(0, boxes):
        for j in range(0, boxes):
            pos.append((i,j))
            
    possible = []
    for from_, to in pos:
        if (len(table[from_])>=1 and len(table[to])<4 and to != from_ 
        and (len(table[to]) == 0 or (abs(int(table[from_][-1]) - int(table[to][-1]))<3))
        and not (len(table[from_])==4 and len(set(table[from_]))==1)
        and not (len(set(table[from_]))==1 and len(table[to]) ==0)):
            possible.append((from_,to))
        
    return possible


def check_win(table):
    temp = []
    not_full =[]
    for i in table:
        temp.append(len(set(i)))
        if len(i)<4:
            not_full.append(i)
    if len(not_full)>2:
        return False
    for i in temp:
        if i>1:
            return False
    print(table)
    return True


def game_loop(agent, picture):

    table, boxes_position, boxes = loading_pc.load_transform_img(picture)
    print(len(boxes_position))

    answer = agent(table, boxes)
    return answer, boxes_position

def random_agent(table, boxes):

    k=5
    l=0
    while True:
        print(l)
        table_copy = copy.deepcopy(table)
        if l%1000 == 0:
            k+=1

        correct_moves = []
        for i in range(boxes*k):
            pmove = possible_moves(table_copy, boxes)
            if len(pmove) == 0:
                win = check_win(table_copy)
                if win:
                    return correct_moves
                else:
                    break
            x, y = random.choice(pmove)
            table_copy = move(table_copy, x, y)
            correct_moves.append((x,y))

        l+=1
        

if __name__ == '__main__':
    answer, boxes_position = game_loop(random_agent, 'level/screen.jpg')
    print('answer', answer)