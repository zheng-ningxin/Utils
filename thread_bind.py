import psutil
import re
import argparse


def parse_core_list(cores):
    core_list = set()
    ranges = re.split(',', cores)
    for c_range in ranges:
        if '-' in c_range:
            _start, _end = re.split('-', c_range)
            _start, _end = int(_start), int(_end)
            core_list.update(list(range(_start, _end+1)))
        else:
            core_list.add(int(c_range))
    return list(core_list)

def get_all_threads(pid):
    process = psutil.Process(pid)
    return [p.id for p in process.threads()]

def bind_threads(pids, cores):
    assert len(cores) > len(pids), \
        "The number of cores is less than the number of threads"
    for i, pid in enumerate(pids):
        process = psutil.Process(pid)
        core = cores[i]
        process.cpu_affinity([core])
        print("Binding Process:", process.pid, " Name:", process.name(), " To core:", core )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', required=True, type=int, help='Pid of the target process')
    parser.add_argument('-c', '--cores', required=True, help='Cores to bind the thread, for example: 1-10,12,14')
    args = parser.parse_args()
    cores = parse_core_list(args.cores)
    print("Get core list: ", cores)
    print("Binding thread for process", args.pid)
    pids = get_all_threads(args.pid)
    bind_threads(pids, cores)