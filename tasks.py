from invoke import task

@task
def start(c):
    c.run("python src/index.py", pty=True)

@task
def test(c):
    c.run("pytest src", pty=True)

@task
def coverage_report(c):
    c.run("coverage run --branch -m pytest src", pty=True)
    c.run("coverage html", pty=True)

@task
def pylint(c):
    c.run("pylint src", pty=True)
