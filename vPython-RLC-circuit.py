from vpython import *
import numpy as np

fd = 120  # 120Hz
# (Your Parameters here)
C=20E-6
L=0.2
R=30
Q=0
T=1/fd
w=2*pi*fd
i=0
v=0
E0=0
E=0
t_i=0
t_v=0
i_pre=i
stage=0
change=False



t = 0
dt = 1.0 / (fd * 5000)  # 5000 simulation points per cycle

scene1 = graph(align='left', xtitle='t', ytitle='i (A) blue, v (100V) red,',
               background=vector(0.2, 0.6, 0.2))
scene2 = graph(align='left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2))

i_t = gcurve(color=color.blue, graph=scene1)
v_t = gcurve(color=color.red, graph=scene1)
E_t = gcurve(color=color.red, graph=scene2)

# (Your program here)
while t <= 20*T:
    if t<12*T:
        v_new=36*sin(2*pi*fd*t)
        if v*v_new <= 0 and v-v_new > 0:
            t_v=t
        v=v_new
        i_the=0.40156*sin(2*pi*fd*t-70/180*pi)
        if stage == 0 and t>=9*T:
            print("t = 9T:")
            print("|i| =", abs(i), "A, |i_theory|:", abs(i_the), 'A')
            print("Error:", (i - i_the) / i_the * 100, '%')
            print("t = 9T:")
            phi = (t_v - t_i) * w / pi *180
            phi_the = (np.arctan(-(w * L - 1 / w / C) / R))/pi *180
            print("phi =", phi, "degree, phi_theory:", phi_the, 'degree')
            print("Error:", (phi - phi_the) / phi_the * 100, '%')
            stage = 1

    else:
        if stage == 1:
            E0 = E
            stage = 2
        elif stage == 2:
            if E <= E0 / 10:
                print("t = ", t, 's ( t-12T = ', t - 12 * T, 's )')
                stage = 3
        v = 0
        i_the = 0
    i = (v + L * i_pre / dt - Q / C) / (R + dt / C + L / dt)
    if i_pre * i <= 0 and i_pre - i > 0:
        t_i = t
    Q += i * dt
    i_pre = i
    t += dt
    E = Q * Q / C / 2 + L * i * i / 2

    i_t.plot(pos=(t, i))
    v_t.plot(pos=(t, v / 100))
    E_t.plot(pos=(t, E))

