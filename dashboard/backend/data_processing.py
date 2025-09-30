
import pandas as pd 
from pathlib import Path
import json
import duckdb


db_path = str(Path(__file__).parents[2] / "pipeline/data_warehouse/job_advertisments.duckdb")
 
def query_job_listings(occupational_field):

    with duckdb.connect(db_path, read_only = True) as conn:
    

        if occupational_field == "Data/IT":
            query='SELECT * FROM marts.mart_data_it'
        elif occupational_field == "Säkerhet och bevakning":
            query='SELECT * FROM marts.mart_safety'
        else:
            query='SELECT * FROM marts.mart_social_work'
   
        
        return conn.query(f"{query}").df()
    
    
def read_json_data():
    working_directory = Path(__file__).parent

    path_geojson = working_directory / "geojson_data"

    with open(path_geojson / "swedish_regions.geojson", "r", encoding= "utf-8") as file:
        json_data = json.load(file)
        
    return json_data

