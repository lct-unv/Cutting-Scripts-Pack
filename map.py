def flag(at):
    if 1<=int(at)<=6 or 13<=int(at)<=18:
        return 1
    elif 7<=int(at)<=9 or 19<=int(at)<=21:
        return 2
    elif 10<=int(at)<=12 or 22<=int(at)<=24:
        return 3
def mapping(file_path):
    result_list = []
    atom_index_map = {}  # Record the type and index of atoms mapping
    current_index = 1    
    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            if len(data) < 4:
                continue
            # Extract the first three columns and the orbit column as a tuple
            lmn = tuple(data[:3])
            orb = int(data[3])
            # Determine the atom type based on the orbit column
            if 1 <= orb <= 6 or 13 <= orb <= 18:
                atom_type = "Gd"
            elif 7 <= orb <= 9 or 19 <= orb <= 21:
                atom_type = "Cl1"
            elif 10 <= orb <= 12 or 22 <= orb <= 24:
                atom_type = "Cl2"
            else:
                continue
            # Conduct the atom identification based on the "lmn" columns and atom type
            atom_id = (lmn, atom_type)
            #  If the atom has been assigned a number, reuse the number; otherwise, assign a new number
            if atom_id not in atom_index_map:
                atom_index_map[atom_id] = current_index
                current_index += 1
            # Get the number and record the result
            result_list.append(atom_index_map[atom_id])
    return result_list,max(result_list)

res,ranindex=mapping("Result.txt");dict={}
for line in range(len(res)):
    if res[line] not in dict:
        dict[res[line]]=[line+1]
    else:
        dict[res[line]].append(line+1)
with open('mapping.txt', 'w') as f:
    for key, value in dict.items():
        stri=str(key)
        for val in value:
            stri+=("    "+str(val)+"    ")
        f.write(stri+"\n")
print("Correspondence Building Done.")

