#version 330

smooth in vec4 theColor;

out vec4 outputColor;

vec4 blueColor;

void main()
{

    blueColor = vec4(0.0f, 0.0f, 1.0f, 1.0f);
    outputColor = theColor;
}

