varying vec3 normal, lightDir;
varying vec2 texCoord;

void main()
{
vec4 ecPos;
ecPos = vec4(gl_ModelViewMatrix * gl_Vertex);
lightDir = normalize(vec3(gl_LightSource[0].position) - ecPos.xyz);
normal = normalize(gl_NormalMatrix * gl_Normal);

texCoord = vec2(gl_MultiTexCoord0);
gl_Position = ftransform();
}

