from vpython import *
import numpy as np

R = 0.12
r = 0.06
z = 0.1
I=1.0

m = 1000
dx = r / m
n = 1000

flux = 0
theta = arange(n)*(2*pi/n)
ds=np.zeros((n, 3))
ds[:, 0] = 2 * pi * R / n * np.cos(pi / 2 + theta)
ds[:, 1] = 2 * pi * R / n * np.sin(pi / 2 + theta)
ds[:, 2] = 0
pos_s = np.zeros((n, 3))
pos_s[:, 0] = R * np.cos(theta)
pos_s[:, 1] = R * np.sin(theta)
pos_s[:, 2] = 0
for i in range(m):
    x = dx * i
    pos_p = vec(x, 0, z)
    B = vec(0, 0, 0)

    for j in range(n):
        dB = 1E-7 * I * cross(vec(ds[j,0], ds[j, 1], ds[j, 2]), norm(pos_p - vec(pos_s[j, 0], pos_s[j, 1], pos_s[j, 2]))) / mag2(pos_p - vec(pos_s[j, 0], pos_s[j, 1], pos_s[j, 2]))
        B += dB

    flux += 2 * pi * x * dx * dot(B, vec(0, 0, 1))
print(flux)


ds[:, 0] = 2 * pi * r / n * np.cos(pi / 2 + theta)
ds[:, 1] = 2 * pi * r / n * np.sin(pi / 2 + theta)
ds[:, 2] = 0
pos_s[:, 0] = r * np.cos(theta)
pos_s[:, 1] = r * np.sin(theta)
pos_s[:, 2] = z
dx = R / m
flux = 0
for i in range(m):
    x = dx * i
    pos_p = vec(x, 0, 0)
    B = vec(0, 0, 0)

    for j in range(n):
        dB = 1E-7 * I * cross(vec(ds[j,0], ds[j, 1], ds[j, 2]), norm(pos_p - vec(pos_s[j, 0], pos_s[j, 1], pos_s[j, 2]))) / mag2(pos_p - vec(pos_s[j, 0], pos_s[j, 1], pos_s[j, 2]))
        B += dB

    flux += 2 * pi * x * dx * dot(B, vec(0, 0, 1))
print(flux)