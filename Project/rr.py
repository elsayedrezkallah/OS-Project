from typing import List, Dict, Any

def rr(arrival_time: List[int], burst_time: List[int], time_quantum: int, process_names: List[str]) -> Dict[str, Any]:
    processes_info = [
        {
            'job': process_names[index],  # Use the provided process name
            'at': item,
            'bt': burst_time[index],
        }
        for index, item in enumerate(arrival_time)
    ]

    # Sort processes based on arrival time
    processes_info.sort(key=lambda x: x['at'])

    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = 0  # Start at time 0
    unfinished_jobs = processes_info.copy()

    remaining_time = {process['job']: process['bt'] for process in processes_info}

    while unfinished_jobs:
        # Add processes to the ready queue that have arrived by current_time
        for process in unfinished_jobs:
            if process['at'] <= current_time and process not in ready_queue:
                ready_queue.append(process)

        if not ready_queue:
            # If the ready queue is empty, move time forward to the next process arrival
            current_time = min(p['at'] for p in unfinished_jobs)
            continue  # Skip to the next iteration

        process_to_execute = ready_queue[0]

        if remaining_time[process_to_execute['job']] <= time_quantum:
            # Execute until finished
            remaining_t = remaining_time[process_to_execute['job']]
            prev_current_time = current_time
            current_time += remaining_t
            gantt_chart_info.append({
                'job': process_to_execute['job'],
                'start': prev_current_time,
                'stop': current_time,
            })
            remaining_time[process_to_execute['job']] = 0
        else:
            # Execute for the time quantum
            remaining_time[process_to_execute['job']] -= time_quantum
            prev_current_time = current_time
            current_time += time_quantum
            gantt_chart_info.append({
                'job': process_to_execute['job'],
                'start': prev_current_time,
                'stop': current_time,
            })

        # When the process finished executing
        if remaining_time[process_to_execute['job']] == 0:
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)

            solved_processes_info.append({
                **process_to_execute,
                'ft': current_time,
                'tat': current_time - process_to_execute['at'],
                'wat': current_time - process_to_execute['at'] - process_to_execute['bt'],
            })
        else:
            # Requeue the process if it still has remaining time
            ready_queue.append(ready_queue.pop(0))  # Move the executed process to the end of the queue

    # Sort the processes by arrival time and then by job name
    solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

    return {'solvedProcessesInfo': solved_processes_info, 'ganttChartInfo': gantt_chart_info}