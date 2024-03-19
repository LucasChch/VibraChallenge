from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from search import search_async

app = Flask(__name__)
socketio = SocketIO(app)

#Endpoint requerido para la búsqueda en el archivo .csv
@app.route('/search', methods=['GET'])
async def search():
    try:
        #Busco los parámentros recibidos del querystring
        name = request.args.get('name')
        city = request.args.get('city')
        quantity = request.args.get('quantity', type=int)
        
        #Nombre del archivo de donde busco los datos
        filename = 'vibra_challenge.csv'

        # Iniciar la búsqueda asincrónica
        results =  await search_async(filename, name, city, quantity)

        # Emitir resultados a través de WebSockets
        socketio.emit('search_results', {'status': 'completed', 'results': results})

        #Esto lo que veo en mi salida del endpoint
        return jsonify({'status': 'Results delivered by websocket'})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'status': 'Error occurred during search'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
