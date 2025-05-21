import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

hide_side = False


def startup():
    update_viewport(None, 800, 800)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)  # Włączamy face culling
    glCullFace(GL_BACK)  # Usuwamy tylne ściany

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("tekstura.tga")
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def render(time):
    global theta, hide_side
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    # Wierzchołki ostrosłupa
    base_vertices = [
        (-2.5, -2.5, 0.0), (-2.5, 2.5, 0.0),
        (2.5, 2.5, 0.0), (2.5, -2.5, 0.0)
    ]
    top_vertex = (0.0, 0.0, 3.5)

    # Rysowanie podstawy (kwadratu)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3fv(base_vertices[0])
    glTexCoord2f(1.0, 0.0)
    glVertex3fv(base_vertices[1])
    glTexCoord2f(1.0, 1.0)
    glVertex3fv(base_vertices[2])
    glTexCoord2f(0.0, 1.0)
    glVertex3fv(base_vertices[3])
    glEnd()

    # Rysowanie ścian bocznych (trójkątów)
    if not hide_side:
        glBegin(GL_TRIANGLES)
        for i in range(4):
            glTexCoord2f(0.5, 1.0)
            glVertex3fv(top_vertex)
            glTexCoord2f(0.0, 0.0)
            glVertex3fv(base_vertices[i])
            glTexCoord2f(1.0, 0.0)
            glVertex3fv(base_vertices[(i - 1) % 4])
        glEnd()

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
    if key == GLFW_KEY_H and action == GLFW_PRESS:
        hide_side = not hide_side


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


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
