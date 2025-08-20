import math    # Para usar infinitos en el algoritmo minimax
import os      # Para limpiar la pantalla en consola
from triqui import Triqui

# Algoritmo Minimax con Poda Alpha-Beta
def minimax(self, estado, jugador, alpha, beta): #VARIABLES para realizar poda alfa-beta
    max_jugador = self.jugadorBot # Jugador que maximiza
    otro_jugador = 'O' if jugador == 'X' else 'X' # Jugador que minimiza

    # Caso base: si el juego terminó
    if self.es_terminal(estado): # Verifica si el estado es terminal
        if Triqui().jugador_gana(estado, self.jugadorBot): 
            return {'posicion': None, 'puntuacion': 1 * (len(self.acciones(estado)) + 1)}
        elif Triqui().jugador_gana(estado, self.jugadorHumano):
            return {'posicion': None, 'puntuacion': -1 * (len(self.acciones(estado)) + 1)}
        else:
            return {'posicion': None, 'puntuacion': 0}

    # Si le toca a la máquina (maximizar)
    if jugador == max_jugador:
        mejor = {'posicion': None, 'puntuacion': -math.inf} # Inicializa mejor con un valor muy bajo
        for posible_movimiento in self.acciones(estado): # Itera sobre los movimientos posibles
            nuevoEstado = self.resultado(estado, posible_movimiento)
            puntuacion_sim = self.minimax(nuevoEstado, otro_jugador, alpha, beta)
            puntuacion_sim['posicion'] = posible_movimiento

            if puntuacion_sim['puntuacion'] > mejor['puntuacion']: # Si encontramos una mejor puntuación
                mejor = puntuacion_sim
            
            # Actualiza el valor de alpha
            alpha = max(alpha, mejor['puntuacion'])
            
            # Poda beta: si alpha es mayor o igual que beta, corta la rama
            if beta <= alpha:
                break
        return mejor
    # Si le toca al humano (minimizar)
    else:
        mejor = {'posicion': None, 'puntuacion': math.inf}
        for posible_movimiento in self.acciones(estado):
            nuevoEstado = self.resultado(estado, posible_movimiento)
            puntuacion_sim = self.minimax(nuevoEstado, otro_jugador, alpha, beta)
            puntuacion_sim['posicion'] = posible_movimiento

            if puntuacion_sim['puntuacion'] < mejor['puntuacion']:
                mejor = puntuacion_sim
            
            # Actualiza el valor de beta
            beta = min(beta, mejor['puntuacion'])
            
            # Poda alfa: si beta es menor o igual que alpha, corta la rama
            if beta <= alpha:
                break
        return mejor