"""
Log parsing utilities.
"""

import re
from typing import List, Dict
from datetime import datetime

class LogParser:
    """Parse various log formats and extract errors"""
    
    @staticmethod
    def parse_logs(log_content: str) -> List[Dict]:
        """Extract errors, warnings, and stack traces from logs"""
        errors = []
        lines = log_content.split('\n')
        
        # Common error patterns
        error_patterns = [
            r'ERROR[:\s]+(.+)',
            r'Exception[:\s]+(.+)',
            r'CRITICAL[:\s]+(.+)',
            r'FATAL[:\s]+(.+)',
            r'Failed[:\s]+(.+)',
        ]
        
        warning_patterns = [
            r'WARNING[:\s]+(.+)',
            r'WARN[:\s]+(.+)',
        ]
        
        for i, line in enumerate(lines):
            # Check for errors
            for pattern in error_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    error_info = {
                        'type': 'ERROR',
                        'line_number': i + 1,
                        'message': match.group(1).strip(),
                        'full_line': line.strip(),
                        'timestamp': LogParser._extract_timestamp(line),
                        'severity': 'HIGH'
                    }
                    
                    # Look for stack trace
                    stack_trace = LogParser._extract_stack_trace(lines, i)
                    if stack_trace:
                        error_info['stack_trace'] = stack_trace
                    
                    errors.append(error_info)
                    break
            
            # Check for warnings
            for pattern in warning_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    errors.append({
                        'type': 'WARNING',
                        'line_number': i + 1,
                        'message': match.group(1).strip(),
                        'full_line': line.strip(),
                        'timestamp': LogParser._extract_timestamp(line),
                        'severity': 'MEDIUM'
                    })
                    break
        
        return errors
    
    @staticmethod
    def _extract_timestamp(line: str) -> str:
        """Extract timestamp from log line"""
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}',
            r'\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}',
        ]
        
        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(0)
        return "N/A"
    
    @staticmethod
    def _extract_stack_trace(lines: List[str], start_index: int) -> str:
        """Extract stack trace following an error"""
        stack_trace = []
        for i in range(start_index + 1, min(start_index + 15, len(lines))):
            line = lines[i].strip()
            if line.startswith('at ') or 'File "' in line or line.startswith('    '):
                stack_trace.append(line)
            elif line and not line.startswith(' '):
                break
        
        return '\n'.join(stack_trace) if stack_trace else ""
