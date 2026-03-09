from enum import Enum

class LightPuzzleColor(Enum):
	NONE = 1
	WHITE = 2
	BLACK = 3
	RED = 4
	GREEN = 5
	BLUE = 6
	YELLOW = 7
	MAGENTA = 8
	CYAN = 9

class LightPuzzleDirections(Enum)
	NONE = 0x00
	NORTH = 0x01
	EAST = 0x02
	SOUTH = 0x04
	WEST = 0x08
	UP = 0x010
	DOWN = 0x020

class NodeAllowedDirections:
	def __init__(self):
		self.allowed_directions = 0x00

	def __init__(self, allow_north, allow_east, allow_south, allow_west, allow_up, allow_down):
		self()

		if (allow_north):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.NORTH

		if (allow_east):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.EAST

		if (allow_south):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.SOUTH

		if (allow_west):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.WEST

		if (allow_up):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.UP

		if (allow_down):
			self.allowed_directions = allowed_directions | LightPuzzleDirections.DOWN

	def directionIsAllowed(self, direction):
		return (self.allowed_directions & direction) != 0

class LightPuzzleNodeInsert:
	def __init__(self, mirror_orientation, is_beam_splitter):
		self.mirror_orientation = mirror_orientation
		self.is_beam_splitter = is_beam_splitter

	def __init__(self)
		self.mirror_orientation = LightPuzzleDirections.NONE
		self.is_beam_splitter = is_beam_splitter

class LightPuzzleNode:
	is_light_source = false
	has_mirror = false
	node_mirror_orientation = LightPuzzleDirections.NONE
	is_beam_splitter = false

	def __init__(self, allow_north, allow_east, allow_south, allow_west, allow_up, allow_down, is_light_source, has_mirror, initial_mirror_orientation, is_beam_splitter):
		self.allowed_directions = NodeAllowedDirections(allow_east, allow_north, allow_south, allow_west, allow_up, allow_down)
		self.is_light_source = is_light_source
		self.has_mirror = has_mirror
		self.node_mirror_orientation = initial_mirror_orientation
		self.is_beam_splitter = is_beam_splitter

	def __init__(self, allowed_directions, is_light_source, has_mirror, initial_mirror_orientation, is_beam_splitter)
		if isinstance(allowed_directions, NodeAllowedDirections):
			self.allowed_directions = allowed_directions
		else:
			raise TypeError('Invalid allowed directions')
		self.is_light_source = is_light_source
		self.has_mirror = has_mirror
		self.node_mirror_orientation = initial_mirror_orientation
		self.is_beam_splitter = is_beam_splitter

#TODO: Implement light propagation logic
#TODO: Implement color combination logic

class LightPuzzle:
	nodes = []

#TODO: Figure out what should all go into the constructor here
#TODO: Add functions to easily add nodes
#TODO: Add function to check if the puzzle is solved