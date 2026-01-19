# MA API Setup Guide

Follow these steps to get the project running locally.

---

## Install Dependencies

Make sure you have Python installed, then install the required packages:

```bash
pip install -r requirements.txt
```

## Run App if no DB

Command to Run the App, it also make the Database instance
```bash
uvicorn main:app --reload
```

## For seeder

Seeder to create testing data, change the BASE_URL in the file
when working with different IP

```bash
python -m utils.seeder
```