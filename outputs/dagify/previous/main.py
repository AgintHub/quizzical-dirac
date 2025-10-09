import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.analyze_trading_results import analyze_trading_results
from code.deserialize_monitoring_snapshot import deserialize_monitoring_snapshot
from code.compute_total_trades import compute_total_trades
from code.calculate_win_rate import calculate_win_rate
from code.calculate_average_return_per_trade import calculate_average_return_per_trade
from code.calculate_max_drawdown import calculate_max_drawdown
from code.calculate_sharpe_ratio import calculate_sharpe_ratio
from code.generate_improvement_suggestions import generate_improvement_suggestions
from code.map_suggestions_to_actions import map_suggestions_to_actions
from code.assess_statistical_significance import assess_statistical_significance
from code.validate_output_schema import validate_output_schema
from code.backtest_trading_strategy import backtest_trading_strategy
from code.validate_strategy_definition import validate_strategy_definition
from code.retrieve_historical_price_data import retrieve_historical_price_data
from code.simulate_trade_execution import simulate_trade_execution
from code.calculate_performance_metrics import calculate_performance_metrics
from code.calculate_annualized_return import calculate_annualized_return
from code.generate_performance_summary import generate_performance_summary
from code.collect_historical_market_data import collect_historical_market_data
from code.parse_market_data_request import parse_market_data_request
from code.select_optimal_data_source import select_optimal_data_source
from code.fetch_raw_market_data import fetch_raw_market_data
from code.clean_and_validate_market_data import clean_and_validate_market_data
from code.calculate_data_quality_score import calculate_data_quality_score
from code.format_market_data_output import format_market_data_output
from code.configure_trading_infrastructure import configure_trading_infrastructure
from code.define_trading_strategy import define_trading_strategy
from code.validate_and_structure_data import validate_and_structure_data
from code.compute_descriptive_statistics import compute_descriptive_statistics
from code.generate_technical_indicators import generate_technical_indicators
from code.analyze_indicator_predictive_power import analyze_indicator_predictive_power
from code.formulate_entry_rules import formulate_entry_rules
from code.design_exit_rules import design_exit_rules
from code.create_position_sizing_rule import create_position_sizing_rule
from code.create_risk_management_rule import create_risk_management_rule
from code.filter_tradeable_assets import filter_tradeable_assets
from code.generate_strategy_name import generate_strategy_name
from code.execute_trades import execute_trades
from code.implement_risk_management import implement_risk_management
from code.monitor_trading_performance import monitor_trading_performance
from code.initialize_monitoring_state import initialize_monitoring_state
from code.load_performance_thresholds import load_performance_thresholds
from code.filter_successful_trades import filter_successful_trades
from code.update_position_map import update_position_map
from code.calculate_trade_pnl import calculate_trade_pnl
from code.update_equity_curve import update_equity_curve
from code.evaluate_performance_stability import evaluate_performance_stability
from code.generate_recommended_adjustments import generate_recommended_adjustments
from code.check_alert_conditions import check_alert_conditions
from code.get_current_iso_timestamp import get_current_iso_timestamp
from code.refine_trading_strategy import refine_trading_strategy

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

analyze_trading_results_async = make_async(analyze_trading_results)
deserialize_monitoring_snapshot_async = make_async(deserialize_monitoring_snapshot)
compute_total_trades_async = make_async(compute_total_trades)
calculate_win_rate_async = make_async(calculate_win_rate)
calculate_average_return_per_trade_async = make_async(calculate_average_return_per_trade)
calculate_max_drawdown_async = make_async(calculate_max_drawdown)
calculate_sharpe_ratio_async = make_async(calculate_sharpe_ratio)
generate_improvement_suggestions_async = make_async(generate_improvement_suggestions)
map_suggestions_to_actions_async = make_async(map_suggestions_to_actions)
assess_statistical_significance_async = make_async(assess_statistical_significance)
validate_output_schema_async = make_async(validate_output_schema)
backtest_trading_strategy_async = make_async(backtest_trading_strategy)
validate_strategy_definition_async = make_async(validate_strategy_definition)
retrieve_historical_price_data_async = make_async(retrieve_historical_price_data)
simulate_trade_execution_async = make_async(simulate_trade_execution)
calculate_performance_metrics_async = make_async(calculate_performance_metrics)
calculate_annualized_return_async = make_async(calculate_annualized_return)
generate_performance_summary_async = make_async(generate_performance_summary)
collect_historical_market_data_async = make_async(collect_historical_market_data)
parse_market_data_request_async = make_async(parse_market_data_request)
select_optimal_data_source_async = make_async(select_optimal_data_source)
fetch_raw_market_data_async = make_async(fetch_raw_market_data)
clean_and_validate_market_data_async = make_async(clean_and_validate_market_data)
calculate_data_quality_score_async = make_async(calculate_data_quality_score)
format_market_data_output_async = make_async(format_market_data_output)
configure_trading_infrastructure_async = make_async(configure_trading_infrastructure)
define_trading_strategy_async = make_async(define_trading_strategy)
validate_and_structure_data_async = make_async(validate_and_structure_data)
compute_descriptive_statistics_async = make_async(compute_descriptive_statistics)
generate_technical_indicators_async = make_async(generate_technical_indicators)
analyze_indicator_predictive_power_async = make_async(analyze_indicator_predictive_power)
formulate_entry_rules_async = make_async(formulate_entry_rules)
design_exit_rules_async = make_async(design_exit_rules)
create_position_sizing_rule_async = make_async(create_position_sizing_rule)
create_risk_management_rule_async = make_async(create_risk_management_rule)
filter_tradeable_assets_async = make_async(filter_tradeable_assets)
generate_strategy_name_async = make_async(generate_strategy_name)
execute_trades_async = make_async(execute_trades)
implement_risk_management_async = make_async(implement_risk_management)
monitor_trading_performance_async = make_async(monitor_trading_performance)
initialize_monitoring_state_async = make_async(initialize_monitoring_state)
load_performance_thresholds_async = make_async(load_performance_thresholds)
filter_successful_trades_async = make_async(filter_successful_trades)
update_position_map_async = make_async(update_position_map)
calculate_trade_pnl_async = make_async(calculate_trade_pnl)
update_equity_curve_async = make_async(update_equity_curve)
evaluate_performance_stability_async = make_async(evaluate_performance_stability)
generate_recommended_adjustments_async = make_async(generate_recommended_adjustments)
check_alert_conditions_async = make_async(check_alert_conditions)
get_current_iso_timestamp_async = make_async(get_current_iso_timestamp)
refine_trading_strategy_async = make_async(refine_trading_strategy)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: compute_total_trades, calculate_sharpe_ratio, evaluate_performance_stability, fetch_raw_market_data, map_suggestions_to_actions, check_alert_conditions, collect_historical_market_data, load_performance_thresholds, calculate_trade_pnl, generate_improvement_suggestions, design_exit_rules, initialize_monitoring_state, generate_performance_summary, calculate_max_drawdown, assess_statistical_significance, generate_strategy_name, calculate_data_quality_score, filter_tradeable_assets, clean_and_validate_market_data, deserialize_monitoring_snapshot, formulate_entry_rules, create_position_sizing_rule, get_current_iso_timestamp, validate_and_structure_data, simulate_trade_execution, calculate_win_rate, validate_output_schema, create_risk_management_rule, select_optimal_data_source, update_position_map, calculate_performance_metrics, format_market_data_output, configure_trading_infrastructure, retrieve_historical_price_data, parse_market_data_request, validate_strategy_definition, compute_descriptive_statistics, update_equity_curve, calculate_average_return_per_trade, calculate_annualized_return, filter_successful_trades, generate_technical_indicators, analyze_indicator_predictive_power, generate_recommended_adjustments
    async def run_compute_total_trades():
        # Call the async version of compute_total_trades with results from dependencies
        return await compute_total_trades_async(user_input)

    async def run_calculate_sharpe_ratio():
        # Call the async version of calculate_sharpe_ratio with results from dependencies
        return await calculate_sharpe_ratio_async(user_input)

    async def run_evaluate_performance_stability():
        # Call the async version of evaluate_performance_stability with results from dependencies
        return await evaluate_performance_stability_async(user_input)

    async def run_fetch_raw_market_data():
        # Call the async version of fetch_raw_market_data with results from dependencies
        return await fetch_raw_market_data_async(user_input)

    async def run_map_suggestions_to_actions():
        # Call the async version of map_suggestions_to_actions with results from dependencies
        return await map_suggestions_to_actions_async(user_input)

    async def run_check_alert_conditions():
        # Call the async version of check_alert_conditions with results from dependencies
        return await check_alert_conditions_async(user_input)

    async def run_collect_historical_market_data():
        # Call the async version of collect_historical_market_data with results from dependencies
        return await collect_historical_market_data_async(user_input)

    async def run_load_performance_thresholds():
        # Call the async version of load_performance_thresholds with results from dependencies
        return await load_performance_thresholds_async(user_input)

    async def run_calculate_trade_pnl():
        # Call the async version of calculate_trade_pnl with results from dependencies
        return await calculate_trade_pnl_async(user_input)

    async def run_generate_improvement_suggestions():
        # Call the async version of generate_improvement_suggestions with results from dependencies
        return await generate_improvement_suggestions_async(user_input)

    async def run_design_exit_rules():
        # Call the async version of design_exit_rules with results from dependencies
        return await design_exit_rules_async(user_input)

    async def run_initialize_monitoring_state():
        # Call the async version of initialize_monitoring_state with results from dependencies
        return await initialize_monitoring_state_async(user_input)

    async def run_generate_performance_summary():
        # Call the async version of generate_performance_summary with results from dependencies
        return await generate_performance_summary_async(user_input)

    async def run_calculate_max_drawdown():
        # Call the async version of calculate_max_drawdown with results from dependencies
        return await calculate_max_drawdown_async(user_input)

    async def run_assess_statistical_significance():
        # Call the async version of assess_statistical_significance with results from dependencies
        return await assess_statistical_significance_async(user_input)

    async def run_generate_strategy_name():
        # Call the async version of generate_strategy_name with results from dependencies
        return await generate_strategy_name_async(user_input)

    async def run_calculate_data_quality_score():
        # Call the async version of calculate_data_quality_score with results from dependencies
        return await calculate_data_quality_score_async(user_input)

    async def run_filter_tradeable_assets():
        # Call the async version of filter_tradeable_assets with results from dependencies
        return await filter_tradeable_assets_async(user_input)

    async def run_clean_and_validate_market_data():
        # Call the async version of clean_and_validate_market_data with results from dependencies
        return await clean_and_validate_market_data_async(user_input)

    async def run_deserialize_monitoring_snapshot():
        # Call the async version of deserialize_monitoring_snapshot with results from dependencies
        return await deserialize_monitoring_snapshot_async(user_input)

    async def run_formulate_entry_rules():
        # Call the async version of formulate_entry_rules with results from dependencies
        return await formulate_entry_rules_async(user_input)

    async def run_create_position_sizing_rule():
        # Call the async version of create_position_sizing_rule with results from dependencies
        return await create_position_sizing_rule_async(user_input)

    async def run_get_current_iso_timestamp():
        # Call the async version of get_current_iso_timestamp with results from dependencies
        return await get_current_iso_timestamp_async(user_input)

    async def run_validate_and_structure_data():
        # Call the async version of validate_and_structure_data with results from dependencies
        return await validate_and_structure_data_async(user_input)

    async def run_simulate_trade_execution():
        # Call the async version of simulate_trade_execution with results from dependencies
        return await simulate_trade_execution_async(user_input)

    async def run_calculate_win_rate():
        # Call the async version of calculate_win_rate with results from dependencies
        return await calculate_win_rate_async(user_input)

    async def run_validate_output_schema():
        # Call the async version of validate_output_schema with results from dependencies
        return await validate_output_schema_async(user_input)

    async def run_create_risk_management_rule():
        # Call the async version of create_risk_management_rule with results from dependencies
        return await create_risk_management_rule_async(user_input)

    async def run_select_optimal_data_source():
        # Call the async version of select_optimal_data_source with results from dependencies
        return await select_optimal_data_source_async(user_input)

    async def run_update_position_map():
        # Call the async version of update_position_map with results from dependencies
        return await update_position_map_async(user_input)

    async def run_calculate_performance_metrics():
        # Call the async version of calculate_performance_metrics with results from dependencies
        return await calculate_performance_metrics_async(user_input)

    async def run_format_market_data_output():
        # Call the async version of format_market_data_output with results from dependencies
        return await format_market_data_output_async(user_input)

    async def run_configure_trading_infrastructure():
        # Call the async version of configure_trading_infrastructure with results from dependencies
        return await configure_trading_infrastructure_async(user_input)

    async def run_retrieve_historical_price_data():
        # Call the async version of retrieve_historical_price_data with results from dependencies
        return await retrieve_historical_price_data_async(user_input)

    async def run_parse_market_data_request():
        # Call the async version of parse_market_data_request with results from dependencies
        return await parse_market_data_request_async(user_input)

    async def run_validate_strategy_definition():
        # Call the async version of validate_strategy_definition with results from dependencies
        return await validate_strategy_definition_async(user_input)

    async def run_compute_descriptive_statistics():
        # Call the async version of compute_descriptive_statistics with results from dependencies
        return await compute_descriptive_statistics_async(user_input)

    async def run_update_equity_curve():
        # Call the async version of update_equity_curve with results from dependencies
        return await update_equity_curve_async(user_input)

    async def run_calculate_average_return_per_trade():
        # Call the async version of calculate_average_return_per_trade with results from dependencies
        return await calculate_average_return_per_trade_async(user_input)

    async def run_calculate_annualized_return():
        # Call the async version of calculate_annualized_return with results from dependencies
        return await calculate_annualized_return_async(user_input)

    async def run_filter_successful_trades():
        # Call the async version of filter_successful_trades with results from dependencies
        return await filter_successful_trades_async(user_input)

    async def run_generate_technical_indicators():
        # Call the async version of generate_technical_indicators with results from dependencies
        return await generate_technical_indicators_async(user_input)

    async def run_analyze_indicator_predictive_power():
        # Call the async version of analyze_indicator_predictive_power with results from dependencies
        return await analyze_indicator_predictive_power_async(user_input)

    async def run_generate_recommended_adjustments():
        # Call the async version of generate_recommended_adjustments with results from dependencies
        return await generate_recommended_adjustments_async(user_input)

    # Run level 0 nodes in parallel
    level_0_results = await asyncio.gather(run_compute_total_trades(), run_calculate_sharpe_ratio(), run_evaluate_performance_stability(), run_fetch_raw_market_data(), run_map_suggestions_to_actions(), run_check_alert_conditions(), run_collect_historical_market_data(), run_load_performance_thresholds(), run_calculate_trade_pnl(), run_generate_improvement_suggestions(), run_design_exit_rules(), run_initialize_monitoring_state(), run_generate_performance_summary(), run_calculate_max_drawdown(), run_assess_statistical_significance(), run_generate_strategy_name(), run_calculate_data_quality_score(), run_filter_tradeable_assets(), run_clean_and_validate_market_data(), run_deserialize_monitoring_snapshot(), run_formulate_entry_rules(), run_create_position_sizing_rule(), run_get_current_iso_timestamp(), run_validate_and_structure_data(), run_simulate_trade_execution(), run_calculate_win_rate(), run_validate_output_schema(), run_create_risk_management_rule(), run_select_optimal_data_source(), run_update_position_map(), run_calculate_performance_metrics(), run_format_market_data_output(), run_configure_trading_infrastructure(), run_retrieve_historical_price_data(), run_parse_market_data_request(), run_validate_strategy_definition(), run_compute_descriptive_statistics(), run_update_equity_curve(), run_calculate_average_return_per_trade(), run_calculate_annualized_return(), run_filter_successful_trades(), run_generate_technical_indicators(), run_analyze_indicator_predictive_power(), run_generate_recommended_adjustments())
    results['compute_total_trades'] = level_0_results[0]
    results['calculate_sharpe_ratio'] = level_0_results[1]
    results['evaluate_performance_stability'] = level_0_results[2]
    results['fetch_raw_market_data'] = level_0_results[3]
    results['map_suggestions_to_actions'] = level_0_results[4]
    results['check_alert_conditions'] = level_0_results[5]
    results['collect_historical_market_data'] = level_0_results[6]
    results['load_performance_thresholds'] = level_0_results[7]
    results['calculate_trade_pnl'] = level_0_results[8]
    results['generate_improvement_suggestions'] = level_0_results[9]
    results['design_exit_rules'] = level_0_results[10]
    results['initialize_monitoring_state'] = level_0_results[11]
    results['generate_performance_summary'] = level_0_results[12]
    results['calculate_max_drawdown'] = level_0_results[13]
    results['assess_statistical_significance'] = level_0_results[14]
    results['generate_strategy_name'] = level_0_results[15]
    results['calculate_data_quality_score'] = level_0_results[16]
    results['filter_tradeable_assets'] = level_0_results[17]
    results['clean_and_validate_market_data'] = level_0_results[18]
    results['deserialize_monitoring_snapshot'] = level_0_results[19]
    results['formulate_entry_rules'] = level_0_results[20]
    results['create_position_sizing_rule'] = level_0_results[21]
    results['get_current_iso_timestamp'] = level_0_results[22]
    results['validate_and_structure_data'] = level_0_results[23]
    results['simulate_trade_execution'] = level_0_results[24]
    results['calculate_win_rate'] = level_0_results[25]
    results['validate_output_schema'] = level_0_results[26]
    results['create_risk_management_rule'] = level_0_results[27]
    results['select_optimal_data_source'] = level_0_results[28]
    results['update_position_map'] = level_0_results[29]
    results['calculate_performance_metrics'] = level_0_results[30]
    results['format_market_data_output'] = level_0_results[31]
    results['configure_trading_infrastructure'] = level_0_results[32]
    results['retrieve_historical_price_data'] = level_0_results[33]
    results['parse_market_data_request'] = level_0_results[34]
    results['validate_strategy_definition'] = level_0_results[35]
    results['compute_descriptive_statistics'] = level_0_results[36]
    results['update_equity_curve'] = level_0_results[37]
    results['calculate_average_return_per_trade'] = level_0_results[38]
    results['calculate_annualized_return'] = level_0_results[39]
    results['filter_successful_trades'] = level_0_results[40]
    results['generate_technical_indicators'] = level_0_results[41]
    results['analyze_indicator_predictive_power'] = level_0_results[42]
    results['generate_recommended_adjustments'] = level_0_results[43]

    # Level 1: define_trading_strategy
    async def run_define_trading_strategy():
        # Call the async version of define_trading_strategy with results from dependencies
        return await define_trading_strategy_async(results['collect_historical_market_data'])

    # Run level 1 nodes in parallel
    results['define_trading_strategy'] = await run_define_trading_strategy()

    # Level 2: implement_risk_management, backtest_trading_strategy
    async def run_implement_risk_management():
        # Call the async version of implement_risk_management with results from dependencies
        return await implement_risk_management_async(results['define_trading_strategy'])

    async def run_backtest_trading_strategy():
        # Call the async version of backtest_trading_strategy with results from dependencies
        return await backtest_trading_strategy_async(results['define_trading_strategy'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_implement_risk_management(), run_backtest_trading_strategy())
    results['implement_risk_management'] = level_2_results[0]
    results['backtest_trading_strategy'] = level_2_results[1]

    # Level 3: execute_trades
    async def run_execute_trades():
        # Call the async version of execute_trades with results from dependencies
        return await execute_trades_async(results['backtest_trading_strategy'], results['configure_trading_infrastructure'], results['implement_risk_management'])

    # Run level 3 nodes in parallel
    results['execute_trades'] = await run_execute_trades()

    # Level 4: monitor_trading_performance
    async def run_monitor_trading_performance():
        # Call the async version of monitor_trading_performance with results from dependencies
        return await monitor_trading_performance_async(results['execute_trades'])

    # Run level 4 nodes in parallel
    results['monitor_trading_performance'] = await run_monitor_trading_performance()

    # Level 5: analyze_trading_results
    async def run_analyze_trading_results():
        # Call the async version of analyze_trading_results with results from dependencies
        return await analyze_trading_results_async(results['monitor_trading_performance'])

    # Run level 5 nodes in parallel
    results['analyze_trading_results'] = await run_analyze_trading_results()

    # Level 6: refine_trading_strategy
    async def run_refine_trading_strategy():
        # Call the async version of refine_trading_strategy with results from dependencies
        return await refine_trading_strategy_async(results['analyze_trading_results'])

    # Run level 6 nodes in parallel
    results['refine_trading_strategy'] = await run_refine_trading_strategy()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
