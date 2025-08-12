import os
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import zipfile
import tempfile
import glob
from datetime import datetime
import json

def handler(request):
    """
    Vercel Serverless Function para coletar dados do INMET e salvar no Neon
    """
    try:
        # Obter string de conexão das variáveis de ambiente
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'DATABASE_URL não configurada'})
            }
        
        # Conectar ao banco de dados
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Criar tabela se não existir
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dados_meteorologicos (
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            hora TIME,
            estacao VARCHAR(10),
            nome_estacao VARCHAR(100),
            uf VARCHAR(2),
            regiao VARCHAR(2),
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            altitude DECIMAL(8, 2),
            temperatura_maxima DECIMAL(5, 2),
            temperatura_minima DECIMAL(5, 2),
            temperatura_media DECIMAL(5, 2),
            umidade_relativa DECIMAL(5, 2),
            precipitacao DECIMAL(8, 2),
            velocidade_vento DECIMAL(5, 2),
            pressao_atmosferica DECIMAL(7, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(data, estacao)
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        
        # Coletar dados do ano atual
        current_year = datetime.now().year
        dados_coletados = 0
        
        # Baixar dados do INMET
        url = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{current_year}.zip"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download do arquivo ZIP
            response = requests.get(url, timeout=300)
            response.raise_for_status()
            
            zip_path = os.path.join(temp_dir, f"{current_year}.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extrair ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Procurar arquivos CSV de São Luiz do Paraitinga
            csv_files = glob.glob(os.path.join(temp_dir, "*SAO LUIZ DO PARAITINGA*.CSV"))
            
            for csv_file in csv_files:
                try:
                    # Ler CSV
                    df = pd.read_csv(csv_file, encoding='latin1', sep=';', skiprows=8, decimal=',')
                    
                    # Limpar nomes das colunas
                    df.columns = [col.strip().replace(' ', '_').replace('.', '') for col in df.columns]
                    
                    # Filtrar apenas São Luiz do Paraitinga
                    df_sjc = df[df.get('NOME_DA_ESTACAO', '').str.upper() == 'SAO LUIZ DO PARAITINGA']
                    
                    if df_sjc.empty:
                        continue
                    
                    # Preparar dados para inserção
                    records = []
                    for _, row in df_sjc.iterrows():
                        try:
                            # Converter data
                            data_str = str(row.get('DATA', ''))
                            if data_str and data_str != 'nan':
                                data = pd.to_datetime(data_str, format='%Y-%m-%d', errors='coerce')
                                if pd.isna(data):
                                    continue
                            else:
                                continue
                            
                            record = (
                                data.date(),
                                row.get('HORA', '12:00'),
                                row.get('ESTACAO', ''),
                                row.get('NOME_DA_ESTACAO', ''),
                                row.get('UF', ''),
                                row.get('REGIAO', ''),
                                float(row.get('LATITUDE', 0)) if pd.notna(row.get('LATITUDE')) else None,
                                float(row.get('LONGITUDE', 0)) if pd.notna(row.get('LONGITUDE')) else None,
                                float(row.get('ALTITUDE', 0)) if pd.notna(row.get('ALTITUDE')) else None,
                                float(row.get('TEMPERATURA_MAXIMA', 0)) if pd.notna(row.get('TEMPERATURA_MAXIMA')) else None,
                                float(row.get('TEMPERATURA_MINIMA', 0)) if pd.notna(row.get('TEMPERATURA_MINIMA')) else None,
                                float(row.get('TEMPERATURA_MEDIA', 0)) if pd.notna(row.get('TEMPERATURA_MEDIA')) else None,
                                float(row.get('UMIDADE_RELATIVA', 0)) if pd.notna(row.get('UMIDADE_RELATIVA')) else None,
                                float(row.get('PRECIPITACAO', 0)) if pd.notna(row.get('PRECIPITACAO')) else None,
                                float(row.get('VELOCIDADE_VENTO', 0)) if pd.notna(row.get('VELOCIDADE_VENTO')) else None,
                                float(row.get('PRESSAO_ATMOSFERICA', 0)) if pd.notna(row.get('PRESSAO_ATMOSFERICA')) else None
                            )
                            records.append(record)
                        except Exception as e:
                            continue
                    
                    # Inserir dados no banco (com ON CONFLICT para evitar duplicatas)
                    if records:
                        insert_query = """
                        INSERT INTO dados_meteorologicos (
                            data, hora, estacao, nome_estacao, uf, regiao,
                            latitude, longitude, altitude, temperatura_maxima,
                            temperatura_minima, temperatura_media, umidade_relativa,
                            precipitacao, velocidade_vento, pressao_atmosferica
                        ) VALUES %s
                        ON CONFLICT (data, estacao) DO UPDATE SET
                            hora = EXCLUDED.hora,
                            temperatura_maxima = EXCLUDED.temperatura_maxima,
                            temperatura_minima = EXCLUDED.temperatura_minima,
                            temperatura_media = EXCLUDED.temperatura_media,
                            umidade_relativa = EXCLUDED.umidade_relativa,
                            precipitacao = EXCLUDED.precipitacao,
                            velocidade_vento = EXCLUDED.velocidade_vento,
                            pressao_atmosferica = EXCLUDED.pressao_atmosferica
                        """
                        
                        execute_values(cur, insert_query, records)
                        conn.commit()
                        dados_coletados += len(records)
                
                except Exception as e:
                    continue
        
        # Fechar conexão
        cur.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Dados coletados com sucesso! {dados_coletados} registros processados.',
                'year': current_year,
                'records': dados_coletados,
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        }

