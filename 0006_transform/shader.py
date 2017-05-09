from OpenGL.GL import *
import OpenGL.GL.shaders

class Shader:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        vertexFile = open(vertexShaderPath, 'r')
        vertexShaderSource = []
        for line in vertexFile.readlines():
            vertexShaderSource.append(line)
        vertexFile.close()
        vertexShaderSource = ''.join(vertexShaderSource)

        fragmentFile = open(fragmentShaderPath, 'r')
        fragmentShaderSource = []
        for line in fragmentFile.readlines():
            fragmentShaderSource.append(line)
        fragmentFile.close()
        fragmentShaderSource = ''.join(fragmentShaderSource)

        vertexShader = OpenGL.GL.shaders.compileShader(vertexShaderSource, GL_VERTEX_SHADER)
        fragmentShader = OpenGL.GL.shaders.compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(vertexShader, fragmentShader)

    def Use(self):
        glUseProgram(self.shader)
