from typing import List

import re
from datetime import datetime


def identify_peak_utilization_times(cpu_metrics: str, memory_metrics: str, container_logs: str) -> List[str]:
    """
    Identify peak resource utilization times based on CPU metrics, memory metrics, and container logs.

    Args:
        cpu_metrics: Input parameter of type str
memory_metrics: Input parameter of type str
container_logs: Input parameter of type str

    Returns:
        List[str]: Output of type List[str]
    """
    
    peak_times = []
    
    # Parse CPU metrics to find high utilization periods
    cpu_lines = cpu_metrics.strip().split('\n')
    for line in cpu_lines:
        if line.strip():
            # Look for patterns like "timestamp cpu_usage%" or similar
            parts = line.split()
            if len(parts) >= 2:
                try:
                    # Try to extract timestamp and CPU percentage
                    timestamp_str = parts[0]
                    cpu_value = float(re.sub(r'[^0-9.]', '', parts[1]))
                    
                    # Consider CPU usage above 80% as peak
                    if cpu_value > 80.0:
                        peak_times.append(timestamp_str)
                except (ValueError, IndexError):
                    continue
    
    # Parse memory metrics to find high utilization periods
    memory_lines = memory_metrics.strip().split('\n')
    for line in memory_lines:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                try:
                    timestamp_str = parts[0]
                    memory_value = float(re.sub(r'[^0-9.]', '', parts[1]))
                    
                    # Consider memory usage above 85% as peak
                    if memory_value > 85.0 and timestamp_str not in peak_times:
                        peak_times.append(timestamp_str)
                except (ValueError, IndexError):
                    continue
    
    # Parse container logs for error patterns or high activity indicators
    log_lines = container_logs.strip().split('\n')
    for line in log_lines:
        if line.strip():
            # Look for error patterns or high activity indicators
            if any(keyword in line.lower() for keyword in ['error', 'timeout', 'overload', 'high load']):
                # Extract timestamp from log line (common formats)
                timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}', line)
                if timestamp_match:
                    timestamp_str = timestamp_match.group()
                    if timestamp_str not in peak_times:
                        peak_times.append(timestamp_str)
    
    # Remove duplicates and sort chronologically
    unique_peak_times = list(set(peak_times))
    
    try:
        # Attempt to sort chronologically
        def parse_timestamp(ts):
            try:
                # Try common timestamp formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%H:%M:%S']:
                    try:
                        return datetime.strptime(ts, fmt)
                    except ValueError:
                        continue
                return datetime.min
            except:
                return datetime.min
        
        unique_peak_times.sort(key=parse_timestamp)
    except:
        # If sorting fails, return as is
        pass
    
    return unique_peak_times