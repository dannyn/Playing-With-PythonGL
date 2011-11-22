varying vec3 lightDir,normal;
uniform sampler1D celTex;

void main()
{
	float intensity;
    vec4 celColor;
    vec3 n;

	// normalizing the lights position to be on the safe side	
	n = normalize(normal);
	
	intensity = dot(lightDir,n);

    celColor = gl_Color * texture1D(celTex, intensity);
    gl_FragColor =  celColor;
} 
