import sys
from glfw.GLFW import *
import random
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def startup():
    update_viewport(None, 900, 900)
    #glClearColor(0.5, 0.5, 0.5, 1.0)
    glClearColor(1.0, 1.0, 1.0, 1.0)


def shutdown():
    pass


def triangle2(x, tab):
    sqt = math.sqrt(3)
    x1 = -x
    x2 = x
    x3 = (x1 + x2) / 2
    y1 = (x1 / 2) * sqt
    y2 = (x1 / 2) * sqt
    y3 = (x2 / 2) * sqt
    rektriangle(x1, y1, x2, y2, x3, y3, tab)
    rekur2(x1, y1, x2, y2, x3, y3, tab)



def rekur2(x1, y1, x2, y2, x3, y3, tab):
    if x2 - x1 > 10:
        rektriangle((x1 + x2) / 2, y1, (x2 + x3) / 2, (y2 + y3) / 2, (x1 + x3) / 2, (y1 + y3) / 2, 0)
        rekur2((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, x2 - ((x2 - x1) / 4), (y1 + y3) / 2, tab)
        rekur2(x1 + ((x2 - x1) / 4), (y1 + y3) / 2, x2 - ((x2 - x1) / 4), (y1 + y3) / 2, (x1 + x2) / 2, y3, tab)
        rekur2(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2, x1 + ((x2 - x1) / 4), (y1 + y3) / 2, tab)



def triangle1(x, tab):
    sqt = math.sqrt(3)
    x1=-x
    x2=x
    x3=(x1+x2)/2
    y1=(x1/2)*sqt
    y2=(x1/2)*sqt
    y3=(x2/2)*sqt
    rekur1(x1, y1, x2, y2, x3, y3, tab)

def rektriangle(x1, y1, x2, y2, x3, y3, tab):
    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 0.0, 0.0)
    if tab !=0:
        glColor3f(tab[0][0], tab[0][1], tab[0][2])
    else:
        glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x1, y1)
  #  glColor3f(0.0, 0.0, 1.0)
    if tab != 0:
        glColor3f(tab[1][0], tab[1][1], tab[1][2])
    else:
        glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x2, y2)
  #  glColor3f(0.0, 1.0, 0.0)
    if tab != 0:
        glColor3f(tab[2][0], tab[2][1], tab[2][2])
    else:
        glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x3, y3)
    glEnd()


def rekur1(x1, y1, x2, y2, x3, y3, tab):

    #print("Vertexes: ", x1, y1, x2, y2, x3, y3)

    if x2 - x1 > 1000:
        rekur1((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, x2 - ((x2 - x1) / 4), (y1 + y3) / 2, tab)
        rekur1(x1 + ((x2 - x1) / 4), (y1 + y3) / 2, x2 - ((x2 - x1) / 4), (y1 + y3) / 2, (x1 + x2) / 2, y3, tab)
        rekur1(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2, x1 + ((x2 - x1) / 4), (y1 + y3) / 2, tab)
    else:
        rektriangle(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2, x1 + ((x2 - x1) / 4), (y1 + y3) / 2, tab)
        rektriangle((x1 + x2) / 2, (y1 + y2) / 2, x2, y2, x2 - ((x2 - x1) / 4), (y1 + y3) / 2, tab)
        rektriangle(x1 + (x2 - x1) / 4, (y1 + y3) / 2, x2 - (x2 - x1) / 4, (y1 + y3) / 2, (x1 + x2) / 2, y3, tab)



def render(time, tab):
    glClear(GL_COLOR_BUFFER_BIT)
    #square(0, 0, 300, 300)
    triangle1(300, tab)

    triangle2(300, tab)

    #rekur(0, 0, 300, 300)
    #triangle()
    glFlush()


def main():
    random.seed()
    if not glfwInit():
        sys.exit(-1)

    rows, cols = (3, 3)

    tab = [[random.randrange(0, 100) / 100 for _ in range(cols)] for _ in range(rows)]


    window = glfwCreateWindow(900, 900, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), tab)
        glfwSwapBuffers(window)
        glfwWaitEvents()
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
        glOrtho(-450.0, 450.0, -450.0 / aspectRatio, 450.0 / aspectRatio,1.0, -1.0)
    else:
        glOrtho(-450.0 * aspectRatio, 450.0 * aspectRatio, -450.0, 450.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == '__main__':
    main()
