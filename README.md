# 📖 TypeIt - Literary Typing Practice

**TypeIt** is a flat, ultra-minimalist, distraction-free web application designed to practice 10-finger typing by typing works of literature, including classic essays, novels, and poetry. It also supports uploading personal documents so you can practice typing any text you want.

---

## ✨ Features

- **Distraction-Free Practice**: Ultra-minimalist interface with no visible input boxes. Type directly over the text body with active cursor highlighting.
- **Typographic & Custom Styles**: Adjust text formatting inside the settings panel:
  - **Fonts**: *Lora*, *Merriweather*, *Crimson Pro*, or *Literata*.
  - **Font Size**: 18px to 30px.
  - **Line Height**: Relaxed spacing (1.6 to 2.2) to give lines breathing room.
- **Real-Time Keyboard Sounds**: Low-latency typing sounds synthesized directly offline using the browser's Web Audio API (no external file downloads required).
  - **7 Sound Profiles**: *Mechanical Tactile*, *Clicky Blue Switch*, *Linear Red Thock*, *Laptop Chiclet*, *Vintage Typewriter*, *Wood Block*, and *Digital Beep*.
  - **Configurable**: Toggle sound effects or mute error sounds in settings.
- **Custom Document Uploads**: Drag and drop or browse to upload your own files:
  - **Plain Text (`.txt`)**: Normalized encodings.
  - **Word Documents (`.docx`)**: Auto-extracted paragraphs.
  - **PDF Documents (`.pdf`)**: Extracted text pages.
- **Bookmark / Favorite System**: Easily save your favorite essays or poems to practice them later.
- **Comprehensive Real-Time Stats**: Tracks speed (WPM), Accuracy, Progress, and Time. A completion modal displays detailed metrics upon finishing a text.

---

## 🛠️ Tech Stack

- **Backend**:
  - [FastAPI](https://fastapi.tiangolo.com/) - Web framework.
  - [Uvicorn](https://www.uvicorn.org/) - ASGI web server.
  - `python-docx` & `pypdf` - Document parsers.
- **Frontend**:
  - [Vue 3](https://vuejs.org/) - Reactive component framework.
  - [Vite](https://vite.dev/) - Build tool and dev server.
  - Vanilla CSS - Flat minimalist styling (no heavy shadows/gradients).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm

### 1. Installation

Clone or navigate to the project directory and install the backend packages:
```bash
# Create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Install the frontend packages and compile the production build:
```bash
# Navigate to frontend folder
cd frontend

# Install npm packages
npm install

# Build compiled assets
npm run build

# Return to root directory
cd ..
```

### 2. Running the Application

Start the FastAPI backend server:
```bash
.venv\Scripts\uvicorn app:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000`** in your browser to start typing!

---

## 💻 Development Mode

To modify the codebase, you can run the backend and frontend dev servers concurrently:

1. **Start Backend Server**:
   ```bash
   .venv\Scripts\uvicorn app:app --reload
   ```
   The backend will watch for python file changes and reload on port 8000.

2. **Start Frontend Dev Server**:
   ```bash
   cd frontend
   npm run dev
   ```
   The Vite dev server will start on port 5173. Requests to `/api/*` are automatically proxied to the backend server on port 8000 (configured in `vite.config.js`). Access the live reloads at `http://localhost:5173/`.
