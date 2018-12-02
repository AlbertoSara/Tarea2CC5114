# -*- coding: utf-8 -*-
#numpy 1.14.0
#matplotlib 2.1.2

import numpy as np
import matplotlib.pyplot as plt
import time

class Boardstate:
    def __init__(self, n):
        ##Para que se parezca más a un "arreglo" de genes, codificamos
        #el tablero como un arreglo, en que cada indice representa la fila
        #y el valor de la celda en dicho indice representa la columna
        #en la cual se encuentra la reina, de esa forma es muy facil controlar
        #la cantidad de reinas en el tablero
        self.n = n
        self.fit = None
        self.board = np.zeros(n)
        for i in range(n):
            self.board[i] = np.random.randint(n)
        
    def fitness(self):
        conflicting_queens = 0
        
        #Como todas las reinas estan en una fila unica, solo hay que
        #ver cuantas se repiten por columna
        
        for i in range(self.n):
            count = np.count_nonzero(self.board == i)
            if count > 0:
                count = count - 1
            conflicting_queens += count
        
        #Contamos los choques diagonales, para esto calculamos el offset
        #vertical y horizontal entre ambas reinas, si es igual signfica
        #que esta en posición diagonal
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    hor = abs(i-j)
                    ver = abs(self.board[i] - self.board[j])
                    if hor == ver:
                        conflicting_queens += 1
        self.fit = conflicting_queens
        #En este caso, mientras más cercano sea a 0 el resultado de la función,
        #más cercano esta a ser el óptimo
        return conflicting_queens

    def reproduce(self, mate, mutation_chance):
        a = np.random.randint(self.n)
        offspring = Boardstate(self.n)

        #se elige el punto donde se hace el crossover al azar
        offspring.board[0:a] = self.board[0:a]
        offspring.board[a:self.n] = mate.board[a:self.n]
        
        #se ve gen por gen si se realiza o no una mutación
        for i in range(self.n):
            if mutation_chance > np.random.random():
                offspring.board[i] = np.random.randint(self.n)
                
        return offspring
 

if __name__ == "__main__":

    population = 200
    board_size = 10
    mutation_rate = 0.15
    filename = "grafico.png"
    
    pop = []
    for i in range(population):
        pop.append(Boardstate(board_size))
    
    found = False
    generations = 0
    solutions = []
    best = []
    avg = []
    
    start = time.time()
    while not found:
        fitness_array = []
        
        for i in pop:
            fitness_array.append(i.fitness())
            
        fitness_array.sort()
        best.append(fitness_array[0])
        avg.append(sum(fitness_array)/population)
        threshold = fitness_array[int(population*.25)]
        mating_pool = []
        
        for i in pop:
            if i.fit <= threshold:
                mating_pool.append(i)
            if i.fit == 0:
                found = True
                solutions.append(i)
                
        pop = []
        for i in range(population):
            a = np.random.randint(len(mating_pool))
            b = np.random.randint(len(mating_pool))
            pop.append(mating_pool[a].reproduce(mating_pool[b], mutation_rate))
            
        generations += 1
        
    end = time.time()
    plt.plot(np.arange(len(best)), best, label="Mejor de cada generación")
    plt.plot(np.arange(len(avg)), avg, label="Promedio de cada generación")
    plt.xlabel("Generación")
    plt.ylabel("Número de reinas atacadas (fitness)")
    plt.title("Evolución de la población de soluciones para \n" \
              "el problema de N-Queens con n = " + str(board_size) + 
              ",\n probablidad de mutación: " + str(mutation_rate) +
              ", y población por generación de: " + str(population))
    
    plt.legend()
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    
    plt.show()
    plt.savefig(filename)
    print("\n")
    print("Generaciones totales: " + str(generations))
    print("Tiempo total: " + str(end-start))
    print("Posible solución:")
    print(solutions[0].board)