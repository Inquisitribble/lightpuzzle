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

class LightPuzzleMirrorOrientation(Enum)
	NONE = 1
	NORTH = 2
	EAST = 3
	SOUTH = 4
	WEST = 5
	UP = 6
	DOWN = 7

class LightPuzzleNode:
	allow_north = true
	allow_east = true
	allow_south = true
	allow_west = true
	allow_up = true
	allow_down = true
	is_light_source = false
	has_mirror = false
	node_mirror_orientation = LightPuzzleMirrorOrientation.NONE
	is_beam_splitter = false

	def __init__(self, allow_north, allow_east, allow_south, allow_west, allow_up, allow_down, is_light_source, has_mirror, initial_mirror_orientation, is_beam_splitter):
		self.allow_north = allow_north
		self.allow_east = allow_east
		self.allow_south = allow_south
		self.allow_west = allow_west
		self.allow_up = allow_up
		self.allow_down = allow_down
		self.is_light_source = is_light_source
		self.has_mirror = has_mirror
		self.node_mirror_orientation = initial_mirror_orientation
		self.is_beam_splitter = is_beam_splitter
