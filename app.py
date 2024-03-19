from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import csv

app = Flask(__name__)
socketio = SocketIO(app)

async def search_async(filename, name=None, city=None, quantity=None):
    results = []

    # Definir los nombres de los campos manualmente ya que el archivo CSV no tiene una fila de encabezado
    fieldnames = ['id', 'name', 'surname', 'email', 'gender', 'company', 'city']

    try:
        with open(filename, newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile,fieldnames=fieldnames)
            for index, row in enumerate(reader,1):
                if (not name or row['name'] == name) and \
                (not city or row['city'] == city):
                    results.append(row)
                    if quantity == index:
                        break
    except Exception as e:
        return(f"Error occurred: {e}")

    return results

#Endpoint requerido para la búsqueda en el archivo .csv
@app.route('/search', methods=['GET'])
async def search():
    try:
        #Busco los parámentros recibidos del querystring
        name = request.args.get('name')
        city = request.args.get('city')
        quantity = request.args.get('quantity', type=int)

        # Iniciar la búsqueda asincrónica
        results =  await search_async('vibra_challenge.csv',name, city, quantity)

        # Emitir resultados a través de WebSockets
        socketio.emit('search_results', {'status': 'completed', 'results': results})

        #Esto lo que veo en mi salida del endpoint
        return jsonify({'status': 'Results delivered by websocket'})
    
    except Exception as e:
        # Manejar la excepción aquí (puedes imprimir un mensaje de error, registrar el error, etc.)
        print(f"Error occurred: {e}")
        return jsonify({'status': 'Error occurred during search'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
