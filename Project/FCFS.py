from typing import List, Dict, Any

def fcfs(arrival_time: List[int], burst_time: List[int], process_names: List[str]) -> Dict[str, Any]:
    processes_info = []
    
    # Create a list of process info using the provided names
    for index, at in enumerate(arrival_time):
        job = process_names[index]  # Use the provided process name
        processes_info.append({
            'job': job,
            'at': at,
            'bt': burst_time[index]
        })

    # Sort processes by arrival time
    processes_info.sort(key=lambda x: x['at'])

    finish_time = []
    gantt_chart_info = []

    for index, process in enumerate(processes_info):
        if index == 0 or process['at'] > finish_time[index - 1]:
            finish_time.append(process['at'] + process['bt'])
            gantt_chart_info.append({
                'job': process['job'],
                'start': process['at'],
                'stop': finish_time[index]
            })
        else:
            finish_time.append(finish_time[index - 1] + process['bt'])
            gantt_chart_info.append({
                'job': process['job'],
                'start': finish_time[index - 1],
                'stop': finish_time[index]
            })

        # Calculate turnaround time (TAT) and waiting time (WT)
        process['ft'] = finish_time[index]
        process['tat'] = finish_time[index] - process['at']
        process['wat'] = finish_time[index] - process['at'] - process['bt']

    return {
        'solvedProcessesInfo': processes_info,
        'ganttChartInfo': gantt_chart_info  # Include Gantt chart info in the return
    }