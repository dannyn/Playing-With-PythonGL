#version 330

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;

vec4  blueColor = vec4(0.0f, 0.0f, 1.0f, 1.0f);
    
smooth out vec4 theColor;

uniform mat4 perspectiveMatrix;
uniform mat4 modelMatrix;

void main()
{
    vec4 cameraPos =  modelMatrix * position; 

    gl_Position = perspectiveMatrix  * cameraPos;
    theColor = color;
}

