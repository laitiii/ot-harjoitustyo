from invoke import task
import sys

pty = sys.platform != "win32"

@task
def start(c):
    c.run("python src/index.py", pty=pty)
@task
def test(c):
    c.run("pytest src", pty=pty)

@task
def coverage_report(c):
    c.run("coverage run --branch -m pytest src", pty=pty)
    c.run("coverage html", pty=pty)

@task
def pylint(c):
    c.run("pylint src", pty=pty)