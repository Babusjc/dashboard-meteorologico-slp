import os
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def setup_database(database_url):
    """
    Configura o banco de dados Neon com a tabela necessária e dados de exemplo
    """
    try:
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        print("Conectado ao banco de dados Neon!")
        
        # Criar tabela
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dados_meteorologicos (
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            hora TIME DEFAULT '12:00:00',
            estacao VARCHAR(10) DEFAULT 'A740',
            nome_estacao VARCHAR(100) DEFAULT 'SAO LUIZ DO PARAITINGA',
            uf VARCHAR(2) DEFAULT 'SP',
            regiao VARCHAR(2) DEFAULT 'SE',
            latitude DECIMAL(10, 6) DEFAULT -23.2283,
            longitude DECIMAL(10, 6) DEFAULT -45.4169,
            altitude DECIMAL(8, 2) DEFAULT 629.0,
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
        print("Tabela 'dados_meteorologicos' criada com sucesso!")
        
        # Verificar se já existem dados
        cur.execute("SELECT COUNT(*) FROM dados_meteorologicos")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("Inserindo dados de exemplo...")
            
            # Gerar dados de exemplo de 2000 até o ano atual
            start_date = datetime(2000, 1, 1)
            end_date = datetime.now()
            
            records = []
            current_date = start_date
            
            while current_date <= end_date:
                # Simular dados meteorológicos realistas para São Luiz do Paraitinga
                day_of_year = current_date.timetuple().tm_yday
                
                # Temperatura com sazonalidade
                temp_base = 20 + 8 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi/2)
                temp_variation = np.random.normal(0, 3)
                temp_media = round(temp_base + temp_variation, 1)
                temp_maxima = round(temp_media + np.random.uniform(3, 8), 1)
                temp_minima = round(temp_media - np.random.uniform(2, 6), 1)
                
                # Umidade relativa
                umidade = round(np.random.normal(65, 15), 1)
                umidade = max(30, min(95, umidade))
                
                # Precipitação (mais chuva no verão)
                precip_prob = 0.3 + 0.2 * np.sin(2 * np.pi * day_of_year / 365.25)
                precipitacao = round(np.random.exponential(5) if np.random.random() < precip_prob else 0, 1)
                
                # Velocidade do vento
                vento = round(np.random.gamma(2, 2), 1)
                
                # Pressão atmosférica
                pressao = round(np.random.normal(1013, 10), 1)
                
                record = (
                    current_date.date(),
                    '12:00:00',
                    'A740',
                    'SAO LUIZ DO PARAITINGA',
                    'SP',
                    'SE',
                    -23.2283,
                    -45.4169,
                    874.0,
                    temp_maxima,
                    temp_minima,
                    temp_media,
                    umidade,
                    precipitacao,
                    vento,
                    pressao
                )
                
                records.append(record)
                current_date += timedelta(days=1)
            
            # Inserir dados
            insert_query = """
            INSERT INTO dados_meteorologicos (
                data, hora, estacao, nome_estacao, uf, regiao,
                latitude, longitude, altitude, temperatura_maxima,
                temperatura_minima, temperatura_media, umidade_relativa,
                precipitacao, velocidade_vento, pressao_atmosferica
            ) VALUES %s
            """
            
            execute_values(cur, insert_query, records)
            conn.commit()
            
            print(f"Inseridos {len(records)} registros de dados de exemplo!")
        else:
            print(f"Banco já contém {count} registros.")
        
        # Criar índices para melhor performance
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_dados_data ON dados_meteorologicos(data);",
            "CREATE INDEX IF NOT EXISTS idx_dados_estacao ON dados_meteorologicos(estacao);",
            "CREATE INDEX IF NOT EXISTS idx_dados_data_estacao ON dados_meteorologicos(data, estacao);"
        ]
        
        for index_query in indices:
            cur.execute(index_query)
        
        conn.commit()
        print("Índices criados com sucesso!")
        
        # Fechar conexão
        cur.close()
        conn.close()
        
        print("Configuração do banco de dados concluída!")
        return True
        
    except Exception as e:
        print(f"Erro ao configurar banco de dados: {e}")
        return False

if __name__ == "__main__":
    # Para testar localmente, defina a variável de ambiente DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("Por favor, defina a variável de ambiente DATABASE_URL")
        print("Exemplo: export DATABASE_URL='postgresql://user:pass@host:port/db'")
    else:
        setup_database(database_url)

