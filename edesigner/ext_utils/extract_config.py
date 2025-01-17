import pathlib
import argparse
from lib_config import DesignConfig

def separate_blocks(token):
    fpath = '../results/' + token + '_config.txt'
    with open(fpath, 'r') as inp:
        lines = []
        for line in inp.readlines():
            lines.append(line.rstrip())
            
    config_blocks = []
    block = ""
    block_count = 0
    for line in lines:
        if line.startswith("# End"):
            block += line + "\n"
            config_blocks.append(block)
            block = ""
            block_count += 1

        else:
            block += line + "\n"

    print("Number of libDESIGNs ", int(block_count/2))

    return config_blocks, fpath

def get_specific_block(blocks, fpath, desnum):
    num = desnum*2
    block = blocks[num]
    config = DesignConfig(block)
    config.modify_config()
    config.write_config(fpath)

def modify_bbfile(bbdir, outdir):
    bbpath = '../' + bbdir
    bb_p = pathlib.Path(bbpath)
    for fpath in bb_p.glob('*.csv'):
        fname = fpath.name
        #print(fname)
        if fname.endswith('_int.csv'):
            with open(fpath, 'r') as inp:
                # Skip the header row
                inp.readline()
                if fname.find('C1') > 0:
                    outfname = f"../{outdir}/C1.int.smi"
                elif fname.find('C2') > 0:
                    outfname = f"../{outdir}/C2.int.smi"
                elif fname.find('C3') > 0:
                    outfname = f"../{outdir}/C3.int.smi"
                
                with open(outfname, 'w') as out:
                    for line in inp.readlines():
                        line = line.replace(',', ' ')
                        out.write(line)


if __name__ == '__main__':
    """
    token = "20230428_3Cboth34"
    desnum = 1
    bbdir = "design1"
    outdir = "bbt"
    #blocks, fpath = separate_blocks(token)
    #get_specific_block(blocks, fpath, desnum)
    modify_bbfile(bbdir, outdir)
    """

    parser = argparse.ArgumentParser(description="""extract_config:
    This script extract a specific library configration from the config list generated by lib_design_interpreter.py.
    Building block files required for structure generation will be also prepared from csv files in the indicated folder.
    Note that all the arguments are mandatory.""")

    parser.add_argument('-tk', '--token', help='DbRun_timestamp e.g. 20230428_3Cboth34', type=str, default=None, required=True)
    parser.add_argument('-df', '--design_number', help='number of the design of interest', type=int, default=0, required=True)
    parser.add_argument('-bf', '--bb_folder', help='folder where the bb csv files are stored', type=str,  default=None, required=True)
    parser.add_argument('-of', '--output_folder', help='folder where the processed bb files will be saved', type=str,  default=None, required=True)
    args = parser.parse_args()

    token = args.token
    desnum = args.design_number
    bbdir = args.bb_folder
    outdir = args.output_folder

    blocks, fpath = separate_blocks(token)
    get_specific_block(blocks, fpath, desnum)
    modify_bbfile(bbdir, outdir)