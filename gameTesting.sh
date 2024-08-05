#!/bin/bash

# Initialize variables
total_percentage=0
run_count=0

 
# Loop through seed values from 1 to 777
for seed in {1..100}; do
    # Run the game and capture the output
    output=$(python /Users/karstenlansing/Downloads/MP2/run_game.py --seed $seed --speed 100)
    
    # Extract the percentage from the output using awk
    percentage=$(echo $output | awk -F 'Percentage:' '{print $2}' | awk '{print $1}')

    # Increment run count
    ((run_count++))

    # Add percentage to total
    total_percentage=$(echo "$total_percentage + $percentage" | bc)
done

# Calculate average percentage
average_percentage=$(echo "scale=2; $total_percentage / $run_count" | bc)

echo "Average Percentage: $average_percentage"