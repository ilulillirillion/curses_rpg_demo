#!/usr/bin/env python
# -*- coding: utf 8 -*-

import curses
import logging

###############################################################################
##### Static Configuration ####################################################
###############################################################################
#
# All values should be relatively safe to change, so long as types are 
# maintained (strings stay strings and bools remain bools), but all
# configurations are not tested and care and troubleshooting may be necessary
# depending on the type and quantity of changes made. Changing any key names
# should be expected to cause (likely fatal) Python errors.
#
INIT_CONFIGURATION = {

	'logging': {
		'custom_levels' : {
			'history'	: {
				'name' : 'history'
			}
		},
		# Governs the number and configuration of individual logging streams. Any
		# number of streams should be supported. Although the literal key assigned
		# to a stream can be any string, strings must be unique among all streams
		# in the configuration.
		# Options:
		#
		#		enabled: Toggles stream functionality
		#		filepath: Specifies filepath for stream. If set to a stream value 
		#							('stdout', 'stderr'), will log to given stream.
		#		formattingG: Formatting string to use for stream.
		#		threshold: Threshold for the stream to start at.
		#
		'streams' : {
			'0' : {
				'enabled'			: True,
				'filepath'		: 'stdout',
				'formatting'	: None,
				'threshold'		:	None,
			}
			'1' : {
				'enabled'			: False,
				'filepath'		: None,
				'formatting'	: None,
				'threshold'		:	None,
			}
			'2' : {
				'enabled'			: False,
				'filepath'		: None,
				'formatting'	: None,
				'threshold'		:	None,
			}
			'3' : {
				'enabled'			: False,
				'filepath'		: None,
				'formatting'	: None,
				'threshold'		:	None,
			}
			'4' : {
				'enabled'			: False,
				'filepath'		: None,
				'formatting'	: None,
				'threshold'		:	None,
			}
		'logfile': 'test_logfile'
	}
}


###############################################################################
##### Static Non-Configurables ################################################
###############################################################################

STATIC_CONFIG = {

	#TODO: CONVERT TO DEDICATED FILE
	logging_stream_template = {
		'enabled'			: False,
		'filepath'		:	None,
		'formatting'	:	None,
		'threshold'		:	None
	}

###############################################################################
##### Top-Level Functions #####################################################
###############################################################################


def main(stdscr):
	"""Main module for the game. Instantiates a new game."""
	
	# Globally defines a game instance. The stdscr object MUST be passed to the
	# game instance in order to avoid errors with curses
	global game
	game = Game(stdscr)


###############################################################################
##### Classes #################################################################
###############################################################################


class Game:
	""" Game class constructor. """

	# Game instances must be handed a stdscr object (from curses) on
	# initialization to avoid curses errors.
	def __init__(self, stdscr):
		""" Game instance constructor. """

		# Set configuration values.
		self.configuration = INIT_CONFIGURATION

		# Set static configuration values.
		self..configuration._static = STATIC_CONFIG

	def initLogger(self):
		""" Instantiates the Logger object. """

		# Instantiate a logger object from the logging module.
		_logger = logging.getLogger()
	
		for _stream, _config in self.configuration

		# Define a new handler and tell it where to log events to
		_handler = logging.FileHandler(config.logfile)







###############################################################################
##### Runtime #################################################################
###############################################################################

# Executes when script is called
if __name__ == '__main__':

	# Starts everything else
	curses.wrapper(main)

