from OpenGL.GL import *
import OpenGL.GL.shaders

class Shader:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        vertexShaderSource = self.loadShader(vertexShaderPath)
        fragmentShaderSource = self.loadShader(fragmentShaderPath)

        self.shader = self.compileShader(vertexShaderSource, fragmentShaderSource)

    def loadShader(self, shaderPath):
        shaderFile = open(shaderPath, 'r')
        shaderSource = shaderFile.read()
        shaderFile.close()
        return shaderSource

    def compileShader(self, vertexShaderSource, fragmentShaderSource):
        vertexShader = OpenGL.GL.shaders.compileShader(vertexShaderSource, GL_VERTEX_SHADER)
        fragmentShader = OpenGL.GL.shaders.compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER)
        return OpenGL.GL.shaders.compileProgram(vertexShader, fragmentShader)

    def Use(self):
        glUseProgram(self.shader)
