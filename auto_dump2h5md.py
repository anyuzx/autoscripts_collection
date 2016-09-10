import sys
import glob
import os
import argparse

parser = argparse.ArgumentParser(description='convert LAMMPS dump files to H5MD files.')
parser.add_argument('-in', '--input', help='LAMMPS dump files path.', dest='input')
parser.add_argument('-time', help='specify time required in minute unit.', dest='time')
args = parser.parse_args()

files = glob.glob(args.input)
nfiles = len(files)

with open('dump2h5md.txt', 'w') as f:
    for fp in files:
        f.write('python $WORK/myapps/toolbox/dump2h5md.py {} {} -l {}\n'.format(fp, fp + '.h5', 'convert_' + fp + '.log'))

with open('convert2h5md.sh', 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('#SBATCH -J dump2h5md\n')
    f.write('#SBATCH -o dump2h5md.out\n')
    f.write('#SBATCH -n {}\n'.format(nfiles))
    f.write('#SBATCH -p normal\n')
    f.write('#SBATCH -t 00:{}:00\n'.format(args.time))
    f.write('module load launcher\n')
    f.write('export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins\n')
    f.write('export LAUNCHER_RMI=SLURM\n')
    f.write('export LAUNCHER_JOB_FILE={}/dump2h5md.txt\n'.format(os.getcwd()))
    f.write('$LAUNCHER_DIR/paramrun\n')
