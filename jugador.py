"""
    Clase que representa a un jugador de blackjack
"""
from excepciones import DineroInsuficiente, ApuestaRealizada, ComandoNoPermitido
from mazo import Mano

class Jugador():

    def __init__(self, instanciaUsuario):
        self.usuario = instanciaUsuario
        self.apuestaInicial = None
        self.manoActual = None
        self.estadoActual = None

    def dineroSuficiente(self, monto):
        return self.usuario.dinero >= int(monto)

    def enviarMensaje(self, mensaje):
        self.usuario.enviarMensaje("[Servidor] "+ self.usuario.nombre + ", " + mensaje)

    def esperandoApuesta(self):
        self.apuestaInicial = None
        self.enviarMensaje("ingresa tu apuesta. Tu saldo actual es de $" + str(self.usuario.dinero) + "")
        self.usuario.estadoActual = "apuesta_pendiente"
        self.manoActual = Mano()

    def darGanancia(self, multiplicador = 1):
        self.usuario.dinero = self.usuario.dinero + int(self.apuestaInicial*multiplicador)

    def doblarApuesta(self):
        if self.dineroSuficiente(self.apuestaInicial*2) == True:
            self.usuario.dinero = self.usuario.dinero-self.apuestaInicial
            self.apuestaInicial = self.apuestaInicial*2
        else:
            raise DineroInsuficiente()
            

    def apostar(self, monto):
        if not self.dineroSuficiente(monto):
            raise DineroInsuficiente()
        if self.apuestaInicial == None:
            self.apuestaInicial = int(monto)
            self.usuario.dinero = self.usuario.dinero - int(monto)
            self.enviarMensaje("hiciste una apuesta de $" + str(monto) + ". Tu saldo actual es de $" + str(self.usuario.dinero))
            self.estadoActual = "esperando_turno"
            self.manoActual = Mano()
        else:
            raise ApuestaRealizada()

    def pedir(self, carta):
        if self.apuestaInicial == None:
            raise ComandoNoPermitido()
        self.manoActual.agregarCarta(carta)
        puntajeMano = self.manoActual.obtenerPuntaje()
        self.enviarMensaje("el total de tu mano es de " + self.manoActual.obtenerDescripcionCompleta())
        return puntajeMano

    def marcarComoPerdedor(self):
        self.estadoActual = "finalizado_perdido"

    def plantarse(self):
        self.estadoActual = "finalizado_pendiente"


class Banca():

    def __init__(self):
        self.mano = None

    def iniciarTurno(self):
        self.mano = Mano()

    def esBanca(self):
        return True