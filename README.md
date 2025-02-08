## Setup Instructions

Follow the steps below to set up the project locally:

**Important Note:** Python must be installed on your machine to proceed with the following steps.

1. **Clone the project**  
   Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/SrinithishB/Service-Portal.git
   ```

2. **Create a virtual environment**  
   Open the command prompt or terminal and navigate to the project directory. Then, create a virtual environment with:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**  
   After creating the virtual environment, activate it using the command:
   ```bash
   venv\Scripts\activate
   ```

4. **Install the required dependencies**  
   With the virtual environment activated, install the necessary Python dependencies using the command:
   ```bash
   cd Service-Portal
   pip install -r requirements.txt
   ```

5. **Run the development server**  
   Finally, run the Django development server to start the project:
   ```bash
   python manage.py runserver
   ```

Now, you can access the application at `http://127.0.0.1:8000/` in your web browser.
