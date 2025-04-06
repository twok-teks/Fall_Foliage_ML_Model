# Fall Foliage ML Model - [Visit](http://fallfrenzy.online/)

Welcome to the **Fall Foliage ML Model** project! 🍁🌳 This project uses machine learning to predict the best times to observe the beautiful fall foliage across various locations in the United States. By analyzing weather data, including temperature, precipitation, and daylight hours, this model provides predictions to help users plan their visits to the most scenic locations during the peak of fall colors.

## Table of Contents
- [Introduction](#introduction)
- [Data Gathering](#data-gathering)
- [Data Processing](#data-processing)
- [Model Training](#model-training)
- [Why These Locations?](#why-these-locations)
- [How to Use](#how-to-use)
- [Installation and Setup](#installation-and-setup)
- [License](#license)
- [Screenshots](#screenshots)

## Introduction

The **Fall Foliage ML Model** predicts the optimal times to view fall foliage using machine learning algorithms. The model considers weather data (such as temperature, precipitation, and daylight) to provide predictions about the status of the fall foliage (e.g., "Peak", "Low-Mod", "Past-Peak") for specific locations.

This project is built using Python, Flask for the web interface, and scikit-learn for the machine learning part.

---

## Data Gathering

Data for training the model is gathered from several key sources:
- **Weather Data**: This includes temperature, precipitation, and daylight duration for each of the selected locations. This data is crucial for predicting foliage color changes.
- **Location Information**: Geographic and environmental attributes of various U.S. locations are considered, including elevation and climate, which directly impact foliage growth and change during the fall season.

Data is collected for each location from publicly available weather data sources and is used to create a dataset that forms the backbone of the model.

---

## Data Processing

Before training the machine learning model, the data undergoes several preprocessing steps:
- **Data Cleaning**: Missing or irrelevant values are removed to ensure the quality of the input data.
- **Feature Engineering**: Features like `Daylight_Group` are created to group similar daylight hours together, improving the model's ability to make accurate predictions.
- **Normalization**: Weather-related features like temperature and precipitation are normalized to ensure that all input variables are on similar scales.

---

## Model Training

The machine learning model is trained using **scikit-learn**. A regression model is used to predict the peak foliage status based on input features. We use cross-validation and hyperparameter tuning to improve the model’s accuracy.

### Training Steps:
1. Load and preprocess the weather data.
2. Split the data into training and testing datasets.
3. Train a regression model using algorithms like **Random Forest** and **Decision Trees**.
4. Validate and tune the model to optimize performance.
5. Save the trained model as a `.pkl` file for deployment.

---

## Why These Locations?

The following U.S. locations were selected for the model because they are famous for their stunning fall foliage displays. These locations are spread across different climates and regions, which allows the model to learn diverse environmental patterns that affect leaf color change during the fall season:

- **Aspen, CO**
- **Montgomery, AL**
- **Great Smoky Mountains, TN/NC**
- **Shenandoah National Park, VA**
- **Yellowstone National Park, WY**
- **Columbia River Gorge, OR**
- **And more...**

These locations were chosen based on their unique climate conditions, natural beauty, and popularity for fall foliage tourism.

---

## How to Use

1. **Web Application**:
    - Navigate to the web app’s homepage.
    - Choose a location from the available list.
    - Input weather data such as temperature, precipitation, and daylight hours.
    - Submit the form to get the prediction of the foliage status for the selected location.

2. **Programmatic Use**:
    - Advanced users can use the trained model to make predictions directly by providing weather data and location as inputs. The model will return predictions like "Low-Mod", "Peak", or "Past-Peak".

---

## Installation and Setup

To set up and run this project locally or on your own server, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/twok-teks/Fall_Foliage_ML_Model.git
cd Fall_Foliage_ML_Model
```

### 2. Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python application.py --host=0.0.0.0
```

The app will be available at http://127.0.0.1:5000/. You can replace 127.0.0.1 with your server’s public IP address if you're running it on a remote server.

