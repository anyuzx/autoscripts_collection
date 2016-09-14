This repository is a collection of several scripts I use on HPC(TACC) often. The scripts are for submitting bunch of jobs on TACC.

## List of files:

* `auto_dump2h5md.py`: convert LAMMPS dump file to H5MD file
* `launcher_template.ls5`: launcher script template on Lonestar 5
* `launcher_template.stampede`: launcher script template on Stampede

## `auto_dump2h5md.py`

This script is used for convert LAMMPS custom dump trajectory files to H5MD format files. It can be used on TACC Lonestar 5 or Stampede. It use `launcher` to submit mutiple jobs on TACC. 
Here is one example:

```bash
python auto_dump2h5md.py -in '*'traj -time 600 -hpc ls5 -run
```

This command will convert all trajectory files to H5MD format on Lonestar 5. The argument `-run` enable the submission of job. Without `-run`, the script will generate a slurm bash script `dump2h5md.sh` which can be submitted manually.