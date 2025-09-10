from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class analyze_sector_performance_output(BaseModel):
    sector_performance: List[str]  # List of sector names (e.g., technology, healthcare, finance)
    sector_average_returns: List[float]  # List of average returns for each sector
    sector_volatility: List[float]  # List of volatility (standard deviation of returns) for each sector
    sector_counts: List[int]  # List of stock counts for each sector
    is_valid: bool  # Whether the sector performance data is valid

class calculate_stock_metrics_output(BaseModel):
    stock_metrics: List[str]  # List of stock symbols with calculated metrics
    daily_returns: List[float]  # List of daily returns for each stock
    volatility: List[float]  # List of volatility (standard deviation of returns) for each stock
    moving_averages_50_day: List[float]  # List of 50-day moving averages for each stock
    moving_averages_200_day: List[float]  # List of 200-day moving averages for each stock

class clean_and_process_stock_data_output(BaseModel):
    cleaned_data: List[float]  # List of cleaned stock prices
    processed_data: List[float]  # List of processed stock prices with normalized values
    date_formats: str  # List of date formats used for conversion
    missing_value_handling_status: bool  # Whether missing values were handled successfully

class generate_insights_and_recommendations_output(BaseModel):
    sector_performance_insights: str  # Summary of sector performance insights
    trending_stocks: List[str]  # List of trending stocks with their direction (up or down)
    investment_opportunities: List[str]  # List of potential investment opportunities
    portfolio_adjustment_recommendations: List[str]  # List of recommendations for portfolio adjustments
    analysis_summary: str  # Summary of the analysis

class identify_trending_stocks_output(BaseModel):
    stock_symbol: str  # The symbol of the stock (e.g., AAPL, GOOGL)
    trend: str  # The trend identifier (e.g., upward, downward)
    trend_confidence: float  # A confidence score for the trend (e.g., 0.8 for a strong upward trend)
    short_term_trend: str  # The short-term trend (50-day) identifier (e.g., upward, downward)
    long_term_trend: str  # The long-term trend (200-day) identifier (e.g., upward, downward)

class retrieve_historical_stock_data_output(BaseModel):
    stock_symbol: str  # Stock symbol (e.g., AAPL, GOOG, SP500)
    historical_prices: List[float]  # List of daily closing prices over the past year
    date: str  # Date in YYYY-MM-DD format
    is_valid: bool  # Whether the retrieved data is valid

class summarize_analysis_results_output(BaseModel):
    summary: str  # Overall summary of the stock market analysis
    key_findings: List[str]  # List of key findings from the analysis
    insights: List[str]  # List of insights gained from the analysis
    recommendations: List[str]  # List of recommendations for investors
    analysis_validity: bool  # Whether the analysis is valid and reliable

class visualize_stock_market_data_output(BaseModel):
    stock_price_charts: List[str]  # List of file paths or URLs to stock price charts
    sector_performance_plots: List[str]  # List of file paths or URLs to sector performance plots
    stock_returns_histogram: str  # File path or URL to stock returns histogram
    volatility_heatmap: str  # File path or URL to volatility heatmap
    sector_average_returns: List[float]  # List of average returns for each sector
    sector_volatility: List[float]  # List of volatility measures for each sector

