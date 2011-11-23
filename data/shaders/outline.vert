

//varying vec3 lightDir,normal;

void main()
{
	//lightDir = normalize(vec3(gl_LightSource[0].position));
	//normal = gl_NormalMatrix * gl_Normal;

    //gl_FrontColor = gl_Color;
	gl_Position = ftransform();
    gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
        
} 
