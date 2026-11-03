
<div align="center">

# ◈ QR STUDIO

### CREATE. CUSTOMIZE. SCAN. MANAGE.

**A Modern Full-Stack QR Code Generation & Management Platform**

Build beautiful, customizable and intelligent QR experiences with a powerful Python backend and modern Next.js frontend.

<br/>

![Project](https://img.shields.io/badge/PROJECT-QR%20STUDIO-0D9488?style=for-the-badge)
![Next.js](https://img.shields.io/badge/NEXT.JS-15-000000?style=for-the-badge&logo=nextdotjs)
![React](https://img.shields.io/badge/REACT-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/PYTHON-3.x-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FASTAPI-API-009688?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TYPESCRIPT-5-3178C6?style=for-the-badge&logo=typescript)

[Features](#-key-features) •
[Architecture](#-system-architecture) •
[Installation](#-installation--setup) •
[API](#-api-documentation) •
[Developer](#-developer)

</div>

---

# 01. PROJECT OVERVIEW

QR Studio is a full-stack QR code generation and management platform designed to simplify how users create, customize, scan and manage QR codes.

The platform combines a responsive Next.js interface with a Python FastAPI backend to deliver a modular and maintainable application architecture.

### Core Objectives

- Generate QR codes for multiple data formats.
- Customize QR appearance with foreground and background colors.
- Embed logos inside QR codes.
- Generate downloadable PNG and SVG outputs.
- Scan and decode QR codes from uploaded images.
- Create dynamic QR links with editable destinations.
- Generate hundreds of QR codes using CSV uploads.
- Maintain QR generation history.
- Track dynamic redirect scans.

---

# 02. KEY FEATURES

## QR Generation Engine

| Feature | Description |
|---|---|
| Text QR | Convert text into QR codes |
| Website QR | Generate website URL QR codes |
| Wi-Fi QR | Share Wi-Fi credentials |
| Email QR | Generate email action QR codes |
| Phone QR | Create telephone QR codes |
| Contact QR | Generate vCard contact QR codes |
| PNG Export | Download QR codes as PNG |
| SVG Export | Generate scalable SVG QR codes |
| Color Customization | Customize foreground and background |
| Logo Embedding | Add a logo inside QR codes |
| Error Correction | L, M, Q and H levels |

## Dynamic QR Management

- Create dynamic QR links.
- Store destination URLs.
- Change destination URLs without regenerating the QR code.
- Redirect users through unique QR identifiers.
- Count visits to dynamic redirect links.

## QR Scanner

- Upload QR code images.
- Decode QR content using OpenCV.
- Identify whether decoded content is a URL.
- Display decoded information.

## Bulk QR Generator

- Upload CSV files.
- Select a content column.
- Generate multiple QR codes.
- Download generated QR images in a ZIP archive.
- Supports up to 500 CSV records per batch.

## History & Analytics

- Save generated QR records.
- View recent QR activity.
- Delete QR history.
- Mark QR codes as favorites.
- Track total QR creations.
- Track dynamic QR links.
- Track dynamic redirect scans.

## PDF Export

Convert an uploaded image into a downloadable PDF containing the image.

---

# 03. TECHNOLOGY STACK

## Frontend Architecture

| Technology | Purpose |
|---|---|
| Next.js 15 | React application framework |
| React 19 | Component-based UI |
| TypeScript | Type safety |
| Tailwind CSS 3 | Styling framework |
| Lucide React | Interface icons |
| Recharts | Data visualization |

## Backend Architecture

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Request validation |
| qrcode | QR code generation |
| Pillow | Image processing |
| OpenCV | QR image scanning |
| ReportLab | PDF generation |
| NumPy | Image array processing |

## Database & Storage

| Technology | Purpose |
|---|---|
| MongoDB | Optional persistent database |
| SQLite | Local development fallback |
| PyMongo | MongoDB integration |

---

# 04. SYSTEM ARCHITECTURE

QR Studio follows a modular full-stack architecture.

```mermaid
flowchart TB
    U["USER"]

    subgraph FRONTEND["PRESENTATION LAYER"]
        N["Next.js 15"]
        R["React 19"]
        T["TypeScript"]
        UI["QR Studio Dashboard"]
    end

    subgraph API["BACKEND LAYER"]
        F["FastAPI Application"]
        V["Request Validation"]
        Q["QR Generation Service"]
        S["QR Scanning Service"]
        D["Dynamic Redirect Service"]
        B["Bulk Processing Service"]
        P["PDF Export Service"]
    end

    subgraph DATA["DATA LAYER"]
        M[("MongoDB")]
        L[("SQLite Fallback")]
    end

    U --> UI
    UI --> N
    N --> R
    R --> T
    UI -->|"HTTP REST API"| F

    F --> V
    V --> Q
    V --> S
    V --> D
    V --> B
    V --> P

    Q --> M
    Q --> L
    D --> M
    D --> L
    F --> M
    F --> L
```

## Architecture Explanation

**1. Presentation Layer**

The Next.js application handles the user interface, navigation, QR generation forms, scanner interface and history dashboard.

**2. API Layer**

FastAPI receives HTTP requests, validates input and connects frontend operations with backend services.

**3. Business Logic Layer**

The backend separates QR generation, image scanning, storage and other processing operations into dedicated modules.

**4. Persistence Layer**

MongoDB is used when a valid MongoDB connection is configured. Otherwise, the application uses SQLite.

---

# 05. QR GENERATION WORKFLOW

```mermaid
flowchart TD
    A([User Opens QR Studio])
    B["Select QR Format"]
    C["Enter QR Content"]
    D["Customize QR Settings"]
    E["Send API Request"]
    F["Validate Request"]
    G["Build QR Payload"]
    H["Generate QR Image"]
    I["Generate PNG and SVG"]
    J["Save Generation History"]
    K["Return QR Response"]
    L["Display Preview"]
    M["Download QR Code"]

    A --> B --> C --> D --> E
    E --> F
    F -->|"Invalid"| C
    F -->|"Valid"| G
    G --> H --> I --> J --> K --> L --> M
```

### Generation Process

1. User selects a QR format.
2. User enters the required information.
3. Frontend sends a request to FastAPI.
4. Backend validates the supplied data.
5. QR service converts the information into a QR payload.
6. QR image is generated.
7. PNG and SVG outputs are produced.
8. Generation details are saved in the database.
9. Frontend receives the generated QR response.
10. User previews and downloads the QR code.

---

# 06. DYNAMIC QR ARCHITECTURE

Dynamic QR codes allow destination URLs to change without changing the QR code itself.

```mermaid
flowchart TD
    A["Create Dynamic QR"]
    B["Enter Destination URL"]
    C["Generate Unique Identifier"]
    D["Save Identifier and Destination"]
    E["Create Redirect URL"]
    F["Generate QR Image"]
    G["User Scans QR Code"]
    H["Backend Receives Redirect Request"]
    I["Find Identifier in Database"]
    J["Increment Scan Counter"]
    K["Redirect to Destination"]

    A --> B --> C --> D --> E --> F
    F --> G --> H --> I
    I -->|"Found"| J --> K
    I -->|"Not Found"| X["Return 404 Error"]
```

### Why Dynamic QR Codes?

Traditional QR codes contain fixed information.

Dynamic QR codes contain a redirect URL that points to a destination stored on the backend.

This allows the destination to be changed without printing a new QR code.

**Example:**

```text
Original QR URL:
https://your-backend.com/r/ABC123

Initial Destination:
https://example.com/page-one

Updated Destination:
https://example.com/page-two
```

The QR code remains the same while the destination changes.

---

# 07. PROJECT DIRECTORY STRUCTURE

```text
QR-CODE-GENARTOR/
│
├── frontend/
│   │
│   ├── app/
│   │   ├── bulk/
│   │   │   └── page.tsx
│   │   │
│   │   ├── create/
│   │   │   └── page.tsx
│   │   │
│   │   ├── dynamic/
│   │   │   └── page.tsx
│   │   │
│   │   ├── history/
│   │   │   └── page.tsx
│   │   │
│   │   ├── scan/
│   │   │   └── page.tsx
│   │   │
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/
│   │   └── shell.tsx
│   │
│   ├── lib/
│   │   └── api.ts
│   │
│   ├── public/
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── backend/
│   │
│   ├── app/
│   │   ├── services/
│   │   │   ├── qr_service.py
│   │   │   └── storage.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── data/
│   │
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
└── README.md
```

---

# 08. INSTALLATION & SETUP

## Prerequisites

- Node.js 20 or later.
- npm.
- Python 3.10 or later.
- Git.
- MongoDB Atlas account (optional).

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

```bash
cd QR-CODE-GENARTOR
```

## Step 2: Configure Frontend

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000
```

## Step 3: Configure Backend

Open another terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 09. ENVIRONMENT CONFIGURATION

## Frontend Environment

File: `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Backend Environment

File: `backend/.env`

```env
MONGODB_URI=
MONGODB_DATABASE=qr_code_studio

FRONTEND_ORIGIN=http://localhost:3000

PUBLIC_BASE_URL=http://localhost:8000
```

### MongoDB Configuration

To enable MongoDB, provide your MongoDB Atlas connection string:

```env
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@YOUR_CLUSTER.mongodb.net/
```

Configure your database:

```env
MONGODB_DATABASE=qr_code_studio
```

**Important:** Keep database credentials private. Never commit `.env` or `.env.local` files to GitHub.

If MongoDB is not configured or its connection fails, the current storage implementation falls back to SQLite.

For production, verify the database connection explicitly rather than assuming MongoDB is active.

---

# 10. API DOCUMENTATION

Base URL:

```text
http://localhost:8000
```

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend health |
| POST | `/api/qr/generate` | Generate QR code |
| POST | `/api/qr/scan` | Scan QR image |
| GET | `/api/history` | Get QR history |
| DELETE | `/api/history/{id}` | Delete QR history |
| PATCH | `/api/history/{id}/favorite` | Update favorite |
| GET | `/api/analytics` | Get analytics |
| POST | `/api/qr/dynamic` | Create dynamic QR |
| PATCH | `/api/qr/dynamic/{code}` | Update destination |
| GET | `/r/{code}` | Dynamic redirect |
| POST | `/api/bulk` | Bulk QR generation |
| POST | `/api/qr/pdf` | Convert image to PDF |

## Example: Generate QR Code

Request:

```http
POST /api/qr/generate
Content-Type: application/json
```

Body:

```json
{
  "type": "url",
  "data": {
    "content": "https://example.com"
  },
  "title": "My Website",
  "foreground": "#111827",
  "background": "#FFFFFF",
  "error_correction": "H",
  "box_size": 10,
  "border": 4
}
```

## Example: Create Dynamic QR

```http
POST /api/qr/dynamic
Content-Type: application/json
```

Body:

```json
{
  "title": "My Dynamic Link",
  "destination": "https://example.com"
}
```

## Example: Update Dynamic Destination

```http
PATCH /api/qr/dynamic/ABC123
Content-Type: application/json
```

Body:

```json
{
  "title": "Updated Link",
  "destination": "https://example.com/new-page"
}
```

---

# 11. DATABASE ARCHITECTURE

QR Studio currently uses two storage options.

```mermaid
flowchart TD
    A["Storage Service"]
    B{"MongoDB URI Available?"}
    C["Connect to MongoDB"]
    D{"Connection Successful?"}
    E[("MongoDB Collections")]
    F[("SQLite Database")]
    G["History Operations"]
    H["Redirect Operations"]
    I["Analytics Operations"]

    A --> B
    B -->|"Yes"| C
    C --> D
    D -->|"Yes"| E
    D -->|"No"| F
    B -->|"No"| F
    E --> G
    E --> H
    E --> I
    F --> G
    F --> H
    F --> I
```

### MongoDB Collections

**history**

Stores QR generation records:

```json
{
  "id": "unique_identifier",
  "title": "My Website",
  "content": "https://example.com",
  "type": "url",
  "created_at": "2026-11-03T10:00:00+00:00",
  "favorite": false
}
```

**redirects**

Stores dynamic QR information:

```json
{
  "code": "ABC123",
  "destination": "https://example.com",
  "created_at": "2026-11-03T10:00:00+00:00",
  "scans": 0
}
```

---

# 12. ERROR CORRECTION LEVELS

QR Studio supports four QR error correction levels.

| Level | Recovery Capacity | Use Case |
|---|---|---|
| L | Approximately 7% | Clean QR codes |
| M | Approximately 15% | General usage |
| Q | Approximately 25% | Moderate damage tolerance |
| H | Approximately 30% | Logo embedding and higher recovery |

Higher error correction generally increases QR code complexity and reduces its maximum data capacity.

For logo embedding, QR Studio requires level H.

---

# 13. TESTING & VALIDATION

Recommended verification checklist:

- [ ] Frontend starts successfully.
- [ ] Backend starts successfully.
- [ ] Health endpoint returns success.
- [ ] Text QR generation works.
- [ ] Website QR generation works.
- [ ] Wi-Fi QR generation works.
- [ ] Email QR generation works.
- [ ] Contact QR generation works.
- [ ] PNG export works.
- [ ] SVG export works.
- [ ] Logo embedding works.
- [ ] QR image scanning works.
- [ ] Dynamic QR creation works.
- [ ] Dynamic destination updating works.
- [ ] Redirect scan counting works.
- [ ] CSV bulk generation works.
- [ ] ZIP download works.
- [ ] History management works.
- [ ] Favorite functionality works.
- [ ] Analytics endpoint works.
- [ ] PDF export works.
- [ ] MongoDB persistence is verified separately.

Build frontend:

```bash
cd frontend
npm run build
```

Run backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

---

# 14. PRODUCTION IMPROVEMENT ROADMAP

The following are potential future improvements, not claims about currently implemented features.

| Priority | Improvement |
|---|---|
| High | Authentication and individual user accounts |
| High | User-level database isolation |
| High | Production MongoDB connection validation |
| High | Secure environment and secret management |
| High | Automated backend tests |
| High | Playwright frontend testing |
| Medium | Redis-based rate limiting |
| Medium | Advanced QR scan analytics |
| Medium | QR templates and design presets |
| Medium | Downloadable PDF QR sheets |
| Medium | QR expiration and access controls |
| Medium | Docker-based deployment |
| Future | Team workspaces |
| Future | Subscription and billing system |
| Future | Advanced analytics dashboard |

---

# 15. SECURITY CONSIDERATIONS

Before public production deployment, consider:

- Validate all incoming user input.
- Restrict uploaded image and CSV sizes.
- Configure CORS for trusted frontend origins.
- Protect MongoDB credentials.
- Add API rate limiting.
- Prevent unauthorized history access.
- Introduce authentication before enabling private user workspaces.
- Add URL validation and protection against unsafe redirect destinations.
- Configure HTTPS.
- Avoid exposing internal errors to clients.
- Monitor database availability.

**Production note:** The current project does not implement authentication or individual user accounts. Its history and dynamic redirects are shared application-level records, not isolated user records.

---

# 16. CONTRIBUTION GUIDELINES

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Implement your changes.
4. Test frontend and backend functionality.
5. Commit your changes.
6. Create a pull request.

Example:

```bash
git checkout -b feature/new-qr-feature
```

```bash
git add .
git commit -m "feat: add new QR functionality"
git push origin feature/new-qr-feature
```

---

# 17. DEVELOPER

<div align="center">

## Vishal Deep

**Software Developer | Full Stack Developer | AI Systems Enthusiast**

Building practical software solutions using modern web technologies, backend engineering and intelligent systems.

[![GitHub](https://img.shields.io/badge/GitHub-VishalDeep1377-181717?style=for-the-badge&logo=github)](https://github.com/VishalDeep1377)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/vishal-deeedeep-14a864255)

</div>

---

# 18. LICENSE

Add a LICENSE file to the repository before declaring a license for this project.

Until then, no open-source license is specified.

---

<div align="center">

### QR STUDIO

**Create Smarter. Scan Faster. Manage Better.**

Built with Next.js, TypeScript, Python and FastAPI.

⭐ If you find this project useful, consider giving it a star!

</div>
