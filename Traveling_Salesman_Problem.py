# -+- coding: utf-8 -*-
# 巡回セールスマン問題

import random
import math
import numpy as np
import csv
import copy
import time

from tkinter import *

maxiter = 5000
popsize = 400
elite = 0.1
mutprob =0.3

# データ読み込み
def read_data():

    # 座標を格納
    place = []
    # 都市番号を格納
    num = []

    for l in open('bays29.csv').readlines():
        data = l[:-1].split(',')

        vec = []
        vec.extend([int(data[1]),int(data[2])])

        place.append(vec)
        num.append(int(data[0]))
    
    return place,num

#評価関数
def eval_func(path, x):

    euclid = 0

    for i in range(len(x)-1):

        dx = x[path[i]-1][0] - x[path[i+1]-1][0]
        dy = x[path[i]-1][1] - x[path[i+1]-1][1]

        euclid += math.sqrt( dx*dx + dy*dy )

    dx = x[path[0]-1][0] - x[path[-1]-1][0]
    dy = x[path[0]-1][1] - x[path[-1]-1][1]

    euclid += math.sqrt( dx*dx + dy*dy )

    return np.round(euclid,1)


# 突然変異
def mutate(r1):

    i = 0

    # ランダムに2点を入れ替え
    while i < mutprob*len(r1):
        p,q = sorted(random.SystemRandom().sample(range(len(r1)),2))
        r1[p],r1[q] = r1[q],r1[p]

        i += 1

    return r1

# 交叉
def PMX(r1, r2):

    # 交叉する2点
    p,q = sorted(random.SystemRandom().sample(range(len(r1)),2))

    # 子にコピー
    c1 = copy.deepcopy(r1)
    c2 = copy.deepcopy(r2)

    # 入れ替え
    while p <= q:

        if c1[p] != r2[p]:
            num1 = c1.index(r2[p])
            c1[p],c1[num1] = c1[num1],c1[p]
            
        if c2[p] != r1[p]:
            num2 = c2.index(r1[p])
            c2[p],c2[num2] = c2[num2],c2[p]

        p += 1

    return c1,c2


# ルーレット選択
def Roulette(f):

    seed = []

    rec = np.reciprocal(np.array(f))
    prob = rec/sum(rec)
        
    while len(seed) < popsize:
        ran = np.random.uniform(0,1)

        for j in range(popsize):
            ran = ran - (prob[j])

            if ran < 0 :
                seed.append(j)
                break

    return seed

 
def main():

    # 遺伝子の初期化
    x = []
    city_d,path = read_data()

    # 画面描画
    POINT_SIZE = 10
    waru = 4
    root = Tk()
    c0 = Canvas(root, width = 1000, height = 700)

    for point in city_d:
        c0.create_oval((point[0]-POINT_SIZE)/waru, (point[1]-POINT_SIZE)/waru
        ,(point[0]+POINT_SIZE)/waru, (point[1]+POINT_SIZE)/waru, fill = "red")
        

    while len(x) < popsize:

        random.shuffle(path)
        x.append(copy.deepcopy(path))

    # 交叉アルゴリズムの選択
    crossover = PMX

    # エリート保存の個数
    topelite = int(elite * popsize)

    scores=[(eval_func(v, city_d),v) for v in x] 
    scores.sort()

    #メインループ
    for i in range(maxiter):

        ranked = [v for (f,v) in scores]
        vallue = [f for (f,v) in scores]

        # ルーレット選択
        a = Roulette(vallue)
        parents = [ranked[i] for i in a]

        # エリート保存
        x = copy.deepcopy(ranked[0:topelite])

        # 次世代の個体
        while len(x) < popsize:

            # 突然変異
            if random.SystemRandom().random() < mutprob:
                c = random.SystemRandom().randint(0,popsize-1)
                x.append(mutate(parents[c]))

            # 交叉 
            else:
                c1 = random.SystemRandom().randint(0,popsize-1)
                c2 = random.SystemRandom().randint(0,popsize-1)
                x1,x2 = crossover(parents[c1],parents[c2])
                x.extend([x1, x2])

        # 評価値と変数(path)の格納
        scores=[(eval_func(v, city_d),v) for v in x] 
        scores.sort()

        time.sleep(0)
        #経路情報を画面に出力
        c0.create_text(200, 10, text = str(i)+'世代目 総距離：' + str(scores[0][0]),font = ('FixedSys', 10),tags='lines')
        c0.create_text(500, 30, text = str(scores[0][1]),font = ('FixedSys', 10),tags='lines')
     
        #経路を画面に出力
        for k in range(len(path)-1):
            c0.create_line(city_d[x[0][k]-1][0]/waru, city_d[x[0][k]-1][1]/waru
            ,city_d[x[0][k+1]-1][0]/waru, city_d[x[0][k+1]-1][1]/waru,tags='lines')
         
        c0.create_line(
            city_d[p_path[0][-1]][0],city_d[p_path[0][-1]][1]
            ,city_d[p_path[0][0]][0],city_d[p_path[0][0]][1],tags='lines')
        
        if i < maxiter-1:
            c0.pack()
            c0.update()
            c0.delete('lines')


    
    print("Answer:",scores[0])
    root.mainloop()

if __name__ == '__main__':
    main()