import os
import sys
import argparse


def main(template, parameter, time, hpc):
    work_path = os.environ['WORK']
    if hpc == 'ls5':
        sys.path.append('{}/myapps/Lammps_Template_Tool'.format(work_path))
        myapps_path = '{}/myapps'.format(work_path)
    elif hpc == 'stampede':
        sys.path.append('{}/stampede/myapps/Lammps_Template_Tool'.format(work_path))
        myapps_path = '{}/stampede/myapps'.format(work_path)
    import ltt

    if time is None:
        sys.stdout.write('ERROR:Please specify a run time.\n')
        sys.stdout.flush()
        sys.exit(0)

    parameter_file_lst = ltt.ltt(template, parameter)
    njobs = len(parameter_file_lst)

    with open('compute.txt', 'w') as f:
        for fp in parameter_file_lst:
            f.write('python {}/H5MD_Analysis/AnalysisTool.py {} -l {}\n'.format(myapps_path, \
                    fp, os.path.splitext(fp)[0]+'.log'))

    with open('compute.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('#SBATCH -J cdp\n')
        f.write('#SBATCH -o cdp.out\n')
        f.write('#SBATCH -n {}\n'.format(njobs))
        f.write('#SBATCH -p normal\n')
        f.write('#SBATCH -t 00:{}:00\n'.format(time))
        if hpc == 'ls5':
            f.write('module load launcher\n')
        elif hpc == 'stampede':
            f.write('module load launcher/2.0\n')
        if hpc == 'ls5':
            f.write('export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins\n')
        elif hpc == 'stampede':
            f.write('export LAUNCHER_PLUGIN_DIR=$TACC_LAUNCHER_DIR/plugins\n')
        f.write('export LAUNCHER_RMI=SLURM\n')
        f.write('export LAUNCHER_JOB_FILE='+os.getcwd()+'/compute.txt\n')
        f.write('$LAUNCHER_DIR/paramrun\n')

if __name__  == '__main__':
    parser = argparse.ArgumentParser(description='compute script.')
    parser.add_argument('template', help='specify template file.')
    parser.add_argument('parameter', help='specify parameter file.')
    parser.add_argument('-time', help='specify time required in minute unit.', dest='time', type=int)
    parser.add_argument('-hpc', help='specify HPC cluster. stampede or ls5.', dest='hpc')
    args = parser.parse_args()

    main(args.template, args.parameter, args.time, args.hpc)
