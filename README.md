## How to setup SLURM?
Follow this tutorial https://github.com/SergioMEV/slurm-for-dummies

## How to setup OpenMPI?
Follow this tutorial https://webpages.charlotte.edu/abw/coit-grid01.uncc.edu/ParallelProgSoftware/Software/OpenMPIInstall.pdf

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


