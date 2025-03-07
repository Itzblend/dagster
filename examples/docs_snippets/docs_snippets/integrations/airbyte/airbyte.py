# isort: skip_file
# pylint: disable=unused-variable

import os


def scope_load_assets_from_airbyte_project():
    # start_load_assets_from_airbyte_project
    from dagster_airbyte import load_assets_from_airbyte_project

    airbyte_assets = load_assets_from_airbyte_project(
        project_dir="path/to/airbyte/project",
    )
    # end_load_assets_from_airbyte_project


def scope_load_assets_from_airbyte_instance():
    # start_load_assets_from_airbyte_instance
    from dagster_airbyte import airbyte_resource, load_assets_from_airbyte_instance

    airbyte_instance = airbyte_resource.configured(
        {
            "host": "localhost",
            "port": "8000",
            # If using basic auth
            "request_additional_params": {
                "auth": (
                    "airbyte",
                    os.getenv("AIRBYTE_PASSWORD"),
                )
            },
        }
    )
    airbyte_assets = load_assets_from_airbyte_instance(airbyte_instance)
    # end_load_assets_from_airbyte_instance


def scope_airbyte_project_config():
    # start_airbyte_project_config
    from dagster_airbyte import airbyte_resource, load_assets_from_airbyte_project

    from dagster import with_resources

    airbyte_assets = with_resources(
        [load_assets_from_airbyte_project(project_dir="path/to/airbyte/project")],
        {
            "airbyte": airbyte_resource.configured(
                {
                    "host": "localhost",
                    "port": "8000",
                    # If using basic auth
                    "request_additional_params": {
                        "auth": (
                            "airbyte",
                            os.getenv("AIRBYTE_PASSWORD"),
                        )
                    },
                }
            )
        },
    )
    # end_airbyte_project_config


def scope_manually_define_airbyte_assets():
    # start_manually_define_airbyte_assets
    from dagster_airbyte import build_airbyte_assets

    airbyte_assets = build_airbyte_assets(
        connection_id="87b7fe85-a22c-420e-8d74-b30e7ede77df",
        destination_tables=["releases", "tags", "teams"],
    )
    # end_manually_define_airbyte_assets


def scope_airbyte_manual_config():
    # start_airbyte_manual_config
    from dagster_airbyte import airbyte_resource, build_airbyte_assets

    from dagster import with_resources

    airbyte_assets = with_resources(
        build_airbyte_assets(
            connection_id="87b7fe85-a22c-420e-8d74-b30e7ede77df",
            destination_tables=["releases", "tags", "teams"],
        ),
        {
            "airbyte": airbyte_resource.configured(
                {
                    "host": "localhost",
                    "port": "8000",
                    # If using basic auth
                    "request_additional_params": {
                        "auth": (
                            "airbyte",
                            os.getenv("AIRBYTE_PASSWORD"),
                        )
                    },
                }
            )
        },
    )
    # end_airbyte_manual_config


def scope_schedule_assets():
    airbyte_assets = []
    # start_schedule_assets
    from dagster import ScheduleDefinition, define_asset_job, repository, AssetSelection

    run_everything_job = define_asset_job("run_everything", selection="*")

    # only my_airbyte_connection
    run_specific_connection_job = define_asset_job(
        "run_specific_connection", AssetSelection.groups("my_airbyte_connection")
    )

    @repository
    def my_repo():
        return [
            airbyte_assets,
            ScheduleDefinition(
                job=run_specific_connection_job,
                cron_schedule="@daily",
            ),
            ScheduleDefinition(
                job=run_everything_job,
                cron_schedule="@weekly",
            ),
        ]

    # end_schedule_assets
