# QR Code Studio — Premium Web Edition

A full-stack web rebuild of the original Python/Tkinter QR Code Studio. The existing QR generation and OpenCV decoding concepts are retained in a FastAPI service; the desktop GUI is replaced with a responsive Next.js dark dashboard.

## Included in this implementation

- Premium responsive dark dashboard and navigation
- QR generation for URL, plain text, Wi-Fi, vCard, email and phone
- Color customization and error-correction selection
- Optional center logo embedding (uses H error correction)
- PNG and SVG download
- QR image scanning with OpenCV
- Searchable QR history, favorites and deletion
- CSV bulk QR generation with ZIP download (up to 500 rows)
- Dynamic redirect QR creation endpoint and scan counting
- PDF export endpoint
- Analytics summary
- MongoDB support when configured; SQLite fallback for local development

## Project structure

```text
qr-code-studio-web/
├── backend/
│   ├── app/main.py
│   ├── app/services/qr_service.py
│   ├── app/services/storage.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── app/
    │   ├── page.tsx
    │   ├── create/page.tsx
    │   ├── scan/page.tsx
    │   ├── history/page.tsx
    │   ├── bulk/page.tsx
    │   └── globals.css
    ├── components/shell.tsx
    ├── lib/api.ts
    └── package.json
```

## Run on Windows with VS Code

Open two VS Code terminals.

### Terminal 1 — Backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

Backend docs: http://localhost:8000/docs

### Terminal 2 — Frontend

```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Open http://localhost:3000

## MongoDB Atlas (optional)

Local development uses SQLite by default, so you can run the app immediately without creating a database account. To use MongoDB Atlas, set `MONGODB_URI` and `MONGODB_DATABASE` in `backend/.env`, then restart FastAPI. The storage adapter uses MongoDB if it can connect and falls back to SQLite if it cannot. For production, configure a persistent database and do not rely on an ephemeral local filesystem.

## Production environment

Backend `.env`:

```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>/<database>
MONGODB_DATABASE=qr_code_studio
FRONTEND_ORIGIN=https://your-frontend-domain.com
PUBLIC_BASE_URL=https://your-backend-domain.com
```

Frontend `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

Deploy frontend to Vercel and backend to Render or another Python ASGI host. Use HTTPS. Set the exact frontend origin in CORS.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/qr/generate` | Generate QR and save history |
| POST | `/api/qr/scan` | Decode uploaded QR image |
| GET | `/api/history` | List QR history |
| DELETE | `/api/history/{id}` | Delete history entry |
| PATCH | `/api/history/{id}/favorite` | Toggle favorite |
| GET | `/api/analytics` | Summary metrics |
| POST | `/api/bulk` | CSV to ZIP of PNG QR images |
| POST | `/api/qr/dynamic` | Create redirect-backed dynamic QR |
| PATCH | `/api/qr/dynamic/{code}` | Update the destination without changing the QR code |
| GET | `/r/{code}` | Redirect and increment scan count |
| POST | `/api/qr/pdf` | Create a PDF from an uploaded QR image |

## Important product limitations

- This is a functional local-first foundation, not yet a multi-tenant SaaS. Authentication, team workspaces, subscription billing, role-based access, and account isolation are not implemented.
- Dynamic QR scan analytics currently records aggregate redirect counts only. It does not collect device, location, or demographic information.
- The PDF API exports an uploaded image; the current browser UI focuses on PNG and SVG exports.
- Webcam scanning and Excel `.xlsx` batch import are not included in this first implementation; image scanning and CSV import are included.
- The optional MongoDB adapter is intentionally simple. Before public launch, add database indexes, robust connection lifecycle management, ownership fields, rate limiting, audit logging, and backups.
- Static QR codes cannot be edited or tracked after distribution. Use the dynamic redirect endpoint when you need a destination that can be changed server-side.
- Always test logo-bearing and highly customized QR codes with multiple camera apps before printing.

## Legacy project mapping

| Original desktop file | Web edition replacement |
|---|---|
| `generator.py` | `backend/app/services/qr_service.py` |
| `reader.py` | `/api/qr/scan` in `backend/app/main.py` |
| `history.json` | `backend/app/services/storage.py` |
| `app.py` | Next.js pages and `components/shell.tsx` |
| `utils.py` | `frontend/lib/api.ts` and backend storage helpers |
| `main.py` | Next.js and FastAPI entry points |

### Included web routes

- `/` — dashboard and activity overview
- `/create` — static QR creation and PNG/SVG export
- `/dynamic` — redirect-backed dynamic QR creation
- `/scan` — image-based QR decoder
- `/bulk` — CSV batch generator
- `/history` — searchable saved QR library
