import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Cargar los datos (suponiendo que tienes el archivo CSV en la ruta correcta)
df = pd.read_csv(r"C:\Users\eynar\Documents\panama_measles_vaccination.csv")

# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app)

@app.route('/api/vaccination/metadata', methods=['GET'])
def get_metadata():
    """
    Devuelve metadatos generales sobre el conjunto de datos
    """
    return jsonify({
        'total_records': len(df),
        'columns': list(df.columns),
        'years_covered': df['year'].unique().tolist(),
        'data_source': 'World Bank'
    })

@app.route('/api/vaccination/yearly', methods=['GET'])
def get_yearly_data():
    """
    Obtiene datos de vacunación por año
    Parámetros opcionales:
    - year: Filtrar por año específico
    - min_rate: Filtrar por tasa mínima de vacunación
    """
    year = request.args.get('year', type=int)
    min_rate = request.args.get('min_rate', type=float, default=0)

    filtered_data = df.copy()

    if year:
        filtered_data = filtered_data[filtered_data['year'] == year]

    filtered_data = filtered_data[filtered_data['vaccination_rate'] >= min_rate]

    return jsonify(filtered_data.to_dict(orient='records'))

@app.route('/api/vaccination/statistics', methods=['GET'])
def get_vaccination_statistics():
    """
    Devuelve estadísticas generales de vacunación
    """
    stats = {
        'mean_vaccination_rate': df['vaccination_rate'].mean(),
        'median_vaccination_rate': df['vaccination_rate'].median(),
        'max_vaccination_rate': df['vaccination_rate'].max(),
        'min_vaccination_rate': df['vaccination_rate'].min(),
        'total_years_data': len(df['year'].unique())
    }
    return jsonify(stats)

@app.route('/api/vaccination/trend', methods=['GET'])
def get_vaccination_trend():
    """
    Obtiene la tendencia de vacunación a lo largo del tiempo
    """
    trend = df.groupby('year')['vaccination_rate'].mean().reset_index()
    return jsonify(trend.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

