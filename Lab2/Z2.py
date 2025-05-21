import sys

import numpy as np
from glfw.GLFW import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180.0 / 3.1415)
   # axes()
    egg()
   # line()
    glFlush()

def line(tab, i1, j1, i2, j2):
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    # glVertex3f(-5.0, 0.0, 0.0)
    # glVertex3f(5.0, 0.0, 0.0)
    glVertex3fv(tab[i1, j1])
    glVertex3fv(tab[i2, j2])
    glEnd()


def egg():
    N=30

 #   glBegin(GL_POINTS)
    glBegin(GL_LINES)
    # Inicjalizacja tablicy na wierzchołki
    tab = np.zeros((N, N, 3))

    # Generowanie wartości dla parametrów u i v (od 0 do 1)
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            # Wzory na jajko (dla u i v)
            theta = u * np.pi
            phi = v * 2 * np.pi

            x =  (-90 * math.pow(u, 5) + 225 * math.pow(u, 4) - 270 * math.pow(u,3) + 180 * math.pow(u,2) - 45 * u)* np.cos(np.pi * v)
            y = 160*math.pow(u,4) - 320*math.pow(u, 3)+160*math.pow(u, 2)-5
            z = (-90 * math.pow(u, 5) + 225 * math.pow(u, 4) - 270 * math.pow(u,3) + 180 * math.pow(u,2) - 45 * u)* np.sin(np.pi * v)

            tab[i, j] = [x, y, z]
    N-=1
 #   print(N)
    glColor3f(1.0, 1.0, 1.0)  # Kolor punktów
    for i in range(N):
        for j in range(N):
            # Wyświetlanie każdego wierzchołka jako punkt
           # glVertex3fv(tab[i, j])
            glVertex3fv(tab[i, j])
            glVertex3fv(tab[i+1, j])
       #     print(tab[i, j], tab[i+1, j])
            glVertex3fv(tab[i, j])
            glVertex3fv(tab[i, j+1])
    glEnd()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()