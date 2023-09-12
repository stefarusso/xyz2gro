#NEED fftols outpus as xyz input

filename_topol = "topol.top"
filename_xyz = "simbox.xyz"
filename_output = "simbox.gro"
#in angstrom
box_length = 20

#EXTRACT INFO OF THE BOX
#like order of molecules and their number
mols_name=[]
mols_n=[]
with open(filename_topol) as file:
    mol_found = False
    for line in file:
        line=line.strip()
        if "molecules" in line:
            mol_found = True
            continue
        if mol_found:
            if not line:
                break
            line = line.split()
            mols_name.append(line[0])
            mols_n.append(line[1])



def extract_mol_type(filename):
    mol1_list=[]
    with open(filename,"r") as file:
        found=False
        for line in file:
            #use only the lines after "[ atoms ]"
            if "atoms" in line:
                found=True
            if found:
                #stop at the first empty line
                if not line.strip():
                    break
                line=line.strip().split()
                if line[0].isnumeric():
                    mol1_list.append(line[4])
    return mol1_list

atom_types=[]
for mol in mols_name:
    atom_types.append(extract_mol_type(str(mol)+".itp"))


#Extract all the atoms coordinates from xyz
with open(filename_xyz) as file:
    atoms = file.readline()
    atoms = int(atoms.strip().split()[0])
    comment_line = file.readline()
    atom_name,x,y,z = [],[],[],[]
    for line in file:
        line=line.strip().split()
        atom_name.append(line[0])
        x.append(line[1])
        y.append(line[2])
        z.append(line[3])
if len(x)==int(atoms) & len(y)==int(atoms) & len(z)==int(atoms):
    print("Loaded " + str(atoms) + " atoms from the xyz")
else:
    print("ERROR:\nFile lenght mismatch")


#Writing on the file
with open(filename_output,"w") as file:
    comment_string=""
    mol_counter=0
    atom_counter=0
    line_strings=[]
    #create the first 3 column of the gro file with the correct order e repetitions
    for mol in mols_name:
        comment_string = comment_string + mol + " "
    print(comment_string)
    file.write(comment_string+'\n')
    file.write(str(atoms)+"\n")
    for mol in mols_name:
        #repeat for every molecule type in the box
        n_mol = int(mols_n[mols_name.index(mol)])
        mol_idx = mols_name.index(mol)
        for i in range(n_mol):
            #repeat the cycle n times for the same molecule
            atom_types_slice = atom_types[mol_idx]
            mol_counter += 1
            for atom in atom_types_slice:
                atom_counter += 1
                line_strings.append(f'{mol_counter:>5d}{mol:<5s}{atom:>5s}{atom_counter:>5d}')
    #add the x,y,z to the strings
    for line,atom_x,atom_y,atom_z in zip(line_strings,x,y,z):
        #xyz are angstrom so we need to multiply 0.1 for having nanometers
        file.write(f'{line}{float(atom_x)*0.1:>8.3f}{float(atom_y)*0.1:>8.3f}{float(atom_z)*0.1:>8.3f}\n')
    file.write(f'{box_length*0.1:8.3f} {box_length*0.1:8.3f} {box_length*0.1:8.3f} ')







