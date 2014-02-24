# -*- coding: utf-8 -*- 
import settings
import os
import random

def cls():
    os.system(['clear','cls'][os.name == 'nt'])


class Cost:
	NEGATIVE_TYPE = 1
	# NEUTRAL_TYPE = 2
	POSITIVE_TYPE = 3

	def __init__(self, cost_type, cost_value, money):
		self.type = cost_type
		self.value = float(cost_value)
		self.money = money


class Building:
	def __init__(self, name, cost):
		self.name = name
		self.cost = cost

class Game:
	def __init__(self):
		self.money = settings.MONEY
		self.positive = settings.POSITIVE
		self.neutral = settings.NEUTRAL
		self.negative = settings.MONEY

		self.science_buildings = [
			Building(u"Институт", 		Cost(Cost.POSITIVE_TYPE, 0, 0)),
			Building(u"Школа", 			Cost(Cost.POSITIVE_TYPE, 1000, 100)),
			Building(u"ПТУ", 			Cost(Cost.POSITIVE_TYPE, 1000, 150)),
			Building(u"Семя-нария", 	Cost(Cost.POSITIVE_TYPE, 1000, 200)),
			Building(u"Церковь'",		Cost(Cost.POSITIVE_TYPE, 1000, 250)),
			Building(u"Храм", 			Cost(Cost.POSITIVE_TYPE, 1000, 300)),
		]

		self.neutral_buildings = [ 
			Building(u"Больница", 		Cost(Cost.NEGATIVE_TYPE, 0, 0)),
			Building(u"Поликлиника", 	Cost(Cost.NEGATIVE_TYPE, 1000, 100)),
			Building(u"Спорт-комплекс", Cost(Cost.NEGATIVE_TYPE, 1000, 150)),
			Building(u"Живой дом", 		Cost(Cost.NEGATIVE_TYPE, 1000, 200)),
			Building(u"Кабак",			Cost(Cost.NEGATIVE_TYPE, 1000, 250)),
			Building(u"Наркопритон", 	Cost(Cost.NEGATIVE_TYPE, 1000, 300)),
		]

		self.setup_buildings()
		self.game_cycle()

	def setup_buildings(self):
		self.buildings = []
		for i in xrange(16):
			self.buildings.append(
				 self.science_buildings[0] if i > 8 else self.neutral_buildings[0]
				)
		random.shuffle(self.buildings)

	def print_buildings(self):
		i = 0
		items = []
		for build in self.buildings:
			items.append("%2d: %13s"  % (i, "[%s]" % build.name))
			i += 1
			if i % settings.PRINT_ROWS == 0:
				print " |".join(items)
				items = []


	def print_menu(self):
		# cls()
		print u"""
%5d $$

:) - %5d
:| - %5d
:( - %5d
		""" % (self.money, self.positive, self.neutral, self.negative)



	def game_cycle(self):
		to_exit = False
		while not to_exit:
			self.print_menu()
			self.print_buildings()
			index = raw_input(u"===> ")
			index = int(index)
			self.lower_build(index)


	def lower_build(self, index):
		building = self.buildings[index]
		n = self.find_next_building(building)

		if n is None:
			print u"Ошибка: Некуда уже понижать"
			return

		cost = n.cost
		
		if cost.type == Cost.POSITIVE_TYPE:
			koeff = self.neutral / (self.positive + self.neutral)
			delta = int(cost.value * koeff)
			print "n/p: %f, delta: %f" % (koeff, delta)
			if self.positive - delta < 0:
				print u"Ошибка: Закончились люди"
				return
			self.positive -= delta
			self.neutral += delta

		elif cost.type == Cost.NEGATIVE_TYPE:
			koeff = self.negative / (self.negative + self.neutral)
			delta = int(cost.value * koeff)
			print "neg/neu: %f, delta: %f" % (koeff, delta)
			if self.neutral - delta < 0:
				print u"Ошибка: Закончились люди"
				return
			self.neutral -= delta
			self.negative += delta
		self.money += cost.money

		self.buildings[index] = n

	def find_next_building(self, building):
		f = False
		for b in self.science_buildings:
			if f == True:
				return b
			if b.name == building.name:
				f = True
		f = False
		for b in self.neutral_buildings:
			if f == True:
				return b
			if b.name == building.name:
				f = True
		return None

game = Game()




