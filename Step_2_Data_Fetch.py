import os
from sqlalchemy import create_engine
import pandas as pd

# Database credentials and connection details
DATABASE = {
    'drivername': 'postgresql',
    'host': 'pmk-smartpack-sql.postgres.database.azure.com',
    'port': '5432',
    'username': 'smartpackuser',
    'password': 'B3Fug!ztZV',
    'database': 'smartpackdb'
}

# Create the SQLAlchemy engine
engine = create_engine(f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")

def fetch_and_store_kategorier(engine):
    query = "SELECT KategoriID, Navn AS KategoriNavn, Beskrivelse AS KategoriBeskrivelse FROM Kategorier;"
    data = pd.read_sql(query, engine)
    data.to_json("data/fetched/kategorier.json", orient='records', indent=4, force_ascii=False)

def fetch_and_store_regelverker(engine):
    query = """SELECT RegelverkID, KategoriID, Betingelse, Verdi, TillattHandBagasje, TillattInnsjekketBagasje, 
    Beskrivelse AS RegelverkBeskrivelse FROM Regelverker;"""
    data = pd.read_sql(query, engine)
    data.to_json("data/fetched/regelverker.json", orient='records', indent=4, force_ascii=False)

def fetch_and_store_gjenstander(engine):
    query = """SELECT GjenstandID, GjenstandNavn, KategoriID, Beskrivelse AS GjenstandBeskrivelse FROM Gjenstander;"""
    data = pd.read_sql(query, engine)
    data.to_json("data/fetched/gjenstander.json", orient='records', indent=4, force_ascii=False)

def fetch_and_store_regelverktag(engine):
    query = """SELECT RegelverkTagID, RegelverkID, GjenstandID FROM RegelverkTag;"""
    data = pd.read_sql(query, engine)
    data.to_json("data/fetched/regelverktag.json", orient='records', indent=4, force_ascii=False)

def fetch_and_store_combined_data(engine):
    complex_query = """
    SELECT 
        Gjenstander.GjenstandNavn AS GjenstandNavn,
        Gjenstander.Beskrivelse AS GjenstandBeskrivelse,
        Kategorier.Navn AS KategoriNavn,
        Kategorier.Beskrivelse AS KategoriBeskrivelse,
        Regelverker.Betingelse,
        Regelverker.Verdi,
        Regelverker.TillattHandBagasje,
        Regelverker.TillattInnsjekketBagasje,
        Regelverker.Beskrivelse AS RegelverkBeskrivelse
    FROM 
        Gjenstander
    JOIN 
        Kategorier ON Gjenstander.KategoriID = Kategorier.KategoriID
    JOIN 
        RegelverkTag ON Gjenstander.GjenstandID = RegelverkTag.GjenstandID
    JOIN 
        Regelverker ON RegelverkTag.RegelverkID = Regelverker.RegelverkID;
    """
    combined_data = pd.read_sql(complex_query, engine)
    json_file_path = "data/fetched/combined_data.json"
    combined_data.to_json(json_file_path, orient='records', indent=4, force_ascii=False)
    return json_file_path

os.makedirs('data', exist_ok=True)

# Execute functions to fetch and store data
json_file_path_combined = fetch_and_store_combined_data(engine)
fetch_and_store_kategorier(engine)
fetch_and_store_regelverker(engine)
fetch_and_store_gjenstander(engine)
fetch_and_store_regelverktag(engine)

print(f"Combined data stored in: {json_file_path_combined}")
