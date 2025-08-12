import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_weather_data(start_date_str, end_date_str, city='SAO LUIZ DO PARAITINGA'):
    """Generate sample weather data for São Luiz do Paraitinga-SP"""
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate realistic weather data for São Luiz do Paraitinga (subtropical climate)
    data = []
    
    for date in date_range:
        # Seasonal temperature variation
        day_of_year = date.timetuple().tm_yday
        base_temp = 20 + 8 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Seasonal variation
        
        # Daily temperature variation
        temp_max = base_temp + np.random.normal(5, 2)
        temp_min = base_temp - np.random.normal(5, 2)
        temp_avg = (temp_max + temp_min) / 2
        
        # Humidity (higher in summer)
        humidity = 60 + 20 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + np.random.normal(0, 10)
        humidity = np.clip(humidity, 30, 95)
        
        # Precipitation (more in summer)
        precip_prob = 0.3 + 0.2 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
        precipitation = np.random.exponential(5) if np.random.random() < precip_prob else 0
        
        # Wind speed
        wind_speed = np.random.gamma(2, 2)
        
        # Atmospheric pressure
        pressure = 1013 + np.random.normal(0, 10)
        
        data.append({
            'DATA': date.strftime('%Y-%m-%d'),
            'HORA': '12:00',
            'ESTACAO': 'A740',
            'NOME_DA_ESTACAO': city,
            'UF': 'SP',
            'REGIAO': 'SE',
            'LATITUDE': -23.2283,
            'LONGITUDE': -45.4169,
            'ALTITUDE': 874.0,
            'TEMPERATURA_MAXIMA': round(temp_max, 1),
            'TEMPERATURA_MINIMA': round(temp_min, 1),
            'TEMPERATURA_MEDIA': round(temp_avg, 1),
            'UMIDADE_RELATIVA': round(humidity, 1),
            'PRECIPITACAO': round(precipitation, 1),
            'VELOCIDADE_VENTO': round(wind_speed, 1),
            'PRESSAO_ATMOSFERICA': round(pressure, 1)
        })
    
    return pd.DataFrame(data)

def save_sample_data():
    """Generate and save sample data for multiple years"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    start_year = 2000
    current_year = datetime.now().year
    
    # Generate data for each year from 2000 to current year
    for year in range(start_year, current_year + 1):
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        # For the current year, generate data only up to the current date
        if year == current_year:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        df = generate_sample_weather_data(start_date, end_date)
        filename = f'data/inmet_data_sao_luiz_do_paraitinga_{year}.csv'
        df.to_csv(filename, index=False)
        print(f'Generated sample data for {year}: {filename}')
    
    # Create a combined dataset for all years from 2000 to current year
    all_data = []
    for year in range(start_year, current_year + 1):
        filename = f'data/inmet_data_sao_luiz_do_paraitinga_{year}.csv'
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv('data/inmet_data_sao_luiz_do_paraitinga_combined.csv', index=False)
        print('Generated combined dataset: data/inmet_data_sao_luiz_do_paraitinga_combined.csv')

if __name__ == "__main__":
    save_sample_data()
    print("Sample weather data generation completed!")

