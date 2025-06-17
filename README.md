# SKU Application

A pharmaceutical SKU (Stock Keeping Unit) management application with both backend API and Angular frontend.

## Project Overview

This application provides a complete solution for managing pharmaceutical SKUs, with features including:

- SKU listing, searching, and filtering
- Create, edit, and delete SKUs
- Status management workflow
- Data validation and verification
- User-friendly interface with Angular Material

## Repository Structure

- `/backend` - FastAPI backend
- `/sku-app` - Angular frontend
- Various utility scripts and testing tools

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Angular CLI
- SQLite

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at http://localhost:8000

### Frontend Setup

```bash
cd sku-app
npm install
ng serve
```

The frontend application will be available at http://localhost:4200

## Command Line Tools

- `list_all_skus.py` - List all SKUs in the database
  - Usage: `./list_all_skus.py [--status STATUS] [--format {table,json}]`
  - Example: `./list_all_skus.py --status Active --format json`

## License

[MIT License](LICENSE)
