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
    query = "SELECT KategoriID, Navn, Beskrivelse FROM Kategorier;"
    data = pd.read_sql(query, engine)
    data.to_csv("data/kategorier.csv", index=False)

def fetch_and_store_regelverker(engine):
    query = """SELECT RegelverkID, KategoriID, Betingelse, Verdi, TillattHandBagasje, TillattInnsjekketBagasje, Beskrivelse FROM Regelverker;"""
    data = pd.read_sql(query, engine)
    data.to_csv("data/regelverker.csv", index=False)

def fetch_and_store_gjenstander(engine):
    query = """SELECT GjenstandID, GjenstandNavn, KategoriID, Beskrivelse FROM Gjenstander;"""
    data = pd.read_sql(query, engine)
    data.to_csv("data/gjenstander.csv", index=False)

def fetch_and_store_regelverktag(engine):
    query = """SELECT RegelverkTagID, RegelverkID, GjenstandID FROM RegelverkTag;"""
    data = pd.read_sql(query, engine)
    data.to_csv("data/regelverktag.csv", index=False)

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
    csv_file_path = "data/combined_data.csv"
    combined_data.to_csv(csv_file_path, index=False)
    return csv_file_path

os.makedirs('data', exist_ok=True)

# Execute functions to fetch and store data
csv_file_path_combined = fetch_and_store_combined_data(engine)
fetch_and_store_kategorier(engine)
fetch_and_store_regelverker(engine)
fetch_and_store_gjenstander(engine)
fetch_and_store_regelverktag(engine)

print(f"Combined data stored in: {csv_file_path_combined}")
