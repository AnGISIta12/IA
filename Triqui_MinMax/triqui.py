import random  # Para decidir aleatoriamente si el humano es X u O
import math    # Para usar infinitos en el algoritmo minimax
import os      # Para limpiar la pantalla en consola

class Triqui:
    def __init__(self):
        # Tablero inicial: 9 casillas con "-"
        self.tablero = ['-' for _ in range(9)]
        
        # Aleatoriamente asigna si el humano juega con X o con O
        if random.randint(0, 1) == 1:
            self.jugadorHumano = 'X'
            self.jugadorBot = "O"
        else:
            self.jugadorHumano = "O"
            self.jugadorBot = "X"

    def mostrar_tablero(self):
        # Imprime el tablero en formato 3x3
        print("")
        for i in range(3):
            print("   ", self.tablero[0+(i*3)], " | ", self.tablero[1+(i*3)], " | ", self.tablero[2+(i*3)])
            print("")

    def tablero_lleno(self,estado):
        # Verifica si el tablero está lleno (empate)
        return not "-" in estado

    def jugador_gana(self,estado,jugador):
        # Todas las combinaciones ganadoras posibles
        victorias = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),
                        (1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        # Revisa si el jugador tiene alguna de ellas
        return any(estado[a]==estado[b]==estado[c]==jugador for a,b,c in victorias)

    def verificarGanador(self):
        # Revisa si el humano ganó
        if self.jugador_gana(self.tablero,self.jugadorHumano):
            os.system("cls")
            print(f"   ¡Jugador {self.jugadorHumano} gana!")
            return True
        # Revisa si la máquina ganó
        if self.jugador_gana(self.tablero,self.jugadorBot):
            os.system("cls")
            print(f"   ¡Jugador {self.jugadorBot} gana!")
            return True
        # Revisa si hubo empate
        if self.tablero_lleno(self.tablero):
            os.system("cls")
            print("   ¡Empate!")
            return True
        return False

    def iniciar(self):
        # Crea jugadores: humano y computadora
        bot = JugadorComputadora(self.jugadorBot)
        humano = JugadorHumano(self.jugadorHumano)

        # Bucle del juego
        while True:
            os.system("cls")  
            print(f"   Turno del jugador {self.jugadorHumano}")
            self.mostrar_tablero()

            # Turno del humano
            casilla = humano.movimiento_humano(self.tablero)
            self.tablero[casilla] = self.jugadorHumano
            if self.verificarGanador():
                break

            # Turno de la máquina (usa minimax)
            casilla = bot.movimiento_maquina(self.tablero)
            self.tablero[casilla] = self.jugadorBot
            if self.verificarGanador():
                break

        print()
        self.mostrar_tablero()

class JugadorHumano:
    def __init__(self,letra):
        self.letra = letra

    def movimiento_humano(self,estado):
        # Pide al humano que ingrese un número entre 1 y 9
        while True:
            casilla = int(input("Ingresa el número de la casilla (1-9): "))
            if estado[casilla-1] == "-":  # Verifica que la casilla esté libre
                break
        return casilla-1  # Devuelve el índice en la lista del tablero

class JugadorComputadora:
    def __init__(self,letra):
        self.jugadorBot = letra
        self.jugadorHumano = "X" if letra == "O" else "O"

    def acciones(self,estado):
        # Devuelve una lista con las posiciones libres
        return [i for i, x in enumerate(estado) if x == "-"]

    def resultado(self,estado,accion):
        # Devuelve un nuevo tablero después de hacer un movimiento
        nuevoEstado = estado.copy()
        jugador = self.jugador_actual(estado)
        nuevoEstado[accion] = jugador
        return nuevoEstado

    def jugador_actual(self,estado):
        # Cuenta X y O para saber a quién le toca jugar
        x = estado.count("X")
        o = estado.count("O")
        return "X" if x == o else "O"

    def es_terminal(self,estado):
        # Revisa si el juego terminó (alguien ganó o empate)
        ttt = Triqui()
        return ttt.jugador_gana(estado,"X") or ttt.jugador_gana(estado,"O") or not "-" in estado

    # Algoritmo Minimax
    def minimax(self, estado, jugador):
        max_jugador = self.jugadorBot  # La máquina intenta maximizar
        otro_jugador = 'O' if jugador == 'X' else 'X'

        # Caso base: si el juego terminó
        if self.es_terminal(estado):
            if Triqui().jugador_gana(estado, self.jugadorBot):
                return {'posicion': None, 'puntuacion': 1 * (len(self.acciones(estado)) + 1)}
            elif Triqui().jugador_gana(estado, self.jugadorHumano):
                return {'posicion': None, 'puntuacion': -1 * (len(self.acciones(estado)) + 1)}
            else:
                return {'posicion': None, 'puntuacion': 0}  # empate

        # Si le toca a la máquina: maximizar
        if jugador == max_jugador:
            mejor = {'posicion': None, 'puntuacion': -math.inf}
        # Si le toca al humano: minimizar
        else:
            mejor = {'posicion': None, 'puntuacion': math.inf}

        # Revisa todos los movimientos posibles
        for posible_movimiento in self.acciones(estado):
            nuevoEstado = self.resultado(estado, posible_movimiento)
            puntuacion_sim = self.minimax(nuevoEstado, otro_jugador)
            puntuacion_sim['posicion'] = posible_movimiento

            # Elige el mejor movimiento según quién juega
            if jugador == max_jugador:
                if puntuacion_sim['puntuacion'] > mejor['puntuacion']:
                    mejor = puntuacion_sim
            else:
                if puntuacion_sim['puntuacion'] < mejor['puntuacion']:
                    mejor = puntuacion_sim
        return mejor

    def movimiento_maquina(self,estado):
        # La máquina elige la mejor jugada usando minimax
        return self.minimax(estado,self.jugadorBot)['posicion']

triquii = Triqui()
triquii.iniciar()

