command to run

for dependencies
pip install -r 'requirement.txt'

for seeder/data
python -m utils.seeder

for running the api
uvicorn main:app --reload