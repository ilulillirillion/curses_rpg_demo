# -*- coding: utf-8 -*-
# low-cavish language module
# part of storgen project

import random

# letters as tuples -- 1: letter; 2: commonality; 3: commonality weight
#vowels = [
#	( 'a', 100, 100 ),
#	( 'i', 'e', 100, 100 ),
#	( 'ʉ', 'u', 100, 100 ),
#]
#consonants = [
#	( 'b', 100, 100 ),
#	( 'd', 100, 100 ),
#	( 'j', 100, 100 ),
#	( 'n', 100, 100 ),
#	( 's', 100, 100 ),
#	( 'v', 100, 100 ),
#	( 'y', 100, 100 )
#]


class Sound():
	def __init__(self,
		phonetic,
		written,
		category):

		self.phonetic = phonetic
		self.written = written
		self.category = category

#vowels = [
#	( 'a', 'a', 100, 100 ),
#  ( 'i', 'i', 100, 100 ),
#  ( 'ʉ', 'u', 100, 100 ),
#	( 'ə', 'u', 100, 100 )
#]

#consonants = [
#	( 'b', 'b', 100, 100 ),
#	( 'd', 'd', 100, 100 ),
#	( 'n', 'n', 100, 100 ),
#	( 'ʈ͡ʂ', 't', 100, 100 ), 
#	( 'z', 'z', 100, 100 )
#]


#sounds = [
#	( 'a', 'a', 'vowel', 100, 100 ),
#	( 'b', 'b', 'consonant', 100, 100 ),
#	( 'd', 'd', 'consonant', 100, 100 ),
# ( 'i', 'i', 'vowel', 100, 100 ),
#	( 'n', 'n', 'consonant', 100, 100 ),
#	( 'ʈ͡ʂ', 't', 'consonant', 100, 100 ), 
# ( 'ʉ', 'u', 'vowel', 100, 100 ),
#	( 'ə', 'u', 'vowel', 100, 100 ),
#	( 'z', 'z', 'consonant', 100, 100 )
#]

sounds = [
	Sound( 'a', 'a', 'vowel' ),
	Sound( 'b', 'b', 'consonant' ),
	Sound( 'd', 'd', 'consonant' ),
	Sound( 'i', 'i', 'vowel' ),
	Sound( 'n', 'n', 'consonant' ),
	Sound( 'ʉ', 'u', 'vowel' ),
	Sound( 'ə', 'u', 'vowel' ),
	Sound( 'z', 'z', 'consonant' )
]



def createName():

	name_phonetic = ''
	name_written = ''
	sound_count = random.randint(1, 8)
	for count in xrange(sound_Count):

		sound = random.choice(sounds)
		#sound_phonetic = sound[0]
		#sound_written = sound[1]
		#sound_type = sound[2]
		name_phonetic = sound.phonetic
		name_written = written.phonetic

		return (name_phonetic, name_written)

		

		
	
		#if sound_count == 1 and count == 1 and sound_type == 'consonant':




	#for count in letter_count:
	choices = [ 'vowel', 'consonant' ]
	for count in xrange(sound_count):
		choice = random.choice(choices)
		if sound_count == 1:
			choice == 'vowel'
		if choice == 'vowel':
			sound_type = 'vowel'
			sound = random.choice(vowels)
			sound_phonetic = sound[0]
			sound_written = sound[1]
		elif choice == 'consonant':
			sound = random.choice(consonants)
			sound_type = 'consonant'
			sound_phonetic = sound[0]


	return name

