# Company Research Web App

A web application that allows users to research companies using a Python script. The app features a modern UI built with Next.js and Shadcn UI components.

## Prerequisites

- Node.js 18+ and npm
- Python 3.x
- Your `research_company.py` script that accepts a company name as a command-line argument and outputs JSON

## Setup

1. Install dependencies:
```bash
npm install
```

2. Place your `research_company.py` script in the root directory of the project.

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Enter a company name in the input field
2. Click the "Research" button
3. The app will execute your Python script with the company name as an argument
4. The results will be displayed in an expandable/collapsible JSON viewer

## Project Structure

- `app/page.tsx` - Main page component with the form and JSON viewer
- `app/api/research/route.ts` - API endpoint that executes the Python script
- `components/ui/` - Shadcn UI components
- `lib/utils.ts` - Utility functions
- `research_company.py` - Your Python script (to be provided)

## Requirements for research_company.py

Your Python script should:
1. Accept a company name as a command-line argument
2. Output valid JSON to stdout
3. Handle errors appropriately

Example usage:
```bash
python3 research_company.py "Company Name"
```

Example output:
```json
{
  "name": "Company Name",
  "description": "Company description",
  "industry": "Technology",
  "founded": 2020
}
``` 