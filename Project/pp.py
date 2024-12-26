from typing import List, Dict, Any

def pp(arrival_time: List[int], burst_time: List[int], priorities: List[int], process_names: List[str]) -> Dict[str, Any]:
    processes_info = [
        {
            'job': process_names[index],  # Use the provided process name
            'at': item,
            'bt': burst_time[index],
            'priority': priorities[index],
        }
        for index, item in enumerate(arrival_time)
    ]

    # Sort processes based on arrival time and priority
    processes_info.sort(key=lambda x: (x['at'], x['priority']))

    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = 0
    unfinished_jobs = processes_info.copy()

    remaining_time = {process['job']: process['bt'] for process in processes_info}

    while unfinished_jobs:
        # Add processes that have arrived by current_time to the ready queue
        for process in unfinished_jobs:
            if process['at'] <= current_time and process not in ready_queue:
                ready_queue.append(process)

        if not ready_queue:
            # If no process is ready, move time forward to the next process arrival
            current_time = min(process['at'] for process in unfinished_jobs)
            continue

        # Sort the ready queue by priority (and FCFS for equal priority)
        ready_queue.sort(key=lambda x: (x['priority'], x['at']))

        # Execute the process with the highest priority
        process_to_execute = ready_queue[0]
        gantt_chart_info.append({
            'job': process_to_execute['job'],
            'start': current_time,
            'stop': current_time + 1,  # Execute for 1 time unit
        })

        # Decrement the remaining time for the executing process
        remaining_time[process_to_execute['job']] -= 1
        current_time += 1

        # Check if the process is finished
        if remaining_time[process_to_execute['job']] == 0:
            # Remove the finished process from unfinished jobs
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)
            solved_processes_info.append({
                **process_to_execute,
                'ft': current_time,
                'tat': current_time - process_to_execute['at'],
                'wat': (current_time - process_to_execute['at'] - process_to_execute['bt']),
            })
        else:
            # If not finished, keep it in the ready queue
            ready_queue.remove(process_to_execute)
            ready_queue.append(process_to_execute)

    # Sort the processes by job name within arrival time
    solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

    return {'solvedProcessesInfo': solved_processes_info, 'ganttChartInfo': gantt_chart_info}