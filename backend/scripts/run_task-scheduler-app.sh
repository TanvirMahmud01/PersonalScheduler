#!/bin/bash

# Path to virtual environment
VENV_PATH="/home/tm/Documents/personal_projects/PersonalScheduler/backend/.mint-venv"

# Activate the virtual environment
source $VENV_PATH/bin/activate

# Navigate to project directory
cd /home/tm/Documents/personal_projects/PersonalScheduler/backend

uvicorn main:app --host 0.0.0.0 --port 8000