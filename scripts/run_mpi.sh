#!/bin/bash

source prepare.sh
source compile_mpi.sh

# Record start time (epoch seconds for easy calculation)
START_TIME=$(date +%s)
START_TIME_READABLE=$(date)
# echo "Current time: $START_TIME_READABLE"

# Submit job and capture job ID
JOB_OUTPUT=$(sbatch mpi.sh)
JOB_ID=$(echo "$JOB_OUTPUT" | grep -o '[0-9]\+')

# echo "Job submitted: $JOB_OUTPUT"
echo "Monitoring job $JOB_ID for completion..."

# Monitor the completion log until our job appears
LOG_FILE="/var/log/slurm/completed_jobs.log"
TIMEOUT=3600  # 1 hour timeout
ELAPSED=0
SLEEP_INTERVAL=10

while [ $ELAPSED -lt $TIMEOUT ]; do
    if [ -f "$LOG_FILE" ] && grep -q "JobId=$JOB_ID " "$LOG_FILE"; then
        echo "Job $JOB_ID found in completion log!"
        
        # Extract completion time from the log
        # The log format varies, so we'll try to parse it
        JOB_LINE=$(grep "JobId=$JOB_ID " "$LOG_FILE")
        # echo "Job completion entry: $JOB_LINE"
        
        # Try to extract end time (format depends on SLURM version)
        # Common formats include EndTime=YYYY-MM-DDTHH:MM:SS or similar
        if [[ $JOB_LINE =~ EndTime=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}) ]]; then
            END_TIME_STR="${BASH_REMATCH[1]}"
            # Convert to epoch seconds (assuming local timezone)
            END_TIME=$(date -d "${END_TIME_STR}" +%s 2>/dev/null)
            
            if [ $? -eq 0 ]; then
                # Calculate difference
                TIME_DIFF=$((END_TIME - START_TIME))
                MINUTES=$((TIME_DIFF / 60))
                SECONDS=$((TIME_DIFF % 60))
                
                echo "================================================"
                echo "TIMING SUMMARY:"
                echo "Start time:      $START_TIME_READABLE"
                echo "End time:        $(date -d @$END_TIME)"
                echo "Total duration:  ${MINUTES}m ${SECONDS}s ($TIME_DIFF seconds)"
                echo "================================================"
            else
                echo "Could not parse end time from: $END_TIME_STR"
                echo "Raw job line: $JOB_LINE"
            fi
        else
            echo "Could not extract EndTime from job completion log"
            echo "Raw job line: $JOB_LINE"
            echo "You may need to manually check the completion time"
        fi
        
        break
    fi
    
    sleep $SLEEP_INTERVAL
    ELAPSED=$((ELAPSED + SLEEP_INTERVAL))
    
    # Show progress every minute
    if [ $((ELAPSED % 60)) -eq 0 ]; then
        echo "Still waiting for job $JOB_ID to complete... (${ELAPSED}s elapsed)"
    fi
done

if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout reached waiting for job $JOB_ID to complete"
    echo "You can manually check later with: sacct -f $LOG_FILE | grep $JOB_ID"
fi
