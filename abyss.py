#!/usr/bin/env python

import logging
import os.path
import subprocess
import sys
import random
import abyss_languages as languages

configuration_data = {
	'dry_run'					:	True,
	'logging_streams'	:	{
		'0'	:	{
			'enabled'			:	True,
			'filepath'		:	None,
			'formatting'	: None,
			'threshold'		:	None,
			},
		'1'	:	{
			'enabled'			: True,
			'filepath'		:	'./process.log',
			'formatting'	:	"[%(lineno)s] - %(message)s",
			'threshold'		:	None
			},
		'2'	: {
			'enabled'			: True,
			'filepath'		:	'./combined_out.log',
			'formatting'	:	None,
			'threshold'		: None
		}
	}
}

def buildLogger(streams):

	logger = logging.getLogger()

	#for stream in streams:
	for stream, stream_config in streams.iteritems():

		configuration = {
			'enabled'			:	True,
			'filepath'		:	None,
			'formatting'	:	None,
			'threshold'		: None
			}

		configuration.update(stream_config)

		enabled = configuration['enabled']
		filepath = configuration['filepath']
		formatting = configuration['formatting']
		threshold = configuration['threshold']

		if not enabled:
			return

		if filepath is not None:
			#TODO: try this with invalid filepath, catch error
			handler = logging.FileHandler(filepath)
		else:
			handler = logging.StreamHandler(sys.stdout)
		
		#TODO: validate that this can run without a formatter
		if formatting:
			formatter = logging.Formatter(formatting)
			handler.setFormatter(formatter)

		logger.addHandler(handler)

		#TODO: make this tolerant of receiving no variable
		#TODO: capitalize this in case user passes lowercase value
		if threshold is None:
			threshold = 'DEBUG'
		level = logging.getLevelName(threshold)
		logger.setLevel(level)

	return logger


class Thing(object):
	def __init__(self):
		logger.debug('creating a new Thing')

		self.name = self.__class__.__name__
		self.serial = self.getSerial()
		logger.debug('creating {}'.format(self.id))

		self.incognito = False
		self.histfile = './lore.txt'

		self.language = 'gibberish'
		self.name = languages.gibberish.createName()

		logger.debug('created a new Thing: {} ({})'.format(self.name, self.id))

	@property
	def id(self):
		return str('{}_{}'.format(self.name, self.serial))

	def getSerial(self):
		logger.debug('getting serial number')
		try:
			serial = daemon.serial
			daemon.serial += 1
			logger.debug('serial is {}'.format(serial))
			logger.debug('incremented daemon serial to {}'.format(daemon.serial))
		except NameError:
			logger.debug('no daemon found, setting serial to 0')
			serial = 0

		return serial

	def writeHistory(self, raw_message):
		if not self.incognito:
			with open(self.histfile, 'ab') as histfile:
				message = str('{}{}'.format(raw_message, '\n'))
				histfile.write(message)


class Meta(object):
	def __init__(self):
		pass


class Daemon(Thing):
	def __init__(self, **kwargs):
		super(Daemon, self).__init__()
		logger.debug('instantiating a new Daemon')

		if kwargs:
			for key, value in kwargs.iteritems():
				self.key = value

		self.serial = 1

		self.incognito = False

		logger.debug('new Daemon instantiated')
		self.writeHistory('A new Daemon was created.')

	def playGame(self):
		firstBeing = Pion()
		secondBeing = Pion()
		thirdBeing = Pion()
		fourthBeing = Pion(
			language = 'gibberish',
			name = languages.gibberish.createName())


class Pion(Thing):
	def __init__(self, **kwargs):
		super(Pion, self).__init__()
		logger.info('instantiating new Pion.')
		self.writeHistory('A new Pion was created')

		self.language = 'american_english_21st_century'
		self.name = languages.american_english_21st_century.createName()

		# Overwrite defaults with explicit kwargs
		if kwargs:
			for key, value in kwargs.iteritems():
				self.key = value

		logger.debug('created a new Pion: {} ({})'.format(self.name, self.id))


if __name__ == '__main__':
	global daemon
	logger = buildLogger(configuration_data['logging_streams'])
	daemon = Daemon()
	daemon.playGame()
