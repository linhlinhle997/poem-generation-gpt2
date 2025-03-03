# Poem Generation using GPT-2

## Introduction

This project aims to generate Vietnamese poems using a fine-tuned `GPT-2` model. The pipeline consists of two main steps:

**1. Data Collection:** Crawling Vietnamese poems from various sources.

**2. Model Training & Inference:** Fine-tuning GPT-2 on the collected poem dataset to generate meaningful and rhythmic poetry.

## Project Structure

- `crawler_data.py`: Script to crawl Vietnamese poems and store them as a dataset.
- `poem_generation_gpt2.ipynb`: Jupyter Notebook to train and generate poems using GPT-2.
- `requirements.txt`: List of required libraries to run the project.

## Installation & Setup

**Setup Selenium on Local Ubuntu**

If you are running `crawler_data.py` locally and using Selenium, install the required dependencies:

```sh
sudo apt update
sudo apt install -y chromium-chromedriver
```

Ensure that `chromedriver` is correctly installed by checking its version:

```sh
chromedriver --version
```

**Install Dependencies**

Run the following command to install the required libraries:

```sh
pip install -r requirements.txt
```

# Usage

**Step 1: Crawl Data (Run Locally)**

Execute the following command to crawl Vietnamese poems:

```sh
python crawler_data.py
```

This will collect and store poems in a structured format for training.

**Step 2: Train & Generate Poems (Run on Google Colab)**

1. Open `poem_generation_gpt2.ipynb` in Google Colab.
2. Upload the `poem_data.csv` and `requirements.txt`.
3. Follow the notebook steps to fine-tune the GPT-2 model and generate poems.
4. Experiment with different prompts to see varied poetic outputs.

## Results

The model generates five-word Vietnamese poems based on the given input prompt. The trained GPT-2 model ensures coherence, rhythm, and meaning in the generated verses.
