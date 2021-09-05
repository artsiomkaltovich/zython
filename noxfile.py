import nox

nox.options.stop_on_first_error = True


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "zython", "--count", "--statistics")


@nox.session
def doc(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_doc.txt")
    session.run("pytest", "doc", "--doctest-glob=*.rst", "--doctest-modules")


@nox.session
def test(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_dev.txt")
    session.run(
        "pytest", "test", "zython",
        "--cov=zython", "--cov-branch", "--cov-report=term-missing",
        "--doctest-modules",
    )
