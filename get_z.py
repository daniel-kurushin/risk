def get_z(CL,BL):
	if        CL < 0.3:
		if        BL < 0.3: return 'H'
		if 0.3 <= BL < 0.7: return 'C'
		if 0.7 <= BL      : return 'B'
	if 0.3 <= CL < 0.7:
		if        BL < 0.3: return 'H'
		if 0.3 <= BL < 0.7: return 'C'
		if 0.7 <= BL      : return 'B'
	if 0.7 <= CL:
		if        BL < 0.3: return 'H'
		if 0.3 <= BL < 0.7: return 'C'
		if 0.7 <= BL      : return 'B'


BL = [0.2331,0.2594,0.2467,0.2638,0.2744]
CL = [0.2662,0.2571,0.2909,0.2460,0.4271]
