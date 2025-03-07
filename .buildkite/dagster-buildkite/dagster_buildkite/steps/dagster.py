import os
from glob import glob
from typing import List

from dagster_buildkite import python_packages

from ..defines import GIT_REPO_ROOT
from ..python_version import AvailablePythonVersion
from ..step_builder import CommandStepBuilder
from ..utils import (
    BuildkiteStep,
    CommandStep,
    is_feature_branch,
    safe_getenv,
    skip_if_no_python_changes,
)
from .helm import build_helm_steps
from .packages import build_library_packages_steps
from .test_project import build_test_project_steps

branch_name = safe_getenv("BUILDKITE_BRANCH")


def build_repo_wide_steps() -> List[BuildkiteStep]:
    # Other linters are run in per-package environments because they rely on the dependencies of the
    # target. `black`, `isort`, and `check-manifest` are run for the whole repo at once.
    return [
        *build_repo_wide_isort_steps(),
        *build_repo_wide_black_steps(),
        *build_repo_wide_check_manifest_steps(),
    ]


def build_dagster_steps() -> List[BuildkiteStep]:
    steps: List[BuildkiteStep] = []

    # Build images containing the dagster-test sample project. This is a dependency of certain
    # dagster core and extension lib tests.
    steps += build_test_project_steps()

    # "Package" used loosely here to mean roughly "a directory with some python modules". For
    # instances, a directory of unrelated scripts counts as a package. All packages must have a
    # toxfile that defines the tests for that package.
    steps += build_library_packages_steps()

    steps += build_helm_steps()
    steps += build_sql_schema_check_steps()
    steps += build_graphql_python_client_backcompat_steps()

    return steps


def build_repo_wide_black_steps() -> List[CommandStep]:
    return [
        CommandStepBuilder(":python-black: black")
        .run("pip install -e python_modules/dagster[black]", "make check_black")
        .with_skip(skip_if_no_python_changes())
        .on_test_image(AvailablePythonVersion.get_default())
        .build(),
    ]


def build_repo_wide_isort_steps() -> List[CommandStep]:
    return [
        CommandStepBuilder(":isort: isort")
        .run("pip install -e python_modules/dagster[isort]", "make check_isort")
        .on_test_image(AvailablePythonVersion.get_default())
        .with_skip(skip_if_no_python_changes())
        .build(),
    ]


def build_repo_wide_check_manifest_steps() -> List[CommandStep]:
    published_packages = [
        "python_modules/dagit",
        "python_modules/dagster",
        "python_modules/dagster-graphql",
        *(
            os.path.relpath(p, GIT_REPO_ROOT)
            for p in glob(f"{GIT_REPO_ROOT}/python_modules/libraries/*")
        ),
    ]

    commands = [
        "pip install check-manifest",
        *(f"check-manifest {library}" for library in published_packages),
    ]

    return [
        CommandStepBuilder(":white_check_mark: check-manifest")
        .on_test_image(AvailablePythonVersion.get_default())
        .run(*commands)
        .with_skip(skip_if_no_python_changes())
        .build()
    ]


def build_sql_schema_check_steps() -> List[CommandStep]:
    return [
        CommandStepBuilder(":mysql: mysql-schema")
        .on_test_image(AvailablePythonVersion.get_default())
        .run("pip install -e python_modules/dagster", "python scripts/check_schemas.py")
        .with_skip(skip_mysql_if_no_changes_to_dependencies(["dagster"]))
        .build()
    ]


def build_graphql_python_client_backcompat_steps() -> List[CommandStep]:
    return [
        CommandStepBuilder(":graphql: GraphQL Python Client backcompat")
        .on_test_image(AvailablePythonVersion.get_default())
        .run(
            "pip install -e python_modules/dagster[test] -e python_modules/dagster-graphql -e python_modules/automation",
            "dagster-graphql-client query check",
        )
        .with_skip(
            skip_graphql_if_no_changes_to_dependencies(["dagster", "dagster-graphql", "automation"])
        )
        .build()
    ]


def skip_mysql_if_no_changes_to_dependencies(dependencies: List[str]):
    if not is_feature_branch():
        return None

    for dependency in dependencies:
        if python_packages.get(dependency) in python_packages.with_changes:
            return None

    return "Skip unless mysql schemas might have changed"


def skip_graphql_if_no_changes_to_dependencies(dependencies: List[str]):
    if not is_feature_branch():
        return None

    for dependency in dependencies:
        if python_packages.get(dependency) in python_packages.with_changes:
            return None

    return "Skip unless GraphQL schemas might have changed"
