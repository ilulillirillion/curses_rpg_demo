# gibberish language module
# part of storgen project

from random import choice, randint

def createName():

	symbols = [
		'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
		'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
	]

	name = ''
	letter_count = randint(1, 25)
	#for count in letter_count:
	for count in xrange(letter_count):
		letter = choice(symbols)
		name = name + letter
	return name
