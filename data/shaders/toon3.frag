varying vec3 normal, lightDir;
varying vec2 texCoord;
uniform sampler2D texture;

void main()
{
float intensity;
vec3 n;
vec4 _color;

n = normalize(normal);
intensity = dot(lightDir, n);

if (intensity > 0.98)
_color = vec4(1.0,1.0,1.0,1.0);
else if (intensity > 0.5)
_color = vec4(0.8,0.8,0.8,1.0);
else if (intensity > 0.35)
_color = vec4(0.4,0.4,0.4,1.0);
else
_color = vec4(0.0,0.0,0.0,1.0);
gl_FragColor = _color * texture2D(texture, texCoord);
}
