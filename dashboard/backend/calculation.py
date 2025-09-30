from datetime import timedelta
from difflib import get_close_matches
from backend.data_processing import read_json_data
from backend.data_filter import region_code, region_vacancies

def days_ago(date):
  return date - timedelta(7)

#Total antal annonser
def num_of_ads(df):
    return df.shape[0]

#Nya annonser senaste 7 dagar
def num_of_ads_7_days(df):
    df_new = df[['occupation', 'number_of_vacancies', 'publication_date']]
    max_date = df_new['publication_date'].max()
    filtered_df = df_new[df_new['publication_date'] > days_ago(max_date)]

    return filtered_df.shape[0]


# ----------------------------#


def get_matches(occupation):
    
    df_occupation = region_code(geojson= read_json_data())
    
    # get all region in a list
    regions = region_vacancies(occupation= occupation)["workplace_region"].values
    
    region_code_map = []
    for region in regions:

        name_macthes = get_close_matches(region, df_occupation.keys(), n= 1)[0]
        code = df_occupation[name_macthes]
        region_code_map.append(code)
        
    return region_code_map


def count_vacancies(data, type = None):


        if type == 'ej specificerad':
            return data[data["workplace_region"] == 'ej specificerad']["number_of_vacancies"].sum()
        else:
            return data["number_of_vacancies"].sum()
        
def count_procent(data):
    
    total = count_vacancies(data= data)
    part = count_vacancies(data= data, type= "ej specificerad")
    return f"{round((part / total) * 100,2)}%" 