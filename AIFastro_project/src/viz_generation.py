
import regex as re
import pandas as pd
import os

# Ruta al folder que contiene los archivos .csv
path = '/AIFastro_project/filtered_data/Carlos_completed/All Design databse/CSV'

# Obtener la lista de archivos en el directorio
files = [f for f in os.listdir(path) if f.endswith('.csv')]

print("Files found:")
print(files)

# Crear un diccionario para almacenar los dataframes
dataframes = {}

# Leer cada archivo .csv y almacenarlo en el diccionario
for file in files:
    # Crear la ruta completa al archivo
    file_path = os.path.join(path, file)

    # Obtener el nombre del archivo sin la extensión .csv
    base_name = os.path.splitext(file)[0]

    # Leer el archivo .csv ignorando las primeras dos filas y usando la tercera como encabezado
    df = pd.read_csv(file_path, skiprows=2)

    # Seleccionar solo las primeras 9 columnas
    df = df.iloc[:, :9]

    # Definir los nuevos nombres de las columnas
    new_column_names = [
        'Authors', 'Title', 'Publication', 'Year', 'Link',
        'Paper ID', 'Abstract', 'Abstract CAPITAL', 'TOTAL Coincidence'
    ]

    # Renombrar las columnas del dataframe
    df.columns = new_column_names

    print(f"File name: {file}")
    print(df.shape)

    # Almacenar el dataframe en el diccionario con la clave ajustada
    dataframes[base_name] = df

# Ahora `dataframes` es un diccionario donde la clave es el nombre completo del archivo sin la extensión
# y el valor es el dataframe correspondiente con las columnas renombradas.
# Nuevo fragmento de código para filtrar los dataframes por 'TOTAL Coincidence' igual a 1
for key in dataframes:
    # Filtrar las filas donde 'TOTAL Coincidence' es igual a 1
    dataframes[key] = dataframes[key][dataframes[key]['TOTAL Coincidence'] == 1]

# Ahora `dataframes` contiene solo las filas donde 'TOTAL Coincidence' es igual a 1
import matplotlib.pyplot as plt

# Crear una función para generar el gráfico de líneas con todas las disciplinas
def plot_all_disciplines(dataframes):
    plt.figure(figsize=(20, 10))

    # Colores diferentes para cada disciplina
    colors = plt.cm.get_cmap('tab20', len(dataframes) + 1)  # +1 para incluir la línea total de publicaciones

    # Diccionario para almacenar el conteo total por año
    total_counts_per_year = {}

    # Lista para almacenar las leyendas
    legends = []

    # Iterar sobre cada dataframe en el diccionario
    for i, (key, df) in enumerate(dataframes.items()):
        # Contar el número de publicaciones por año
        counts_per_year = df['Year'].value_counts().sort_index()

        # Agregar los valores al conteo total
        for year, count in counts_per_year.items():
            if year in total_counts_per_year:
                total_counts_per_year[year] += count
            else:
                total_counts_per_year[year] = count

        # Crear la línea para cada disciplina
        plt.plot(counts_per_year.index, counts_per_year.values, marker='o', linestyle='-', color=colors(i), label=key)
        legends.append(key)  # Agregar el nombre del archivo CSV a las leyendas

    # Ordenar el conteo total por año
    total_years = sorted(total_counts_per_year.keys())
    total_counts = [total_counts_per_year[year] for year in total_years]

    # Crear la línea para el total de publicaciones
    plt.plot(total_years, total_counts, marker='o', linestyle='--', color='black', label='Total Publications')
    legends.append('Total Publications')  # Agregar la leyenda del total de publicaciones a la lista

    # Configuración del gráfico
    plt.title('Number of Publications per Year by Discipline')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.legend()
    plt.grid(True)
    plt.show()

    return legends

# Llamar a la función para generar el gráfico y obtener la lista de leyendas
legends = plot_all_disciplines(dataframes)

# Imprimir la lista de leyendas para hacer cambios manualmente
print(legends)

import matplotlib.pyplot as plt

# Crear una función para generar el gráfico de barras con el recuento de publicaciones por disciplina
def plot_bar_disciplines(dataframes):
    # Lista para almacenar el recuento de publicaciones por disciplina
    counts_per_discipline = []
    # Lista para almacenar los nombres de las disciplinas
    disciplines = []

    # Contar el número de publicaciones por cada disciplina
    for key, df in dataframes.items():
        disciplines.append(key)
        counts_per_discipline.append(len(df))

    # Crear el gráfico de barras
    plt.figure(figsize=(12, 8))
    bars = plt.bar(disciplines, counts_per_discipline, color='skyblue')

    # Agregar el total de publicaciones encima de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height}',
            ha='center',
            va='bottom'
        )

    # Configuración del gráfico
    plt.title('Number of Publications per Discipline')
    plt.xlabel('Discipline')
    plt.ylabel('Number of Publications')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.show()

# Llamar a la función para generar el gráfico de barras
plot_bar_disciplines(dataframes)
