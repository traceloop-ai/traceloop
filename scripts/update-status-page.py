#!/usr/bin/env python3
"""
Update the status page with latest validation results from JSON file
"""

import json
import os
from datetime import datetime

def load_status_data():
    """Load status data from JSON file"""
    status_file = "../traceloop-website/status.json"
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            return json.load(f)
    return None

def update_status_html(status_data):
    """Update the status.html file with latest data"""
    html_file = "../traceloop-website/status.html"
    
    if not os.path.exists(html_file):
        print(f"Status HTML file not found: {html_file}")
        return
    
    # Read current HTML
    with open(html_file, 'r') as f:
        html_content = f.read()
    
    if not status_data:
        print("No status data available")
        return
    
    # Update last updated time
    last_updated = status_data.get('last_updated', datetime.now().isoformat())
    # Find and replace the last updated time in the HTML
    import re
    pattern = r'id="lastUpdated">[^<]*</span>'
    replacement = f'id="lastUpdated">{last_updated}</span>'
    html_content = re.sub(pattern, replacement, html_content)
    
    # Update overall status
    overall_status = status_data.get('overall_status', 'unknown')
    working_count = status_data.get('working_count', 0)
    total_count = status_data.get('total_count', 0)
    
    # Update status indicators based on test results
    tests = status_data.get('tests', {})
    
    # Map test names to HTML elements
    test_mapping = {
        'go_install': 'Go Installation',
        'docker_install': 'Docker Installation', 
        'homebrew_install': 'Homebrew Installation',
        'server_health': 'HTTP Server',
        'server_traces_api': 'Traces API',
        'server_stats_api': 'Stats API',
        'python_install': 'Installation',
        'python_import': 'Basic Tracing',
        'simple_example': 'Simple Test',
        'test_script': 'Test Script'
    }
    
    # Update individual test statuses
    for test_key, test_name in test_mapping.items():
        if test_key in tests:
            test_status = tests[test_key]['status']
            test_notes = tests[test_key].get('notes', '')
            
            # Determine status class
            status_class = "status-unknown"
            if test_status == "working":
                status_class = "status-working"
            elif test_status == "broken":
                status_class = "status-broken"
            elif test_status == "partial":
                status_class = "status-partial"
            
            # Find the step item with data-test attribute
            pattern = rf'<li class="step-item" data-test="{test_key}">.*?</li>'
            match = re.search(pattern, html_content, re.DOTALL)
            if match:
                # Extract the existing step item
                step_item = match.group(0)
                
                # Update the status indicator and text
                step_item = re.sub(
                    r'<span class="status-indicator status-unknown"></span>',
                    f'<span class="status-indicator {status_class}"></span>',
                    step_item
                )
                step_item = re.sub(
                    r'<span class="status-text">Loading\.\.\.</span>',
                    f'<span class="status-text">{test_status.title()}</span>',
                    step_item
                )
                
                # Update notes if available
                if test_notes and test_notes.strip():
                    step_item = re.sub(
                        r'<div class="step-notes"></div>',
                        f'<div class="step-notes">{test_notes}</div>',
                        step_item
                    )
                
                # Replace the step item in the HTML
                html_content = html_content.replace(match.group(0), step_item)
    
    # Update overall status section
    overall_status_text = "Core functionality working"
    overall_status_class = "status-working"
    
    if overall_status == "broken":
        overall_status_text = "Multiple issues detected"
        overall_status_class = "status-broken"
    elif overall_status == "partial":
        overall_status_text = "Some issues need attention"
        overall_status_class = "status-partial"
    
    # Update overall status indicator
    html_content = html_content.replace(
        '<span class="status-indicator status-working"></span>',
        f'<span class="status-indicator {overall_status_class}"></span>'
    )
    
    html_content = html_content.replace(
        '<strong>Core functionality working</strong>',
        f'<strong>{overall_status_text}</strong>'
    )
    
    # Update progress text
    progress_text = f"{working_count}/{total_count} tests passing"
    html_content = html_content.replace(
        'The main Go + Python workflow is solid, but Docker and Homebrew methods need fixes.',
        f'Progress: {progress_text}. The main Go + Python workflow is solid, but some installation methods need fixes.'
    )
    
    # Write updated HTML
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"Updated status page: {working_count}/{total_count} tests passing")
    print(f"Overall status: {overall_status}")

def main():
    """Main function"""
    print("Updating status page with latest validation results...")
    
    # Change to project root
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Load and update status
    status_data = load_status_data()
    if status_data:
        update_status_html(status_data)
        print("Status page updated successfully!")
    else:
        print("No status data found to update")

if __name__ == "__main__":
    main()
