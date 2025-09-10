# AI Workflow

This is an AI-powered workflow using CrewAI agents to accomplish complex tasks through collaboration.

## Workflow Steps

1. **retrieve_historical_stock_data**: Retrieve historical stock prices for major indices and stocks.
2. **clean_and_process_stock_data**: Clean and process the retrieved stock data. (using output from retrieve_historical_stock_data)
3. **calculate_stock_metrics**: Calculate key metrics for each stock, such as daily returns and volatility. (using output from clean_and_process_stock_data)
4. **analyze_sector_performance**: Analyze the performance of different sectors in the stock market. (using output from calculate_stock_metrics)
5. **identify_trending_stocks**: Identify stocks that are trending upwards or downwards. (using output from calculate_stock_metrics)
6. **generate_insights_and_recommendations**: Generate insights and recommendations based on the analysis. (using output from analyze_sector_performance, identify_trending_stocks)
7. **visualize_stock_market_data**: Visualize key stock market data and insights. (using output from calculate_stock_metrics, analyze_sector_performance)
8. **summarize_analysis_results**: Summarize the results of the stock market analysis. (using output from generate_insights_and_recommendations, visualize_stock_market_data)

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
