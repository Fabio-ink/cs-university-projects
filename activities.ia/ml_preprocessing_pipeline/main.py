# Nome do arquivo: processamento.py

print("Iniciando script de pré-processamento...")

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
import os # Boa prática para checar arquivos

# --- Define o caminho base do script para tornar os caminhos dos arquivos robustos ---
script_dir = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# === PARTE 1: BASE DE DADOS RISCO DE CRÉDITO BÁSICO
# =============================================================================

print("\n--- Processando: Risco de Crédito ---")

# --- Carregar os dados ---
# O caminho agora é relativo ao local do script.
csv_risco = os.path.join(script_dir, 'assets', 'risco_credito.csv')

if not os.path.exists(csv_risco):
    print(f"AVISO: Arquivo '{csv_risco}' não encontrado.")
    print("Criando um DataFrame de exemplo para continuar a execução...")
    data = [
        ['ruim', 'alta', 'nenhuma', '0_15', 'alto'],
        ['desconhecida', 'alta', 'nenhuma', '15_35', 'alto'],
        ['desconhecida', 'baixa', 'nenhuma', '15_35', 'moderado'],
        ['desconhecida', 'baixa', 'nenhuma', 'acima_35', 'alto'],
        ['desconhecida', 'baixa', 'nenhuma', 'acima_35', 'baixo'],
        ['desconhecida', 'baixa', 'adequada', 'acima_35', 'baixo'],
        ['ruim', 'baixa', 'nenhuma', '0_15', 'alto'],
        ['ruim', 'baixa', 'adequada', 'acima_35', 'moderado'],
        ['boa', 'baixa', 'nenhuma', 'acima_35', 'baixo'],
        ['boa', 'alta', 'adequada', 'acima_35', 'baixo'],
        ['boa', 'alta', 'nenhuma', '0_15', 'alto'],
        ['boa', 'alta', 'nenhuma', '15_35', 'moderado'],
        ['boa', 'alta', 'nenhuma', 'acima_35', 'baixo'],
        ['ruim', 'alta', 'nenhuma', '15_35', 'alto']
    ]
    df_risco = pd.DataFrame(data, columns=['historia', 'divida', 'garantias', 'renda', 'risco'])
else:
    df_risco = pd.read_csv(csv_risco)

# --- Exibir os dados (inspeção inicial) ---
print("\nHead (Risco de Crédito):")
print(df_risco.head())

# --- Visualização dos dados (Risco de Crédito) ---
print("\nSalvando gráficos para a base de Risco de Crédito...")
plots_risco_dir = os.path.join(script_dir, 'plots', 'risco_credito')
os.makedirs(plots_risco_dir, exist_ok=True)

for column in df_risco.columns:
    plt.figure(figsize=(8, 5))
    sns.countplot(x=column, data=df_risco, palette='pastel')
    plt.title(f'Distribuição de "{column}"')
    plt.xlabel(column)
    plt.ylabel('Contagem')
    plt.tight_layout()
    output_path = os.path.join(plots_risco_dir, f'dist_{column}.png')
    plt.savefig(output_path)
    plt.close()
print(f"Gráficos salvos em: {plots_risco_dir}")

# --- Separar X e y ---
X_risco_credito = df_risco.iloc[:, 0:4].values
y_risco_credito = df_risco.iloc[:, 4].values

print("\nX (Risco de Crédito) - Antes:")
print(X_risco_credito)
print("\ny (Risco de Crédito):")
print(y_risco_credito)

# --- Codificar atributos preditores (LabelEncoder) ---
X_risco_codificado = np.empty(X_risco_credito.shape, dtype=int)
for i in range(X_risco_credito.shape[1]):
    le = LabelEncoder()
    X_risco_codificado[:, i] = le.fit_transform(X_risco_credito[:, i])

X_risco_credito = X_risco_codificado

print("\nX (Risco de Crédito) - Codificado:")
print(X_risco_credito)

# --- Salvar em pickle ---
with open(os.path.join(script_dir, 'risco_credito.pkl'), 'wb') as f:
    pickle.dump([X_risco_credito, y_risco_credito], f)

print("\nArquivo 'risco_credito.pkl' salvo com sucesso.")


# =============================================================================
# === PARTE 2: BASE DE DADOS SOBRE COBERTURA VEGETAL
# =============================================================================

print("\n\n--- Processando: Cobertura Vegetal ---")

# --- Carregar os dados ---
colunas = [
    'Elevacao', 'Orientacao', 'Inclinacao', 
    'Dist_Horizontal_Hidrografia', 'Dist_Vertical_Hidrografia', 
    'Dist_Horizontal_Estradas', 'Sombra_9h', 'Sombra_12h', 'Sombra_15h',
    'Dist_Horizontal_Incendio', 'Area_Selvagem', 'Tipo_Solo', 'Tipo_Cobertura'
]

csv_cover = os.path.join(script_dir, 'assets', 'cov_types.csv')

if not os.path.exists(csv_cover):
    print(f"AVISO: Arquivo '{csv_cover}' não encontrado.")
    df_cover = pd.DataFrame(columns=colunas) # Cria DF vazio para o script não quebrar
else:
    df_cover = pd.read_csv(csv_cover)

# Apenas continua se o DataFrame tiver dados
if not df_cover.empty:
    # --- Exploração dos dados ---
    print("\nHead (Cover Type):")
    print(df_cover.head())
    
    print("\nColunas (Cover Type):")
    print(df_cover.columns)
    
    print("\nHead 10 (Cover Type):")
    print(df_cover.head(10))
    
    print("\nTail 10 (Cover Type):")
    print(df_cover.tail(10))
    
    print("\nEstatísticas (Cover Type):")
    print(df_cover.describe())

    # --- Visualização dos dados ---
    plots_cover_dir = os.path.join(script_dir, 'plots', 'cover_type')
    os.makedirs(plots_cover_dir, exist_ok=True)
    print(f"\nSalvando gráficos para a base de Cobertura Vegetal em: {plots_cover_dir}")
    
    # Frequência das classes
    print("\nFrequência das Classes (Cover Type):")
    print(df_cover['Tipo_Cobertura'].value_counts())

    # Gráfico de barras
    print("Salvando gráfico de barras...")
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Tipo_Cobertura', data=df_cover, palette='viridis')
    plt.title('Frequência dos Tipos de Cobertura Vegetal')
    plt.xlabel('Tipo de Cobertura (Classe)')
    plt.ylabel('Contagem')
    plt.savefig(os.path.join(plots_cover_dir, 'freq_tipo_cobertura.png'))
    plt.close()

    # Histogramas
    print("Salvando histogramas (um por um)...")
    colunas_numericas = colunas[0:10]
    for col in colunas_numericas:
        plt.figure(figsize=(8, 5))
        sns.histplot(df_cover[col], kde=True, bins=30)
        plt.title(f'Histograma de {col}')
        plt.xlabel(col)
        plt.ylabel('Frequência')
        plt.tight_layout()
        plt.savefig(os.path.join(plots_cover_dir, f'hist_{col}.png'))
        plt.close()

    # Grid de Correlação (Pairplot)
    print("Salvando pairplot com uma amostra de 0.5% dos dados. Isso PODE DEMORAR...")
    # Usando amostra de 0.5% para não travar
    df_sample = df_cover.sample(frac=0.005, random_state=1)
    cols_pairplot = colunas_numericas + ['Tipo_Cobertura']

    pairplot_fig = sns.pairplot(df_sample[cols_pairplot], hue='Tipo_Cobertura', palette='bright')
    pairplot_fig.fig.suptitle('Grid de Correlação (Amostra de 0.5%)', y=1.02)
    pairplot_fig.savefig(os.path.join(plots_cover_dir, 'pairplot_correlacao.png'))
    plt.close(pairplot_fig.fig)
    print("Todos os gráficos foram salvos.")

    # --- Divisão entre previsores e classe ---
    X = df_cover.iloc[:, 0:12].values
    y = df_cover.iloc[:, 12].values

    print("\nShape de X (Cover Type) - Antes:")
    print(X.shape)
    
    print("\nShape de y (Cover Type) - Antes:")
    print(y.shape)

    # --- Tratamento da variável alvo (LabelEncoder) ---
    label_encoder_y = LabelEncoder()
    y = label_encoder_y.fit_transform(y)

    print("\nValores de y (Cover Type) - Codificado:")
    print(y)
    print(f"Classes originais: {label_encoder_y.classes_}")
    print(f"Classes transformadas: {np.unique(y)}")

    """
    Explicação: LabelEncoder

    O que é o `LabelEncoder`?
    O `LabelEncoder` é uma ferramenta do Scikit-learn usada para converter 
    rótulos categóricos (sejam eles texto, como "alto", "baixo", ou números 
    não sequenciais) em valores numéricos inteiros. Ele atribui um número 
    inteiro único para cada classe distinta, começando por `0`.

    Importância:
    1.  Requisito de Algoritmos: A maioria dos algoritmos de machine learning 
        (como Regressão Logística, SVMs, Redes Neurais) não consegue processar 
        dados de texto ("labels") diretamente. Eles exigem que *todas* as 
        entradas e saídas (features e alvos) sejam numéricas.
    2.  Codificação da Variável Alvo (y): Ele é a ferramenta ideal para 
        codificar a variável alvo (`y`) em problemas de classificação. 
        No nosso caso, as classes originais eram `[1, 2, 3, 4, 5, 6, 7]`. 
        Muitos algoritmos esperam que as classes comecem em `0`. 
        O `LabelEncoder` fez exatamente esse remapeamento, transformando 
        as classes em `[0, 1, 2, 3, 4, 5, 6]`, o que garante a 
        compatibilidade com as bibliotecas de machine learning.
    """

    # --- Tratamento das variáveis preditoras (StandardScaler e OneHotEncoder) ---
    # Índices 0-9 (10 colunas): Numéricos (Aplicar StandardScaler)
    # Índices 10-11 (2 colunas): Categóricos (Aplicar OneHotEncoder)
    
    print("\nAplicando ColumnTransformer (StandardScaler + OneHotEncoder)...")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), list(range(10))), # Colunas 0-9
            ('cat', OneHotEncoder(), [10, 11])           # Colunas 10 e 11
        ],
        remainder='passthrough',
        sparse_threshold=0  # Força a saída a ser um array denso
    )

    X = preprocessor.fit_transform(X)

    print("\nValores de X (Cover Type) - Pós-transformação:")
    print(X)
    print(f"\nNovo shape de X (após OneHotEncoding): {X.shape}")

    # --- Divisão em split de treinamento e teste ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.25, 
        random_state=0
    )

    # --- Exibir dimensões dos splits ---
    print("\nShapes do Split de Treinamento:")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")

    print("\nShapes do Split de Teste:")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")

    # --- Salvar as variáveis ---
    with open(os.path.join(script_dir, 'cover_type.pkl'), 'wb') as f:
        pickle.dump([X_train, y_train, X_test, y_test], f)
        
    print("\nArquivo 'cover_type.pkl' salvo com sucesso.")

else:
    print(f"\nScript da Parte 2 (Cover Type) não executado pois o arquivo '{csv_cover}' não foi carregado.")

print("\n--- Script finalizado ---")