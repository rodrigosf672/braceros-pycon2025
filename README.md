# Honrando las Narrativas de Braceros
## Un Enfoque Pythonico para Minería de Textos de Historias de Trabajo Arduo, Migración y Resiliencia
### PyCon US 2025 (Charla): https://us.pycon.org/2025/schedule/presentation/15/

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/fe75fbfb-1f64-4302-8f49-fbfd76c35c39" />

This project explores and visualizes oral histories from the Bracero Program using Python. It includes:

- Structured quote extraction from interview transcripts
- Topic modeling and keyword analysis
- Interactive Shiny app to explore quotes by topic/interviewee
- Static HTML visualizations of major themes

---

## Project Structure 
``` braceros-pycon2025/ 
├── data/ # Input CSVs including quotes and topic data
├── output/ # Static HTML visualizations (viewable in browser)
├── scripts/ # Python scripts for scraping, processing, and Shiny apps
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Run the Quote Browser App

```bash
shiny run scripts/Script05-ShinyApp.py
```

Features:
- Filter by topic and interviewee
- Paginated quote browsing across thousands of quotes

## Open HTML Reports
- Open files in your browser to see `top20_topics_barchart.html`, `topic_hierarchy.html`, and `topics_overview.html`

## Installation Requirements
```bash
pip install -r requirements.txt
```

## About the Data
- The quotes are drawn from structured interviews in the [Bracero History Archive](https://braceroarchive.org), which documents the experiences of Mexican migrant workers in the U.S. between 1942 and 1964.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code and ideas in this repository with attribution.

### Disclaimer

This repository includes scripts for data extraction, cleaning, classification, and visualization using publicly available data from [Bracero History Archive](https://braceroarchive.org). It is provided **strictly for educational and academic purposes**.

I do **not endorse or encourage** scraping or making HTTP requests to any website **without understanding and complying with**:

- That website’s **Terms of Service**
- **Local and international laws**, including but not limited to data privacy, copyright, and computer misuse laws
- The rules and **ethical expectations** of academic and professional communities

You are fully responsible for how you use or adapt the provided scripts. By accessing or using this codebase, you agree that:

- You will verify permissions before extracting data from any source of any website.
- You are solely responsible for any consequences, including rate-limiting, bans, legal penalties, or data misuse.
- I (the author) disclaim all liability for damages, data loss, violations, or legal actions resulting from the use of this code.
