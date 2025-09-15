# Student Information Search Portal

A secure and dynamic Flask web application designed to search for student information from an Excel sheet and display it through a clean, user-friendly interface. This project, part of a Software Testing and Quality Assurance (STQA) course, demonstrates best practices in web development, security, and deployment.

---

## ✨ Key Features

* **Secure Search:** Utilizes the `POST` method to hide sensitive information (like enrollment numbers) from the URL.
* **Dynamic Data Handling:** Reads directly from a `students.xlsx` file and automatically displays only the available data for a given student.
* **Intelligent Column Detection:** The backend automatically identifies the enrollment number column, making the system flexible to minor changes in the Excel sheet format.
* **Interactive UI:** The results page features a professional, tabular layout with controls to dynamically show or hide specific fields.
* **CSRF Protection:** Integrated with Flask-WTF to prevent cross-site request forgery attacks.
* **Responsive Design:** The interface is fully responsive and works seamlessly on desktops, tablets, and mobile devices.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Data Processing:** Pandas
* **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
* **Deployment:** Vercel

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

Make sure you have the following installed:
* Python 3.8+
* `pip` (Python package installer)
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/STQA_PROJECT.git](https://github.com/your-username/STQA_PROJECT.git)
    cd STQA_PROJECT
    ```

2.  **Create and activate a virtual environment:**
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the Data File:**
    * Ensure your student data file is named `students.xlsx` and is placed in the root directory.
    * The file must contain a column with "enrollment" in its name for automatic detection.

5.  **Set Up Environment Variables:**
    * For security, the Flask `SECRET_KEY` is managed via an environment variable. Create a file named `.flaskenv` in the root directory and add the following line:
    ```
    SECRET_KEY="your-own-strong-random-secret-key"
    ```
 

---

## 🏃‍♂️ Running the Application

1.  With your virtual environment activated, run the Flask application:
    ```bash
    flask run
    ```
2.  Open your web browser and navigate to:
    `http://127.0.0.1:5000`

---

## 🌐 Deployment

This application is configured for easy deployment on **Vercel**. The `vercel.json` file in the repository contains the necessary build and routing rules. To deploy:

1.  Push the project to a GitHub repository.
2.  Import the repository into your Vercel account.
3.  Set the `SECRET_KEY` as an environment variable in your Vercel project settings.
4.  Vercel will automatically build and deploy the application.

---

## 🧑‍💻 Developed By

**Adesh Sarwade**

* **LinkedIn:** [sarwade-adesh-375297273](https://www.linkedin.com/in/sarwade-adesh-375297273/)
* **GitHub:** [@ADESHSARWADE](https://github.com/ADESHSARWADE)
