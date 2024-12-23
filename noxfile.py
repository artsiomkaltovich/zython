import sys
import nox

nox.options.stop_on_first_error = True


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "zython")


@nox.session
def test(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_dev.txt")
    session.run(
        "pytest",
        "-s",
        "test",
        "zython",
        "--cov=zython",
        "--cov-branch",
        "--cov-report=term-missing",
        "--doctest-modules",
    )


@nox.session
def doctest(session):
    if sys.version_info.major == 3 and sys.version_info.minor == 13:
        print("Skipping doctest for python 3.13, see https://github.com/twmr/pytest-sphinx/issues/67")
        return
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_dev.txt")
    session.run("pytest", "doc", "--doctest-glob=*.rst", "--doctest-modules")


@nox.session(default=False)
def gendoc(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_doc.txt")
    session.run("sphinx-apidoc", "-f", "-o", "docs/source/api", "zython")
    session.run(
        "python",
        "-m",
        "sphinx",
        "-T",
        "-E",
        "-b",
        "html",
        "-d",
        "docs/_build/doctrees",
        "-D",
        "language=en",
        "doc/source",
        "doc/build/html",
    )


@nox.session(default=False)
def testcov(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements_dev.txt")
    session.run("pytest", "test", "zython", "doc", "--doctest-glob=*.rst", "--doctest-modules", "--cov=zython", "--cov-branch", "--cov-report=term-missing")
