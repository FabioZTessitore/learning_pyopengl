#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec2 texCoords;

out vec3 ourColor;
out vec2 TexCoords;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0f);
    ourColor = color;
    TexCoords = texCoords;
}
