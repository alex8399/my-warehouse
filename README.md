# Backend for MyWarehouse

MyWarehouse is a powerful inventory management tool that enables accurate recording of item quantities and seamless coordination of collections across multiple warehouses. It streamlines the entire inventory process, ensuring that all aspects of warehousing — from stock tracking to collection — are managed with precision and ease.

## Content
[Features](#features)

[Entity-Relationship Diagram](#entity-relationship-diagram)

[Technology Stack](#technology-stack)

[How to run](#how-to-run)

## Features

* **REST APIs:** The backend provides REST APIs for every function, ensuring seamless integration and interaction with the system. This architecture not only supports scalability but also offers the flexibility to expand and adapt the application as needed, making it easier to integrate with other services and scale as your business grows. REST APIs are implemented using ```Django Rest Framework (DRF)```.

* **Role-based access control:** Users with different roles have varying levels of access and can perform specific tasks based on their assigned roles. For instance, a loader has the ability to update the status of a shipment but does not have the permission to delete the shipment or create a new one. Before any operation is executed, the system validates the user's permissions through the ```AccessAPI``` model, ensuring that each action is authorized according to their role. This role-based access control guarantees that users only have the ability to perform actions appropriate to their responsibilities, enhancing security and maintaining the integrity of the system.

* **JSON Web Token Authentication:** Authentication is managed using JSON Web Tokens (JWT), a widely adopted standard for stateless user authentication. JWTs encode information in JSON format and can be signed and optionally encrypted to ensure the integrity and confidentiality of the data. The secure transmission of JWTs between the client and server relies on the use of HTTPS. This functionality is implemented using ```Simple JWT``` plugin.

* **History logs:** The system automatically saves the updated state of an object to the logs whenever any changes are made to a project. These logs record details such as the user who performed the action, the time of the change, and other relevant information. This ensures that users can always track what has been modified within the system. The logging functionality is implemented using ```django-simple-history``` library.

## Entity-Relationship Diagram
![ER diagram](/docs/diagram/er-diagram.svg)


## Technology Stack
* **Python 3.12:** Programming language
* **Django 5.0.4:** Web framework
* **Django Rest Framework 3.15.1:** Toolkit for building REST APIs
* **Simple JWT 5.3.1:** JSON Web Token authentication plugin
* **Django-simple-history 3.5.0:** Logging library

## How to run

### Prerequisites

1. **Python 3.12+**: Ensure you have Python 3.12 or later installed.
2. **Generated secret key**: Secret key for Django app.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/alex8399/my-warehouse.git
    cd my-warehouse
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **Secret Key**: Ensure your `src/config/settings/base.py` file contains your secret key. You can generate it on [djecrety.ir](https://djecrety.ir/):
    ```python
    # src/config/settings/base.py
    SECRET_KEY = 'YOUR_SECRET_KEY'
    ```

2. **Configure database**: Make migrations for database:
    ```bash
    python src/manage.py makemigrations
    python src/manage.py migrate
    ```

3. **Create superuser**: Create a user that you will be able to use to log into the admin panel:
    ```bash
    python src/manage.py createsuperuser
    ```

### Running the Application

1. **Run the Django app**:
    ```bash
    python src/manage.py runserver
    ```

2. **Access the app**: Open your web browser and go to ```http://localhost:8000/```.
