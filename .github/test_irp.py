import re
import tomllib
import pytest
import pathlib

FOUR_MB = 4_194_304  # in bytes
EIGHT_MB = 2 * FOUR_MB

deliverables_dir = pathlib.Path("./deliverables")
title_dir = pathlib.Path("./title")
logbook_dir = pathlib.Path("./logbook")


@pytest.fixture(scope="session")
def username():
    """Extract username from the repo name."""
    repo_name = pathlib.Path(__file__).parents[1].name
    return re.search(r"-(.*)", repo_name).group(1)


@pytest.fixture(scope="session")
def title():
    """Extract title from title.toml."""
    with open(title_dir / "title.toml", "r", encoding="utf-8") as file:
        yield tomllib.loads(file.read())["title"]


@pytest.fixture(scope="session")
def project_plan(username):
    """Derive project plan path."""
    return deliverables_dir / f"{username}-project-plan.pdf"


@pytest.fixture(scope="session")
def final_report(username):
    """Derive final report path."""
    return deliverables_dir / f"{username}-final-report.pdf"


class TestTitle:
    """Test title.toml file."""

    def test_dir(self):
        assert title_dir.is_dir()

    def test_file(self):
        assert (title_dir / "title.toml").is_file()

    def test_content(self, title):
        assert isinstance(title, str)
        assert title


class TestProjectPlan:
    """Test project plan file."""

    def test_dir(self):
        assert deliverables_dir.is_dir()

    def test_file(self, project_plan):
        assert project_plan.is_file()

    def test_size(self, project_plan):
        assert project_plan.stat().st_size <= FOUR_MB


class TestFinalReport:
    """Test final report file."""

    def test_dir(self):
        assert deliverables_dir.is_dir()

    def test_file(self, final_report):
        assert final_report.is_file()

    def test_size(self, final_report):
        assert final_report.stat().st_size <= EIGHT_MB

class TestLogbook:
    """Test logbook file."""

    def test_dir(self):
        assert logbook_dir.is_dir()

    def test_file(self):
        assert (logbook_dir / "logbook.md").is_file()
