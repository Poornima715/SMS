import mysql.connector
from mysql.connector import Error

def connect_to_database():
    connection = None
    cursor = None
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',        # Replace with your database host
            database='sdp',          # Replace with your database name
            user='root',             # Replace with your MySQL username
            password='root123'       # Replace with your MySQL password
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            cursor = connection.cursor()

            # Step 2: Create a table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                gender VARCHAR(10),
                salary decimal(10,2),
                bonus decimal(10,2)
            )
            """
            cursor.execute(create_table_query)
            print("Table 'employee' created successfully.")

            # Step 3: Insert records into the table (Create)
            insert_query = """
            INSERT INTO employee (name, age, gender, salary, bonus)
            VALUES (%s, %s, %s, %s, %s)
            """
            employee_records = [
                ('Alice', 22, 'Female', 65000, 2500),
                ('Bob', 24, 'Male', 80000, 3000),
                ('Charlie', 23, 'Male', 78000, 2800 )
            ]
            cursor.executemany(insert_query, employee_records)
            connection.commit()
            print(f"{cursor.rowcount} records inserted into 'employee' table.")

            # Step 4: Retrieve records from the table (Read)
            select_query = "SELECT * FROM employee"
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Fetching data from 'employee' table:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Salary: {row[4]}, Bonus: {row[5]}")

            # Step 5: Update records in the table (Update)
            update_query = """
            UPDATE employee
            SET age = %s
            WHERE name = %s
            """
            data_to_update = (25, 'Alice')
            cursor.execute(update_query, data_to_update)
            connection.commit()
            print(f"Record updated for {cursor.rowcount} employee(s).")

            # Verify the update
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Data after update:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Salary: {row[4]}, Bonus: {row[5]}")

            # Step 6: Delete records from the table (Delete)
            delete_query = "DELETE FROM employee WHERE name = %s"
            name_to_delete = ('Bob',)
            cursor.execute(delete_query, name_to_delete)
            connection.commit()
            print(f"Record deleted for {cursor.rowcount} employee(s).")

            # Verify the deletion
            cursor.execute(select_query)
            records = cursor.fetchall()
            print("Data after deletion:")
            for row in records:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Salary: {row[4]}, Bonus: {row[5]}")

            # Step 7: Drop the table after operations (Cleanup)
            drop_table_query = "DROP TABLE IF EXISTS employee"
            cursor.execute(drop_table_query)
            print("Table 'employee' dropped successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Call the function to execute CRUD operations
connect_to_database()
