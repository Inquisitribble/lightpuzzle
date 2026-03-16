from enum import Enum
from colorutils inport Color

class LightPuzzleDirections(Enum):
	NONE = 0x00
	NORTH = 0x01
	EAST = 0x02
	SOUTH = 0x04
	WEST = 0x08
	UP = 0x010
	DOWN = 0x020

class LightPuzzleInsertType(Enum):
	NONE = 1
	SPLITTER = 2
	LIGHT_SOURCE = 3
	COLOR_CRYSTAL = 4
	COLOR_FILTER = 5
	RECEIVER = 6

class NodeAllowedDirections:
	def __init__(self, allow_north=False, allow_east=False, allow_south=False, allow_west=False, allow_up=False, allow_down=False):
		self.allowed_directions = 0x00

		if allow_north:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.NORTH

		if allow_east:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.EAST

		if allow_south:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.SOUTH

		if allow_west:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.WEST

		if allow_up:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.UP

		if allow_down:
			self.allowed_directions = allowed_directions | LightPuzzleDirections.DOWN

	def directionIsAllowed(self, direction):
		return (self.allowed_directions & direction) != 0

class LightPuzzleNodeInsert:
	def __init__(self, insert_orientation=LightPuzzleDirections.NONE, insert_color=Color(web='WHITE'), insert_type=LightPuzzleInsertType.NONE):
		if isinstance(insert_orientation, LightPuzzleDirections):
			self.insert_orientation = insert_orientation
		else
			raise TypeError('Invalid insert orientation')

		if isinstance(insert_color, Color):
			self.insert_color = insert_color
		else
			raise TypeError('Invalid insert color')

		if isinstance(insert_type, LightPuzzleInsertType):
			self.insert_type = insert_type
		else:
			raise TypeError('Invalid insert type')

	def combineColors(self, incoming_color):
		if not isinstance(incoming_color, Color):
			raise TypeError('Invalid colors provided')

		match self.insert_type:
			case LightPuzzleInsertType.COLOR_CRYSTAL:
				if self.insert_color is Color(web='WHITE'):
					return incoming_color
				return self.insert_color + incoming_color
			case LightPuzzleInsertType.COLOR_FILTER:
				return self.insert_color - incoming_color
			case _:
				return incoming_color

class LightPuzzleNode:
	def __init__(self, allowed_directions, insert):
		if isinstance(allowed_directions, NodeAllowedDirections):
			self.allowed_directions = allowed_directions
		else:
			raise TypeError('Invalid allowed directions')

		if isinstance(insert, LightPuzzleNodeInsert):
			self.insert = LightPuzzleNodeInsert
		elif insert is not None:
			raise TypeError('Invalid allowed directions')

		self.insert = LightPuzzleNodeInsert(insert_orientation, insert_color, insert_type)

#TODO: Implement light propagation logic

class LightPuzzle:
	nodes = []

#TODO: Figure out what should all go into the constructor here
#TODO: Add functions to easily add nodes
#TODO: Add function to check if the puzzle is solved