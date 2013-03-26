"""
Utility classes and functions. Anything in here handles
the mathematical side of the game, mostly.
"""
from math import sqrt
import pyglet
from pyglet.gl import *
import numpy as np


def clamp(x, low, high):
    """Clamps a number between two numbers

    Args:
        x: the number to clamp
        low: the minimum value the number can have
        high: the maximum value the number can have
    Returns:
        the value of x clamped between low and high
    """
    if x < low:
        return low
    elif x > high:
        return high
    else:
        return x


def project(verts, axis):
    """Projects a shape onto an axis

    Args:
        verts: the vertices defining the shape
        axis: the axis to project the shape onto
    Returns:
        the projection of the shape onto the axis
    """
    # v_min and v_max represent the minimum and maximum
    # values of the projection
    # Start with the projection value for the first vertex
    v_min = axis.dot(verts[0])
    v_max = v_min

    # Loop over the rest of the vertices and
    # find the projection values for each
    for i in range(1, len(verts)):
        p = axis.dot(verts[i])

        # Set the new minimum or maximum, if applicable
        if p < v_min:
            v_min = p
        elif p > v_max:
            v_max = p

    return Projection(v_min, v_max)


def generate_axes(verts):
    """Generates a list of perpendicular axes for a shape

    Args:
        verts: the vertices making up the shape
    Returns:
        a list of normalized axes perpendicular to the sides
        of the shape
    """
    axes = []

    # Generate vectors for each pair of vertices
    # representing the sides
    for i in range(0, len(verts)):
        p1 = verts[i]
        if (i + 1 == len(verts)):
            p2 = verts[0]
        else:
            p2 = verts[i + 1]

        edge = p1 - p2

        # Create the vector perpendicular to the side
        # and normalize it
        normal = Vector(edge.y, -edge.x)
        normal = normal.normalize()
        axes.append(normal)
    return axes


class Vector(object):
    """Represents a vector in 2D space

    Can hold integers or floats, and supports mathematically
    valid vector operations, such as addition/subtraction, as
    well as multiplication by a scalar.

    Attributes:
        x: x component of the vector
        y: y component of the vector
    """
    def __init__(self, x, y):
        """Creates a new vector

        Args:
            x: x component of the new vector
            y: y component of the new vector
        Returns:
            a new vector (x, y)

        """
        self.x = x
        self.y = y

    def __add__(self, other):
        """Adds two vectors component-wise

        Args:
            other: The vector to add to this one
        Returns:
            a new vector representing the sum of
            'self' and 'other'
        Raises:
            TypeError: if 'other' is not a vector

        """
        newX = self.x + other.x
        newY = self.y + other.y
        return Vector(newX, newY)

    def __sub__(self, other):
        """Subtracts two vectors component-wise

        Args:
            other: The vector to subtract from this one
        Returns:
            a new vector representing the subtractions of
            'other' from 'self'
        Raises:
            TypeError: if 'other' is not a vector

        """
        newX = self.x - other.x
        newY = self.y - other.y
        return Vector(newX, newY)

    def __mul__(self, k):
        """Multiplies the vector by a scalar

        Args:
            k: the scalar to multiply the vector by
        Returns:
            a new vector representing 'self' multiplied
            by a scalar k
        Raises:
            TypeError: if k is not a number

        """
        # Ensure that k is a number
        if (isinstance(k, int) or isinstance(k, float)):
            newX = self.x * k
            newY = self.y * k
            return Vector(newX, newY)
        else:
            raise TypeError("unsupported operand type(s)" +
                            "for +: '{}' and '{}'".format(self.__class__,
                                                          type(k)))

    def __rmul__(self, k):
        """Multiplies the vector by a scalar

        Args:
            k: the scalar to multiply the vector by
        Returns:
            a new vector representing 'self' multiplied
            by a scalar k
        Raises:
            TypeError: if k is not a number

        """
        return self.__mul__(k)

    def __repr__(self):
        """Converts the vector to a string representation

        Returns:
            a string representation of the vector

        """
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __str__(self):
        """Converts the vector to a string representation

        Returns:
            a string representation of the vector

        """
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def to_tuple(self):
        """Converts the vector to a tuple representation

        Returns:
            a tuple representing the vector

        """
        return (self.x, self.y)

    def to_list(self):
        """Converts the vector to a list representation

        Returns:
            a list representing the vector

        """
        return [self.x, self.y]

    def length(self):
        """Gets the length of the vector

        Returns:
            the length of the vector

        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Returns a normalized version of this vector,
        which maintains the same direction but has length 1

        Returns:
            a normalized vector pointing in the same direction
            as this one
        """
        length = self.length()
        if length == 0.0:
            return self

        # Note that length is a float, so we don't need a type conversion
        # even if x and y are ints
        new_x = self.x / length
        new_y = self.y / length
        return Vector(new_x, new_y)

    def dot(self, other):
        """Returns the dot product of this vector and another

        Args:
            other: another vector
        Returns:
            the dot product of the two vectors

        """
        return (self.x * other.x) + (self.y * other.y)

    @staticmethod
    def Zero():
        """Gets an empty vector (0, 0)

        Returns:
            the zero vector (0, 0)
        """
        return Vector(0, 0)

    def toMatrix(self):
        return np.matrix([[self.x], [self.y], [0], [1]])


class Projection(object):
    """Represents a 1-dimensional projection onto an axis, with
    a minimum and maximum value to represent it

    Attributes:
        minimum: the low-value of the projection
        maximum: the high-value of the projection
    """
    def __init__(self, minimum, maximum):
        """Creates a new Projection

        Args:
            minimum: the low-value of the projection
            maximum: the high-value of the projection
        Returns:
            a new Projection
        """
        self.minimum = minimum
        self.maximum = maximum

    def overlaps(self, other):
        """Checks if this projection overlaps another

        Args:
            other: the other projection to check for overlap
        Returns:
            True if the two projections overlap, False if they do not
        """
        return (self.minimum <= other.maximum) and \
               (other.minimum <= self.maximum)


class Shape(object):
    """Represents a closed geometric shape in 2D space

    Stores the vertices of the shape as wellas a list of indices.
    Also contains a draw method for drawing the shape to the screen,
    accounting for position, rotation, and scale.

    The vertices are stored as a tuple to ensure immutability of
    the vertices.

    Attributes:
        __verts: a tuple defining the vertices of the shape
        __num_verts: the number of vertices defining the shape
        __indices: the indices defining how to draw the shape
    """

    def __init__(self, verts, pos, rot, scale):
        """Creates a new drawable shape

        Args:
            verts: a tuple of numbers which define the vertices of
                   the shape (every 2 numbers makes up a vertex)
        Returns:
            a new Shape

        """
        self.__verts = tuple(verts)
        self.__num_verts = len(verts) // 2
        self.__indices = self.__gen_indices()
        self.pos = pos
        self.rot = rot
        self.scale = scale

    def __gen_indices(self):
        """Generates the indices for the shape
        Because the shape is closed, we want the indices to
        follow a pattern similar to [0, 1, 1, 2, 2, 0]. This
        method generates such a list.

        """
        indices = []

        # Generate the indices based on a pattern like
        # [0, 1, 1, 2, 2, 3, 3, 0]:
        # For i = 0 we just add 0 to start, and from there just append
        # two instances of i
        # For the last index, we also append an extra 0 to close the shape
        for i in range(0, self.__num_verts):
            if i == 0:
                indices.append(0)
            elif i == self.__num_verts - 1:
                indices.extend([i, i, 0])
            else:
                indices.extend([i, i])

        return indices

    def collides(self, other):
        """Checks if this shape collides with another

        Args:
            other: the shape to test collision against
        Returns:
            True if the two shapes collide, False if they do not
        """
        # First grab the transformed (world-space) vertices of each shape
        # Then, grab the axes, which are normalized vectors perpendicular
        # to each side
        verts1 = self.__get_transformed_verts()
        verts2 = other.__get_transformed_verts()
        axes1 = generate_axes(verts1)
        axes2 = generate_axes(verts2)

        # Loop over each set of axes, and project both shapes onto each axis
        # If they don't overlap on the axis, the shapes do not collide
        for axis in axes1:
            proj1 = project(verts1, axis)
            proj2 = project(verts2, axis)

            if not proj1.overlaps(proj2):
                return False

        for axis in axes2:
            proj1 = project(verts1, axis)
            proj2 = project(verts2, axis)

            if not proj1.overlaps(proj2):
                return False

        # If we got this far, the shapes overlap on each axis,
        # and the shapes collide
        return True

    def __gen_vectors(self):
        """Converts the tuple of vertex values for this shape
        into a list of vectors

        Returns:
            a list of vectors defining the shape
        """
        vectors = []

        # Every 2 values in the __verts list represents a vector.
        # This for loop turns each pair of verts into vectors
        for i in range(0, len(self.__indices), 2):
            vectors.append(Vector(self.__verts[i], self.__verts[i + 1]))
        return vectors

    def __get_model_view(self):
        """Grabs the model view matrix based on the
        current state of the shape.

        Returns:
            the model view matrix for this shape
        """
        # Use OpenGL commands to generate the model-view matrix,
        # based on position, rotation, and scale values
        glLoadIdentity()
        glTranslatef(self.pos.x, self.pos.y, 0.0)
        glRotatef(self.rot, 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)

        # Now we grab the model view matrix and store it in
        # an array of GLfloat's
        float_arr = (GLfloat * 16)()
        glGetFloatv(GL_MODELVIEW_MATRIX, float_arr)

        # The final step is to convert the array of floats into
        # a NumPy matrix. We convert the values to a list to
        # construct the matrix, and then resize it to a 4x4 matrix.
        # We need to take the transpose to get the matrix in the
        # correct orientation
        mv = np.matrix(list(float_arr))
        mv.resize((4, 4))
        mv = mv.transpose()
        return mv

    def __get_transformed_verts(self):
        """Gets the transformed vertices of the shape

        Returns:
            the vertices of the object, in world-space
        """
        # Grab the model view matrix and the non-transformed
        # vertices of the objects as vectors
        mv = self.__get_model_view()
        verts = self.__gen_vectors()

        # For each vertex, convert it to a matrix and then
        # multiply by the model-view matrix
        # Then, transform it back into a vector and store it in
        # the list
        transVerts = []
        for vert in verts:
            v_m = vert.toMatrix()
            v_m = mv * v_m
            v_t = Vector(v_m[0, 0], v_m[1, 0])
            transVerts.append(v_t)

        return transVerts

    def draw(self):
        """Draws the shape onto the screen"""
        # Start with the identity matrix and then load in
        # the transformation matrices
        glLoadIdentity()
        glTranslatef(self.pos.x, self.pos.y, 0.0)
        glRotatef(self.rot, 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)

        # Draw the lines that make up the shape
        # Use the 'v2f' format in case we're using vertices with floats
        pyglet.graphics.draw_indexed(self.__num_verts, GL_LINES,
                                     self.__indices, ('v2f', self.__verts))
