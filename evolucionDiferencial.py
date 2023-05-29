import sys
import math
import ED

def main():
    if len(sys.argv) == 1:
        print("Uso: python evolucionDiferencial.py ENTRADA [F <valor F>] [NP <tamaño poblacion>] [CR <valor CR>] [enteros] [maxIters <máximas iteraciones>] [maxTime <duración máxima (minutos)>]") 
        return
    
    #Recibir entrada
    archivo = open(sys.argv[1], "r")
    string = archivo.read().split("\n")
    string1 = string[0].split()
    maquinas = int(string1[0])#Número de máquinas en que se divide
    rangoTiempo = int(string1[1])#Rango de tiempo para los programas
    programas = string[1]#Lista de duraciones de programas
    programas = programas[1:len(programas)-1]
    programas = programas.split(", ")
    for p in range(len(programas)):
        programas[p] = float(programas[p])
    
    #Valores default
    F = 0.9 #Differential weight. Valor en rango [0,2]
    NP = 10 * len(programas) #Tamaño de población, recomendado 10*tamaño de vector
    CR = 0.8  #Crossover probability. Valor en rango [0,1]
    floor = False
    maxIters = 1000000
    maxTime = float('inf')
    
    #Recibir parámetros
    for i in range(len(sys.argv)):
        match sys.argv[i]:
            case "F":
                F = float(sys.argv[i+1])
            case "NP":
                NP = float(sys.argv[i+1])
            case "CR":
                CR = float(sys.argv[i+1])
            case "enteros":
                floor = True
            case "maxIters":
                maxIters = float(sys.argv[i+1])
            case "maxTime":
                maxTime = float(sys.argv[i+1])
        
    ed = ED.evolucionDiferencial(F, NP, CR, programas, rangoTiempo, maquinas, floor, maxTime, maxIters)
    sol = ed.differentialEvolution()
    considerados = ed.considerados(sol)
    valor = ed.evaluar(sol)
    for t in range(len(sol)):
        if considerados[t] == False:
            sol[t] = "n/a"
    print("Solución: ")
    print(sol)
    print("Evaluación: " + str(valor))

if __name__ == "__main__":
    main()