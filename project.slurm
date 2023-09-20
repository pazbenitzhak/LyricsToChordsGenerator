#! /bin/sh

#SBATCH --job-name=project
#SBATCH --output=results/project.out # redirect stdout
#SBATCH --error=results/project.err # redirect stderr
#SBATCH --partition=studentkillable # (see resources section)
#SBATCH --time=300 # max time (minutes)
#SBATCH --signal=USR1@120 # how to end job when time’s up
#SBATCH --nodes=1 # number of machines
#SBATCH --ntasks=1 # number of processes
#SBATCH --mem=100000 # CPU memory (MB)
#SBATCH --cpus-per-task=4 # CPU cores per process
#SBATCH --gpus=4 # GPUs in total


# Create and activate a virtual environment
python -m venv nlp_project
# source myenv/bin/activate

# Install required packages within the virtual environment
# pip install requirements.txt

# Run your Python script or any other commands
python project.py

# Deactivate the virtual environment when you're done
conda deactivate

