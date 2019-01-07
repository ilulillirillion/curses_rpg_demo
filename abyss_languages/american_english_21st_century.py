from random import choice, randint

MALE_NAMES_FILEPATH = 'abyss_languages/data/american_english_21st_century_male_names'

#male_names_file = open(MALE_NAMES_FILEPATH, 'r')
#male_names = [line.split(',') for line in male_names_file.readlines()]
with open(MALE_NAMES_FILEPATH) as f:
	male_names = [str(name) for name in f.read().split()]

def createName():

	name = choice(male_names)
	return name
