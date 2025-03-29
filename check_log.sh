#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=23:00:00
#SBATCH --job-name=check-log
#SBATCH --partition=short
#SBATCH --mem=10Gb
#SBATCH --output=%j.o.slurm
#SBATCH --error=%j.e.slurm

# Get the workflow folder from user input
workflow=$1

if [ -z "$workflow" ]; then
  echo "Error: No workflow folder specified."
  echo "Usage: sbatch check_log.sh <workflow-folder>"
  exit 1
fi

# Use relative path based on current directory
cd "$workflow" || { echo "Directory not found: $workflow"; exit 1; }

# Print current directory and find files with imaginary frequencies
pwd
echo "Files with imaginary frequencies:"
grep -l "imaginary frequencies" *.log

# Count "Normal" terminations, only show files that don't have exactly 2
echo "Files with abnormal 'Normal' count:"
grep -c "Normal" *.log | awk -F: '$2 != 2'
