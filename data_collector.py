
import requests
import pandas as pd
import os
import zipfile
import glob
from datetime import datetime

def download_inmet_data(year, output_dir="data"):
    """Downloads INMET historical data for a given year."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    url = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{year}.zip"
    file_path = os.path.join(output_dir, f"{year}.zip" )

    print(f"Downloading data for year {year} from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for HTTP errors

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {year}.zip")
    return file_path

def extract_zip(zip_file_path, extract_dir):
    """Extracts a zip file."""
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Extracted {zip_file_path} to {extract_dir}")

def process_inmet_data(file_path, city_name="SAO LUIZ DO PARAITINGA", output_dir="data"):
    """Processes INMET data to filter for a specific city and saves as CSV."""
    df = pd.read_csv(file_path, encoding='latin1', sep=';', skiprows=8, decimal=',')
    
    # Clean column names
    df.columns = [col.strip().replace(' ', '_').replace(".", '') for col in df.columns]

    # Filter for São Luiz do Paraitinga
    df_sjc = df[df['NOME_DA_ESTACAO'] == city_name.upper()]

    if df_sjc.empty:
        print(f"No data found for {city_name} in {file_path}")
        return None

    output_csv_path = os.path.join(output_dir, f"inmet_data_{city_name.lower().replace(' ', '_')}_{os.path.basename(file_path).split('_')[-1].split('.')[0]}.csv")
    df_sjc.to_csv(output_csv_path, index=False)
    print(f"Processed data saved to {output_csv_path}")
    return output_csv_path

if __name__ == "__main__":
    start_year = 2000
    current_year = datetime.now().year
    end_year = current_year # Fetch data up to the current year
    
    for year in range(start_year, end_year + 1):
        zip_file = download_inmet_data(year)
        if zip_file:
            extract_dir = os.path.join("data", str(year))
            extract_zip(zip_file, extract_dir)
            
            # Find the CSV file dynamically within the extracted directory
            csv_files = glob.glob(os.path.join(extract_dir, "*.CSV"))
            if csv_files:
                # Assuming there's only one CSV file per zip or we take the first one
                extracted_csv_path = csv_files[0]
                process_inmet_data(extracted_csv_path)
            else:
                print(f"No CSV file found in {extract_dir}.")


