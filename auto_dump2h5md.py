import sys
import glob
import os
import argparse

def main(input, time, hpc):
    files = glob.glob(input)
    nfiles = len(files)

    # get $WORK directory path
    work_path = os.environ['WORK']

    if hpc is None:
        sys.stdout.write('Please specify HPC cluster. Options: stampede and ls5.')
        sys.stdout.flush()
        sys.exit(0)

    if hpc == 'ls5':
        myapps_path = $WORK/myapps
    elif hpc == 'stampede':
        myapps_path = $WORK/stampede/myapps

    script_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(work_path+'/myapps/Lammps_Template_Tool')
    import ltt

    if time is None:
        sys.stdout.write('ERROR:Please specify a run time.\n')
        sys.stdout.flush()
        sys.exit(0)

    with open('dump2h5md.txt', 'w') as f:
        for fp in files:
            f.write('python {}/toolbox/dump2h5md.py {} {} -l {}\n'.format(myapps_path, \
                    fp, fp + '.h5', 'convert_' + fp + '.log'))

    with open('ltt_parameter.temp', 'w') as f:
        f.write('FILE: convert2h5md.sh\n')
        f.write("job_name='dump2h5md'\n")
        f.write("core_number={}\n".format(nfiles))
        f.write("job_time={}\n".format(time))
        if hpc == 'ls5':
            f.write("job_file={}/dump2h5md.txt\n".format(os.getcwd()))
        elif hpc == 'stampede':
            f.write("job_file=dump2h5md.txt\n")

    if hpc == 'ls5':
        ltt.main('{}/launcher_template.ls5', '{}/ltt_parameter.temp'.format(script_path, script_path))
    elif hpc == 'stampede':
        ltt.main('{}/launcher_template.stampede', '{}/ltt_parameter.temp'.format(script_path, script_path))

    #os.system("sbatch convert2h5md.sh")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert LAMMPS dump files to H5MD files.')
    parser.add_argument('-in', '--input', help='LAMMPS dump files path.', dest='input')
    parser.add_argument('-time', help='specify time required in minute unit.', dest='time', type=int)
    parser.add_argument('-hpc', help='specify HPC cluster. stampede or ls5.', dest='hpc')
    args = parser.parse_args()

    main(args.input, args.time, args.hpc)
