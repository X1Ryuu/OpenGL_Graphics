import random
import sys

import numpy as np
from glfw.GLFW import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 800, 800)
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
   # glRotatef(angle, 0.0, 1.0, 0.0)
   # glRotatef(angle, 0.0, 0.0, 1.0)


def render(time, N, colors):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
   # spin(time * 180.0 / 3.1415)
    spin(time*90/3.1415)
   # axes()
   # egg(N, colors)
  #  cube_with_squares(5)
    pyramid(10)
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



def pyramid(N):
    glBegin(GL_TRIANGLES)
    licz=4
    # Inicjalizacja siatki podstawy
    u_values = np.linspace(-1.0, 1.0, N + 1)  # Współrzędne w płaszczyźnie x
    v_values = np.linspace(-1.0, 1.0, N + 1)  # Współrzędne w płaszczyźnie y
    base = np.zeros((N + 1, N + 1, 3))       # Tablica współrzędnych wierzchołków podstawy

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            base[i, j] = [u*licz, v*licz, -1.0*licz]  # Z wysokością 0 dla podstawy

    # Rysowanie podstawy jako siatki kwadratów
    for i in range(N):
        for j in range(N):
            v1 = base[i, j]
            v2 = base[i + 1, j]
            v3 = base[i + 1, j + 1]
            v4 = base[i, j + 1]

            # Rysowanie dwóch trójkątów tworzących jeden kwadrat
            glColor3f(1.0, 1.0, 0.0)  # Żółty kolor dla podstawy
            glVertex3fv(v1)
            glVertex3fv(v2)
            glVertex3fv(v3)

            glVertex3fv(v1)
            glVertex3fv(v3)
            glVertex3fv(v4)

    # Wierzchołek piramidy
    apex = [0.0, 0.0, 1.0*licz]  # Wierzchołek na wysokości 1.0

    # Rysowanie ścian bocznych
    for i in range(N):
        for j in range(N):
            # Cztery rogi jednego kwadratu podstawy
            v1 = base[i, j]
            v2 = base[i + 1, j]
            v3 = base[i + 1, j + 1]
            v4 = base[i, j + 1]

            # Rysowanie trójkątów do wierzchołka
            glColor3f(1.0, 0.0, 0.0)  # Czerwony kolor dla ścian
            glVertex3fv(v1)
            glVertex3fv(v2)
            glVertex3fv(apex)

            glColor3f(0.0, 1.0, 0.0)  # Zielony kolor dla ścian
            glVertex3fv(v2)
            glVertex3fv(v3)
            glVertex3fv(apex)

            glColor3f(0.0, 0.0, 1.0)  # Niebieski kolor dla ścian
            glVertex3fv(v3)
            glVertex3fv(v4)
            glVertex3fv(apex)

            glColor3f(1.0, 0.5, 0.0)  # Pomarańczowy kolor dla ścian
            glVertex3fv(v4)
            glVertex3fv(v1)
            glVertex3fv(apex)

    glEnd()



def cube_with_squares(N):
    glBegin(GL_TRIANGLES)
    tab = np.zeros((6, N + 1, N + 1, 3))  # Tablica wierzchołków dla każdej ściany

    # Generowanie wartości dla parametrów u i v (od -1 do 1)
    u_values = np.linspace(-1.0, 1.0, N + 1)
    v_values = np.linspace(-1.0, 1.0, N + 1)

    # Definiowanie każdej ściany sześcianu
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            # Przód (z = 1)
            print("u: ", u, "v: ", v, "i: ", i, "j: ", j)
            tab[0, i, j] = [u*N, v*N, 1.0*N]
            # Tył (z = -1)
            tab[1, i, j] = [u*N, v*N, -1.0*N]
            # Góra (y = 1)
            tab[2, i, j] = [u*N, 1.0*N, v*N]
            # Dół (y = -1)
            tab[3, i, j] = [u*N, -1.0*N, v*N]
            # Lewa (x = -1)
            tab[4, i, j] = [-1.0*N, u*N, v*N]
            # Prawa (x = 1)
            tab[5, i, j] = [1.0*N, u*N, v*N]

    # Rysowanie kwadratów jako dwóch trójkątów dla każdej ściany
    for face in range(6):
        for i in range(N):
            for j in range(N):
                if j==3:
                # Cztery wierzchołki kwadratu
                    v1 = tab[face, i, j]
                    v2 = tab[face, i + 1, j]
                    v3 = tab[face, i + 1, j + 1]
                    v4 = tab[face, i, j + 1]

                    # Rysowanie dwóch trójkątów dla kwadratu
                    glColor3f(abs(v1[0]), abs(v1[1]), abs(v1[2]))  # Kolory w zależności od współrzędnych
                    glVertex3fv(v1)
                    glVertex3fv(v2)
                    glVertex3fv(v3)

                    glColor3f(abs(v4[0]), abs(v4[1]), abs(v4[2]))  # Inny kolor dla drugiego trójkąta
                    glVertex3fv(v1)
                    glVertex3fv(v3)
                    glVertex3fv(v4)

    glEnd()




def cube(N):
    glBegin(GL_POINTS)
    tab = np.zeros((6, N, N, 3))  # Tablica punktów dla 6 ścian sześcianu

    # Generowanie wartości dla parametrów u i v (od -1 do 1)
    u_values = np.linspace(-1.0, 1.0, N)
    v_values = np.linspace(-1.0, 1.0, N)

    # Ściany sześcianu: przód, tył, góra, dół, lewa, prawa
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            # Przód (z = 1)
            tab[0, i, j] = [u, v, 1.0]
            # Tył (z = -1)
            tab[1, i, j] = [u, v, -1.0]
            # Góra (y = 1)
            tab[2, i, j] = [u, 1.0, v]
            # Dół (y = -1)
            tab[3, i, j] = [u, -1.0, v]
            # Lewa (x = -1)
            tab[4, i, j] = [-1.0, u, v]
            # Prawa (x = 1)
            tab[5, i, j] = [1.0, u, v]

    # Rysowanie punktów
    glColor3f(1.0, 1.0, 1.0)  # Białe punkty
    for face in range(6):
        for i in range(N):
            for j in range(N):
                glVertex3fv(tab[face, i, j])

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
       # glOrtho(-15, 15, -15 / aspect_ratio, 15 / aspect_ratio, 15, -15)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)
       # glOrtho(-15 * aspect_ratio, 15 * aspect_ratio, -15, 15, 15, -15)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    random.seed()
    N = 30
    colors = np.random.rand(N, N, 3)
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), N, colors)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()