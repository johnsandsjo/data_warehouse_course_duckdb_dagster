
from setuptools import setup, find_packages

setup(
    name="hr_agency",
    version="0.1.0",
    description="A Streamlit dashboard for HR analytics.",
    author="Marcus, John",
    packages=find_packages(),
    install_requires=["streamlit", "duckdb", "pandas", "plotly"],
    package_data={
        "backend.geojson_data": ["*.geojson"],
    },
)