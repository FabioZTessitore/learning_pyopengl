import glfw
from OpenGL.GL import *
import numpy
from PIL import Image

from shader import Shader

(WIDTH, HEIGHT) = (800, 600)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

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

    (width, height) = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

    glfw.set_key_callback(window, key_callback)

    glClearColor(0.2, 0.3, 0.2, 1.0)

    quad = [
        # coords            # colors        # texture
        -0.5, -0.5, 0.0,    1.0, 0.0, 0.0,  0.0, 0.0,
         0.5, -0.5, 0.0,    0.0, 1.0, 0.0,  1.0, 0.0,
         0.5,  0.5, 0.0,    0.0, 0.0, 1.0,  1.0, 1.0,
        -0.5,  0.5, 0.0,    1.0, 1.0, 1.0,  0.0, 1.0
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
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)
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

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        ourShader.Use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indexes), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
