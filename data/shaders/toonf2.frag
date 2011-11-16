varying vec3 lightDir,normal;
uniform sampler1D texture;

void main()
{
	float intensity;
	
	// normalizing the lights position to be on the safe side
	
	vec3 n = normalize(normal);
	
	intensity = dot(lightDir,n);
    //intensity += 1;
	gl_FragColor = gl_Color * texture1D(texture, intensity);
    //gl_FragColor = gl_Color * intensity;
} 
