 #!/usr/bin/env python
# -*- coding: utf-8 -*-

	#---------------------------------------------------------------------------#
	#																			#
	#	                	LIBRERÍA PANTALLA PRETECOR SAS	     				#
	#																			#
	#---------------------------------------------------------------------------#
	# Versión: v1.3																#
	# Fecha de actualización 19/10/2020											#
	#---------------------------------------------------------------------------#
	# Mejoras:	-> Posibilidad de conectar los datos arriba y abajo  			#
	#																			#
	# 																			#
	#---------------------------------------------------------------------------#
	#																			#
	#		CONFIGURACIÓN:														#
	#																			#
	#---------------------------------------------------------------------------#
	# Importar la clase:														#
	#---------------------------------------------------------------------------#
	#																			#
	# 	from Pantalla import LTSmart											#
	#																			#
	#---------------------------------------------------------------------------#
	# Para inicializarla como objeto:											#
	#---------------------------------------------------------------------------#
	#																			#
	# Se pueden inicializar dos objetos uno con cada pin para controlar dos		#
	# pantallas distintas														#
	#																			#
	# 	LTSmart(pin, channel, cintas, longitud, longitud_baliza)				#
	#																			#
	#	pin: 12     debe ir con    channel: 0 (Canal PWM)						#
	#   pin: 13     debe ir con    channel: 1 (Canal PWM)						#
	#																			#
	#   cintas: 5    (Sólo funciona con matrices de 5 cintas)					#
	#																			#
	#	longitud: La longitud en LEDS de cada cinta (usualmente 60leds/m)		#
	#																			#
	#	longitud_baliza: Debe ir la cantidad de leds que tiene la baliza 		#
	#																			#
	#---------------------------------------------------------------------------#
	# Mostrar en la pantalla: 													#
	#---------------------------------------------------------------------------#
	#																			#
	# Mostrar mensajes y la barra en la pantalla se usa el siguiente método:	#
	#																			#
	# screen(msg,r,g,b,sentido,brillo,barra,var,lim_sup,lim_inf,L1,L2,L3)		#
	#																			#
	#	msg: Mensaje para mostrar en la pantalla 								#
	#	r,g,b:  0 a 255  --> Valores RGB del color del texto					#
	#	sentido:  0  --> El texto se muestra estático desde la parte superior 	#
	#			  1  --> El texto se desplaza de arriba hacia abajo 			#
	#   brillo:  0 a 255  --> Brillo con el que se mostrará el texto y la barra #
	#	barra:  0 --> No muestra la barra, mensaje en toda la pantalla			#
	#			1 --> Muestra la barra en la parte superior (ocupa 1m o 60leds)	#
	#	var:  variable que se va a representar en la barra 						#
	#	lim_sup: Límite superior de la variable a mostrar en la barra 			#
	#	lim_inf: Límite inferior de la variable a mostrar en la barra 			#
	#	L1:        var < L1 es VERDE 	---> Límite para cambio de color		#
	#	L2:  L1 <= var < L2 es AMARILLO  ---> Límite para cambio de color		#
	#	L3:  L2 <= var < L3 es NARANJA  ---> Límite para cambio de color		#
	#	     L3 <= var      es ROJO	---> Límite para cambio de color			#
	#																			#
	#---------------------------------------------------------------------------#
	# Mostrar en la baliza 												 		#
	#---------------------------------------------------------------------------#
	#																			#
	# El color de la baliza se controla con el siguiente método: 				#
	#																			#
	# nivel_baliza(var, lim_sup, lim_inf, L1, L2, L3)							#
	#																			#
	#	var:  variable que se va a representar en la barra 						#
	#	lim_sup: Límite superior de la variable a mostrar en la baliza 			#
	#	lim_inf: Límite inferior de la variable a mostrar en la baliza			#
	#	L1:        var < L1 es VERDE 	---> Límite para cambio de color		#
	#	L2:  L1 <= var < L2 es AMARILLO  ---> Límite para cambio de color		#
	#	L3:  L2 <= var < L3 es NARANJA  ---> Límite para cambio de color		#
	#	     L3 <= var      es ROJO	---> Límite para cambio de color			#
	#																			#
	#---------------------------------------------------------------------------#
	# Apagar todo	(pantalla y baliza)									 		#
	#---------------------------------------------------------------------------#
	#																			#
	# Usar el siguiente método para apagar todo 								#
	#																			#
	# 	apagar()																#
	#																			#
	#---------------------------------------------------------------------------#
	# Reiniciar contador pantalla 										 		#
	#---------------------------------------------------------------------------#
	#																			#
	# Usar el siguiente método para reiniciar desde abajo el contador 			#
	#																			#
	# 	reiniciar()																#
	#																			#
	#---------------------------------------------------------------------------#

import time
import logging
from neopixel import Adafruit_NeoPixel, Color
import datetime
from api_pretecor import API
test_script = 1
import requests


class LTSmart:

	mensaje = 'POSTE'
	contador_pantalla = -8
	contador_pantalla_max = 0
	contador_barra = 0

	def __init__(self, pin, channel, cintas, longitud, longitud_baliza):

		# ARREGLO LINEAL LED
		self.long_baliza = longitud_baliza
		self.Longitud = longitud 								# Longitud de cada cinta Led
		self.Numero = cintas									# Numero de cintas Leds
		self.LED_COUNT = longitud * cintas + longitud_baliza	# Number of LED pixels.
		self.LED_PIN = pin 										# GPIO pin connected to the pixels (must support PWM!).
		self.LED_FREQ_HZ = 800000								# LED signal frequency in hertz (usually 800khz)
		self.LED_DMA = 10										# DMA channel to use for generating signal (try 10)
		self.LED_BRIGHTNESS = 150								# Set to 0 for darkest and 255 for brightest
		self.LED_INVERT = False									# True to invert the signal (when using NPN transistor level shift)
		self.LED_CHANNEL = channel
		
		self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
		self.strip.begin()

		self.ConvBin2 = [0,0,0,0,0,0,0,0] #Vector Conversor a Binario
		self.mensaje_anterior = 'POSTE'
		self.contador_dp = 0 			# Contador para los dos puntos

	#---------------------------------------------------------------------------#
	#		Escribir pantalla													#
	#---------------------------------------------------------------------------#
	def screen(self, msg, Rojo, Verde, Azul, sentido, brillo, activar_barra, variable, lim_sup, lim_inf, n1, n2, n3):
		
		self.strip.setBrightness(brillo)
		self.mensaje = msg

		if self.mensaje_anterior != self.mensaje:
			self.contador_pantalla = -8

		self.CleanScreen(Color(0, 0, 0))

		if activar_barra == 0:
			# La barra está desactivada, muestra el texto completo en la pantalla
			if sentido == 0:
				# El texto se muestra estático
				self.contador_pantalla = self.Longitud - 10
				self.Message(self.mensaje, self.contador_pantalla, Color(Verde, Rojo, Azul))
				self.strip.show() 			# Mostrar el programa
			else:
				# El texto se desplaza hacia arriba
				self.contador_pantalla_max = len(self.mensaje) * 8 + self.Longitud
				if self.contador_pantalla < len(self.mensaje) * 8 + self.Longitud:
					self.CleanScreen(Color(0, 0, 0))
					self.Message(self.mensaje, self.contador_pantalla, Color(Verde, Rojo, Azul))
					self.strip.show() 		# Mostrar el programa
				else:
					self.contador_pantalla = -8
		else:
			# La barra está activada, quita el último metro de la pantalla
			if sentido == 0:
				# El texto se muestra estático
				self.nivel(variable, lim_sup, lim_inf, n1, n2, n3)
				self.contador_pantalla = self.Longitud - 10 - 61
				self.Message(self.mensaje, self.contador_pantalla, Color(Verde, Rojo, Azul))
				self.strip.show() 			# Mostrar el programa
			else:
				# El texto se desplaza hacia arriba
				self.contador_pantalla_max = len(self.mensaje) * 8 + self.Longitud - 50
				if self.contador_pantalla < len(self.mensaje) * 8 + self.Longitud - 50:
					self.CleanScreen(Color(0, 0, 0))
					self.Message(self.mensaje, self.contador_pantalla, Color(Verde, Rojo, Azul))
					self.CleanBarra(self.Longitud - 61, self.Longitud - 1)
					self.nivel(variable, lim_sup, lim_inf, n1, n2, n3)
					self.strip.show()  #Mostrar el programa
				else:
					self.contador_pantalla = -8

		self.contador_pantalla += 1
		self.mensaje_anterior = self.mensaje

	#---------------------------------------------------------------------------#
	#		Apagar pantalla														#
	#---------------------------------------------------------------------------#
	def apagar(self):
		self.CleanAll(Color(0, 0, 0))
		self.strip.show() 	# Mostrar el programa

	#---------------------------------------------------------------------------#
	#		Mostrar barra														#
	#---------------------------------------------------------------------------#
	def nivel(self, variable, lim_sup, lim_inf, n1, n2, n3):
		# self.CleanScreen(Color(0, 0, 0))
		j = self.Longitud - 60
		self.line(j, Color(255,0,255))
		j = self.Longitud - 59
		self.line(j, Color(255,0,255))
		j = self.Longitud - 3
		self.line(j, Color(255,0,255))
		j = self.Longitud - 2
		self.line(j, Color(255,0,255))

		led_nivel = int(round(variable * 56 / (lim_sup - lim_inf)))
		# print(led_nivel)
		grb=[0,0,0]

		for k in range(self.Longitud - 58, self.Longitud - 60 + led_nivel-1):
			if variable < 1:		
				grb=[0,0,0]
			elif variable < n1:
				grb=[255,0,0]
			elif variable < n2:
				grb=[255,255,0]
			elif variable < n3:
				grb=[100,255,0]
			else:
				grb=[0,255,0]

			self.line(k, Color(grb[0], grb[1], grb[2]))
		
		if self.contador_barra <  k:
			self.contador_barra=k+1
		elif self.contador_barra != k:
			self.contador_barra=self.contador_barra-1
			
		self.line(self.contador_barra, Color(255, 255, 255))

	#---------------------------------------------------------------------------#
	#		Mostrar baliza														#
	#---------------------------------------------------------------------------#
	def nivel_baliza(self, variable, lim_sup, lim_inf, n1, n2, n3):
		grb=[0,0,0]
		if variable < 1:		
			grb=[0,0,0]
		elif variable < n1:
			grb=[255,0,0]
		elif variable < n2:
			grb=[255,255,0]
		elif variable < n3:
			grb=[100,255,0]
		else:
			grb=[0,255,0]

		for k in range(self.LED_COUNT - self.long_baliza, self.LED_COUNT):
			self.strip.setPixelColor(k, Color(grb[0], grb[1], grb[2]))

	#---------------------------------------------------------------------------#
	#		Binario convertido a Leds	(Se usa en el medio)					#
	#---------------------------------------------------------------------------#
	def Bin2Led_medio(self, hexa, posicion, color, direccion):
		ConvBin = bin(hexa)
		if direccion == 0:
			for i in range(2, len(ConvBin)):
				if ConvBin[i] == '0':
					self.strip.setPixelColor(posicion + len(ConvBin) - i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion + len(ConvBin) - i, color)
		else:
			for i in range(2, len(ConvBin)):
				if ConvBin[i] == '0':
					self.strip.setPixelColor(posicion - len(ConvBin) + i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion - len(ConvBin) + i, color)

	#---------------------------------------------------------------------------#
	#		Binario convertido a Leds2	(Se usa en el borde superior)			#
	#---------------------------------------------------------------------------#
	def Bin2Led_superior(self, hexa, posicion, color, direccion, dif):
		ConvBin = bin(hexa)

		if len(ConvBin) != 10:
			self.ConvBin2 =['0','0','0','0','0','0','0','0']
			for j in range(2, len(ConvBin)):
				self.ConvBin2[10 - len(ConvBin) + j - 2] = ConvBin[j]
		else:
			for i in range(0, 7):
				self.ConvBin2[i] = ConvBin[i + 2] 
		# Los leds en la misma dirección
		if direccion == 0:
			for i in range(0, dif):
				if self.ConvBin2[8 - dif + i] == '0':
					self.strip.setPixelColor(posicion + dif - i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion + dif - i, color)
		# Los leds en dirección opuesta
		else:
			for i in range(0, dif):
				if self.ConvBin2[8 - dif + i] == '0':
					self.strip.setPixelColor(posicion - dif + i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion - dif + i, color)

	#---------------------------------------------------------------------------#
	#		Binario convertido a Leds2	(Se usa en el borde inferior)			#
	#---------------------------------------------------------------------------#
	def Bin2Led_inferior(self, hexa, posicion, color, direccion, dif):
		ConvBin = bin(hexa)

		if len(ConvBin) != 10:
			self.ConvBin2 =['0','0','0','0','0','0','0','0']
			for j in range(2, len(ConvBin)):
				self.ConvBin2[10 - len(ConvBin) + j - 2] = ConvBin[j]
		else:
			for i in range(0, 7):
				self.ConvBin2[i] = ConvBin[i + 2] 
		# Los leds en la misma dirección
		if direccion == 0:
			for i in range(0, dif):
				#print(8 - dif + i)
				if self.ConvBin2[i] == '0':
					self.strip.setPixelColor(posicion +8 - i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion +8 - i, color)
		# Los leds en dirección opuesta
		else:
			for i in range(0, dif):
				if self.ConvBin2[i] == '0':
					self.strip.setPixelColor(posicion -8 + i, Color(0, 0, 0))
				else:
					self.strip.setPixelColor(posicion -8 + i,  color)

	#---------------------------------------------------------------------------#
	#		Letras convertidas a Leds											#
	#---------------------------------------------------------------------------#
	def Letras2Led(self, posicion2, color, hexa):
		# Borde superior
		if posicion2 > self.Longitud - 9:
			dif = self.Longitud - 1 - posicion2
			if dif > 0:
				self.Bin2Led_superior(hexa[4], posicion2, color, 0, dif)
				self.Bin2Led_superior(hexa[3], 2*self.Longitud - posicion2 - 1, color, 1, dif)
				self.Bin2Led_superior(hexa[2], 2*self.Longitud + posicion2, color, 0, dif)
				self.Bin2Led_superior(hexa[1], 4*self.Longitud - posicion2 - 1, color, 1, dif)
				self.Bin2Led_superior(hexa[0], 4*self.Longitud + posicion2, color, 0, dif)
		# Borde inferior
		elif posicion2 < -1:
			dif2 = 9-posicion2 * -1
			self.Bin2Led_inferior(hexa[4], posicion2, color, 0, dif2)
			self.Bin2Led_inferior(hexa[3], 2*self.Longitud - posicion2 - 1, color, 1, dif2)
			self.Bin2Led_inferior(hexa[2], 2*self.Longitud + posicion2, color, 0, dif2)
			self.Bin2Led_inferior(hexa[1], 4*self.Longitud - posicion2 - 1, color, 1, dif2)
			self.Bin2Led_inferior(hexa[0], 4*self.Longitud + posicion2, color, 0, dif2)

		# El centro de la pantalla
		else:
			self.Bin2Led_medio(hexa[4], posicion2, color, 0)
			self.Bin2Led_medio(hexa[3], 2*self.Longitud - posicion2 - 1, color, 1)
			self.Bin2Led_medio(hexa[2], 2*self.Longitud + posicion2, color, 0)
			self.Bin2Led_medio(hexa[1], 4*self.Longitud - posicion2 - 1, color, 1)
			self.Bin2Led_medio(hexa[0], 4*self.Longitud + posicion2, color, 0)

	#---------------------------------------------------------------------------#
	#		Limpiar pantalla													#
	#---------------------------------------------------------------------------#
	def CleanScreen(self, color):
		for i in range(self.LED_COUNT - self.long_baliza):
			self.strip.setPixelColor(i, color)

	#---------------------------------------------------------------------------#
	#		Limpiar pantalla y baliza											#
	#---------------------------------------------------------------------------#
	def CleanAll(self, color):
		for i in range(self.LED_COUNT):
			self.strip.setPixelColor(i, color)

	#---------------------------------------------------------------------------#
	#		Limpiar barra														#
	#---------------------------------------------------------------------------#
	def CleanBarra(self, j, k):
		for i in range(j, k):
			self.line(i, Color(0, 0, 0))

	#---------------------------------------------------------------------------#
	#		Dibujar una línea													#
	#---------------------------------------------------------------------------#
	def line(self, i, color):
		self.strip.setPixelColor(i, color)
		self.strip.setPixelColor((2 * self.Longitud - i) - 1, color)
		self.strip.setPixelColor(2 * self.Longitud + i, color)
		self.strip.setPixelColor((4 * self.Longitud - i) - 1, color)
		self.strip.setPixelColor(4 * self.Longitud + i, color)

	#---------------------------------------------------------------------------#
	#		Mensaje convertido a cada letra, numero o simbolo 					#
	#---------------------------------------------------------------------------#
	
	def tabla (self, valor, posicion3, color, i):
		
		switcher = {
			# MAYUSCULAS
			"A": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x3E,0x48,0x88,0x48,0x3E]),
			"B": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x6C,0x92,0x92,0x92,0xFE]),
			"C": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x44,0x82,0x82,0x82,0x7C]),
			"D": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0x82,0x82,0x82,0xFE]),
			"E": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x82,0x92,0x92,0x92,0xFE]),
			"F": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x80,0x90,0x90,0x90,0xFE]),
			"G": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xCE,0x8A,0x82,0x82,0x7C]),
			"H": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFE,0x10,0x10,0x10,0xFE]),
			"I": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x82,0xFE,0x82,0x00]),
			"J": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x80,0xFC,0x82,0x02,0x04]),
			"K": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x82,0x44,0x28,0x10,0xFE]),
			"L": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x02,0x02,0x02,0x02,0xFE]),
			"M": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFE,0x40,0x38,0x40,0xFE]),
			"N": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFE,0x08,0x10,0x20,0xFE]),
			#"Ñ": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xBE,0x84,0x88,0x90,0xBE]),
			"O": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0x82,0x82,0x82,0x7C]),
			"P": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x60,0x90,0x90,0x90,0xFE]),
			"Q": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7A,0x84,0x8A,0x82,0x7C]),
			"R": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x62,0x94,0x98,0x90,0xFE]),
			"S": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x4C,0x92,0x92,0x92,0x64]),
			"T": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xC0,0x80,0xFE,0x80,0xC0]),
			"U": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFC,0x02,0x02,0x02,0xFC]),
			"V": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xF8,0x04,0x02,0x04,0xF8]),
			"W": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFE,0x02,0x1C,0x02,0xFE]),
			"X": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xC6,0x28,0x10,0x28,0xC6]),
			"Y": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xC0,0x20,0x1E,0x20,0xC0]),
			"Z": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xC2,0xB2,0x92,0x9A,0x86]),

			# MINUSCULAS
			"a": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x02,0x1E,0x2A,0x2A,0x04]),
			"b": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x1C,0x22,0x22,0x14,0xFE]),
			"c": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x14,0x22,0x22,0x22,0x1C]),
			"d": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFE,0x14,0x22,0x22,0x1C]),
			"e": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x18,0x2A,0x2A,0x2A,0x1C]),
			"f": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x40,0x90,0x7E,0x10,0x00]),
			"g": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x3C,0x72,0x4A,0x4A,0x30]),
			"h": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x1E,0x20,0x20,0x10,0xFE]),
			"i": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x02,0xBE,0x22,0x00]),
			"j": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0xBC,0x02,0x02,0x04]),
			"k": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x22,0x14,0x08,0xFE]),
			"l": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x02,0xFE,0x82,0x00]),
			"m": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x3E,0x20,0x1E,0x20,0x3E]),
			"n": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x1E,0x20,0x20,0x10,0x3E]),
			"o": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x1C,0x22,0x22,0x22,0x1C]),
			"p": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x30,0x48,0x48,0x30,0x7E]),
			"q": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7E,0x30,0x48,0x48,0x30]),
			"r": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x10,0x20,0x20,0x10,0x3E]),
			"s": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x24,0x2A,0x2A,0x2A,0x12]),
			"t": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x24,0x12,0xFC,0x20,0x20]),
			"u": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x3E,0x04,0x02,0x02,0x3C]),
			"v": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x38,0x04,0x02,0x04,0x38]),
			"w": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x3C,0x02,0x0C,0x02,0x3C]),
			"x": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x22,0x14,0x08,0x14,0x22]),
			"y": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0x12,0x12,0x12,0x64]),
			"z": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x22,0x32,0x2A,0x26,0x22]),
			
			# NUMEROS
			"0": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0xA2,0x92,0x8A,0x7C]),
			"1": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x02,0xFE,0x42,0x00]),
			"2": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x62,0x92,0x92,0x92,0x4E]),
			"3": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xCC,0xB2,0x92,0x82,0x84]),
			"4": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x08,0xFE,0x48,0x28,0x18]),
			"5": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x9C,0xA2,0xA2,0xA2,0xE4]),
			"6": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x8C,0x92,0x92,0x52,0x3C]),
			"7": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xE0,0x90,0x88,0x84,0x82]),
			"8": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x6C,0x92,0x92,0x92,0x6C]),
			"9": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x78,0x94,0x92,0x92,0x62]),

			# SIMBOLOS
			"=": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x28,0x28,0x28,0x28,0x28]),
			"(": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x82,0x44,0x38,0x00]),
			")": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x38,0x44,0x82,0x00]),
			":": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x28,0x00,0x00]),
			";": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x2C,0x02,0x00]),
			" ": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x00,0x00,0x00]),
			",": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x0C,0x02,0x00]),
			"?": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x60,0x90,0x9A,0x80,0x40]),
			".": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x0C,0x0C,0x00,0x00]),
			"%": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x46,0x26,0x10,0xC8,0xC4]),
			"/": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x04,0x08,0x10,0x20,0x40]),
			"@": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7E,0x81,0x8F,0x89,0x46]), #Tipo 1
			#"@": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x72,0xB1,0xB1,0x81,0x7E]), # Tipo 2
			"*": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x50,0xE0,0x50,0x00]), #Tipo 1
			#"*": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x14,0x08,0x3E,0x08,0x14]), # Tipo 2
			"$": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x44,0x4A,0xFF,0x4A,0x32]),
			"!": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0xFA,0x00,0x00]),
			"#": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x44,0xFF,0x44,0xFF,0x44]),
			"+": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x10,0x10,0x7C,0x10,0x10]),
			"-": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x10,0x10,0x10,0x00]),
			"_": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x01,0x01,0x01,0x01,0x01]),
			
			# ESPECIALES

			# Unidades
			"\x80": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x22,0x41,0x22,0xDC,0xC0]), # °C
			"\x81": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x00,0xC0,0xC0]), # ° pequeño
			"\x82": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0xE0,0xA0,0xE0]), # ° grande
			"\x83": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x78,0x04,0x04,0x7F,0x00]), # u letra griega
			
			# Simbolos
			"\x84": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0x10,0x00,0x00]), # Punto centro Pequeño
			"\x85": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x1C,0x1C,0x1C,0x00]), # Punto centro Grande

			# Iconos
			"\x86": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x30,0x78,0x3C,0x78,0x30]), # Corazón relleno
			"\x87": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x30,0x48,0x24,0x48,0x30]), # Corazón blanco
			"\x88": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x38,0xE4,0x27,0xE4,0x38]), # Conector
			"\x89": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x00,0x00,0xFF,0x00,0x00]), # Cable	
			"\x90": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFC,0x4C,0x20,0x1F,0x03]), # Nota musical
			"\x91": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0xFF,0x4F,0x4F,0x4F,0x7F]), # Celular
			"\x92": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x08,0x78,0xFA,0x78,0x08]), # Campana
			"\x93": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x08,0x44,0x14,0x44,0x08]), # Cara feliz
			
			#Animaciones			
			"\x94": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0x3E,0x1E,0x3E,0x7C]), # Pacman abierto
			"\x95": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0xFE,0xFE,0xFE,0x7C]), # Pacman cerrado
			"\x96": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7C,0xCF,0xFE,0xCF,0x7C]), # Fantom1
			"\x97": lambda: self.Letras2Led(posicion3 - 8 * i, color, [0x7F,0xCC,0xFF,0xCC,0x7F]), # Fantom2		
		}.get(valor, lambda: None)()

	def Message(self, mensaje, posicion3, color):
		for i in range(len(mensaje)):
			
			self.tabla(mensaje[i],posicion3, color, i)

	#---------------------------------------------------------------------------#
	#		Reiniciar contador de Pantalla 		 								#
	#---------------------------------------------------------------------------#

	def reiniciar(self):
		self.contador_pantalla = -8

	#---------------------------------------------------------------------------#
	#																			#
	#	                  	PARA EJECUTAR LA PRUEBA  		        			#
	#																			#
	#---------------------------------------------------------------------------#


if test_script == 1:
	#LTSmart(pin, channel, cintas, longitud, longitud_baliza):
	poste_pantalla_1_obj = LTSmart(12, 0, 5, 120, 300)		# Creacion del Objeto de la pantalla 1
	poste_pantalla_2_obj = LTSmart(13, 1, 5, 120, 300)		# Creacion del Objeto de la pantalla 2

	# Variables extra
	contador2 = 0
	dia_1 = '0'

	# Inicialización de variables 
	mensaje1 = 'INFO NUEVO'



	# Variables específicas
	rgb_1=[0,255,255]
	rgb_2=[255,0,255]
	sentido1 = 0
	sentido2 = 0
	activar_barra1 = 0
	activar_barra2 = 0

	# Variables comunes
	brillo = 50
	lim_sup = 120
	lim_inf = 30
	L1 = 75
	L2 = 85
	L3 = 90
	variable=30

	colorR= 'Cian'
	duracion = 1

	msg_list =["       "]
	color_list =["negro"]
	duracion_list =["1"]
	id_list = ["0"]
	tipo_list =["Texto"]

	url_temp = 'http://api.openweathermap.org/data/2.5/weather?q=Bucaramanga,co&APPID=426452f13b335aba243398419e669c0f'
	url_cop = 'https://openexchangerates.org/api/latest.json?app_id=fa90403ea433408fb508f2d9daee407a'

	device_id = 9

	while True:
		while contador2 < len(id_list):
			start = time.time()

			#-----------

			api = API()
			status,response = api.get_data(device_id)

			if(status=="sent"):
				msg_list =["       "]
				color_list =["Negro"]
				duracion_list =["1"]
				id_list = ["0"]
				tipo_list =["texto"]

				for datos in response["respuesta"]:
					
					
					if(str(datos["activo"]) == "1"):

						msg_list.append(str(datos["mensaje"]))
						color_list.append(str(datos["color"]))
						duracion_list.append(str(datos["duracion"]))
						id_list.append(str(datos["id"]))
						tipo_list.append(str(datos["tipo"]))
            
			if contador2 >= len(id_list):
				contador2 = 1
			if len(id_list) == 1:
				contador2 = 0
				
				

			
			if tipo_list[contador2] == 'Fecha':
				now = datetime.datetime.now()
				mensaje1=now.strftime("  %m/%d/%Y")
				
			elif tipo_list[contador2] == 'Hora':
				now = datetime.datetime.now()
				mensaje1='    ' + now.strftime("%H") + ':' + now.strftime("%M")
				

			elif tipo_list[contador2] == 'Texto':
				mensaje1 = msg_list[contador2]
				
			elif tipo_list[contador2] == 'Texto_especial':
				mensaje1 = msg_list[contador2]
			elif tipo_list[contador2] == 'Bandera':
				mensaje1 = '    '
			elif tipo_list[contador2] == 'Temperatura':
				

				#if(status=="sent"):
				#	r = requests.get(url = url_temp,timeout=1) 
				#	content = r.json()
				#	formatted_data = abs(content['main']['temp']-273.15)

				#	mensaje1 = str(formatted_data) + ' \x80'
				#else:
				#	mensaje1='NO RED TEMP'

				mensaje1 = '    '

			elif tipo_list[contador2] == 'TRM':
				

				#if(status=="sent"):
				#	now = datetime.datetime.now()
				#	if now.strftime("%d") != dia_1:
				#		r2 = requests.get(url = url_cop,timeout=1) 
				#		content2 = r2.json()
				#		formatted_data_cop = abs(content2['rates']['COP'])
				#		dia_1 = now.strftime("%d")
				#	mensaje1 = 'TRM ' + str(int(formatted_data_cop))
				#else:
				#	mensaje1='NO RED TRM'

				mensaje1 = '    '


			status,response = api.insert_event(device_id,"1")
			#print(status, response)




			colorR = color_list[contador2]
			duracion = duracion_list[contador2]



			if colorR == 'Azul':
				rgb_1=[0,0,255]
			elif colorR == 'Verde':
				rgb_1=[0,255,0]
			elif colorR == 'Rojo':
				rgb_1=[255,0,0]
			elif colorR == 'Blanco':
				rgb_1=[255,255,255]
			elif colorR == 'Negro':
				rgb_1=[0,0,0]
			elif colorR == 'Cian':
				rgb_1=[0,255,255]
			elif colorR == 'Rosado':
				rgb_1=[0,0,0]
			elif colorR == 'Amarillo':
				rgb_1=[255,255,0]
			elif colorR == 'Naranja':
				rgb_1=[100,255,0]
			elif colorR == 'Morado':
				rgb_1=[255,0,255]
			elif colorR == 'Fucsia':
				rgb_1=[255,0,128]
			else:
				rgb_1=[0,255,255]

			if(status!="sent"):
				if (contador2 == 0):
					mensaje1='  ELECTROREY'
					contador2= 1
				else:
					#mensaje1='           '
					contador2= 0



			#------------

			#mensaje1 ='\x86\x87\x88\x89\x90\x91\x92\x93'
			#print(mensaje1)


			# Actualización de las pantallas y baliza

			#screen(mensaje,r,g,b,sentido,brillo,activación de barra, variable, lim_sup, lim_inf, L1, L2, L3)
			poste_pantalla_1_obj.screen(mensaje1, rgb_1[0], rgb_1[1], rgb_1[2], sentido1, brillo, activar_barra1, variable, lim_sup, lim_inf, L1, L2, L3)
			poste_pantalla_1_obj.nivel_baliza(variable, lim_sup, lim_inf, L1, L2, L3)
			poste_pantalla_2_obj.screen(mensaje1, rgb_1[0], rgb_1[1], rgb_1[2], sentido1, brillo, activar_barra1, variable, lim_sup, lim_inf, L1, L2, L3)
			poste_pantalla_2_obj.nivel_baliza(variable, lim_sup, lim_inf, L1, L2, L3)


			contador2 = contador2 + 1




			# Retardo de actualización de pantalla


			duracion = int(duracion)

			if duracion < 1:
				duracion = 1
			stop = time.time() - start
			if stop >= duracion:
				stop = 0



			time.sleep(duracion-stop)
			stop = time.time() - start
			#print(stop)


			#if stop <= 0.05:
			#    time.sleep(0.05 - stop)
		
		if(len(id_list)==1):
			contador2=0
		else:
			contador2 = 1



