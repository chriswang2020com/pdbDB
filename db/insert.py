import pymysql
import os
import re
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors

# Connect to the database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="000000",
  database="pdbqtDB"
)

# Create cursor
mycursor = mydb.cursor()

# Specify the directory you want to read from
dir_path = '~/output'

# Convert the tilde in the path to the user's home directory
dir_path = os.path.expanduser(dir_path)

# Get a list of all files in the directory
files = os.listdir(dir_path)

def importmolecule(dir_path, files):
    # For each file in the directory
    for filename in files:
        # If the file has the .pdbqt extension
        if filename.endswith(".pdbqt"):
            # Read the file
            with open(os.path.join(dir_path, filename), 'r') as file:
                pdbqt_text = file.read()

                # Search for SMILES string
                smiles_search = re.search(r'REMARK    SMILES: (.*)', pdbqt_text)

                if smiles_search:
                    smiles_string = smiles_search.group(1)
                    #print("SMILES String for file ", filename, " is ", smiles_string)
                    # 从 SMILES 字符串创建一个分子对象
                    molecule = Chem.MolFromSmiles(smiles)

                    # 计算各种性质
                    MW = Descriptors.MolWt(molecule)  # 分子量
                    HBA1 = Lipinski.NumHAcceptors(molecule)  # 氢键受体数量
                    HBA2 = rdMolDescriptors.CalcNumLipinskiHBA(molecule)  # Lipinski规则的氢键受体数量
                    HBD = Lipinski.NumHDonors(molecule)  # 氢键供体数量
                    SlogP = Descriptors.MolLogP(molecule)  # 分子的SlogP
                    TPSA = rdMolDescriptors.CalcTPSA(molecule)  # 分子的拓扑极性表面积
                    RotB = Descriptors.NumRotatableBonds(molecule)  # 可旋转键的数量

                    # Insert file content to database
                    sql = "INSERT INTO pdbqtData (pdbqtText, smiles, MW, HBA1, HBA2, HBD, SlogP, TPSA, RotB) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (pdbqt_text, smiles_string, MW, HBA1, HBA2, HBD, SlogP, TPSA, RotB)
                    mycursor.execute(sql, val)
            
importmolecule(dir_path,files)            
# Commit the transaction
mydb.commit()

print(len(files), "records inserted.")

# Close the connection
mydb.close()
