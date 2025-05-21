import random
import sys

import numpy as np
from glfw.GLFW import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *

theta = 0.0
phi = 0.0
pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_y_pos_old = 0
mouse_x_pos_old = 0
delta_x = 0
delta_y = 0

normals_flag=False


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

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

def keyboard_key_callback(window, key, scancode, action, mods):

    global normals_flag

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        normals_flag = not normals_flag


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
 #   glRotatef(angle, 0.0, 1.0, 0.0)
  #  glRotatef(angle, 0.0, 0.0, 1.0)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_y
    global mouse_y_pos_old


    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed


    left = button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS
    if left:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

def draw_normals(tab, normals, N):
    glBegin(GL_LINES)
    for i in range(N - 1):
        for j in range(N - 1):
            start = tab[i, j]
            end = start + normals[i, j] * -1  # Dodaj wektor normalny do wierzchołka
            glVertex3fv(start)
            glVertex3fv(end)
    glEnd()


def render(time, N, colors):
    global phi, delta_y, piy2angle, left_mouse_button_pressed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
   # spin(time * 180.0 / 3.1415)
    if left_mouse_button_pressed:
        phi += delta_y * -piy2angle
        #spin(time*90/3.1415)
    axes()
    glRotatef(phi/10, 1.0, 0.0, 0.0)
    egg(N, colors)
   # line()
    glFlush()

def calc(N):
    tab = np.zeros((N, N, 3))
    normals = np.zeros((N, N, 3))
    # Generowanie wartości dla parametrów u i v (od 0 do 1)
    u_values = np.linspace(0.0, 1.0, N)
    v_values = np.linspace(0.0, 1.0, N)
    #  print(len(u_values), len(v_values))

    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):

            x = (-90 * math.pow(u, 5) + 225 * math.pow(u, 4) - 270 * math.pow(u, 3) + 180 * math.pow(u,
                                                                                                     2) - 45 * u) * np.cos(
                np.pi * v)
            y = 160 * math.pow(u, 4) - 320 * math.pow(u, 3) + 160 * math.pow(u, 2) - 5
            z = (-90 * math.pow(u, 5) + 225 * math.pow(u, 4) - 270 * math.pow(u, 3) + 180 * math.pow(u,
                                                                                                     2) - 45 * u) * np.sin(
                np.pi * v)

            tab[i, j] = [x, y, z]

            xu = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * np.cos(np.pi * v)
            xv = np.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * np.sin(np.pi * v)
            yu = 640 * u ** 3 - 960 * u ** 2 + 320 * u
            yv = 0
            zu = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 * u - 45) * np.sin(np.pi * v)
            zv = -np.pi * (90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 * u) * np.cos(np.pi * v)

            # Iloczyn wektorowy
            normal = np.cross([xu, yu, zu], [xv, yv, zv])
            if np.linalg.norm(normal) > 0:
                normal = normal / np.linalg.norm(normal)  # Normalizacja
            if u < 0.5:  # Odwracanie normalnych dla drugiej połówki modelu
                normal *= -1
            normals[i, j] = normal
    return tab, normals

def egg(N, colors):
    global normals_flag
    tab, normals = calc(N)

    for i in range(N -1):
        for j in range(N -1):
         #   if i<1 or i>N-3:
                glBegin(GL_TRIANGLES)
                glColor3fv(colors[i, j])
                glNormal3fv(normals[i, j])
                glVertex3fv(tab[i, j])

                glColor3fv(colors[i, j + 1])
                glNormal3fv(normals[i, j + 1])
                glVertex3fv(tab[i, j + 1])

                glColor3fv(colors[i + 1, j])
                glNormal3fv(normals[i + 1, j])
                glVertex3fv(tab[i + 1, j])

                glColor3fv(colors[i, j + 1])
                glNormal3fv(normals[i, j + 1])
                glVertex3fv(tab[i, j + 1])

                glColor3fv(colors[i + 1, j + 1])
                glNormal3fv(normals[i + 1, j + 1])
                glVertex3fv(tab[i + 1, j + 1])

                glColor3fv(colors[i + 1, j])
                glNormal3fv(normals[i + 1, j])
                glVertex3fv(tab[i + 1, j])
                glEnd()

    if normals_flag:
        draw_normals(tab, normals, N)




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
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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