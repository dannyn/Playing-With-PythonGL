varying vec3 lightDir,normal;

void main()
{

	float intensity;
	vec4 color;
	
	// normalizing the lights position to be on the safe side
	
	vec3 n = normalize(normal);
	
	intensity = dot(lightDir,n);
	

    // these steps are creating ambient lighting, 
    // this will need to be fixed
	if (intensity > 0.95)
        color = gl_Color * 0.95;
	else if (intensity > 0.5)
        color = gl_Color * 0.70;
	else if (intensity > 0.25)
        color = gl_Color * 0.40;
	else
        color = gl_Color * 0.25;	

	gl_FragColor = color;
} 
