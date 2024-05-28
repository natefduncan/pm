from dataclasses import dataclass, field
import click

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
            task_prec = [i.a for i in self.precedences if i.b == task.id]
            task_prec = task_prec if task_prec else [None]
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
@click.pass_obj
def gantt_chart(project):
    project.p.plot_gantt_cpm(early=True,save=False)

@cli.command()
@click.pass_obj
def dot(project):
    project.p.plot_network_diagram(plot_type = 'dot')

if __name__=="__main__":
    cli()
