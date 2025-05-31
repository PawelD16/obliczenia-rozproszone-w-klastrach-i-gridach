## How to setup SLURM?
Follow this tutorial https://github.com/SergioMEV/slurm-for-dummies

## How to setup OpenMPI?
Follow this tutorial https://webpages.charlotte.edu/abw/coit-grid01.uncc.edu/ParallelProgSoftware/Software/OpenMPIInstall.pdf

## How to setup completion logging?
The following lines were commited to `example_slurm.conf` file:
```bash
JobCompType=jobcomp/filetxt
JobCompLoc=/var/log/slurm/completed_jobs.log
``` 
Then you need to create the directory and set permissions:
```bash
sudo mkdir -p /var/log/slurm
sudo chown slurm:slurm /var/log/slurm
sudo chmod 755 /var/log/slurm
```
If you made these changes after SLURM was already running, you need to restart the service:
```bash
sudo systemctl restart slurmctld
sudo systemctl restart slurmd
```

Using sacct command you can see the completed jobs:
```bash
sacct -f /var/log/slurm/completed_jobs.log
```

## Useful commands
- see info on nodes:
```bash
sinfo -N -l
```

- to reset a drained/invalid node:
```bash
sudo systemctl reset slurmd
sudo systemctl reset slurmctl
sudo scontrol update NodeName=<node name> State=IDLE
```

- to run :
```bash
bash run_<script>.sh
```

- to see current jobs:
```bash
squeue
```

- to see more info on node (like allocated resources or errors):
```bash
scontrol show node <node name>
```


