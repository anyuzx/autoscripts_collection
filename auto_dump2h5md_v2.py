import sys
import glob
import os
import argparse

def dump2h5md(input, time, hpc, run):
    files = glob.glob(input)
    if len(files) == 0:
        sys.stdout.write('No trajectories found. Please check the path is correct.\n')
        sys.stdout.flush()
        sys.exit(0)
    else:
        for fp in files:
            if os.path.isfile(fp):
                continue
            else:
                sys.stdout.write('{} is not a file.\n'.format(fp))
                sys.stdout.flush()
                sys.exit(0)

    nfiles = len(files)

    # get $WORK directory path
    work_path = os.environ['WORK']

    if hpc is None:
        sys.stdout.write('Please specify HPC cluster. Options: stampede and ls5.')
        sys.stdout.flush()
        sys.exit(0)

    if hpc == 'ls5':
        myapps_path = '{}/myapps'.format(work_path)
    elif hpc == 'stampede':
        myapps_path = '{}/stampede/myapps'.format(work_path)

    script_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(myapps_path+'/Lammps_Template_Tool')
    import ltt

    if time is None:
        sys.stdout.write('ERROR:Please specify a run time.\n')
        sys.stdout.flush()
        sys.exit(0)

    with open('dump2h5md.txt', 'w') as f:
        for fp in files:
            fp_base = os.path.basename(fp)
            f.write('python {}/toolbox/dump2h5md.py {} {} -l {}{}\n'.format(myapps_path, \
                    fp, fp_base + '.h5', 'convert_' + fp + '.log', \
                    (lambda x: ' '+args.others if x is not None else '')(args.others)))

    with open('ltt_parameter.temp', 'w') as f:
        f.write('FILENAME=convert2h5md.sh\n')
        f.write("job_name=['dump2h5md']\n")
        f.write("core_number=[{}]\n".format(nfiles))
        f.write("job_time=[{}]\n".format(time))
        if hpc == 'ls5':
            f.write("job_file=['{}/dump2h5md.txt']\n".format(os.getcwd()))
        elif hpc == 'stampede':
            f.write("job_file=['dump2h5md.txt']\n")

    if hpc == 'ls5':
        ltt.ltt('{}/launcher_template.ls5'.format(script_path), 'ltt_parameter.temp')
    elif hpc == 'stampede':
        ltt.ltt('{}/launcher_template.stampede'.format(script_path), 'ltt_parameter.temp')

    os.remove('ltt_parameter.temp')

    if run:
        os.system("sbatch convert2h5md.sh")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert LAMMPS dump files to H5MD files.')
    parser.add_argument('-in', '--input', help='LAMMPS dump files path.', dest='input')
    parser.add_argument('-time', help='specify time required in minute unit.', dest='time', type=int)
    parser.add_argument('-hpc', help='specify HPC cluster. stampede or ls5.', dest='hpc')
    parser.add_argument('-run', help='run the job directly.', action='store_true', dest='run')
    parser.add_argument('-others', help="specify additional argument. Provide with quote around it. Example: -others '-others -s 10'.", type=str, dest='others')
    args = parser.parse_args()

    dump2h5md(args.input, args.time, args.hpc, args.run, args.others)
