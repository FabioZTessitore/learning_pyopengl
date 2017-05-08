import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

(WIDTH, HEIGHT) = (800, 600)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Hello World", None, None)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3);
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3);
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE);
    if not window:
        glfw.terminate()
        return -1
    glfw.make_context_current(window)

    (width, height) = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height);

    glfw.set_key_callback(window, key_callback);

    glClearColor(0.2, 0.3, 0.2, 1.0)

    triangle1 = [
        -0.75, -0.5, 0.0,
        -0.25, -0.5, 0.0,
        -0.5,   0.5, 0.0
    ]
    triangle1 = numpy.array(triangle1, dtype=numpy.float32)
    indexes1 = [
        0, 1, 2
    ]
    indexes1 = numpy.array(indexes1, dtype=numpy.uint32)

    triangle2 = [
         0.25, -0.5, 0.0,
         0.75, -0.5, 0.0,
         0.5,   0.5, 0.0
    ]
    triangle2 = numpy.array(triangle2, dtype=numpy.float32)
    indexes2 = [
        0, 1, 2
    ]
    indexes2 = numpy.array(indexes2, dtype=numpy.uint32)

    vertex_shader_source = """
    #version 330 core

    layout (location = 0) in vec3 position;

    void main()
    {
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader_source1 = """
    #version 330 core

    out vec4 color;

    void main()
    {
        color = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }
    """

    fragment_shader_source2 = """
    #version 330 core

    out vec4 color;

    void main()
    {
        color = vec4(1.0f, 1.0f, 0.0f, 1.0f);
    }
    """

    vertex_shader = OpenGL.GL.shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader1 = OpenGL.GL.shaders.compileShader(fragment_shader_source1, GL_FRAGMENT_SHADER)
    fragment_shader2 = OpenGL.GL.shaders.compileShader(fragment_shader_source2, GL_FRAGMENT_SHADER)
    shader1 = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader1)
    shader2 = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader2)

    VAO1 = glGenVertexArrays(1)
    VBO1 = glGenBuffers(1)
    EBO1 = glGenBuffers(1)

    glBindVertexArray(VAO1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO1)
    glBufferData(GL_ARRAY_BUFFER, triangle1.itemsize * len(triangle1), triangle1, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO1)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexes1.itemsize * len(indexes1), indexes1, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    VAO2 = glGenVertexArrays(1)
    VBO2 = glGenBuffers(1)
    EBO2 = glGenBuffers(1)

    glBindVertexArray(VAO2)
    glBindBuffer(GL_ARRAY_BUFFER, VBO2)
    glBufferData(GL_ARRAY_BUFFER, triangle2.itemsize * len(triangle2), triangle2, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO2)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indexes2.itemsize * len(indexes2), indexes2, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader1)
        glBindVertexArray(VAO1)
        glDrawElements(GL_TRIANGLES, len(indexes1), GL_UNSIGNED_INT, None)
        #glBindVertexArray(0)

        glUseProgram(shader2)
        glBindVertexArray(VAO2)
        glDrawElements(GL_TRIANGLES, len(indexes2), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
