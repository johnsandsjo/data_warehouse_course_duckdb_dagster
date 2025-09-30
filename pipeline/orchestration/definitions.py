from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

import sys
sys.path.insert(0, "../data_extract_load")
from dlt_daily_update import job_ads_source

db_path = str(Path(__file__).parents[1] / "data_warehouse/job_advertisments.duckdb")

# asset
dlt_resource = DagsterDltResource()

## create dlt asset
@dlt_assets(dlt_source= job_ads_source(),dlt_pipeline= dlt.pipeline(
    pipeline_name = "job_ads_stream_daily",
    dataset_name = "staging",
    destination = dlt.destinations.duckdb(db_path))
    )
def dlt_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context= context)
    
## create dbt asset
dbt_project_dir = Path(__file__).parents[1] / "data_transformation"
profiles_path = Path.home() / ".dbt"

dbt_project = DbtProject(project_dir= dbt_project_dir, profiles_dir = profiles_path)
dbt_resource = DbtCliResource(project_dir = dbt_project)

dbt_project.prepare_if_dev()

@dbt_assets(manifest= dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context = context).stream()

# create job
job_dlt = dg.define_asset_job("job_dlt", selection = dg.AssetSelection.keys("dlt_job_ads_source_jobsearch_resource"))

job_dbt = dg.define_asset_job("job_dbt", selection = dg.AssetSelection.key_prefixes("warehouse", "marts"))


# schedule
schedule_dlt = dg.ScheduleDefinition(
    job= job_dlt,
    cron_schedule= "33 12 * * *"
)

# sensor
@dg.asset_sensor(asset_key= dg.AssetKey("dlt_job_ads_source_jobsearch_resource"), job_name= "job_dbt")
def dlt_load_sensor():
    yield dg.RunRequest()

# Definition
defs = dg.Definitions(
    assets=[dlt_load, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_dlt, job_dbt],
    schedules=[schedule_dlt],
    sensors= [dlt_load_sensor]
)

