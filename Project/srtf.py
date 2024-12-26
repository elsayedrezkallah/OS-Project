from typing import List, Dict, Any

class SRTFScheduler:
    def __init__(self, arrival_time: List[int], burst_time: List[int], process_names: List[str]):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.process_names = process_names  # Store the process names
        self.processes_info = self.initialize_processes()
        self.solved_processes_info = []
        self.gantt_chart_info = []

    def initialize_processes(self) -> List[Dict[str, Any]]:
        return [
            {
                'job': self.process_names[index],  # Use the provided process name
                'at': item,
                'bt': self.burst_time[index]
            }
            for index, item in enumerate(self.arrival_time)
        ]

    def schedule(self) -> Dict[str, Any]:
        self.processes_info.sort(key=lambda x: (x['at'], x['bt']))

        ready_queue = []
        current_time = self.processes_info[0]['at']
        unfinished_jobs = self.processes_info.copy()

        remaining_time = {process['job']: process['bt'] for process in self.processes_info}

        ready_queue.append(unfinished_jobs[0])
        while sum(remaining_time.values()) > 0 and unfinished_jobs:
            prev_idle = False
            if not ready_queue and unfinished_jobs:
                prev_idle = True
                ready_queue.append(unfinished_jobs[0])

            ready_queue.sort(key=lambda x: (remaining_time[x['job']], x['at']))

            process_to_execute = ready_queue[0]

            process_at_less_than_bt = [
                p for p in self.processes_info
                if p['at'] <= remaining_time[process_to_execute['job']] + current_time
                and p != process_to_execute
                and p not in ready_queue
                and p in unfinished_jobs
            ]

            got_interruption = False
            for p in process_at_less_than_bt:
                if prev_idle:
                    current_time = process_to_execute['at']

                amount = p['at'] - current_time

                if current_time >= p['at']:
                    ready_queue.append(p)

                if p['bt'] < remaining_time[process_to_execute['job']] - amount:
                    remaining_time[process_to_execute['job']] -= amount
                    ready_queue.append(p)
                    prev_current_time = current_time
                    current_time += amount
                    self.gantt_chart_info.append({
                        'job': process_to_execute['job'],
                        'start': prev_current_time,
                        'stop': current_time,
                    })

                    got_interruption = True
                    break

            process_to_arrive = [
                p for p in self.processes_info
                if p['at'] <= current_time
                and p != process_to_execute
                and p not in ready_queue
                and p in unfinished_jobs
            ]

            # Push new processes to readyQueue
            ready_queue.extend(process_to_arrive)

            if not got_interruption:
                if prev_idle:
                    remaining_t = remaining_time[process_to_execute['job']]
                    remaining_time[process_to_execute['job']] -= remaining_t
                    current_time = process_to_execute['at'] + remaining_t

                    for p in process_at_less_than_bt:
                        if current_time >= p['at'] and p not in ready_queue:
                            ready_queue.append(p)

                    self.gantt_chart_info.append({
                        'job': process_to_execute['job'],
                        'start': process_to_execute['at'],
                        'stop': current_time,
                    })
                else:
                    remaining_t = remaining_time[process_to_execute['job']]
                    remaining_time[process_to_execute['job']] -= remaining_t
                    prev_current_time = current_time
                    current_time += remaining_t

                    for p in process_at_less_than_bt:
                        if current_time >= p['at'] and p not in ready_queue:
                            ready_queue.append(p)

                    self.gantt_chart_info.append({
                        'job': process_to_execute['job'],
                        'start': prev_current_time,
                        'stop': current_time,
                    })

            # Requeueing (move head/first item to tail/last)
            ready_queue.append(ready_queue.pop(0))

                        # When the process finished executing
            if remaining_time[process_to_execute['job']] == 0:
                unfinished_jobs.remove(process_to_execute)
                ready_queue.remove(process_to_execute)

                self.solved_processes_info.append({
                    **process_to_execute,
                    'ft': current_time,
                    'tat': current_time - process_to_execute['at'],
                    'wat': current_time - process_to_execute['at'] - process_to_execute['bt'],
                })

        # Sort the processes by job name within arrival time
        self.solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

        return {
            'solvedProcessesInfo': self.solved_processes_info,
            'ganttChartInfo': self.gantt_chart_info
        }