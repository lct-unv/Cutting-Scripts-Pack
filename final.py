import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.spatial import ConvexHull
from shapely.geometry import Point, LineString, Polygon
# 读取坐标文件并处理
atomord = np.loadtxt('coords')
atoms = atomord[:, :-1].T  # 转置并去掉最后一列后再转置回来

# 绘制原子坐标二维图
plt.figure()
plt.scatter(atoms[0], atoms[1], s=5)
plt.title("Atoms Position")
plt.show()

data = np.loadtxt('matrix.datpro', delimiter='\t')
max_index = int(max(data[:, 0].max(), data[:, 1].max()))
# Initialize the matrix as a complex type
H = np.zeros((max_index, max_index), dtype=np.complex128)
for row in data:
    i, j, re, im = row
    H[int(i) - 1, int(j) - 1] = re + 1j * im  
# 计算特征系统
eigen_values, eigen_vectors = np.linalg.eigh(H)  

print("特征系统维度:", eigen_values.shape, eigen_vectors.shape)
EI = eigen_values
dim = len(EI)

# 计算特征向量范数
norms = [np.linalg.norm(eigen_vectors[:, i]) for i in range(dim)]

# 绘制特征值分布
plt.figure()
plt.scatter(range(dim), EI, s=5)
plt.title("Eigenvalues")
plt.show()

# 筛选特定范围特征值
cornerEI = EI[(EI > -2.5) & (EI < -1.5)]

# 处理第470个特征向量（Python索引从0开始，此为单个版）
'''
nb = 452  # 453-1
eigennb = eigen_vectors[:, nb]
'''
# 处理指定的特征向量
target_indices = [479] #Corner:438,439,440;Edge:
# 读取映射文件
# --- 处理不规则mapping文件 ---
def load_mapping(filename):
    """读取列数不一致的映射文件，返回列表的列表"""
    atommap = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            items = line.split()
            if len(items) < 1:  # 跳过无效行
                continue
            # 格式：标识符 + 轨道索引（允许索引数量不同）
            atommap.append([items[0]] + list(map(int, items[1:]))) 
    return atommap

# 读取映射文件（自动处理不同列数）
atommap = load_mapping('mapping.txt')

# --- 计算DOS（单个特征向量版） ---
'''
DOS = []
for row in atommap:
    if len(row) < 2:  # 跳过无索引的行
        continue
    identifier = row[0]
    indices = np.array(row[1:]) - 1  # 假设原始索引是1-based，转为0-based
    # 检查索引是否越界
    if np.any(indices < 0) or np.any(indices >= len(eigennb)):
        print(f"警告：{identifier} 的索引越界，已跳过")
        continue
    dos = np.sum(np.abs(eigennb[indices])**2)
    DOS.append(dos)
'''
# --- 计算多个特征向量的DOS ---
def calculate_dos(target_indices):
    DOS_total = np.zeros(len(atommap))  # 初始化总DOS
    for idx in target_indices:
        eigennb = eigen_vectors[:, idx]  # 当前特征向量
        DOS = []
        for row in atommap:
            if len(row) < 2:  # 跳过无索引的行
                continue
            identifier = row[0]
            indices = np.array(row[1:]) - 1  # 假设原始索引是1-based，转为0-based
        # 检查索引是否越界
            if np.any(indices < 0) or np.any(indices >= len(eigennb)):
                print(f"警告：{identifier} 的索引越界，已跳过")
                continue
            dos = np.sum(np.abs(eigennb[indices])**2)
            DOS.append(dos)
    # 将当前特征向量的DOS加入总DOS
        DOS_total += np.array(DOS)
    return DOS_total
# --- 构建3D数据点（单个版） ---
# 确保原子坐标数量与DOS长度匹配
'''
if len(DOS) != atomord.shape[0]:
    raise ValueError("DOS长度与原子坐标数量不匹配，请检查mapping文件")

dosatom = np.hstack((atomord[:, :2], np.array(DOS)[:, np.newaxis]))
'''
# --- 构建3D数据点 ---
# 确保原子坐标数量与DOS长度匹配
DOS_tot = calculate_dos(target_indices)
if len(DOS_tot) != atomord.shape[0]:
    raise ValueError("DOS长度与原子坐标数量不匹配，请检查mapping文件")
dosatom = np.hstack((atomord[:, :2], DOS_tot[:, np.newaxis]))

# --- 可视化 ---
fig = plt.figure()
ax = fig.add_subplot(111)#, projection='3d')
sc = ax.scatter(dosatom[:, 0], dosatom[:, 1],c=dosatom[:, 2], cmap='rainbow', s=1000*dosatom[:, 2])
plt.colorbar(sc, label='DOS')
ax.set_title("3D DOS Distribution")
plt.show()
# --- 获取原子状态 ---
coords = np.loadtxt('coords.txt')

# 分离 x, y 坐标和标签
x_coords = coords[:, 0]
y_coords = coords[:, 1]
labels = coords[:, 2].astype(int)

# 创建一个空白图像用于可视化
img_size = 1000
img = np.zeros((img_size, img_size, 3), np.uint8)

# 将坐标缩放到图像尺寸
x_min = np.min(x_coords)
x_max = np.max(x_coords)
y_min = np.min(y_coords)
y_max = np.max(y_coords)

x_scale = img_size / (x_max - x_min)
y_scale = img_size / (y_max - y_min)

scaled_x = ((x_coords - x_min) * x_scale).astype(int)
scaled_y = ((y_coords - y_min) * y_scale).astype(int)

# 绘制所有点
for x, y, label in zip(scaled_x, scaled_y, labels):
    cv2.circle(img, (x, y), 5, (255, 255, 255), -1)
    cv2.putText(img, str(label), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# 找到点的凸包
hull = ConvexHull(coords[:, :2])

# 将凸包点的坐标缩放到图像尺寸
hull_scaled_x = ((coords[hull.vertices, 0] - x_min) * x_scale).astype(int)
hull_scaled_y = ((coords[hull.vertices, 1] - y_min) * y_scale).astype(int)

# 绘制凸包
for i in range(len(hull.vertices)):
    cv2.line(img, (hull_scaled_x[i], hull_scaled_y[i]), 
             (hull_scaled_x[(i+1)%len(hull.vertices)], hull_scaled_y[(i+1)%len(hull.vertices)]), 
             (0, 255, 0), 2)

# 找出凸包顶点和边上的点
vertex_points = []
edge_points = []

# 找出与凸包顶点最近的点
for vertex in hull.vertices:
    vertex_points.append(vertex)

# 创建凸包多边形
convex_polygon = Polygon(coords[hull.vertices, :2])

# 找出凸包边上的点（不包括顶点）
for i, (x, y) in enumerate(coords[:, :2]):
    if i in vertex_points:
        continue  # 跳过顶点
    point = Point(x, y)
    # 检查点是否在凸包的边上
    on_edge = False
    for j in range(len(hull.vertices)):
        pt1 = coords[hull.vertices[j]]
        pt2 = coords[hull.vertices[(j+1) % len(hull.vertices)]]
        line = LineString([pt1, pt2])
        if line.distance(point) < 1e-5:
            edge_points.append(i)
            break
# 输出凸包顶点和边上的点的标签
print("凸包顶点上的点的标签:")
corneratom=set([int(labels[idx]) for idx in vertex_points])
print(corneratom)
print("凸包边上的点的标签:")
edgeatom=set([int(labels[idx]) for idx in edge_points])
print(edgeatom)
stateatom=set([i for i in range(0,len(DOS_tot))])
bulkatom=stateatom-corneratom-edgeatom
# --- 染色 ---
def colorstate(corner,edge,bulk,state):
    R=0;G=0;B=0
    doslist=calculate_dos([state])
    R=sum([doslist[i] for i in corner])/len(corner)
    G=sum([doslist[i] for i in edge])/len(edge)
    B=sum([doslist[i] for i in bulk])/len(bulk)
    R0=R/(R+G+B);G0=G/(R+G+B);B0=B/(R+G+B)
    if R0>14.83/24:
        return (1,0,0)
    else:
        return (0,0,1)
colormap=[colorstate(corneratom,edgeatom,bulkatom,i) for i in range(len(EI))]
plt.figure()
plt.scatter(range(dim)[650:700], EI[650:700], s=150, c=colormap[650:700])
plt.title("Eigenvalues")
plt.show()
