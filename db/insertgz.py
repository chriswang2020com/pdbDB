import os
import tarfile
import pymysql
import re
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski
from rdkit.Chem import rdMolDescriptors
import time
from pathlib import Path
# Connect to the database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="000000",
  database="pdbqtDB"
)
# Create cursor
mycursor = mydb.cursor()


def opengz(targz_path, i):
    begintime = time.time()

    data_to_insert = []
    sql = "INSERT INTO pdbqtData (pdbqtText, smiles, MW, HBA1, HBA2, HBD, SlogP, TPSA, RotB) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    print("loading...")

    with tarfile.open(targz_path) as tar_file:
        for member in tar_file.getmembers():
            i += 1
            if Path(member.name).suffix != ".pdbqt":
                continue
            id = Path(member.name).stem
            pdbqt_tmp = tar_file.extractfile(member).read()
            pdbqt_text = pdbqt_tmp.decode('ascii')
            smiles_search = re.search(r'REMARK    SMILES: (.*)', pdbqt_text)
            if smiles_search:
                smiles_string = smiles_search.group(1)
                #smiles_string = "CC"
                if 'q' in smiles_string:
                    continue  # 如果包含字符"q"，跳过当前文件，处理下一个文件
                # 从 SMILES 字符串创建一个分子对象
                
                try:
                # 计算各种性质
                    molecule = Chem.MolFromSmiles(smiles_string)
                    MW = Descriptors.MolWt(molecule)  # 分子量
                    HBA1 = Lipinski.NumHAcceptors(molecule)  # 氢键受体数量
                    HBA2 = rdMolDescriptors.CalcNumLipinskiHBA(molecule)  # Lipinski规则的氢键受体数量
                    HBD = Lipinski.NumHDonors(molecule)  # 氢键供体数量
                    SlogP = Descriptors.MolLogP(molecule)  # 分子的SlogP
                    TPSA = rdMolDescriptors.CalcTPSA(molecule)  # 分子的拓扑极性表面积
                    RotB = Descriptors.NumRotatableBonds(molecule)  # 可旋转键的数量

                    # Insert file content to database

                    val = ("TEST", smiles_string, MW, HBA1, HBA2, HBD, SlogP, TPSA, RotB)
                    data_to_insert.append(val)
                    #mycursor.execute(sql, val)
                except:
                    val = ("TEST", smiles_string, 0, 0, 0, 0, 0, 0, 0)
                    data_to_insert.append(val)
                    #mycursor.execute(sql, val)
    #print(data_to_insert)
    mycursor.executemany(sql,data_to_insert)
    mydb.commit()

    endtime = time.time()

    print("time", endtime-begintime)
    
    return None    
            

def opendir(dir_path):
    contents = os.listdir(dir_path)
    dirs = [item for item in contents if os.path.isdir(os.path.join(dir_path, item))]
    i = 0
    # iterate over each directory
    for dir in dirs:
        dir_full_path = os.path.join(dir_path, dir)

        # iterate over each file in the directory
        for filename in os.listdir(dir_full_path):
            if filename.endswith('.tar.gz'):
                opengz(os.path.join(dir_full_path, filename), i)
    print("FILE PROCESSED: ", i)
    mydb.close()

    

    
opendir(os.path.expanduser('~/pdbDB/pdbDB/db/input/DF'))
