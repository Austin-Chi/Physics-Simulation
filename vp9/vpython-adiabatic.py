from vpython import *
import numpy as np
from histogram import *
N = 200
m, size = 4E-3/6E23, 31E-12*10 # He atom are 10 times bigger for easiear collision but not too big for accuracy
L = ((24.4E-3/(6E23))*N)**(1/3.0)/2 + size # 2L is the cubic container's original length, width, and height
k, T = 1.38E-23, 298.0 # Boltzmann Constant and initial temperature
t, dt = 0, 3E-13
times=0
vrms = (2*k*1.5*T/m)**0.5 # the initial root mean square velocity
stage = 0 # stage number
atoms = [] # list to store atoms
# histogram setting
deltav = 50. # slotwidth for v histogram
vdist = graph(x=800, y=0, ymax = N*deltav/1000.,width=500, height=300, xtitle='v', ytitle='dN', align = 'left')
theory_low_T = gcurve(color=color.cyan) # for plot of the curve for the atom speed distribution
theory_high_T = gcurve(color=color.cyan)
dv = 10.
for v in arange(0.,4201.+dv,dv): # theoretical speed distribution
    theory_low_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))
observation = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.red) # for the simulation speed distribution
observationn = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.blue)
#initialization
scene = canvas(width=500, height=500, background=vector(0.2,0.2,0), align = 'left')
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.2, color = color.yellow )
p_a, v_a = np.zeros((N,3)), np.zeros((N,3)) # particle position array and particle velocity array, N particles and 3 for x, y, z
v_W = 0
total_mv = 0
has_done =False
for i in range(N):
    p_a[i] = [2 * L*random() - L, 2 * L*random() - L, 2 * L*random() - L] # particle is initially random positioned in container
    if i== N-1: # the last atom is with yellow color and leaves a trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=color.yellow, make_trail = True, retain = 50)
    else: # other atoms are with random color and leaves no trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=vector(random(), random(), random()))
    ra = pi*random()
    rb = 2*pi*random()
    v_a[i] = [vrms*sin(ra)*cos(rb), vrms*sin(ra)*sin(rb), vrms*cos(ra)] # particle initially same speed but random direction
    atoms.append(atom)
def vcollision(a1p, a2p, a1v,a2v): # the function for handling velocity after collisions between two atoms
    v1prime = a1v - (a1p - a2p) * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p) * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

def keyinput(evt):
    global stage
    if evt.key=='n':
        stage+=1
scene.bind('keydown', keyinput)

while True:

    t += dt
    times+=1
    rate(10000)
    p_a += v_a*dt # calculate new positions for all atoms
    for i in range(N): atoms[i].pos = vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]) # to display atoms at new positions
    if stage == 0 : observation.plot(data = np.sqrt(np.sum(np.square(v_a),-1))) ## freeze histogram for stage != 1
    if stage == 1 :
        if container.length>=L:
            v_W = L / (20000.0*dt)
            container.length-=2*v_W*dt
        else: 
            stage += 1
            v_W = 0
    if stage >= 2 : 
        v_W = 0
        observationn.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
    if stage == 2 : 
        if has_done==False:
            T = 1/2*m*(np.sum(np.square(v_a)))/(3*N*k/2)
            for v in arange(0.,4201.+dv,dv): # theoretical speed distribution
                theory_high_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))
            has_done=True
    if stage == 3 :
        container.length=2*L
    ### find collisions between pairs of atoms, and handle their collisions
    r_array = p_a-p_a[:,np.newaxis] # array for vector from one atom to another atom for all pairs of atoms
    rmag = np.sqrt(np.sum(np.square(r_array),-1)) # distance array between atoms for all pairs of atoms
    hit = np.less_equal(rmag,2*size)-np.identity(N) # if smaller than 2*size meaning these two atoms might hit each other
    hitlist = np.sort(np.nonzero(hit.flat)[0]).tolist() # change hit to a list
    for ij in hitlist: # i,j encoded as i*Natoms+j
        i, j = divmod(ij,N) # atom pair, i-th and j-th atoms, hit each other
        hitlist.remove(j*N+i) # remove j,i pair from list to avoid handling the collision twice
        if sum((p_a[i]-p_a[j])*(v_a[i]-v_a[j])) < 0 : # only handling collision if two atoms are approaching each other
            v_a[i], v_a[j] = vcollision(p_a[i], p_a[j], v_a[i], v_a[j]) # handle collision
    #find collisions between the atoms and the walls, and handle their elastic collisions
    for i in range(N):
        if abs(p_a[i][0]) >= container.length/2 - size and p_a[i][0]*v_a[i][0] > 0 :
            if v_a[i][0]>0:
                v_a[i][0] = - v_a[i][0] - 2*v_W
            else:
                v_a[i][0] = - v_a[i][0] + 2*v_W
            total_mv+=m*(2*abs(v_a[i][0]) + 2*v_W)
            
        if abs(p_a[i][1]) >= L - size and p_a[i][1]*v_a[i][1] > 0 :
            v_a[i][1] = - v_a[i][1]
            total_mv+=m*(2*abs(v_a[i][1]))
        if abs(p_a[i][2]) >= L - size and p_a[i][2]*v_a[i][2] > 0 :
            v_a[i][2] = - v_a[i][2]
            total_mv+=m*(2*abs(v_a[i][2]))

    if times%1000==0 :
        T = 1/2*m*(np.sum(np.square(v_a)))/(3*N*k/2)
        P = total_mv/(1000*dt*2*(container.height*container.length+container.length*container.width+container.width*container.height))
        total_mv=0
        V = container.height*container.length*container.width
        print(f"T = {T}"+f" p = {P}"+f" V = {V}"+f" p*V = {P*V}"+f" N*k*T = {N*k*T}"+f" p*V**gamma = {P*(V**(5/3))}")