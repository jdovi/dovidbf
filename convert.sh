#!/bin/bash
source $HOME/.pam_environment
source activate dovidbf
cd /home/sysadmin/dovidbf
python convert.py
source deactivate
