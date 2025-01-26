import numpy as np
import matplotlib.pyplot as plt

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
target_indices = [476]
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

# --- 构建3D数据点（单个版） ---
# 确保原子坐标数量与DOS长度匹配
'''
if len(DOS) != atomord.shape[0]:
    raise ValueError("DOS长度与原子坐标数量不匹配，请检查mapping文件")

dosatom = np.hstack((atomord[:, :2], np.array(DOS)[:, np.newaxis]))
'''
# --- 构建3D数据点 ---
# 确保原子坐标数量与DOS长度匹配
if len(DOS_total) != atomord.shape[0]:
    raise ValueError("DOS长度与原子坐标数量不匹配，请检查mapping文件")
dosatom = np.hstack((atomord[:, :2], DOS_total[:, np.newaxis]))

# --- 可视化 ---
fig = plt.figure()
ax = fig.add_subplot(111)#, projection='3d')
sc = ax.scatter(dosatom[:, 0], dosatom[:, 1],c=dosatom[:, 2], cmap='rainbow', s=1000*dosatom[:, 2])
plt.colorbar(sc, label='DOS')
ax.set_title("3D DOS Distribution")
plt.show()