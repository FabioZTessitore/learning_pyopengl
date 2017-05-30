import glfw
from OpenGL.GL import *
import numpy
from PIL import Image
import pyrr
import math

from shader import Shader

(WIDTH, HEIGHT) = (800, 600)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Hello World", None, None)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    if not window:
        glfw.terminate()
        return -1
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    (width, height) = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

    glfw.set_key_callback(window, key_callback)

    glClearColor(0.2, 0.3, 0.2, 1.0)

    quad = [
        # coords          # texture
        -0.5, -0.5, 0.0,  0.0, 0.0,
         0.5, -0.5, 0.0,  1.0, 0.0,
         0.5,  0.5, 0.0,  1.0, 1.0,
        -0.5,  0.5, 0.0,  0.0, 1.0
    ]
    quad = numpy.array(quad, dtype=numpy.float32)
    indexes = [
        0, 1, 2,
        0, 2, 3
    ]
    indexes = numpy.array(indexes, dtype=numpy.uint32)

    ourShader = Shader('vertex_shader.vs', 'fragment_shader.frag')

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, quad.itemsize * len(quad), quad, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize * len(indexes), indexes, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image = Image.open('../textures/wall.jpg')
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ourShader.Use()

        modelLoc = glGetUniformLocation(ourShader.shader, "model")
        rot_x = pyrr.Matrix44.from_x_rotation(1.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.5 * glfw.get_time())
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, numpy.array(rot_x * rot_y))

        viewLoc = glGetUniformLocation(ourShader.shader, "view")
        translate = pyrr.Matrix44.from_translation(pyrr.Vector3([0., 0., -3.]))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, numpy.array(translate))

        projectionLoc = glGetUniformLocation(ourShader.shader, "projection")
        proj = pyrr.Matrix44.perspective_projection(45.0, float(WIDTH)/float(HEIGHT), 0.1, 100.)
        glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, numpy.array(proj))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indexes), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
