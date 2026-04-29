from enum import Enum
from colorutils import Color
import networkx 

class LightPuzzleDirections(Enum):
	NONE = 0x00
	NORTH = 0x01
	EAST = 0x02
	NORTH_AND_EAST = 0x03
	SOUTH = 0x04
	SOUTH_AND_NORTH = 0x05
	SOUTH_AND_EAST = 0x06
	SOUTH_AND_NORTH_AND_EAST = 0x07
	WEST = 0x08
	WEST_AND_NORTH = 0x09
	WEST_AND_EAST = 0x0A
	WEST_AND_NORTH_AND_EAST = 0x0B
	WEST_AND_SOUTH = 0x0C
	WEST_AND_SOUTH_AND_NORTH = 0x0D
	WEST_AND_SOUTH_AND_EAST = 0x0E
	WEST_AND_SOUTH_AND_NORTH_AND_EAST = 0x0F
	UP = 0x010
	UP_AND_NORTH = 0x011
	UP_AND_EAST = 0x012
	UP_AND_NORTH_AND_EAST = 0x013
	UP_AND_SOUTH = 0x014
	UP_AND_SOUTH_AND_NORTH = 0x015
	UP_AND_SOUTH_AND_EAST = 0x016
	UP_AND_SOUTH_AND_NORTH_AND_EAST = 0x017
	UP_AND_WEST = 0x018
	UP_AND_WEST_AND_NORTH = 0x019
	UP_AND_WEST_AND_EAST = 0x01A
	UP_AND_WEST_AND_NORTH_AND_EAST = 0x01B
	UP_AND_WEST_AND_SOUTH = 0x01C
	UP_AND_WEST_AND_SOUTH_AND_NORTH = 0x01D
	UP_AND_WEST_AND_SOUTH_AND_EAST = 0x01E
	UP_AND_WEST_AND_SOUTH_AND_NORTH_AND_EAST = 0x01F
	DOWN = 0x020
	DOWN_AND_NORTH = 0x021
	DOWN_AND_EAST = 0x022
	DOWN_AND_NORTH_AND_EAST = 0x023
	DOWN_AND_SOUTH = 0x024
	DOWN_AND_SOUTH_AND_NORTH = 0x025
	DOWN_AND_SOUTH_AND_EAST = 0x026
	DOWN_AND_SOUTH_AND_NORTH_AND_EAST = 0x027
	DOWN_AND_WEST = 0x028
	DOWN_AND_WEST_AND_NORTH = 0x029
	DOWN_WEST_AND_EAST = 0x02A
	DOWN_WEST_AND_NORTH_AND_EAST = 0x02B
	DOWN_WEST_AND_SOUTH = 0x02C
	DOWN_WEST_AND_SOUTH_AND_NORTH = 0x02D
	DOWN_WEST_AND_SOUTH_AND_EAST = 0x02E
	DOWN_WEST_AND_SOUTH_AND_NORTH_AND_EAST = 0x02F
	DOWN_AND_UP = 0x030
	DOWN_AND_UP_AND_NORTH = 0x031
	DOWN_AND_UP_AND_EAST = 0x032
	DOWN_AND_UP_AND_NORTH_AND_EAST = 0x033
	DOWN_AND_UP_AND_SOUTH = 0x034
	DOWN_AND_UP_AND_SOUTH_AND_NORTH = 0x035
	DOWN_AND_UP_AND_SOUTH_AND_EAST = 0x036
	DOWN_AND_UP_AND_SOUTH_AND_NORTH_AND_EAST = 0x037
	DOWN_AND_UP_AND_WEST = 0x038
	DOWN_AND_UP_AND_WEST_AND_NORTH = 0x039
	DOWN_AND_UP_AND_WEST_AND_EAST = 0x03A
	DOWN_AND_UP_AND_WEST_AND_NORTH_AND_EAST = 0x03B
	DOWN_AND_UP_AND_WEST_AND_SOUTH = 0x03C
	DOWN_AND_UP_AND_WEST_AND_SOUTH_AND_NORTH = 0x03D
	DOWN_AND_UP_AND_WEST_AND_SOUTH_AND_EAST = 0x03E
	DOWN_AND_UP_AND_WEST_AND_SOUTH_AND_NORTH_AND_EAST = 0x03F
	ALL = 0x03F

class LightPuzzleInsertType(Enum):
	NONE = 1
	SPLITTER = 2
	LIGHT_SOURCE = 3
	COLOR_CRYSTAL = 4
	COLOR_FILTER = 5
	RECEIVER = 6
	WALL = 7

class NodeAllowedDirections:
	def __init__(self, allowedDirections):
		if not isinstance(allowedDirections, LightPuzzleDirections):
			raise TypeError('Invalid insert orientation')

		self.allowed_directions = allowedDirections

	def directionIsAllowed(self, direction):
		return (self.allowed_directions.value & direction.value) != 0

class LightPuzzleNodeInsert:
	def __init__(self, insert_orientation=LightPuzzleDirections.NONE, insert_color=Color(web='WHITE'), insert_type=LightPuzzleInsertType.NONE):
		if isinstance(insert_orientation, LightPuzzleDirections):
			self.insert_orientation = insert_orientation
		else:
			raise TypeError('Invalid insert orientation')

		if isinstance(insert_color, Color):
			self.insert_color = insert_color
		else:
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

class LightPuzzle:
	def __init__(self, max_x=0, max_y=0, max_z=0):
		self.max_x = max_x
		self.max_y = max_y
		self.max_z = max_z
		self.nodes = {}
		self.is_finalized = False
		self.graph = networkx.DiGraph()

	def addNode(self, coordinates, node=None):
		if self.is_finalized:
			raise RuntimeError('Puzzle has been finalized, no further additions may be made.')

		if coordinates is not None and isinstance(coordinates, tuple) and len(coordinates) == 3:
			if coordinates[0] > self.max_x:
				raise ValueError('x value ' + str(coordinates[0]) + ' is out of bounds.')
			if coordinates[1] > self.max_y:
				raise ValueError('y value ' + str(coordinates[1]) + ' is out of bounds.')
			if coordinates[2] > self.max_z:
				raise ValueError('z value ' + str(coordinates[2]) + ' is out of bounds.')
		else:
			raise TypeError('Invalid coordinates provided.')

		if node is not None:
			if not isinstance(node, LightPuzzleNode):
				raise TypeError('Invalid puzzle node provided.')
			else:
				try:
					if self.nodes[coordinates] is not None:
						raise ValueError('Coordinates ' + str(coordinates) + ' is already occupied.')
				except KeyError:
					self.nodes[coordinates] = node

	def finalize(self):
		self.is_finalized = True

	def generateGraph(self):
		#check for coordinates co-linear along the X axis
		for y in range(0, max_y):
			for z in range(0, max_z):
				candidate_node = None
				for x in range(0, max_x):
					try:
						node = self.nodes[(x, y, z)]
						if node is not None:
							if node[1].directionIsAllowed(LightPuzzleDirections.NORTH):
								if candidate_node is None:
									candidate_node = node
									continue
								else:
									if candidate_node[1].directionIsAllowed(LightPuzzleDirections.NORTH):
										graph.add_edge(node, candidate_node)
					except KeyError:
						pass

		#check for coordinates co-linear along the Y axis
		for z in range(0, max_y):
			for x in range(0, max_z):
				candidate_node = None
				for y in range(0, max_x):
					try:
						node = self.nodes[(x, y, z)]
						if node is not None:
							if node[1].directionIsAllowed(LightPuzzleDirections.EAST):
								if candidate_node is None:
									candidate_node = node
									continue
								else:
									if candidate_node[1].directionIsAllowed(LightPuzzleDirections.WEST):
										graph.add_edge(node, candidate_node)
					except KeyError:
						pass

		#check for coordinates co-linear along the Z axis
		for x in range(0, max_x):
			for y in range(0, max_y):
				candidate_node = None
				for z in range(0, max_z):
					try:
						node = self.nodes[(x, y, z)]
						if node is not None:
							if node[1].directionIsAllowed(LightPuzzleDirections.UP):
								if candidate_node is None:
									candidate_node = node
									continue
								else:
									if candidate_node[1].directionIsAllowed(LightPuzzleDirections.DOWN):
										graph.add_edge((node, candidate_node))
					except KeyError:
						pass
	
	def subGraphIsSolvable(self, current_node, receivers):
		for successor in self.graph.successors(current_node):
			if successor in receivers:
				return True
			return subGraphIsSolvable(successor, receivers)
		return False

	def isSolvable(self):
		light_sources = []
		receivers = []
		for node in list(self.graph):
			if node[1].insert_type is LightPuzzleInsertType.LIGHT_SOURCE:
				light_sources.append(node)
			elif node[1].insert_type is LightPuzzleInsertType.RECEIVER:
				receivers.append(node)

		if not light_sources or not receivers:
			return False

		for light_source in light_sources:
			if subGraphIsSolvable(light_source, receivers):
				return True

		return False


def test_allowedDirections():
	for currentDirection in range(LightPuzzleDirections.NONE.value, LightPuzzleDirections.ALL.value):
		directions = LightPuzzleDirections(currentDirection)
		allowed_directions = NodeAllowedDirections(directions)

		allow_north = directions.value & LightPuzzleDirections.NORTH.value
		allow_east = directions.value & LightPuzzleDirections.EAST.value
		allow_south = directions.value & LightPuzzleDirections.SOUTH.value
		allow_west = directions.value & LightPuzzleDirections.WEST.value
		allow_up = directions.value & LightPuzzleDirections.UP.value
		allow_down = directions.value & LightPuzzleDirections.DOWN.value

		if allow_north:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.NORTH)
		if allow_east:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.EAST)
		if allow_south:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.SOUTH)
		if allow_west:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.WEST)
		if allow_up:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.UP)
		if allow_down:
			assert allowed_directions.directionIsAllowed(LightPuzzleDirections.DOWN)