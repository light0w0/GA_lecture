# -+- coding: utf-8 -*-
import random #ランダムモジュール
import math
import copy
import numpy as np
 
def nimotu_init():
 
 omosa=np.array([9, #1
 7, #2
 8, #3
 2, #4
 10, #5
 7, #6
 7, #7
 8, #8
 5, #9
 4, #10
 7, #11
 5, #12
 7, #13
 5, #14
 9, #15
 9, #16
 9, #17
 8, #18
 8, #19
 2, #20
 7, #21
 7, #22
 9, #23
 8, #24
 4, #25
 7, #26
 3, #27
 9, #28
 7,   #29
 7,   #30
 9, #31
 5, #32
 10, #33
 7, #34
 10, #35
 10, #36
 7, #37
 10, #38
 10, #39
 10, #40
 3, #41
 8, #42
 3, #43
 4, #44
 2, #45
 2, #46
 5, #47
 3, #48
 9,   #49
 2   #50
 ])

 nedan=np.array([20,
 28, #2
 2, #3
 28, #4
 15, #5
 28, #6
 21, #7
 7, #8
 28, #9
 12, #10
 21, #11
 4, #12
 31, #13
 28, #14
 24, #15
 36, #16
 33, #17
 2, #18
 25, #19
 21, #20
 35, #21
 14, #22
 36, #23
 25, #24
 12, #25
 14, #26
 40, #27
 36, #28
 2,   #29
 28,   #30
 33, #31
 40, #32
 22, #33
 2, #34
 18, #35
 22, #36
 14, #37
 22, #38
 15, #39
 22, #40
 40, #41
 7, #42
 4, #43
 21, #44
 21, #45
 28, #46
 40, #47
 4, #48
 24,   #49
 21   #50
 ])

 return [omosa,nedan]
 
##評価関数
def eval_func(gean):
    omosa,nedan = nimotu_init()
##    gean = [0,0,1,0,1,1,1,0,1,1]
    vallue = sum(nedan * gean)
    weight = sum(omosa * gean)
    weightmax = 60
    if weight<= weightmax:
        return vallue
    else:
        vallue = int(vallue * 0.01)
        return vallue
 
def geneticoptimize(maxiter = 10000, maximize = True, popsize = 50, popnum = 50, elite = 0.2, mutprob =0.3):

    # 突然変異
    def mutate(vec):
        i = random.SystemRandom().randint(0,popnum-1)
        if vec[i] == 0:
            return vec[:i] + [1]+vec[i+1:]
        else:
            return vec[:i] + [0]+vec[i+1:]
     # 1点交叉 非推奨
    def one_point_crossover(r1,r2):
        i = random.SystemRandom().randint(1,popnum-2)
 
        return random.SystemRandom().choice((r1[0:i] + r2[i:], r2[0:i] + r1[i:]))
 
    # 2点交叉
    def two_point_crossover(r1,r2):
        i, j = sorted(random.SystemRandom().sample(range(popnum),2))
        return random.SystemRandom().choice((r1[0:i] + r2[i:j] + r1[j:] , r2[0:i] + r1[i:j] + r2[j:]))
 
    # 一様交叉
    def uniform_crossover(r1, r2):

        q1 = copy.copy(r1)
        q2 = copy.copy(r2)
        for i in range(len(r1)):
            if random.SystemRandom().random() < 0.5:
                q1[i], q2[i] = q2[i], q1[i]
 
        return random.SystemRandom().choice([q1,q2])
    #遺伝子の初期化
    pop = []
    for i in range(popsize):
        vec = [random.SystemRandom().randint(0,1) for i in range(popnum)]
        if i == 1 :
           vec= [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        #print(vec)
        pop.append(vec)
 
    # 交叉アルゴリズムの選択
    #crossover = two_point_crossover
    crossover = uniform_crossover
 
    #メインループ
    topelite = int(elite * popsize)
    for i in range(maxiter):
        scores=[(eval_func(v),v) for v in pop]
        scores.sort()
        if maximize:
            scores.reverse()
        ranked = [v for (s,v) in scores]
        # 弱い遺伝子は淘汰される
        pop = ranked[0:topelite]
        # 生き残った遺伝子同士で交叉したり突然変異したり
        while len(pop) < popsize:
            if random.SystemRandom().random() < mutprob:
                # 突然変異
                c = random.SystemRandom().randint(0,topelite)
                pop.append(mutate(ranked[c]))
 
            else:
                # 交叉
                c1 = random.SystemRandom().randint(0,topelite)
                c2 = random.SystemRandom().randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))
##        # 暫定の値を出力
        #print(scores[0][0])
        #print(scores[0])
        if i%1000 == 0:
             print(i)
    return scores[0]
 
 
def main():
    omosa,nedan = nimotu_init()
    ans = geneticoptimize()
    print("Ans:",ans)
 
if __name__ == '__main__':
    main()