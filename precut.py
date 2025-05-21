from shapely.geometry import Point, Polygon
def vector_sum(a,b):#矢量相加
    return [float(a[0])+float(b[0]),float(a[1])+float(b[1]),float(a[2])+float(b[2])]
def vector_del(a,b):#矢量相减
    return [float(a[0])-float(b[0]),float(a[1])-float(b[1]),float(a[2])-float(b[2])]
def multiple(a,b):
    return [a*float(b[0]),a*float(b[1]),a*float(b[2])]
def vector_dot(a,b):#矢量点乘
    return float(a[0])*float(b[0])+float(a[1])*float(b[1])+float(a[2])*float(b[2])
def vector_cross(a,b):#矢量叉乘
    return [float(a[1])*float(b[2])-float(a[2])*float(b[1]),float(a[2])*float(b[0])-float(a[0])*float(b[2]),float(a[0])*float(b[1])-float(a[1])*float(b[0])]
def cross2D(a,b):#二维向量叉乘
    return float(a[0])*float(b[1])-float(a[1])*float(b[0])
def trans2D(a,baseof):#坐标变换到笛卡尔坐标系
    return [float(a[0])*baseof[0][0]+float(a[1])*baseof[1][0]+float(a[2])*baseof[2][0],float(a[0])*baseof[0][1]+float(a[1])*baseof[1][1]+float(a[2])*baseof[2][1],float(a[0])*baseof[0][2]+float(a[1])*baseof[1][2]+float(a[2])*baseof[2][2]]
def intri(S1,S2,S3,P,Base):
    S1=tuple(trans2D(S1,Base))[:2];S2=tuple(trans2D(S2,Base))[:2];S3=tuple(trans2D(S3,Base))[:2];P=tuple(trans2D(P,Base))[:2]
    polygon=Polygon([S1,S2,S3])
    return polygon.contains(Point(P[0],P[1]))
def flag(at):
    if 1<=int(at)<=5 or 12<=int(at)<=16:
        return 1
    elif 6<=int(at)<=8 or 17<=int(at)<=19:
        return 2
    elif 9<=int(at)<=11 or 20<=int(at)<=22:
        return 3
s0=[];s1=[];av=[];data=[];atom=[]
f0=open("./POSCAR","r")
for s in f0.readlines():
    s0.append(s)
for ii in range(len(s0)):
    if s0[ii].strip()=='Direct':
        s1=s0[ii+1:]
for m in range(len(s1)):
    a1=[float(p) for p in s1[m].strip().split()]
    atom.append(a1)
for ma in range(2,5):
    am1=[float(pm) for pm in s0[ma].strip().split()]
    av.append(am1)
f1=open("./wannier90_hr.dat","r")
data=[]
for d in f1.readlines():
    d1=[float(p) for p in d.strip().split()]
    data.append(d1)
f1.close()
long=float(eval(input("Enter the length of the cut-triangle: ")))
shift1=float(eval(input("Enter the left-shift-x of the cut-triangle: ")))
shift2=float(eval(input("Enter the down-shift-y of the cut-triangle: ")))
dot1=[long*1/3-shift1,long*2/3-shift2,0]
dot2=[long*1/3-shift1,-long*1/3-shift2,0]
dot3=[-long*2/3-shift1,-long*1/3-shift2,0]
datao=[];lengt=len(data)
for l in range(lengt):
    res1=vector_sum(data[l][0:3],atom[int(flag(data[l][4]))-1])
    if intri(dot1,dot2,dot3,res1,av): 
        datao.append(str(int(data[l][0]))+"    "+str(int(data[l][1]))+"    "+str(int(data[l][2]))+"    "+str(int(data[l][3]))+"    "+str(int(data[l][4]))+"    "+"{:.14f}".format(data[l][5])+"    "+"{:.14f}".format(data[l][6])+"\n")
f2=open("./wannier90_hr.datS","w")
f2.writelines(datao)
f2.close()
print("Cutting Process Done.")
