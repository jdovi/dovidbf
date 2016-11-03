#!/bin/bash
source $HOME/.pam_environment
source activate dovidbf
cd /home/dovimotors/dovidbf
python convert.py
source deactivate
