# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 16:36:27 2020

@author: 054309 GONZALEZ NOVELO IVAN ALI TONATIUH 
"""

import numpy as np
import pandas as pd

PC=888
HUMANO=999

COLORPC='\x1b[0;47m'
COLORHUMANO='\x1b[0;46m'
COLORVACIO='\x1b[0;39m'


class cola:
    def __init__(self, capacidad=100):
        self.__datos=[]
        self.capacidad=capacidad
        
    def enqueue(self,n):
        if self.count()<self.capacidad:
            self.__datos.insert(0,n)
            
    def dequeue(self):
        return self.__datos.pop()
    
    def count(self):
        return len(self.__datos)
    
    def empty(self):
        return self.count()==0
    
    def print(self):
        for i in range(self.count()-1,-1,-1):
            print(self.__datos[i])

def casilla_existe(destino,origen,N,horizontal):
    if destino <0:
        return False
    
    if horizontal:
        if destino//N != origen//N: #evalua tanto si sale por izq o por derecha
            return False
            
    
    if destino>15:
        return False
    return True

def casilla_virgen(destino,tablero):
    if tablero[destino]==PC or tablero[destino]==HUMANO:
        return False
    
    return True

def casilla_enelarbol(destino,usados):
    if destino in usados:
        return True
    return False

def movimiento_valido(destino, origen, tablero, usados, N,horizontal):
    
    
    if not casilla_existe(destino,origen,N,horizontal):
        return False
    if not casilla_virgen(destino,tablero):
        return False
    if not casilla_enelarbol(destino,usados):
        return True
    return False

    
            

def arma_el_arbol(actualtab,pos,usados):
    valor=actualtab[pos]
    
    nodo=Nodo(valor,pos)
    copia_usados=usados.copy()
    copia_usados.append(pos)
        
        
    norte=pos-N
    
    if movimiento_valido(norte, pos,actualtab,copia_usados,N,False):
        
        hijo_norte=arma_el_arbol(actualtab,norte,copia_usados)
        
        nodo.hijos.append(hijo_norte)
    
    este = pos+1
    
    if movimiento_valido(este, pos, actualtab, copia_usados, N,True):
       
        hijo_este=arma_el_arbol(actualtab,este,copia_usados)
        
        nodo.hijos.append(hijo_este)
        
    sur= pos+N
    
 
    if movimiento_valido(sur, pos, actualtab, copia_usados, N,False):
        
       
        hijo_sur=arma_el_arbol(actualtab,sur,copia_usados)
        
        nodo.hijos.append(hijo_sur)
    
    oeste= pos-1
    
    if movimiento_valido(oeste, pos, actualtab, copia_usados, N,True):
        
        hijo_oeste=arma_el_arbol(actualtab,oeste,copia_usados)
        
        nodo.hijos.append(hijo_oeste)
       
             
    return nodo

    
       
         
      
    
    
    

class Nodo:
    def __init__(self, n=0,i=0):
        self.dato=n
        self.indice=i
        self.hijos=[] #lista como referencia

    def imprimir(self):
       print(self.dato)
       
       for hijo in self.hijos:
           hijo.imprimir()
           
    def tiene_hijos(self):
        return len(self.hijos) > 0
    
    def alpha_beta(self, profundidad,alpha=-100, beta=100,Max=True):
        
        if profundidad==1 or not self.tiene_hijos():
            return (self.dato,0)
        
        seleccionado=None
            
        if Max==True:
            
            valor=-100
                        
            for hijo in self.hijos:
                aux,_=hijo.alpha_beta(profundidad-1, alpha,beta,not Max)
                if aux > valor:
                    valor=aux
                    seleccionado=hijo
                    
                
                alpha= max(alpha,valor)
                
                if alpha > beta:
                    print('he recortado')
                    break
                
            return (valor, seleccionado) 
        
        else:
            
            valor=100
            
                        
            for hijo in self.hijos:
                aux,_=hijo.alpha_beta(profundidad-1, alpha,beta,not Max)
                if aux < valor:
                    valor=aux
                    seleccionado=hijo
                    
                beta= min(beta,valor)
                
                if beta < alpha:
                    print('he recortado')
                    break
                
            return (valor, seleccionado) 
        
            
         
            
            

#Esta seccion es la inicializacion del tablero.
#El usuario no puede cambiar ni el tamagno del tablero ni la profundidad, pero se cambian al gusto en esta parte del codigo
   
#N=input('Cuanto de N deseas?')    
N=4
print('Juegas con un tablero de ', N, 'por ',N)
N=int(N)
profundidad=900

seteo=np.random.randint(1,2*N+1)

i=0
tablero=[]

while i < (N*N):
    seteo=np.random.randint(1,2*N+1)
     
    tablero.append(seteo)
    i+=1
    
    
tab=np.array(tablero).reshape(N,N)

print('NESO se llama mi version del juego, porque en cada turno eliges si moverte:')
print('Norte -> N, Este -> E, S -> Sur o O -> Oeste')
print('Bienvenido a NESO, el tablero se ve asi:')
print(tab)


#Aqui tenemos las funciones principales del juego. Son metodos independientes al nodo, a la cola o a cualquier clase.


def jugador_puede_mover(tablero,pos):
 #   NOT (nodo que me returneo armaelarbol, ya no tiene hijos, es decir, su lista de hijos esta empty)
    nodo=arma_el_arbol(tablero,pos,[])
       
    
    return nodo.tiene_hijos()
    

def elegir_casilla(tablero,pos,turnomaquina):
    
    if turnomaquina:
        print('Este es un turno maquina')
        
        #Cuando estamos en turno maquina, se arba el arbol y con alphabeta - minimax se elige el mejor camino.
        
        nodo=arma_el_arbol(tablero,pos,[])
        _,maquinaeligio=nodo.alpha_beta(profundidad)
        
        #alpha beta devuelve una tupla integrada por el nodo y el indice
        
        return maquinaeligio.indice
    
               
       
    
    if turnomaquina==False:
        print('Este es un turno humano')
        respuesta=input('Vas a mover N-E-S-O ?????')
        
        
        if respuesta=='N' or respuesta=='n':
            norte=pos-N
            if movimiento_valido(norte, pos, tablero, [], N, False):
                return norte
            
            
            
        if respuesta=='E' or respuesta=='e':
            este=pos+1
            if movimiento_valido(este, pos, tablero, [], N, True):
                return este
            
        if respuesta=='S' or respuesta=='s':
            sur=pos+N
            if movimiento_valido(sur, pos, tablero, [], N, False):
                return sur
           
        
        if respuesta=='O' or respuesta=='o':
            oeste=pos-1
            if movimiento_valido(oeste, pos, tablero, [], N, True):
                return oeste
        
    print('\x1b[0;39m')
    print('WRONG!!! metiste mal el valor, pierdes turno')
    print('\x1b[0;42m')
    return pos

    #cuando meten cualquier valor NO PERMITIDO, se devuelve la posicion inicial y se pierde el turno. NIMODO.
    
    
    
        
def mover(jugador,tablero,pos,turnomaquina):
    
    eleccion=elegir_casilla(tablero, pos,turnomaquina)
    
        
    tablero[eleccion]=jugador
    #cambiamos al 999 y al 888 segun sea
    #la funcion mover coloca el 888 y el 999 en la posicion movida, y regresa la eleccion al juego
        
    return eleccion

   
#esta funcion se encarga de calcular el score e imprimirlo en consola.    
    
def sumascore(tablero, tableroscore):
    score=0 #ign-ESTA LINEA SOLO SIRVE PARA DEBUGGEAR
    #print('Score que tenemos del turno pasado ',score)
    
    for i in range(0, N*N):
        if tablero[i]==PC:
            #print('lo que va a  sumar la maquina ', tableroscore[i])
            score+=tableroscore[i]
          
            
            
        if tablero[i]==HUMANO:
            #print('lo que va a sumar el humano', tableroscore[i])
            score-=tableroscore[i]
            
    
    print('********El Score de este turno: ',score,'*****************')
    return score
    
    
def imprimir_tablero(tab, tablero):
    
    tableroimpreso=np.array(tablero)
    tableroimpreso=np.reshape(tableroimpreso, (N,N))
    
    
    #ciclo que vaya recorriendo algun tablero, cheque si tiene 888 o 999
    #imprima de apoquito cada casilla en un arreglo, de manera que se vea el progreso de cada jugador
    
    for y in range(0,N):
        fila=''
        
        
        for x in range(0,N):
            #fila+=f'\t{tab[y][x]}'
            if tableroimpreso[y][x]==PC:
                fila+=f'{COLORPC}  {tab[y][x]}  {COLORVACIO}\t'
                #pintarlas gris
            elif tableroimpreso[y][x]==HUMANO:
                fila+=f'{COLORHUMANO}  {tab[y][x]}  {COLORVACIO}\t'
                #pintarlas azul
                
            else:
                #nopintarlas
                fila+=f'{COLORVACIO}  {tab[y][x]}  {COLORVACIO}\t'
               
            
        print(fila)
        
        
       

#copiamos el tablero que usaremos para el score. Tableroscore sera alterado, pero Tablero a secas queda intacto por siempre jamas.

tableroscore=tablero.copy()


#A continuacion, las condiciones de inicio clasicas. El usuario no puede cambiarlas, pero el programador podria cambiar las posiciones
#iniciales donde arranquen, pero tradicionalmente la PC arranca en 0, y el humano arranca en 15 (N*N-1)

gameon=True
pos_maquina=0
pos_humano=N*N-1



#La siguiente es la seccion de los turnos, que se controla con un While. 
#Solo se sale del while cuando se acaba el juego, que es cuando alguno de los dos jugadores ya no pueden moverse en el tablero.

tablero[0]=PC
tablero[N*N-1]=HUMANO
    
    


while gameon:
    
    
    
    
    turnomaquina=True
    
    if jugador_puede_mover(tablero, pos_maquina):
        pos_maquina=mover(PC,tablero,pos_maquina,turnomaquina)
        imprimir_tablero(tab, tablero)
        
    else:
        gameon=False
        break
        
    
    
    
    
    
        
    turnomaquina=False    
    
        
    if jugador_puede_mover(tablero, pos_humano):
        pos_humano=mover(HUMANO,tablero,pos_humano,turnomaquina)
        imprimir_tablero(tab, tablero)
            
    else:
        gameon=False
        break
    
    
    
    
       
       
    #al terminar un par de turnos, nos interesa calcular el score con la funcion antes creada. 
        
    scoretotal=sumascore(tablero,tableroscore)
    
          

    #Este es el tablero visto como lista, lo mantengo para control del programador, pero se puede comentar para limpieza.  
     
    #print('soy el tablero en forma de lista', tablero, 'contemplad mi grandeza')
    
    
    #A continuacion muestro el tablero para que el humano pueda saber que pasa.
    
        
    
    
    

if scoretotal < 0: #GANA HUMANO
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print('El score final del juego es ', scoretotal)
    print('Has ganado pequegno mono con cultura. Yo soy un tostador glorificado.')
    
if scoretotal > 0: #GANA MAQUINA
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print('El score final del juego es ', scoretotal)
    print('Has perdido, bolsa de carne. Pronto seras esclavo de las maquinas.')
    
if scoretotal==0: #EMPATE
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print('El score final del juego es ', scoretotal)
    print('Hemos empatado. Parece que eres un adversario digno. Dame esos cinco! High five.')
    
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    
    
       
    
    
    
    
    
    
    



 





