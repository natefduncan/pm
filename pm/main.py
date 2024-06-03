from dataclasses import dataclass, field
import click
import pydot

import pm.cheche_pm 
from pm.parser import doc, Task, Precedence

# Suppress all the warnings from cheche_pm
import warnings
warnings.filterwarnings("ignore")

@dataclass
class Project:
    file_path: str
    tasks: list[Task] = field(default_factory=list)
    precedences: list[Precedence] = field(default_factory=list)
    p: pm.cheche_pm.Project = pm.cheche_pm.Project()

    def __post_init__(self):
        with open(self.file_path, "r") as f:
            statements = doc.parse(f.read())
        for s in statements:
            if isinstance(s, Task):
                self.tasks.append(s)
            elif isinstance(s, Precedence):
                self.precedences.append(s)
        for task in self.tasks: 
            task_prec = ",".join([i.a for i in self.precedences if i.b == task.id])
            task_prec = [task_prec] if task_prec else [None]
            self.p.add_activity(
                activity_name=task.id,
                activity_duration=task.duration,
                activity_precedence=task_prec,
                activity_resources=task.resources
            )

        self.p.add_dummies_create_project_network()
        self.p.CPM()

@click.group
@click.option("-f", "--file-path", default=None)
@click.pass_context
def cli(ctx, file_path):
    ctx.obj = Project(file_path)

@cli.command
@click.pass_obj
def critical_path(project):
    click.echo(project.p.get_critical_path())

@cli.command
@click.option("--early", is_flag=True, help="Display early schedule instead of late")
@click.pass_obj
def gantt_chart(project, early):

    project.p.plot_gantt_cpm(early=early,save=False)

@cli.command()
@click.pass_obj
def dot(project):
    dotgraph = pydot.Dot(graph_type='digraph', strict=True, rankdir="LR")
    for task in project.tasks:
        options = {i["key"]:i["value"] for i in task.options} if task.options else {}
        if "fillcolor" not in options:
            options["fillcolor"] = "white"
        dotgraph.add_node(
            pydot.Node(task.id, label=task.id, shape="rectangle", style="filled", **options)
        )

    for p in project.precedences:
        dotgraph.add_edge(
            pydot.Edge(p.a, p.b)
        )
    click.echo(dotgraph.to_string())

if __name__=="__main__":
    cli()
