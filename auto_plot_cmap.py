import sys
import os
import argparse
import glob
import numpy as np

def auto_cmap(input, time, hpc, run, avg, others):
    files = glob.glob(input)
    if len(files) == 0:
        sys.stdout.write('No contact map found. Please check the path is correct.\n')
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

    with open('cmap_plot.txt', 'w') as f:
        for fp in files:
            fp_base = os.path.basename(fp)
            f.write('python {}/toolbox/contactmap.py -in {} -out {}{}\n'.format(myapps_path,\
                fp, 'cmap_'+fp_base+'.png',(lambda x: ' '+others if x is not None else '')(others)))

    if avg is not None:
        for fp in files:
            try:
                cmap += np.load(fp)
            except:
                cmap = np.load(fp)
        np.save(avg, cmap)
        with open('cmap_plot.txt', 'a') as f:
            fp_base = os.path.basename(avg)
            f.write('python {}/toolbox/contactmap.py -in {} -out {}{}\n'.format(myapps_path,\
                avg, fp_base+'.png',(lambda x: ' '+others if x is not None else '')(others)))

    with open('ltt_parameter.temp', 'w') as f:
        f.write('FILENAME=cmap_plot.sh\n')
        f.write("job_name=['cmap_plot']\n")
        f.write("core_number=[{}]\n".format(nfiles))
        f.write("job_time=[{}]\n".format(time))
        if hpc == 'ls5':
            f.write("job_file=['{}/cmap_plot.txt']\n".format(os.getcwd()))
        elif hpc == 'stampede':
            f.write("job_file=['cmap_plot.xt']\n")

    if hpc == 'ls5':
        ltt.ltt('{}/launcher_template.ls5'.format(script_path), 'ltt_parameter.temp')
    elif hpc == 'stampede':
        ltt.ltt('{}/launcher_template.stampede'.format(script_path), 'ltt_parameter.temp')

    os.remove('ltt_parameter.temp')

    if run:
        os.system("sbatch cmap_plot.sh")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script is used to plot contactmap from multiple contactmap data files on TACC using Launcher.')
    parser.add_argument('-in', '--input', help='Contact map data file path. Put quote around wildcard.', dest='input')
    parser.add_argument('-time', help='Specify time required in unit of minute.', dest='time', type=int)
    parser.add_argument('-hpc', help='Specify HPC cluster. Options: stampede or ls5.', dest='hpc', choices=['ls5','stampede'])
    parser.add_argument('-avg', '--average', help='plot average from multiple files. Specify average data file name.', dest='avg', type=str)
    parser.add_argument('-run', help='Submit the job directly. Otherwise this script just generate a slurm script file', action='store_true', dest='run')
    parser.add_argument('-others', help="Specify additional argument. Provide with quote around it. Additional arguments info can be found in toolbox/contactmap.py")
    args = parser.parse_args()

    auto_cmap(args.input, args.time, args.hpc, args.run, args.avg, args.others)
