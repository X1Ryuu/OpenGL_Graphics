import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math

import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image




viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0
phi = 0.0
piy2angle = 1.0
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
delta_y = 0
mouse_y_pos_old = 0
hide_side = False

space_pressed = 0

images = []

flag = True # ustawiona
texture = 0





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

def egg(N):
    global normals_flag
    tab, normals = calc(N)

    for i in range(N -1):
        for j in range(N -1):
         #   if i<1 or i>N-3:
                glBegin(GL_TRIANGLES)
           #     glColor3fv(colors[i, j])
                glNormal3fv(normals[i, j])
                glVertex3fv(tab[i, j])

           #     glColor3fv(colors[i, j + 1])
                glNormal3fv(normals[i, j + 1])
                glVertex3fv(tab[i, j + 1])

          #      glColor3fv(colors[i + 1, j])
                glNormal3fv(normals[i + 1, j])
                glVertex3fv(tab[i + 1, j])

         #       glColor3fv(colors[i, j + 1])
                glNormal3fv(normals[i, j + 1])
                glVertex3fv(tab[i, j + 1])

           #     glColor3fv(colors[i + 1, j + 1])
                glNormal3fv(normals[i + 1, j + 1])
                glVertex3fv(tab[i + 1, j + 1])

           #     glColor3fv(colors[i + 1, j])
                glNormal3fv(normals[i + 1, j])
                glVertex3fv(tab[i + 1, j])
                glEnd()


def startup():
    global images
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)  # Włączamy face culling
    glCullFace(GL_BACK)  # Usuwamy tylne ściany

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #image = Image.open("tekstura.tga")
    images = [
        Image.open("tekstura.tga"),
        Image.open("CarbonFiber256.tga"),]
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, images[0].size[0], images[0].size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, images[0].tobytes("raw", "RGB", 0, -1)
    )


def render(time):
    global theta, hide_side, flag, texture, images, phi, delta_y, piy2angle

    if flag == False:
        texture = (texture + 1) % 2
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, images[texture].size[0], images[texture].size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, images[texture].tobytes("raw", "RGB", 0, -1)
        )
        flag = True



    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # if left_mouse_button_pressed:
    #     theta += delta_x * pix2angle

    if left_mouse_button_pressed:
        phi += delta_y * piy2angle

    glRotatef(phi, 1.0, 0.0, 0.0)

    # Wierzchołki ostrosłupa
    base_vertices = [
        (-2.5, -2.5, 0.0), (-2.5, 2.5, 0.0),
        (2.5, 2.5, 0.0), (2.5, -2.5, 0.0)
    ]
    top_vertex = (0.0, 0.0, 3.5)

    # Rysowanie podstawy (kwadratu)
    egg(30)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, (height - width) // 2, width, width)
    else:
        glViewport((width - height) // 2, 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global hide_side
    global space_pressed
    global flag

    if key == GLFW_KEY_H and action == GLFW_PRESS:
        hide_side = not hide_side
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        space_pressed = 1
        flag = False

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old, delta_y, mouse_y_pos_old
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, "Textured Pyramid", None, None)
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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()


if __name__ == '__main__':
    main()
