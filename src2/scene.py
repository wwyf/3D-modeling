import sys
import numpy
from node import Sphere, Cube, SnowFigure
from Lines import *

class Scene(object):
    # the default depth from the camera to place an object at
    PLACE_DEPTH = 15.0

    def __init__(self):
        # The scene keeps a list of nodes that are displayed
        self.node_list = list()
        # Keep track of the currently selected node.
        # Actions may depend on whether or not something is selected
        self.selected_node = None

    def add_node(self, node):
        """ Add a new node to the scene """
        self.node_list.append(node)
    
    def remove_node(self, node):
        """ remove an selected node from the scene """
        self.node_list.remove(node)

    def render(self):
        """ Render the scene. This function simply calls the render function for each node. """
        for node in self.node_list:
            node.render()

    def pick(self, start, direction, mat):
        """ Execute selection.
            Consume: start, direction describing a Ray
                     mat              is the inverse of the current modelview matrix for the scene """
        if self.selected_node is not None:
            self.selected_node.select(False)
            self.selected_node = None

        # Keep track of the closest hit.
        mindist = sys.maxint
        closest_node = None
        for node in self.node_list:
            hit, distance = node.pick(start, direction, mat)
            if hit and distance < mindist:
                mindist, closest_node = distance, node

        # If we hit something, keep track of it.
        if closest_node is not None:
            closest_node.select()
            closest_node.depth = mindist
            closest_node.selected_loc = start + direction * mindist
            self.selected_node = closest_node

    def move_selected(self, start, direction, inv_modelview):
        """ Move the selected node, if there is one.
            Consume:  start, direction  describes the Ray to move to
                      inv_modelview     is the inverse modelview matrix for the scene """
        if self.selected_node is None: return

        # Find the current depth and location of the selected node
        node = self.selected_node
        depth = node.depth
        oldloc = node.selected_loc

        # The new location of the node is the same depth along the new ray
        newloc = (start + direction * depth)

        # transform the translation with the modelview matrix
        translation = newloc - oldloc
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 0])
        translation = inv_modelview.dot(pre_tran)

        # translate the node and track its location
        node.translate(translation[0], translation[1], translation[2])
        node.selected_loc = newloc

    def place(self, shape, start, direction, inv_modelview):
        """ Place a new node.
            Consume:  shape             the shape to add
                      start, direction  describes the Ray to move to
                      inv_modelview     is the inverse modelview matrix for the scene """
        if self.selected_node is not None: return
        new_node = None
        if shape == 'sphere': new_node = Sphere()
        elif shape == 'cube': new_node = Cube()
        elif shape == 'figure': new_node = SnowFigure()
        elif shape == 'line':
            startPoint = Point(-1, -1, -1)
            endPoint = Point(1, 1, 1)
            new_node = Line(startPoint, endPoint)

        self.add_node(new_node)

        # place the node at the cursor in camera-space
        translation = (start + direction * self.PLACE_DEPTH)

        # convert the translation to world-space
        pre_tran = numpy.array([translation[0], translation[1], translation[2], 1])
        translation = inv_modelview.dot(pre_tran)

        new_node.translate(translation[0], translation[1], translation[2])

    def rotate_selected_color(self, forwards):
        """ Rotate the color of the currently selected node """
        if self.selected_node is None: return
        self.selected_node.rotate_color(forwards)

    def scale_selected(self, up):
        """ Scale the current selection """
        if self.selected_node is None: return
        self.selected_node.scale(up)

    ################################################v
    def scalex_selected(self, up):
        """ Scale the current selection """
        if self.selected_node is None: return
        self.selected_node.scalex(up)

    def scaley_selected(self, up):
        """ Scale the current selection """
        if self.selected_node is None: return
        self.selected_node.scaley(up)

    def scalez_selected(self, up):
        """ Scale the current selection """
        if self.selected_node is None: return
        self.selected_node.scalez(up)
    ################################################^

    def rotatex_selected(self, angle):
        """ Rotate the current selection in axis X """
        if self.selected_node is None: return
        self.selected_node.rotatex(angle)

    def rotatey_selected(self, angle):
        """ Rotate the current selection in axis Y"""
        if self.selected_node is None: return
        self.selected_node.rotatey(angle)

