# PM

Project Scheduling CLI to simplify project management tasks. This uses the [cheche_pm](https://pypi.org/project/cheche-pm) package. I haven't been able to find this code hosted anywhere online, so I've copied the code here to make a few adjustments.

## Installation

`pip3 install .`

## Usage

Create a file that lists out tasks and precedence (see `./examples/test.proj`).

- Print project critical path: `pm -f ./examples/test.proj critical-path`

`['Start', 'id1', 'id2', 'id3', 'End']`

- Print project dot graph: `pm -f ./examples/test.proj dot | dot -Tpng | timg -`

![image](https://github.com/natefduncan/pm/assets/30030731/0a7221d7-9eca-4287-a05b-e9c1b31d0fc4)

- Show project gantt chart: `pm -f ./examples/test.proj gantt-chart | timg -`

![image](https://github.com/natefduncan/pm/assets/30030731/734c7d5a-2698-42c2-855b-3cd3374fcb32)
