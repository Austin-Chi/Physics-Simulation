import numpy as np
from vpython import *
A, N = 0.10, 50
size, m, k, d = 0.06, 0.1, 10.0, 0.4
scene = graph(title='Phonon dispersion relationship', width=800, height=300, background=vec(0.5,0.5,0), center = vec((N-1)*d/2, 0, 0))
#balls = [sphere(radius=size, color=color.red, pos=vector(i*d, 0, 0), v=vector(0,0,0)) for i in range(N)] #3
#springs = [helix(radius = size/2.0, thickness = d/15.0, pos=vector(i*d, 0, 0), axis=vector(d,0,0)) for i in range(N-1)] #3
#1
pic = gdots(graph = scene, color=color.black)


for n in range(1, N//2):
    t, dt = 0, 0.0003
    Unit_K = 2 * pi/(N*d)
    Wavevector = n * Unit_K
    phase = Wavevector * arange(N) * d
    ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d + A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d
    while(ball_pos[1]-d)>0:
        
        t += dt
        spring_len[-1] = ball_pos[0] + N*d - ball_pos[-1]
        spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
        
        ball_v[1:] += (spring_len[1:] - d)*k/m*dt - (spring_len[:-1] - d)*k/m*dt #6
        ball_v[0] += (spring_len[0]-d)*k*dt - (spring_len[-1] - d)*k*dt
        ball_pos += ball_v*dt
    pic.plot(pos = (Wavevector, pi/(2*t)))
    
    