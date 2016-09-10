import sys
import argparse
import os

parser = argparse.ArgumentParser(description='submit jobs')
parser.add_argument('-beta',help='specify beta value', dest='beta')
parser.add_argument('-hpc',help='specify lonestar5/stampede', dest='hpc')
parser.add_argument('-p', '--partition',help='speicfy number of independent jobs', dest='partition', type=int)
args = parser.parse_args()

with open('Chr5_SC_FENE_parameter','w') as f:
    f.write('FILENAME=Chr5_SC_FENE_BETA{{beta}}.in\n')
    f.write("beta=['{}']\n".format(args.beta))
    f.write("index_lst=[' '.join([str(i) for i in range(1,91)])]\n")
    f.write("input_file=['Chr5_SC_SAW_${index_id}.dat']\n")
    f.write("output_file=['Chr5_SC_FENE_BETA{}_${{index_id}}']\n".format(args.beta))
    f.write("seed=[' '.join([str(i) for i in PyRanOrg.choice(1,900000000,90)])]\n")

os.system('python ltt.py Chr5_SC_FENE_template Chr5_SC_FENE_parameter')

with open('Chr5_SC_FENE_BETA{}.sh'.format(args.beta),'w') as f:
    f.write('#!/bin/bash\n')
    f.write('#SBATCH -J Chr5_SC_FENE_BETA{}\n'.format(args.beta))
    f.write('#SBATCH -o Chr5_SC_FENE_BETA{}.out\n'.format(args.beta))
    f.write('#SBATCH -p normal\n')
    f.write('#SBATCH -t 48:00:00\n')
    if args.hpc == 'ls5':
        f.write('#SBATCH -n {}\n'.format(int(args.partition*4)))
    elif args.hpc == 'stampede':
        f.write('#SBATCH -n {}\n'.format(int(args.partition*2)))
    f.write('#SBATCH -N {}\n'.format(args.partition))
    f.write('#SBATCH --mail-user=stefanshi1988@gmail.com\n')
    f.write('#SBATCH --mail-type=ALL\n')
    if args.hpc == 'ls5':
        f.write('export OMP_NUM_THREADS={}\n'.format(6))
    elif args.hpc == 'stampede':
        f.write('export OMP_NUM_THREADS={}\n'.format(8))
    if args.hpc == 'ls5':
        f.write('ibrun tacc_affinity $WORK/lmp_30JUL16_lonestar_intel_cpu_v1 -partition {}x4 -sf omp -in Chr5_SC_FENE_BETA{}.in\n'.format(args.partition, args.beta))
    elif args.hpc == 'stampede':
        f.write('ibrun tacc_affinity $WORK/stampede/lmp_30JUL16_stampede_intel_phi_v1 -partition {}x2 -sf omp -in Chr5_SC_FENE_BETA{}.in\n'.format(args.partition, args.beta))
