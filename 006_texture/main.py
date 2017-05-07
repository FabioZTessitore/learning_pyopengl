import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr
from PIL import Image

def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    cube = [
    #    position         color            texture
        -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
         0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  0.0, 1.0,
         0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  1.0, 1.0,

        -0.5,  0.5, -0.5,  1.0, 1.0, 0.0,  3.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 0.0, 1.0,  2.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 1.0, 1.0,  3.0, 1.0,
         0.5,  0.5,  0.5,  0.5, 1.0, 1.0,  2.0, 1.0
    ]
    cube = numpy.array(cube, dtype=numpy.float32)

    indexes = [
        0, 1, 2, 1, 2, 3,
        0, 2, 4, 2, 4, 6,
        4, 5, 6, 5, 6, 7,
        2, 3, 6, 3, 6, 7,
        1, 3, 5, 3, 5, 7,
        0, 1, 4, 1, 4, 5
    ]
    indexes = numpy.array(indexes, dtype=numpy.uint32)

    vertex_shader = """
    #version 330 core

    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 color;
    layout (location = 2) in vec2 textCoords;

    out vec3 ourColor;
    out vec2 ourTextCoords;

    uniform mat4 transform;

    void main()
    {
        gl_Position = transform * vec4(position, 1.0f);
        ourColor = color;
        ourTextCoords = textCoords;
    }
    """

    fragment_shader = """
    #version 330 core

    in vec3 ourColor;
    in vec2 ourTextCoords;

    out vec4 color;
    uniform sampler2D samplerText;

    void main()
    {
        color = texture(samplerText, ourTextCoords);
    }
    """

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 256, cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 144, indexes, GL_STATIC_DRAW)

    #position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    #color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image = Image.open('../textures/wall.jpg')
    img_data = numpy.array(list(image.getdata()), numpy.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    #texture_coords = glGetAttribLocation(shader, "textCoords")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, numpy.array(rot_x * rot_y))

        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
