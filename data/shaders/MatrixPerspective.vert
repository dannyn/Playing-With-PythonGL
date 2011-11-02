#version 330

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;

smooth out vec4 theColor;

uniform mat4 perspectiveMatrix;
uniform mat4 modelMatrix;

void main()
{
    vec4 cameraPos =  modelMatrix * position; 

    gl_Position = perspectiveMatrix  * cameraPos;
    theColor = color;
}

