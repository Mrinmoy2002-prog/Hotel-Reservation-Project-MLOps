# Hotel Reservation Prediction System (MLOps Pipeline)
This project is an end-to-end Machine Learning web application that predicts hotel reservation outcomes. It features a complete MLOps pipeline, utilizing Docker for containerization, Jenkins for continuous integration and continuous deployment (CI/CD), and Google Cloud Run for scalable, serverless production hosting.


## 🛠 Tech Stack
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, LightGBM
* **Web Framework:** Python, Flask
* **Containerization:** Docker
* **CI/CD:** Jenkins, GitHub Webhooks
* **Cloud Infrastructure (GCP):** Google Container Registry (GCR), Google Cloud Run, Google Cloud IAM


## 🚀 Local Deployment (Without Docker)

1. **Clone the repository:**
   `git clone https://github.com/Mrinmoy2002-prog/Hotel-Reservation-Project-MLOps.git`
   `cd Hotel-Reservation-Project-MLOps`

2. **Create and activate a virtual environment:**
   `python -m venv venv`
   *(Windows):* `venv\Scripts\activate`
   *(Linux/Mac):* `source venv/bin/activate`

3. **Install dependencies:**
   `pip install --upgrade pip`
   `pip install -e .`

4. **Run the Flask application:**
   `python app.py`
   The app will be available at `http://localhost:5000`.


## 🐳 Docker Deployment (Local)

1. **Build the Docker image:**
   `docker build -t hotel-reservation-app .`

2. **Run the container:**
   `docker run -p 5000:5000 hotel-reservation-app`


## ⚙️ CI/CD Pipeline Setup (Jenkins)
This project utilizes Jenkins to automate the building, testing, and deployment of the application to Google Cloud Platform.


### Prerequisites for Jenkins Server:
* A running Jenkins instance (Docker-in-Docker configuration recommended).
* Python 3 and virtual environment packages installed on the Jenkins node.
* Google Cloud CLI (`gcloud`) installed on the Jenkins node.


### Pipeline Configuration Steps:
1. **Google Cloud Service Account:**
   * Create a Service Account in GCP with the following roles: `Storage Admin`, `Cloud Run Admin`, and `Service Account User`.
   * Download the JSON key file.

2. **Jenkins Credentials:**
   * Navigate to **Manage Jenkins -> Credentials**.
   * Add a new **Secret file** credential.
   * Upload the GCP JSON key and assign it the ID: `gcp-key`.
   * Add your GitHub credentials with the ID: `github-token`.

3. **Pipeline Execution:**
   * Create a new Pipeline job in Jenkins.
   * Point the "Pipeline script from SCM" to this GitHub repository.
   * Jenkins will read the `Jenkinsfile` and automatically execute the following stages:
     * **Stage 1:** Clone Repository.
     * **Stage 2:** Setup Virtual Environment & Install Dependencies.
     * **Stage 3:** Build and Push Docker Image to GCR.
     * **Stage 4:** Deploy to Google Cloud Run (listening on Port 5000).


## ☁️ Cloud Architecture 
The final application is hosted on **Google Cloud Run**. When code is pushed to the `main` branch, Jenkins automatically triggers a build, creates a lightweight Python 3.10-slim Docker image, securely stores it in GCR, and updates the Cloud Run service to serve the latest predictions globally with zero downtime.