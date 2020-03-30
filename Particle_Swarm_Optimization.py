# -+- coding: utf-8 -*-
import random
import math
import copy
import numpy as np

#評価関数
def eval_func(x):

    # 変数が設定の範囲内
    if (-1.5 <= x[0] <= 4) and (-3 <= x[1] <= 4):
        f = math.sin(x[0] + x[1]) + (x[0] - x[1])**2 - 1.5*x[0] + 2.5*x[1] + 1
        return np.round(f,4)
    
    else:
        x = [4,4]
        f = math.sin(x[0] + x[1]) + (x[0] - x[1])**2 - 1.5*x[0] + 2.5*x[1] + 1
        return np.round(f,4)

def geneticoptimize(Tim = 50, particle_n = 100, digit = 5, w = 0.5, r = 1):

    def PSO(x, v, p, g):

        new_X = [0 for i in range(2)]
        new_V = [0 for i in range(2)]

        # 位置更新
        new_X[0] = x[0] + v[0]
        new_X[1] = x[1] + v[1]
        
        # 速度更新
        c1 = random.SystemRandom().random()
        c2 = random.SystemRandom().random()

        new_V[0] = w*v[0] + c1*r*(p[0]-x[0]) + c2*r*(g[0]-x[0])
        new_V[1] = w*v[1] + c1*r*(p[1]-x[1]) + c2*r*(g[1]-x[1])

        return new_X, new_V

    # 遺伝子の初期化
    x = [ np.round([random.uniform(-1.5, 4),random.uniform(-3, 4)],digit) for i in range(particle_n)]
    v = [ [0,0] for i in range(particle_n)]

    personal_best_positions = copy.deepcopy(x)
    personal_best_scores=[eval_func(h) for h in x]
    best_particle = np.argmin(personal_best_scores)
    global_best_position = personal_best_positions[best_particle]

    #メインループ
    for t in range(Tim):

        for j in range(particle_n):

            p = personal_best_positions[j]
            new_X, new_V = PSO(x[j], v[j], p, global_best_position)
            
            v[j] = copy.deepcopy(new_V)

            score = eval_func(new_X)

            if score < personal_best_scores[j]:
                personal_best_scores[j] = score
                personal_best_positions[j] = copy.deepcopy(new_X)


    return list([min(personal_best_scores), global_best_position])
 
 
def main():
    ans = geneticoptimize()
    print("Ans:",ans)
 
if __name__ == '__main__':
    main()