from OpenGL.GL import *
import OpenGL.GL.shaders

class Shader:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        vertexFile = open(vertexShaderPath, 'r')
        vertexShaderSource = vertexFile.read()
        vertexFile.close()

        fragmentFile = open(fragmentShaderPath, 'r')
        fragmentShaderSource = fragmentFile.read()
        fragmentFile.close()

        vertexShader = OpenGL.GL.shaders.compileShader(vertexShaderSource, GL_VERTEX_SHADER)
        fragmentShader = OpenGL.GL.shaders.compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(vertexShader, fragmentShader)

    def Use(self):
        glUseProgram(self.shader)
