# Delivery Time Prediction App

Predict delivery time accurately based on agent, location, order, and traffic details using a machine learning model.
---

### Project Overview

The Delivery Time Prediction App is a machine learning-powered Streamlit application designed to predict the estimated delivery time of orders based on multiple factors including:

* Agent details (age, rating)

* Vehicle type and traffic conditions

* Weather conditions

* Order category and location coordinates

* Order and pickup times

The app calculates key metrics like distance between store and drop location and time to pickup, then uses a trained XGBoost model to predict delivery time in minutes, hours, or days. Users get real-time predictions displayed in modern, interactive mini-cards and an animated pop-out card.
---
### Importance of the Project

* Optimizes Delivery Operations:
Accurately predicting delivery times helps logistics companies plan routes, manage workforce, and improve efficiency.

* Enhances Customer Experience:
Customers get realistic delivery estimates, reducing uncertainty and increasing satisfaction.

* Supports Data-Driven Decisions:
Businesses can analyze delivery patterns, agent performance, and traffic impact, helping strategic decision-making.

* Professional Dashboard Interface:
Modern UI with mini-cards and interactive elements allows managers or staff to quickly interpret delivery metrics.

* Scalable & Deployable:
Can be integrated into web platforms, apps, or internal dashboards, providing actionable insights in real-time.
---

### Installation

* Clone the repository:

```bash
git clone https://github.com/your-username/delivery-time-prediction.git
cd delivery-time-prediction
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
```
---

### Let’s Connect

If you're working on something similar, want feedback on your analytics project, or would like to collaborate — feel free to connect!