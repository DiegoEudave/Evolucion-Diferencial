import math
import random
import sys
import time

class evolucionDiferencial:
    def __init__(self, F, NP, CR, programas, rangoTiempo, maquinas, floor, maxTime, maxIters):
        self.F = F
        self.NP = NP
        self.CR = CR
        self.programas = programas
        self.rangoTiempo = rangoTiempo
        self.maquinas = maquinas
        self.floor = floor
        self.iters = 0
        self.maxIters = maxIters
        self.t_ini = time.time()
        self.t_fin = self.t_ini + 60 * maxTime
    
    def condicion_termino(self):
        if time.time() > self.t_fin:
            return False
        if self.iters <= self.maxIters:
            return True
        return False

    def inicializar(self):
        sol = []
        for n in range(self.NP):
            s = []
            for i in range(len(self.programas)):
                rdm = random.random()
                val = rdm * self.rangoTiempo * self.maquinas
                if self.floor == True:
                    s.append(math.floor(val))
                else:
                    s.append(val)
            sol.append(s)
        return sol
    
    def evaluar(self, sol):
        valor = self.evaluarTiempos(sol)
        return valor
    
    def evaluarProgramas(self, sol):
        considerados = self.considerados(sol)
        valor = 0
        for i in considerados:
            if i == True:
                valor += 1
        return -valor
    
    def evaluarTiempos(self, sol):
        considerados = self.considerados(sol)
        valor = 0
        for i in range(len(considerados)):
            if considerados[i] == True:
                valor += self.programas[i]
        return -valor

    def considerados(self, sol):        
        considerado = [True] * len(sol)
        for i in range(len(sol)):
            #Para cada tiempo en la solución, se comprueba que no choque con los anteriores ni los intervalos
            inicio_i = sol[i]
            final_i = sol[i] + self.programas[i]
            #Si está entre ejecuciones de máquinas se ignora
            for m in range(self.maquinas):
                limite = self.rangoTiempo * (m + 1)
                if inicio_i < limite  and final_i > limite:
                    considerado[i] = False
                    continue
            
            #Se verifica que no choque con los programas anteriores
            for j in range(i):
                if considerado[j] == True:
                    inicio_j = sol[j]
                    final_j = sol[j] + self.programas[j]
                    if not (final_i <= inicio_j or final_j <= inicio_i):
                        considerado[i] = False
                        considerado[j] = False
                        break
        return considerado
    
    
                

    def differentialEvolution(self):
        #Inicializar vectores
        
        sols = self.inicializar()
        self.iters = 0
        while(self.condicion_termino()):
            self.iters += 1
            for s in range(len(sols)):
                #print("Recombinando " + str(s))
                #Elige tres vectores al azar diferentes de s; a, b y c            
                indices = list(range(len(sols)))
                indices.remove(s)
                a_n = random.choice(indices)#"Base" vector
                indices.remove(a_n)
                b_n = random.choice(indices)
                indices.remove(b_n)
                c_n = random.choice(indices)
                a = sols[a_n]
                b = sols[a_n]
                c = sols[a_n]
                
                #Elegimos un índice al azar de la lista
                indices = list(range(len(self.programas)))
                R = random.choice(indices)                
                #Recombinamos
                nuevoVector = sols[s].copy()#Nueva solución candidato
                for i in range(len(nuevoVector)):
                    r = random.random()
                    if r < self.CR or i == R:
                        nuevoVector[i] = a[i] + self.F * (b[i] - c[i])
                        if self.floor == True:
                            nuevoVector[i] = math.floor(nuevoVector[i])
                    #En caso contrario permanece con el valor original de la base, es decir nuevaSol[i] = a[i]
                #Sustituimos si su evaluacion es menor o igual
                
                if self.evaluar(nuevoVector) <= self.evaluar(sols[s]):
                    sols[s] = nuevoVector
        mejorSol = sols[0]
        for s in sols:
            if self.evaluar(s) < self.evaluar(mejorSol):
                mejorSol = s
        return mejorSol