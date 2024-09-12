import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",         
        user="admin",             
        password="*******",    
        database="emp_db"         
    )
    return connection

# Function to register a new admin
def register(connection):
    cursor = connection.cursor()
    username = input("Create username: ")

    # Check if the username is already registered
    cursor.execute("SELECT username FROM admin WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        print("Username already taken!")
    else:
        name = input("Enter name: ")
        password = input("Create password: ")
        
        cursor.execute("""
        INSERT INTO admin (username, password, name)
        VALUES (%s, %s, %s)
        """, (username, password, name))
        connection.commit()
        print("Admin Registered successfully!")
    
    cursor.close()

# Function to login
def login(connection):
    cursor = connection.cursor()
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Fetch the plain-text password from the database
    cursor.execute("SELECT password FROM admin WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]  # result is a tuple, so fetch the first element

        # Compare the entered password with the stored password
        if password == stored_password:
            print("Login successful!")
            return True
        else:
            print("Invalid password!")
            return False
    else:
        print("Username not found!")
        return False

    cursor.close()

# Function to add a new employee
def add_emp(connection):
    email = input("Enter email: ")
    
    cursor = connection.cursor()
    # Check if the email is already registered
    cursor.execute("SELECT email FROM employees WHERE email = %s", (email,))
    existing_email = cursor.fetchone()

    if existing_email:
        print("Email already registered!")
    else:
        name = input("Enter name: ")
        gender = input("Enter gender: ")
        age = int(input("Enter age: "))
        salary = input("Enter salary: ")
        department = input("Enter department: ")

        cursor.execute("""
            INSERT INTO employees (email, emp_name, gender, age, salary, department)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (email, name, gender, age, salary, department))
        connection.commit()
        print("Employee created successfully!")

# Function to view all employees
def view_all_emp(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"Employee ID: {row[0]}, Name: {row[1]}, Email: {row[6]}, Gender: {row[2]}, Age: {row[3]}, Salary: {row[4]}, Department: {row[5]}")

# Function to update employee details
def update(connection):
    emp_id = input("Enter employee ID to update: ")

    cursor = connection.cursor()
    
    print("\nWhich field would you like to update?")
    print("1. Salary")
    print("2. Age")
    print("3. Department")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        new_salary = input("Enter new salary: ")
        cursor.execute("UPDATE employees SET salary = %s WHERE emp_id = %s", (new_salary, emp_id))
        connection.commit()
        print("Salary updated successfully!")

    elif choice == "2":
        new_age = input("Enter new age: ")
        cursor.execute("UPDATE employees SET age = %s WHERE emp_id = %s", (new_age, emp_id))
        connection.commit()
        print("Age updated successfully!")

    elif choice == "3":
        new_department = input("Enter new department: ")
        cursor.execute("UPDATE employees SET department = %s WHERE emp_id = %s", (new_department, emp_id))
        connection.commit()
        print("Department updated successfully!")

    else:
        print("Invalid option!")

# Function to delete an employee
def delete(connection):
    emp_id = int(input("Enter the ID of the employee to delete: "))
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
    connection.commit()
    print(f"Deleted employee ID {emp_id}.")

# Main function to run the console application
def main():
    connection = connect_to_database()
    print("Welcome to the Employee Management System!")
    
    while True:
        print("1. Login")
        print("2. Register as Admin")
        print("3. Quit")
        n = int(input("Enter your choice: "))
        
        if n == 1:
            if login(connection):
                # Once logged in, allow admin operations
                while True:
                    print("\nEMPLOYEE MANAGEMENT SYSTEM")
                    print("1. Add Employee")
                    print("2. View Employees")
                    print("3. Update Employee")
                    print("4. Delete Employee")
                    print("5. Exit")
                    choice = int(input("Enter your choice: "))
                    
                    if choice == 1:
                        add_emp(connection)
                    elif choice == 2:
                        view_all_emp(connection)
                    elif choice == 3:
                        update(connection)
                    elif choice == 4:
                        delete(connection)
                    elif choice == 5:
                        print("Exiting Employee Management System...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif n == 2:
            register(connection)
        elif n == 3:
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
