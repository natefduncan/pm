# PM

Project Scheduling CLI to simplify project management tasks. This uses the [cheche_pm](https://pypi.org/project/cheche-pm) package. I haven't been able to find this code hosted anywhere online, so I've copied the code here to make a few adjustments.

## Installation

`pip3 install .`

## Usage

Create a file that lists out tasks and precedence (see `./examples/test.proj`).

- Print project critical path: `pm -f ./examples/test.proj critical-path`

`['Start', 'id1', 'id2', 'id3', 'End']`

- Print project dot graph: `pm -f ./examples/test.proj dot | dot -Tsvg | timg -`

- Show project gantt chart: `pm -f ./examples/test.proj gantt-chart | timg -`
