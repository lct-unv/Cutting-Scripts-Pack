lattice_vectors = []
atomic_coordinates = []
import pandas as pd
def trans2D(a,baseof):#坐标变换到笛卡尔坐标系
    return [float(a[0])*baseof[0][0]+float(a[1])*baseof[1][0]+float(a[2])*baseof[2][0],float(a[0])*baseof[0][1]+float(a[1])*baseof[1][1]+float(a[2])*baseof[2][1],float(a[0])*baseof[0][2]+float(a[1])*baseof[1][2]+float(a[2])*baseof[2][2]]
# Read POSCAR file
with open("POSCAR", 'r') as poscar_file:
    lines = poscar_file.readlines()
    scale_factor = float(lines[1].strip())  # Scaling factor
    lattice_vectors = [[float(x) * scale_factor for x in line.split()] for line in lines[2:5]]
    atomic_coordinates = [[float(x) for x in line.split()[:3]] for line in lines[8:11]]

# Read the Result.txt file and map indices to atomic coordinates
results = []
with open("Result.txt", 'r') as result_file:
    results = [list(map(float, line.strip().split())) for line in result_file]

# Step 3: Map orbital indices to atom types based on specific rules
# Mapping of orbital indices to atom types
def flag(at):
    if 1<=int(at)<=5 or 12<=int(at)<=16:
        return 1
    elif 6<=int(at)<=8 or 17<=int(at)<=19:
        return 2
    elif 9<=int(at)<=11 or 20<=int(at)<=22:
        return 3
def load_mapping(filename):
    #读取 mapping.txt 文件，返回字典：{原子标识符: [轨道编号列表]}
    atom_map = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            items = line.split()
            if len(items) < 2:  # 跳过无效行
                continue
            atom_id = items[0]  # 原子标识符
            orbital_indices = list(map(int, items[1:]))  # 轨道编号列表
            atom_map[int(atom_id)] = orbital_indices
    return atom_map
atom_map = load_mapping('mapping.txt')
# Compute Cartesian coordinates for each row in Result.txt
x_coords = [];y_coords = []
def vector_sum(a,b):#矢量相加
    return [float(a[0])+float(b[0]),float(a[1])+float(b[1]),float(a[2])+float(b[2])]
for result in results:
    frac=vector_sum(result,atomic_coordinates[int(flag(result[3]))-1])
    cartesian_coords = trans2D(frac,lattice_vectors)
    x_coords.append(cartesian_coords[0])
    y_coords.append(cartesian_coords[1])
alphaq=[];cnt=0
for line in range(len(results)):
    alphaq.append([x_coords[cnt],y_coords[cnt]])
    cnt+=1
uni_alphaq=pd.Series(alphaq).tolist()
coords=[]
for i in range(len(uni_alphaq)):
    coords.append([uni_alphaq[i][0],uni_alphaq[i][1]])
with open('coords', 'w') as f:
    for ind in range(len(atom_map)):
        f.write(str(coords[atom_map[ind+1][0]][0])+"    "+str(coords[atom_map[ind+1][0]][1])+"    "+str(ind)+"\n")