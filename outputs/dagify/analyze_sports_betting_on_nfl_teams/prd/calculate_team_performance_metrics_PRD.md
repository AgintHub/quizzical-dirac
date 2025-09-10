# calculate_team_performance_metrics PRD

## Description
Calculate performance metrics for NFL teams, including their win rates, points scored, and other relevant statistics.


## Implementation Plan

### 1. Retrieve cleaned team data from the output of the 'clean_and_process_data' node

| Category | Details |
| --- | --- |
| **Reason** | The 'clean_and_process_data' node provides the necessary cleaned team data for calculating performance metrics |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the 'cleaned_teams_data' output field from the 'clean_and_process_data' node |

### 2. Calculate win rates for each team using their win-loss records

| Category | Details |
| --- | --- |
| **Reason** | Win rates are a crucial performance metric for NFL teams |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Use the 'processed_win_loss_records' output field from the 'clean_and_process_data' node and apply a formula to calculate win rates |

### 3. Calculate points scored and allowed for each team

| Category | Details |
| --- | --- |
| **Reason** | Points scored and allowed are essential performance metrics for NFL teams |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the 'cleaned_points_scored' output field from the 'clean_and_process_data' node |

### 4. Calculate yards gained for each team

| Category | Details |
| --- | --- |
| **Reason** | Yards gained is a relevant performance metric for NFL teams |
| **Impact** | MEDIUM |
| **Complexity** | MEDIUM |
| **Method** | Use the 'processed_win_loss_records' output field from the 'clean_and_process_data' node and apply a formula to calculate yards gained |

### 5. Compile the calculated metrics into a list of teams with their corresponding metrics

| Category | Details |
| --- | --- |
| **Reason** | The output should be a comprehensive list of teams with their performance metrics |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use a data structure such as a Pandas DataFrame to compile the metrics |
