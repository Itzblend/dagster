.. currentmodule:: dagster

Run Requests
============
.. autoclass:: RunRequest
.. autoclass:: SkipReason

Schedules
=========

.. autodecorator:: schedule

.. autoclass:: ScheduleDefinition

.. autoclass:: ScheduleEvaluationContext

.. autofunction:: build_schedule_context

.. currentmodule:: dagster._core.scheduler

.. autoconfigurable:: DagsterDaemonScheduler
  :annotation: Scheduler

Partitioned Schedules
=====================

.. currentmodule:: dagster

.. autofunction:: build_schedule_from_partitioned_job

.. autoclass:: PartitionScheduleDefinition

.. autodecorator:: hourly_partitioned_config
    :noindex:

.. autodecorator:: daily_partitioned_config
    :noindex:

.. autodecorator:: weekly_partitioned_config
    :noindex:

.. autodecorator:: monthly_partitioned_config
    :noindex:

Sensors
=======

.. currentmodule:: dagster

.. autodecorator:: sensor

.. autoclass:: SensorDefinition

.. autoclass:: SensorEvaluationContext
   :noindex:

.. autoclass:: MultiAssetSensorEvaluationContext

.. autofunction:: build_sensor_context

.. autofunction:: build_multi_asset_sensor_context

.. autoclass:: AssetSensorDefinition

.. autodecorator:: asset_sensor

.. autoclass:: MultiAssetSensorDefinition

.. autodecorator:: multi_asset_sensor

.. autofunction:: build_asset_reconciliation_sensor


.. autoclass:: RunStatusSensorDefinition

.. autoclass:: RunStatusSensorContext

.. autoclass:: RunFailureSensorContext

.. autoclass:: JobSelector
.. autoclass:: RepositorySelector

.. autofunction:: build_run_status_sensor_context

.. autodecorator:: run_status_sensor

.. autodecorator:: run_failure_sensor
