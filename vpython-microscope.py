from vpython import *
L=2; size=0.1; th=radians(45.); H=3.0
scene = canvas(background=vec(0.8, 0.8, 0.8), width=500, height=500, center = vec(3,0,10), fov = 0.004)
R = 4.0
receiver = box(length=3, height=0.1, width=3, pos=vec(0, 6.1, 0), color=color.black)
receiverpos=vec(0, 6.1, 0)
pinhole = box(length=2, height=0.1, width=2, pos=vec(0, 6, 0), color=color.black)
laser = box(length = 2, height=1, width=1, pos=vec(-7, 0, 0), color=color.black)
lens_surface1 = shapes.ellipse( width=sqrt(R*R-(R-0.15)**2),height=0.15, angle1=0, angle2=pi)
circle1 = paths.arc(pos=vec(0, -3.0, 0), radius=0.0000001, angle2=2*pi, up = vec(1,0,0))
lens_surface2 = shapes.ellipse(width=sqrt(R*R-(R-0.15)**2),height=0.15, angle1=-pi, angle2=0)
circle2 = paths.arc(pos=vec(0, -3.0, 0), radius=0.0000001, angle2=2*pi, up = vec(1,0,0))
extrusion(path=circle1, shape=lens_surface1, color=vec(147.0/255.0, 224.0/255.0, 1.0), opacity = 0.6)
extrusion(path=circle2, shape=lens_surface2, color=vec(147.0/255.0, 224.0/255.0, 1.0), opacity = 0.6)
mirror = box(length=L, height=0.1, width=1, color=vec(147.0/255.0, 224.0/255.0, 1.0))
mirror.pos = vector(0, 0, 0)
mirror.axis=vector(-cos(th), sin(th),0)
objpos = vec(0, -10.3, 0)
obj = sphere(pos=objpos, radius = 1, color=color.green)
dgraph = graph(width = 400, allign = 'right', xtitle = 'x', ytitle = 'y')

def reflect_vector(theta, normal_v):

	v_out = vector(cos(-(theta+pi/2)), sin(-(theta+pi/2)), 0)
	return v_out

def refraction_vector(n1, n2, v_in, normal_v):
	# find the unit vector of velocity of the outgoing ray
	sin_theta1 = sin(diff_angle(normal_v, v_in))
	sin_theta2 = n1/n2*sin_theta1
	cos_theta2 = (1-sin_theta2**2)**(1/2)
	sign = (cross(normal_v, v_in)/mag(cross(normal_v, v_in))).z
	# print("sign = ", sign)
	v_out = vec(cos_theta2*normal_v.x-sign*sin_theta2*normal_v.y, sign*sin_theta2*normal_v.x+cos_theta2*normal_v.y, 0)
	return v_out

thickness = 0.3

g2center = vec(0, -R + thickness / 2 - H, 0)
g1center = vec(0, R - thickness / 2 - H, 0)
# ball1 = sphere(pos = g1center-vec(0, 0, 15), radius =R, color = color.green)
# ball2 = sphere(pos = g2center-vec(0, 0, 15), radius =R, color = color.yellow)
nair = 1
nglass = 1.5
ray1 = sphere (pos=vec(-6, 0, 0), color = color.blue, radius = 0.01, make_trail=True)
ray1.v = vector (cos(-2/40.0), sin(-2/40.0), 0)
ray2 = sphere (pos=vec(-6, 0, 0), color = color.blue, radius = 0.01, make_trail=True)
ray2.v = vector (cos(-1/40.0), sin(-1/40.0), 0)
done1 = False
done2 = False
inside1 = False
inside2 = False
reflect1 = False
reflect2=False
dt = 0.002
while True:
	rate(1000)
	if not done1:
		ray1.pos = ray1.pos + ray1.v*dt
	if not done2:
		ray2.pos = ray2.pos + ray2.v*dt
	# your code here
	if ray1.pos.y+ray1.pos.x>=0 and reflect1 == False:
		ray1.v = reflect_vector(-2/40, mirror.axis)
		print(ray1.v)
		reflect1 = True

	if mag(ray1.pos - g2center)<R and ray1.pos.y>-H and inside1==False:
		inside1 = True
		print("number 1 first refract")
		ray1.v=refraction_vector(1, nglass, ray1.v, -norm(ray1.pos - g2center))
	if mag(ray1.pos - g1center)>R and ray1.pos.y<-H and inside1==True:
		inside1=False
		print("number1 second refract")
		ray1.v = refraction_vector(nglass, 1, ray1.v, norm(ray1.pos - g1center))

	if ray2.pos.y+ray2.pos.x>=0 and reflect2 == False:
		ray2.v = reflect_vector(-1/40, mirror.axis)
		print(ray2.v)
		reflect2 = True

	if mag(ray2.pos - g2center)<R and ray2.pos.y>-H and inside2==False:
		inside2 = True
		print("number 2 first refract")
		ray2.v=refraction_vector(1, nglass, ray2.v, -norm(ray2.pos - g2center))
	if mag(ray2.pos - g1center)>R and ray2.pos.y<-H and inside2==True:
		inside2=False
		print("number 2 second refract")
		ray2.v = refraction_vector(nglass, 1, ray2.v, norm(ray2.pos - g1center))
	if ray2.pos.x <= 0 and reflect2==True:
		done2 = True
	if ray1.pos.x <= 0 and reflect1==True:
		done1 = True
	if done1 and done2:
		break
fray1 = sphere (pos=vec(0, ray2.pos.y,  0), color = vec(105.0/255.0, 225.0/255.0, 71.0/255.0), radius = 0.01, make_trail=True)
fray2 = sphere (pos=vec(0, ray1.pos.y, 0), color = vec(105.0/255.0, 225.0/255.0, 71.0/255.0), radius = 0.01, make_trail=True)
fpos = ray2.pos.y
fray1.pos=vec(0, fpos,  0)
fray1.visible = True
fray1.v = vector (cos((-1/40.0+pi/2)), sin((-1/40.0+pi/2)), 0)
print("fray1v = ", fray1.v)
fray2.pos=vec(0, fpos, 0)
fray2.visible = True
fray2.v = vector (cos((-2/40.0+pi/2)), sin((-2/40.0+pi/2)), 0)
print("fray2v = ", fray2.v)
fdone1 = False
fdone2 = False
finside1 = False
finside2 = False
while True:
	rate(10000)
	if not fdone1:
		fray1.pos = fray1.pos + fray1.v*dt
	if not fdone2:
		fray2.pos = fray2.pos + fray2.v*dt
	# your code here
	if mag(fray1.pos - g1center)<R and fray1.pos.y<-H and finside1==False:
		finside1 = True
		print("number f1 first refract")
		fray1.v=refraction_vector(1, nglass, fray1.v, -norm(fray1.pos - g1center))
		print("fray1.v = ", fray1.v)
	if mag(fray1.pos - g2center)>R and fray1.pos.y>-H and finside1==True:
		finside1=False
		print("number1 second refract")
		fray1.v = refraction_vector(nglass, 1, fray1.v, norm(fray1.pos - g2center))
		print("fray1.v = ", fray1.v)

	if mag(fray2.pos - g1center)<R and fray2.pos.y<-H and finside2==False:
		finside2 = True
		print("number 2 first refract")
		fray2.v=refraction_vector(1, nglass, fray2.v, -norm(fray2.pos - g1center))
		print("fray2.v = ", fray2.v)
	if mag(fray2.pos - g2center)>R and fray2.pos.y>-H and finside2==True:
		finside2=False
		print("number f2 second refract")
		fray2.v = refraction_vector(nglass, 1, fray2.v, norm(fray2.pos - g2center))
		print("fray2.v = ", fray2.v)
	if fray2.pos.x <= 0 :
		fdone2 = True
		print("fray2.pos.y = ", fray2.pos.y)
	if fray1.pos.x <= 0:
		print("fray1.pos.y = ", fray1.pos.y)
		fdone1 = True
	if fdone1 and fdone2:
		break	
for y in range(0, 7):
	ddot = gdots(color=vec(random(), random(), random()), graph = dgraph)
	for z in range(-20, 20):
		for x in range(-20, 20):
			
			receiver.pos = receiverpos+vec(x*0.05, 0, z*0.05)
			obj.pos = objpos+vec(x*0.05, -y*0.2, z*0.05)
			isin2 = False
			isin1 = False
			over1 = False
			over2 = False
			fpos=0
			if mag(ray2.pos - obj.pos)<=1:
				# print(obj.pos.y, " 2 is in")
				isin2 = True
				fpos = ray2.pos.y
			else:
				# print(obj.pos.y, " 2 is not in")
				over2 = True
			
			if mag(ray1.pos - obj.pos)<=1:
				# print(obj.pos.y, " 1 is in")
				isin1 = True
				fpos = ray1.pos.y
			else:
				# print(obj.pos.y, " 1 is not in")
				over1 = True
			if isin1 == True or isin2 == True:
				# print("fpos = ", fpos)
				ddot.plot(pos=(0.05*x, 0.05*z))
				sleep(0.01)


