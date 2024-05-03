import psycopg2


# Функция для создания структуры БД
def create_db_structure():
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    # Создание таблицы clients
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Создание таблицы phones
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

# Функция для добавления нового клиента
def add_client(first_name, last_name, email):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    cur.execute("INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s)", (first_name, last_name, email))

    conn.commit()
    cur.close()
    conn.close()

# Функция для добавления телефона для существующего клиента
def add_phone(client_id, phone_number):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    cur.execute("INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)", (client_id, phone_number))

    conn.commit()
    cur.close()
    conn.close()

# Функция для изменения данных о клиенте
def update_client(client_id, first_name, last_name, email):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    cur.execute("UPDATE clients SET first_name = %s, last_name = %s, email = %s WHERE id = %s", (first_name, last_name, email, client_id))

    conn.commit()
    cur.close()
    conn.close()

# Функция для удаления телефона для существующего клиента
def delete_phone(phone_id):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    cur.execute("DELETE FROM phones WHERE id = %s", (phone_id,))

    conn.commit()
    cur.close()
    conn.close()

# Функция для удаления существующего клиента
def delete_client(client_id):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    # Сначала удаляем телефоны клиента
    cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))
    # Затем удаляем самого клиента
    cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))

    conn.commit()
    cur.close()
    conn.close()

# Функция для поиска клиента по данным
def find_client(query):
    conn = psycopg2.connect("dbname=clients_db user=postgres password=your_password")
    cur = conn.cursor()

    # Поиск по имени, фамилии, email или телефону
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.phone_number
        FROM clients c
        LEFT JOIN phones p ON c.id = p.client_id
        WHERE c.first_name ILIKE %s
           OR c.last_name ILIKE %s
           OR c.email ILIKE %s
           OR p.phone_number ILIKE %s
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))

    result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return result

#  код демонстрирующий работу всех написанных функций

# Создание структуры БД
create_db_structure()

# Добавление новых клиентов
add_client("Иван", "Иванов", "ivan@example.com")
add_client("Петр", "Петров", "petr@example.com")
add_client("Мария", "Сидорова", "maria@example.com")

# Добавление телефонов для клиентов
add_phone(1, "+79001112233")
add_phone(1, "+79004445566")
add_phone(2, "+79007778899")

# Изменение данных о клиенте
update_client(1, "Иван", "Новый", "ivan_new@example.com")

# Удаление телефона для клиента
delete_phone(2)

# Удаление клиента
delete_client(3)

# Поиск клиентов
print(find_client("Иван"))
print(find_client("Петр"))
print(find_client("9001112233"))
