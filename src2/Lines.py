#-*- coding:utf-8 -*-
from primitive import G_OBJ_CUBE, G_OBJ_SPHERE
from transformation import scaling, translation
from color import *
import random
from node import Primitive

from OpenGL.GL import glBegin, glColor3f, glEnd, glEndList, glLineWidth, glNewList, glNormal3f, glVertex3f, \
                      GL_COMPILE, GL_LINES, GL_QUADS
from OpenGL.GLU import gluDeleteQuadric, gluNewQuadric, gluSphere


class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def raw(self):
        return (self.x, self.y, self.z)

class Line(Primitive):
    def __init__(self, startpoint, endpoint, color = None):
        super(Line, self).__init__()

        self.startpoint = startpoint
        self.endpoint = endpoint
        if color is not None:
            self.color_index = color
        else:
            self.color_index = random.randint(MIN_COLOR, MAX_COLOR)

    def render_self(self):
        glLineWidth(8)
        glBegin(GL_LINES)
        glColor3f(*COLORS[self.color_index])
        glVertex3f(*self.startpoint.raw())
        glVertex3f(*self.endpoint.raw())
        glEnd()
    def show():
        '''
        画线的代码
        '''
    def hide():
        '''
        隐藏线的代码
        '''
    def changeColor(color):
        self.color = color
    def changePoint1(point):
        self.point1 = point
    def changePoint2(point):
        self.point2 = point

class drawLine():
    def __init__(self, line):
        self.line = line
    def do():
        line.show()
    def undo():
        line.hide()

class changeLineColor():
    def __init__(self, line, color):
        self.line = line
        self.oldColor = line.color
        self.newColor = color
    def do():
        line.hide()
        line.changeColor(self.newColor)
        line.show()
    def undo():
        line.hide()
        line.changeColor(self.oldColor)
        line.show()

class changeLinePoint1():
    def __init__(self, line, point):
        self.line = line
        self.oldPoint = line.point1
        self.newPoint = point
    def do():
        line.hide()
        line.changePoint1(oldPoint)
        line.show()
    def undo():
        line.hide()
        line.changePoint1(newPoint)
        line.show()

class changeLinePoint2():
    def __init__(self, line, point):
        self.line = line
        self.oldPoint = line.point2
        self.newPoint = point
    def do():
        line.hide()
        line.changePoint2(oldPoint)
        line.show()
    def undo():
        line.hide()
        line.changePoint2(newPoint)
        line.show()

if __name__ == '__main__':
    revoke = []         #撤销栈
    redo = []           #重做栈
    # while (command = input('>> ')) != 'exit':
    #     if command == 'undo':
    #         operation = revoke.pop()
    #         operation.undo()
    #         redo.append(operation)
    #     elif command == 'redo':
    #         operation = redo.pop()
    #         operation.do()
    #         revoke.append(operation)
    #     else:
    #         if command == 'drawLine':
    #             x1 = int(input('x1 = '))
    #             y1 = int(input('y1 = '))
    #             z1 = int(input('z1 = '))
    #             x2 = int(input('x2 = '))
    #             y2 = int(input('y2 = '))
    #             z2 = int(input('z2 = '))
    #             color = input('color = ')
    #             line = line(x1, y1, z1, x2, y2, z2, color)
    #             operation = drawLine(line)
    #         elif command == 'changeLineColor':
    #             color = input('new color = ')
    #             operation = changeLineColor(line, color)
    #         redo.clear()
    #         operation.do()
    #         revoke.append(operation)


