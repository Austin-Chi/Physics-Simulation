from vpython import *
from numpy import *

N = 100
R, lamda = 1.0, 500E-9
d = 100E-6

dx, dy = d/N, d/N
scene1 = canvas(align = 'left', height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene2 = canvas(align = 'right', x=600, height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene1.lights, scene2.lights = [], []
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99)
side = linspace(-0.01*pi, 0.01*pi, N)
x,y = meshgrid(side,side)
hole_side = linspace(-d/2, d/2, N)
X, Y = meshgrid(hole_side, hole_side)
inside = X**2+Y**2 <= (d/2)**2
k=2*pi/lamda
E_field = cos(10000*((x-0.005)**2 + (y- 0.002)**2 )) # change this to calculate the electric field of diffraction of the aperture

for i in range(N):
    for j in range(N):
        E_field[i, j] = sum(cos(k*x[i, j]/R * X + k*y[i, j]/R * Y) * dx * dy * inside) / R

Inte = abs(E_field) ** 2
maxI = amax(Inte)
for i in range(N):
	for j in range(N):
		box(canvas = scene1, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
			color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))
intensity = Inte[50][50]
pos = 0

for i in range(50, N):
    if Inte[i][50] <= intensity:
        intensity = Inte[i][50]
        pos = i
    else:
        break

theta = -0.01 * pi + pos * (0.02 * pi) / N
print("simulation value:", theta)
print("theoretical value:", 1.22 * lamda / d)
Inte = abs(E_field)
maxI = amax(Inte)
for i in range(N):
	for j in range(N):
		box(canvas = scene2, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
			color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))

