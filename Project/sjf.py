from typing import List, Dict, Any

def sjf(arrival_time: List[int], burst_time: List[int], process_names: List[str]) -> Dict[str, Any]:
    processes_info = [
        {
            'job': process_names[index],  # Use the provided process name
            'at': item,
            'bt': burst_time[index],
        }
        for index, item in enumerate(arrival_time)
    ]

    # Sort processes based on arrival time and burst time
    processes_info.sort(key=lambda x: (x['at'], x['bt']))

    finish_time = []
    gantt_chart_info = []

    solved_processes_info = []
    ready_queue = []
    finished_jobs = []

    for i in range(len(processes_info)):
        if i == 0:
            ready_queue.append(processes_info[0])
            finish_time.append(processes_info[0]['at'] + processes_info[0]['bt'])
            solved_processes_info.append({
                **processes_info[0],
                'ft': finish_time[0],
                'tat': finish_time[0] - processes_info[0]['at'],
                'wat': finish_time[0] - processes_info[0]['at'] - processes_info[0]['bt'],
            })

            for p in processes_info:
                if p['at'] <= finish_time[0] and p not in ready_queue:
                    ready_queue.append(p)

            ready_queue.pop(0)
            finished_jobs.append(processes_info[0])

            gantt_chart_info.append({
                'job': processes_info[0]['job'],
                'start': processes_info[0]['at'],
                'stop': finish_time[0],
            })
        else:
            if not ready_queue and len(finished_jobs) != len(processes_info):
                unfinished_jobs = [p for p in processes_info if p not in finished_jobs]
                unfinished_jobs.sort(key=lambda x: (x['at'], x['bt']))
                ready_queue.append(unfinished_jobs[0])

            rq_sorted_by_bt = sorted(ready_queue, key=lambda x: (x['bt'], x['at']))
            process_to_execute = rq_sorted_by_bt[0]

            previous_finish_time = finish_time[-1]

            if process_to_execute['at'] > previous_finish_time:
                finish_time.append(process_to_execute['at'] + process_to_execute['bt'])
                newest_finish_time = finish_time[-1]
                gantt_chart_info.append({
                    'job': process_to_execute['job'],
                    'start': process_to_execute['at'],
                    'stop': newest_finish_time,
                })
            else:
                finish_time.append(previous_finish_time + process_to_execute['bt'])
                newest_finish_time = finish_time[-1]
                gantt_chart_info.append({
                    'job': process_to_execute['job'],
                    'start': previous_finish_time,
                    'stop': newest_finish_time,
                })

            solved_processes_info.append({
                **process_to_execute,
                'ft': newest_finish_time,
                'tat': newest_finish_time - process_to_execute['at'],
                'wat': newest_finish_time - process_to_execute['at'] - process_to_execute['bt'],
            })

            for p in processes_info:
                if p['at'] <= newest_finish_time and p not in ready_queue and p not in finished_jobs:
                    ready_queue.append(p)

            ready_queue.remove(process_to_execute)
            finished_jobs.append(process_to_execute)

    # Sort the processes by job name within arrival time
    solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

    return {'solvedProcessesInfo': solved_processes_info, 'ganttChartInfo': gantt_chart_info}