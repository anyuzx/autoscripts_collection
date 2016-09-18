import os
import sys
import argparse


def main(template, parameter, time, hpc, run):
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
    nfiles = len(parameter_file_lst)

    with open('compute.txt', 'w') as f:
        for fp in parameter_file_lst:
            f.write('python {}/H5MD_Analysis/AnalysisTool.py {} -l {}\n'.format(myapps_path, \
                    fp, os.path.splitext(fp)[0]+'.log'))

    with open('ltt_parameter.temp', 'w') as f:
        f.write('FILENAME=compute.sh\n')
        f.write("job_name=['compute']\n")
        f.write("core_number=[{}]\n".format(nfiles))
        f.write("job_time=[{}]\n".format(time))
        if hpc == 'ls5':
            f.write("job_file=['{}/compute.txt']\n".format(os.getcwd()))
        elif hpc == 'stampede':
            f.write("job_file=['compute.txt']\n")

    if hpc == 'ls5':
        ltt.ltt('{}/launcher_template.ls5'.format(script_path), 'ltt_parameter.temp')
    elif hpc == 'stampede':
        ltt.ltt('{}/launcher_template.stampede'.format(script_path), 'ltt_parameter.temp')

    os.remove('ltt_parameter.temp')

    if run:
        os.system("sbatch convert2h5md.sh")

if __name__  == '__main__':
    parser = argparse.ArgumentParser(description='compute script.')
    parser.add_argument('template', help='specify template file.')
    parser.add_argument('parameter', help='specify parameter file.')
    parser.add_argument('-time', help='specify time required in minute unit.', dest='time', type=int)
    parser.add_argument('-hpc', help='specify HPC cluster. stampede or ls5.', dest='hpc')
    parser.add_argument('-run', help='Submit the job directly. Otherwise this script just generate a slurm script file', action='store_true', dest='run')
    args = parser.parse_args()

    main(args.template, args.parameter, args.time, args.hpc, args.run)
