# Ski Resorts EDA Dashboard

A Streamlit app for exploratory data analysis (EDA) on ski resort data — visualizing trends and patterns through interactive charts.

## Features

- Interactive exploration of ski resort data
- Visualizations and charts to surface trends (e.g. by country, price, elevation, season length)
- Filters/widgets to slice the data

## Tech Stack

- **Python**
- **Streamlit** – app framework
- **Pandas** – data manipulation
- **Plotly** – interactive visualizations

## Project Structure

```
.
├── myapp.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/dragangolic/Ski-Resorts-.git
   cd your-repo-name
   ```

2. (Optional) Create a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Live Demo

> Add your Streamlit Cloud URL here, e.g. `https://ski-resorts.streamlit.app/`

## Data

Data sourced from [Kaggle](https://www.kaggle.com/) 


## License

This project is open source and available under the [MIT License](LICENSE).
