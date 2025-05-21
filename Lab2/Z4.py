import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 900, 900)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def rekur(x, y, a, b, tab):
    addons = [-a, 0, a]
    if a>10:
        for i in addons:
            for j in addons:
                if not (i==j==0):
                    square(x + i, y + j, a, b, 0, tab)
                    rekur(x + i, y + j, a / 3, b / 3, tab)
                else:
                    square(x + i, y + j, a, b, 1, tab)





def square(x, y, a, b, c, tab):
    halfA = a/2
    halfB = b/2
    glBegin(GL_QUADS)

    # rows, cols = (4, 3)
    # tab = [[random.randrange(0, 100) / 100 for _ in range(cols)] for _ in range(rows)]

    if c==1:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(tab[0][0], tab[0][1], tab[0][2])
    glVertex2f(x - halfA, y - halfB)
    if c==1:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(tab[1][0], tab[1][1], tab[1][2])
    glVertex2f(x - halfA, y + halfB)
    if c==1:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(tab[2][0], tab[2][1], tab[2][2])
    glVertex2f(x + halfA, y + halfB)
    if c==1:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(tab[3][0], tab[3][1], tab[3][2])
    glVertex2f(x + halfA, y - halfB)

    glEnd()

def render(time, tab):
    glClear(GL_COLOR_BUFFER_BIT)
    #square(0, 0, 300, 300)

    rekur(0, 0, 300, 300, tab)
    #triangle()
    glFlush()


def main():
    random.seed()
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(900, 900, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(100)

    rows, cols = (4, 3)
 #   tab = [[random.randrange(0, 100) / 100 for _ in range(cols)] for _ in range(rows)]

    startup()
    while not glfwWindowShouldClose(window):
        tab = [[random.randrange(0, 100) / 100 for _ in range(cols)] for _ in range(rows)]
        print(tab)
        render(glfwGetTime(), tab)
        glfwSwapBuffers(window)
      #  glfwWaitEvents()
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
    print(aspectRatio)
    if width <= height:
        glOrtho(-450.0, 450.0, -450.0 / aspectRatio, 450.0 / aspectRatio,1.0, -1.0)
    else:
        glOrtho(-450.0 * aspectRatio, 450.0 * aspectRatio, -450.0, 450.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == '__main__':
    main()
