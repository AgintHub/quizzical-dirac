# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **collect_betting_odds_data**: Collect data on sports betting odds for NFL teams, including point spreads, moneylines, and over/unders.
2. **collect_nfl_teams_data**: Collect data on NFL teams, including their performance, standings, and statistics.
3. **clean_and_process_data**: Clean and process the collected data, including handling missing values and outliers. (using output from collect_nfl_teams_data, collect_betting_odds_data)
4. **analyze_betting_odds**: Analyze the sports betting odds data to identify trends and patterns, and provide insights on the odds. (using output from clean_and_process_data)
5. **calculate_team_performance_metrics**: Calculate performance metrics for NFL teams, including their win rates, points scored, and other relevant statistics. (using output from clean_and_process_data)
6. **generate_insights**: Generate insights on NFL teams based on their performance metrics and betting odds analysis. (using output from calculate_team_performance_metrics, analyze_betting_odds)
7. **visualize_results**: Visualize the results of the analysis, including charts and graphs. (using output from generate_insights)

## Running the Workflow

This workflow is self-contained and requires minimal setup:

1. Install uv if you haven't already:
```bash
pip install uv
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

3. Run the workflow:
```bash
./run.sh
```

That's it! The workflow will automatically handle all dependencies and execution.

## Input/Output

- The workflow accepts input as either plain text or JSON
- Each agent processes its input and produces structured output
- Final results are displayed for each step of the workflow
