import datetime
import math
import sys
from glfw.GLFW import *
import random

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def square(x, y, a, b, d, tab):


    halfA = a/2
    halfB = b/2

    glBegin(GL_QUADS)

    glColor3f(tab[0][0], tab[0][1], tab[0][2])
    glVertex2f(x - d-d-halfA, y - d-d-halfB)
    glColor3f(tab[1][0], tab[1][1], tab[1][2])
    glVertex2f(x + halfA - d-d, y - halfB +d)
    glColor3f(tab[2][0], tab[2][1], tab[1][2])
    glVertex2f(x + d+d+halfA, y + d+d+halfB)
    glColor3f(tab[3][0], tab[3][1], tab[1][2])
    glVertex2f(x - halfA +d, y + halfB -d)

    glEnd()

def render(time, a, tab):
    glClear(GL_COLOR_BUFFER_BIT)
    #random.seed()

    square(0, 0, 50, 50, a, tab)



    #triangle()
    glFlush()


def main():
    random.seed()
    a = 0


    if not glfwInit():
        sys.exit(-1)
    raisin = True
    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(5)

    random.seed()

    rows, cols = (4, 3)
    tab = [[random.randrange(0, 100) / 100 for _ in range(cols)] for _ in range(rows)]



    startup()
    while not glfwWindowShouldClose(window):
        if raisin:
            if a==50:
                raisin = False
            else:
                a += 1
        elif not raisin:
            if a==-50:
                raisin = True
            else: a-=1

        render(glfwGetTime(),  a, tab)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == '__main__':
    main()
