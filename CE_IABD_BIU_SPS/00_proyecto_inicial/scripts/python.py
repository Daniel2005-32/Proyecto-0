import csv
import os
from datetime import datetime
import psycopg2


# 11. Crea una clase User para representar a cada usuario válido del CSV
class User:
    def __init__(self, name, surname, email, genre, birth, phone, country, city, state):
        self.name = name
        self.surname = surname
        self.email = email
        self.genre = genre
        self.birth = birth
        self.phone = phone
        self.country = country
        self.city = city
        self.state = state

    def __repr__(self):
        return f"User({self.name} {self.surname}, {self.email})"


# 14. Crear una función llamada: database_init_connection()
def database_init_connection():
    """
    Establece una conexión con la base de datos PostgreSQL que corre en Docker.
    """
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="1234"
    )
    return connection


# 15. Insertar los usuarios válidos creando una función llamada: database_insertion_query(db_connection, users)
def database_insertion_query(db_connection, users):
    """
    1. Recibir una conexión a la base de datos y la lista de usuarios válidos.
    2. Crear un cursor para ejecutar consultas SQL.
    3. Recorrer la lista users.
    4. Insertar cada usuario en la tabla users.
    5. Guardar los cambios en la base de datos mediante commit.
    6. Cerrar el cursor.
    7. Cerrar la conexión con la base de datos.
    """
    cursor = db_connection.cursor()

    # 16. Asegurar que la tabla existe según el esquema del enunciado
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        surname VARCHAR(50) NOT NULL,
        email VARCHAR(255) NOT NULL,
        genre VARCHAR(20),
        birth DATE,
        phone VARCHAR(20),
        country VARCHAR(50),
        city VARCHAR(50),
        state VARCHAR(50)
    );
    """
    cursor.execute(create_table_query)

    insert_query = """
    INSERT INTO users (name, surname, email, genre, birth, phone, country, city, state)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # 4. Insertar cada usuario en la tabla users
    for user in users:
        cursor.execute(insert_query, (
            user.name,
            user.surname,
            user.email,
            user.genre,
            user.birth,
            user.phone,
            user.country,
            user.city,
            user.state
        ))

    # 5. Guardar los cambios en la base de datos mediante commit
    db_connection.commit()

    # 6. Cerrar el cursor
    cursor.close()

    # 7. Cerrar la conexión con la base de datos
    db_connection.close()
    print(f"Se han insertado {len(users)} usuarios en la base de datos con éxito.")


def main():
    # 2. Obtener la fecha actual con el mismo formato: mes_día_año (ej. 10_06_26)
    current_date = datetime.now().strftime("%m_%d_%y")

    # 3. Leer el archivo ../users/extracted/users.csv
    csv_file_path = "../users/extracted/users.csv"

    rejected_rows = []
    imported_rows = []
    users = []  # 12. Lista de objetos User válidos

    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Cabecera: id, name, surname, email, genre, birth, phone, country, city, state
        header = next(reader, None)

        # 4. Recorrer todas las filas del CSV
        for row in reader:
            if not row:
                continue

            # 5. Detectar si una fila contiene algún dato ausente
            has_missing_data = len(row) < 10 or any(field.strip() == "" for field in row)

            if has_missing_data:
                # 6. Si una fila tiene un dato ausente, añadirla a una lista de filas rechazadas
                rejected_rows.append(row)
            else:
                # 7. Si una fila no tiene datos ausentes, añadirla a una lista de filas importadas
                imported_rows.append(row)

                # 11 y 12. Crear un objeto de la clase User y añadirlo a la lista users
                user = User(
                    name=row[1],
                    surname=row[2],
                    email=row[3],
                    genre=row[4],
                    birth=row[5],
                    phone=row[6],
                    country=row[7],
                    city=row[8],
                    state=row[9]
                )
                users.append(user)

    # 8. Crear dos archivos dentro de la carpeta logs:
    #    FECHA_rejected_rows.txt y FECHA_imported_rows.txt
    log_directories = ["logs", "../logs"]
    for log_dir in log_directories:
        os.makedirs(log_dir, exist_ok=True)

        rejected_file = os.path.join(log_dir, f"{current_date}_rejected_rows.txt")
        imported_file = os.path.join(log_dir, f"{current_date}_imported_rows.txt")

        # 9. En el archivo de rechazadas:
        #    o Una primera línea indicando cuántas filas han sido rechazadas.
        #    o Las filas rechazadas debajo.
        with open(rejected_file, mode="w", encoding="utf-8") as f_rej:
            f_rej.write(f"There were {len(rejected_rows)} rejected rows.\n")
            for row in rejected_rows:
                f_rej.write(",".join(row) + "\n")

        # 10. En el archivo de importadas:
        #     o Una primera línea indicando cuántas filas han sido importadas correctamente.
        #     o Las filas importadas debajo.
        with open(imported_file, mode="w", encoding="utf-8") as f_imp:
            f_imp.write(f"There were {len(imported_rows)} imported rows.\n")
            for row in imported_rows:
                f_imp.write(",".join(row) + "\n")

    print(f"Filas importadas correctamente: {len(imported_rows)}")
    print(f"Filas rechazadas por datos ausentes: {len(rejected_rows)}")

    # 13, 14, 15. Conexión con PostgreSQL e inserción
    try:
        db_connection = database_init_connection()
        database_insertion_query(db_connection, users)
    except psycopg2.OperationalError as e:
        print("\n[Aviso PostgreSQL]: No se pudo conectar a la base de datos.")
        print("Recuerda iniciar el contenedor de Docker indicado en el enunciado:")
        print("  docker run -d -p 5432:5432 --name proyecto0 -e POSTGRES_PASSWORD=1234 postgres")
        print(f"Detalle de la conexión: {e}")


if __name__ == "__main__":
    main()
