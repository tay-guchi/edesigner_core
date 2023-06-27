import sys
import pathlib
from datetime import datetime
from multiprocessing import Pool
import multiprocessing as multi
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors


def descriptor_calc(smi):
    desc_list = ['MolWt', 'TPSA', 'MolLogP', 'NumAromaticRings', 'NumRotatableBonds', 'HeavyAtomCount', 'FractionCSP3']
    #desc_list = ['MolWt', 'TPSA', 'MolLogP', 'HeavyAtomCount']
    CALCULATOR = MoleculeDescriptors.MolecularDescriptorCalculator(desc_list)
    
    mol = Chem.MolFromSmiles(smi)
    descs = CALCULATOR.CalcDescriptors(mol)
    res_list = [smi]
    for desc in descs:
        if desc:
            res_list.append(str(round(desc, 3)))
        else:
            res_list.append("")
    
    res_row = "\t".join(res_list)
    
    return res_row


def run_calculation(inpfile):
    smis = []
    with open(inpfile, "r") as inp:
        for line in inp.readlines():
            smi, _ = line.split(" ")
            if smi:
                smis.append(smi)
                
    print(f"{len(smis)} compounds will be processed.")
    p = Pool(multi.cpu_count()-2)
    results = p.map(descriptor_calc, smis)
    p.close()
    
    if len(results) == len(smis):
        print("All the structures were successfully calculated")
    else:
        print(f"Error occured for {len(smis)-len(results)} structures")
        
    pref = inpfile.name.split(".")[0]
    outf = pref + "_descs.txt"
    with open(outf, 'w') as out:
        out.write("SMILES\tMW\tTPSA\tLogP\tAROM\tROTB\tHAC\tFSP3\n")
        for res in results:
            out.write(f"{res}\n")
            
            
if __name__ == "__main__":
    inpdir = sys.argv[1]
    #print(inpdir)
    p_obj = pathlib.Path(inpdir)
    
    for inpfile in p_obj.glob('*.smi'):
        #print(inpfile.name)
        if inpfile:
            stime = datetime.now()
            run_calculation(inpfile)
            etime = datetime.now()
            delta = etime - stime	
            print("calculation time {}".format(delta))
        else:
            print("Please specify the input file.")