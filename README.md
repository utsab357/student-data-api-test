 # School Project (Django REST API) 🚀

This repository contains a backend-only Django REST API for managing students and their invoices/payments. It uses Django 4.x, Django REST Framework, SQLite3, and includes helpful endpoints for listing, filtering, exporting CSVs, and aggregating summary data.

**Base URL**

```
http://127.0.0.1:8000/api/
```

## Features

- Student and Invoice models with full CRUD via DRF viewsets
- Filtering, searching, and ordering for students and invoices
- Pagination (page size = 20)
- CSV export endpoints for students and per-student invoices
- Summary endpoint with unpaid invoice totals and department counts
- `populate_students` management command to generate realistic seed data
- Basic API tests using DRF `APITestCase`

---

## Quickstart (PowerShell)

1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Prepare database

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Populate sample data (optional)

```powershell
python manage.py populate_students
```

5. Run tests

```powershell
python manage.py test
```

6. Start development server

```powershell
python manage.py runserver
```

Open the API in your browser or use the examples below.

---

## API Endpoints

Base: `http://127.0.0.1:8000/api/`

### Student Endpoints (🟦)

- List all students
	- GET `/students/`

- Paginated students (example page 2)
	- GET `/students/?page=2`

- Filter by department
	- GET `/students/?department=CSE|ECE|ME|IT`

- Filter by roll number
	- GET `/students/?roll_number=R0001`

- Search (name, roll_number, email, phone)
	- GET `/students/?search=John`

- Ordering
	- GET `/students/?ordering=name` or `/students/?ordering=enrollment_date`

### Student Detail & CRUD (🟩)

- Retrieve student (includes nested invoices)
	- GET `/students/{id}/`

- Create student
	- POST `/students/`
	- Body (JSON):

```json
{
	"name": "Test Student",
	"roll_number": "RTEST001",
	"address": "Test Address",
	"department": "CSE",
	"phone": "9876543210",
	"email": "test@example.com"
}
```

- Update student (partial)
	- PATCH `/students/{id}/`
	- Body example: `{"phone":"9998887777","status":"inactive"}`

- Delete student
	- DELETE `/students/{id}/`

### Invoice Endpoints (🟧)

- List invoices
	- GET `/invoices/`

- Invoice detail
	- GET `/invoices/{id}/`

- Create invoice
	- POST `/invoices/`
	- Body example:

```json
{
	"student": 1,
	"invoice_number": "INV-R0001-TEST",
	"amount": "3000.00",
	"paid": false
}
```

- Update invoice (PATCH/PUT)
	- PATCH `/invoices/{id}/`

- Delete invoice
	- DELETE `/invoices/{id}/`

### Summary & Analytics (🟥)

- Summary of students and unpaid invoice totals
	- GET `/students/summary/`
	- Optional: `?department=CSE`

### CSV Export (🟪)

- Export all students as CSV
	- GET `/students/export/`
	- Optional: `?department=CSE`

- Export invoices for a single student (CSV)
	- GET `/students/{id}/export_invoices/`

---

## Request Examples (curl)

- List students

```bash
curl "http://127.0.0.1:8000/api/students/"
```

- Create a student

```bash
curl -X POST -H "Content-Type: application/json" \
	-d '{"name":"Requestly Tester","roll_number":"RTEST1000","department":"CSE","phone":"9998887776","email":"req.tester@example.com"}' \
	"http://127.0.0.1:8000/api/students/"
```

- Create an invoice

```bash
curl -X POST -H "Content-Type: application/json" \
	-d '{"student":123,"invoice_number":"INV-RTEST1000-1","amount":"3500.00","paid":false}' \
	"http://127.0.0.1:8000/api/invoices/"
```

### PowerShell (Invoke-RestMethod)

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/students/" | ConvertTo-Json -Depth 5

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/students/export/" | Select-Object -ExpandProperty Content
```

---

## Testing Workflow (recommended)

1. `GET /api/students/` — confirm list
2. `POST /api/students/` — create a temporary student and note the returned `id`
3. `GET /api/students/{id}/` — confirm creation
4. `POST /api/invoices/` — create invoice for that student
5. `GET /api/invoices/{invoice_id}/` — confirm invoice
6. `PATCH /api/students/{id}/` — update phone/status
7. `PATCH /api/invoices/{invoice_id}/` — update `paid`
8. `DELETE /api/invoices/{invoice_id}/` then `DELETE /api/students/{id}/` — cleanup

Notes: deleting a student will cascade-delete their invoices.

---

## Common Gotchas & Tips

- `roll_number` must be unique — POST with an existing roll_number returns 400.
- Use `PUT` only when sending a full representation of the resource; prefer `PATCH` for partial updates.
- CSV endpoints are GET-only and return `text/csv`.
- Authentication is not configured by default; if you add auth later, include appropriate headers.

---

## Management Command

- `python manage.py populate_students` — creates 200 students (`R0001`..`R0200`) and 0–3 invoices per student. Uses `Faker` if installed, otherwise deterministic fallbacks.

## Want an importable Requestly collection?

I can generate a JSON collection for Requestly/Postman that includes all endpoints and example bodies. If you want it, say: **Create Requestly collection** and I will produce the file content.

---

If you find issues or want enhancements (authentication, API docs, more analytics endpoints), open an issue or ask and I can implement them.

Happy hacking! ✨

