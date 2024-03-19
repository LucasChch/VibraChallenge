import csv

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