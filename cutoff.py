def vector_del(a,b):#矢量相减
    return [float(a[0])-float(b[0]),float(a[1])-float(b[1]),float(a[2])-float(b[2])]#,float(a[3])-float(b[3]),float(a[4])-float(b[4])]
def build_pool_dict(pool):
    pool_dict = {}
    for item in pool:
        key = tuple(item[:5])  
        pool_dict[key] = item[5:]  
    return pool_dict
def find(pre, pool_dict):
    pre_tuple = tuple(pre)  
    return pool_dict.get(pre_tuple, [0, 0])
f1=open("./wannier90_hr.datS","r")
f2=open("./wannier90_hr.dat","r")
data=[];data1=[]
for d in f1.readlines():
    d1=[float(p) for p in d.strip().split()]
    data.append(d1)
for d2 in f2.readlines():
    d3=[float(p2) for p2 in d2.strip().split()]
    data1.append(d3)
f1.close();f2.close()
pool_dict = build_pool_dict(data1)
a1list=[]
for i in range(len(data)):
      if [int(data[i][0]),int(data[i][1]),int(data[i][2]),int(data[i][4])] not in a1list:
           a1list.append([int(data[i][0]),int(data[i][1]),int(data[i][2]),int(data[i][4])])
dot1=[5,10,0];dot2=[5,-5,0];dot3=[-10,-5,0];datao=[];datam=[];lengt=len(data)
for ast in a1list:
    for aen in a1list:
            start=ast[:3];end=aen[:3]
            r0=vector_del(end,start)
            r1=r0+[ast[3]]+[aen[3]]
            finding=find(r1,pool_dict)
            datam.append(start+end+[ast[3]]+[aen[3]]+finding)
print("Finding Done.")
for l in range(len(datam)):
    datao.append(str(int(datam[l][0]))+"    "+str(int(datam[l][1]))+"    "+str(int(datam[l][2]))+"    "+str(int(datam[l][3]))+"    "+str(int(datam[l][4]))+"    "+str(int(datam[l][5]))+"    "+str(int(datam[l][6]))+"    "+str(int(datam[l][7]))+"    "+"{:.14f}".format(datam[l][8])+"    "+"{:.14f}".format(datam[l][9])+"\n")
f2=open("./wannier90_hr.datO","w")
f2.writelines(datao)
f2.close()