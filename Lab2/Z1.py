import sys
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def square(x, y, a, b):
    halfA = a/2
    halfB = b/2
    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x - halfA, y - halfB)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x + halfA, y - halfB)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(x + halfA, y + halfB)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x - halfA, y + halfB)

    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    square(0, 0, 50, 50)
    #triangle()
    glFlush()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
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
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == '__main__':
    main()
