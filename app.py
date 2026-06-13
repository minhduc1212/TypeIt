import os
import json
import uuid
import docx
from pypdf import PdfReader
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

app = FastAPI(title="TypeIt - Literary Typing Practice Backend")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories for uploads and data storage
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

INDEX_FILE = os.path.join(DATA_DIR, "uploaded_docs.json")
if not os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# Default preloaded documents
DEFAULT_DOCUMENTS = [
    {
        "id": "def-1",
        "title": "The Strange Idea That Your Brain Lives in the Past",
        "author": "Scientific Essay",
        "type": "essay",
        "content": (
            "You think you live in the present. It seems like a safe bet. But in fact, you live in the past. "
            "Your brain receives information from your senses, processes it, and constructs a picture of the world. "
            "But this processing takes time. By the time your brain has processed the light entering your eyes "
            "and the sound entering your ears, the event has already happened. You are always living a fraction "
            "of a second in the past. When you watch a tennis match, or listen to someone speak, or look at a "
            "shooting star, you are experiencing history. This delay is small, but it is real. It means that "
            "our experience of 'now' is a construction, a post-hoc reconstruction of events that have already "
            "passed. We are time travelers of a very special kind, forever chasing a present that we can never "
            "quite catch."
        ),
        "bookmarked": False
    },
    {
        "id": "def-2",
        "title": "The Road Not Taken",
        "author": "Robert Frost",
        "type": "poem",
        "content": (
            "Two roads diverged in a yellow wood,\n"
            "And sorry I could not travel both\n"
            "And be one traveler, long I stood\n"
            "And look'd down one as far as I could\n"
            "To where it bent in the undergrowth;\n\n"
            "Then took the other, as just as fair,\n"
            "And having perhaps the better claim,\n"
            "Because it was grassy and wanted wear;\n"
            "Though as for that the passing there\n"
            "Had worn them really about the same,\n\n"
            "And both that morning equally lay\n"
            "In leaves no step had trodden black.\n"
            "Oh, I kept the first for another day!\n"
            "Yet knowing how way leads on to way,\n"
            "I doubted if I should ever come back.\n\n"
            "I shall be telling this with a sigh\n"
            "Somewhere ages and ages hence:\n"
            "Two roads diverged in a wood, and I—\n"
            "I took the one less traveled by,\n"
            "And that has made all the difference."
        ),
        "bookmarked": False
    },
    {
        "id": "def-3",
        "title": "A Scandal in Bohemia (Excerpt)",
        "author": "Arthur Conan Doyle",
        "type": "novel",
        "content": (
            "To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name. "
            "In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion "
            "akin to love for Irene Adler. All emotions, and that one particularly, were abhorrent to his cold, "
            "precise but admirably balanced mind. He was, I take it, the most perfect reasoning and observing "
            "machine that the world has seen, but as a lover he would have placed himself in a false position. "
            "He never spoke of the softer passions, save with a gibe and a sneer. They were admirable things for "
            "the observer—excellent for drawing the veil from men's motives and actions. But for the trained "
            "reasoner to admit such intrusions into his own delicate and finely adjusted temperament was to "
            "introduce a distracting factor which might throw a doubt upon all his mental results. Grit in a "
            "sensitive instrument, or a crack in one of his own high-power lenses, would not be more disturbing "
            "than a strong emotion in a nature such as his."
        ),
        "bookmarked": False
    },
    {
        "id": "def-4",
        "title": "Nam Quốc Sơn Hà",
        "author": "Lý Thường Kiệt",
        "type": "poem",
        "content": (
            "Nam quốc sơn hà Nam đế cư\n"
            "Tiệt nhiên định phận tại thiên thư\n"
            "Như hà nghịch lỗ lai xâm phạm\n"
            "Nhữ đẳng hành khan thủ bại hư."
        ),
        "bookmarked": False
    },
    {
        "id": "def-5",
        "title": "Tôi đi học (Trích)",
        "author": "Thanh Tịnh",
        "type": "essay",
        "content": (
            "Hằng năm cứ vào cuối thu, lá ngoài đường rụng nhiều và trên không có những đám mây bàng bạc, "
            "lòng tôi lại nao nức những kỷ niệm hoang mang của buổi tựu trường. Tôi không thể nào quên được "
            "những cảm giác trong sáng ấy nảy nở trong lòng tôi như mấy cành hoa tươi mỉm cười giữa bầu trời quang đãng. "
            "Buổi mai hôm ấy, một buổi mai đầy sương thu và gió lạnh. Mẹ tôi âu yếm nắm tay tôi dẫn đi trên "
            "con đường làng dài và hẹp. Con đường này tôi đã đi lại nhiều lần, nhưng lần này tự nhiên tôi thấy lạ. "
            "Cảnh vật chung quanh tôi đều thay đổi, vì chính lòng tôi đang có sự thay đổi lớn: Hôm nay tôi đi học."
        ),
        "bookmarked": False
    }
]

def load_uploaded_docs() -> List[Dict[str, Any]]:
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_uploaded_docs(docs: List[Dict[str, Any]]):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

def get_doc_stats(content: str) -> tuple[int, int]:
    # Returns (char_count, word_count)
    char_count = len(content)
    # Simple word counting by splitting on whitespace
    word_count = len(content.split())
    return char_count, word_count

@app.get("/api/documents")
def get_documents():
    uploaded = load_uploaded_docs()
    all_docs = []
    
    # Preloaded docs first
    for doc in DEFAULT_DOCUMENTS:
        char_cnt, word_cnt = get_doc_stats(doc["content"])
        all_docs.append({
            "id": doc["id"],
            "title": doc["title"],
            "author": doc["author"],
            "type": doc["type"],
            "char_count": char_cnt,
            "word_count": word_cnt,
            "bookmarked": doc["bookmarked"]
        })
        
    # Uploaded docs next
    for doc in uploaded:
        char_cnt, word_cnt = get_doc_stats(doc["content"])
        all_docs.append({
            "id": doc["id"],
            "title": doc["title"],
            "author": doc.get("author", "Uploaded Document"),
            "type": "uploaded",
            "char_count": char_cnt,
            "word_count": word_cnt,
            "bookmarked": doc.get("bookmarked", False)
        })
        
    return all_docs

@app.get("/api/documents/{doc_id}")
def get_document(doc_id: str):
    # Search in defaults
    for doc in DEFAULT_DOCUMENTS:
        if doc["id"] == doc_id:
            char_cnt, word_cnt = get_doc_stats(doc["content"])
            return {
                **doc,
                "char_count": char_cnt,
                "word_count": word_cnt
            }
            
    # Search in uploaded
    uploaded = load_uploaded_docs()
    for doc in uploaded:
        if doc["id"] == doc_id:
            char_cnt, word_cnt = get_doc_stats(doc["content"])
            return {
                **doc,
                "char_count": char_cnt,
                "word_count": word_cnt
            }
            
    raise HTTPException(status_code=404, detail="Document not found")

@app.post("/api/documents/toggle-bookmark/{doc_id}")
def toggle_bookmark(doc_id: str):
    # If default doc
    for doc in DEFAULT_DOCUMENTS:
        if doc["id"] == doc_id:
            doc["bookmarked"] = not doc["bookmarked"]
            return {"id": doc_id, "bookmarked": doc["bookmarked"]}
            
    # If uploaded doc
    uploaded = load_uploaded_docs()
    for doc in uploaded:
        if doc["id"] == doc_id:
            doc["bookmarked"] = not doc.get("bookmarked", False)
            save_uploaded_docs(uploaded)
            return {"id": doc_id, "bookmarked": doc["bookmarked"]}
            
    raise HTTPException(status_code=404, detail="Document not found")

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(None),
    author: str = Form(None)
):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in [".txt", ".docx", ".pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Supported formats: .txt, .docx, .pdf")
        
    content = ""
    file_bytes = await file.read()
    
    try:
        if ext == ".txt":
            # Try utf-8 then latin-1
            try:
                content = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                content = file_bytes.decode("latin-1")
        elif ext == ".docx":
            # We need to save temporary or use BytesIO
            import io
            doc_file = io.BytesIO(file_bytes)
            doc_obj = docx.Document(doc_file)
            content = "\n".join([p.text for p in doc_obj.paragraphs])
        elif ext == ".pdf":
            import io
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            pages_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            content = "\n".join(pages_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
        
    if not content.strip():
        raise HTTPException(status_code=400, detail="The file is empty or no readable text was extracted.")
        
    # Standardize whitespace and line endings slightly but preserve paragraph structure
    # For nice display, replace multiple consecutive newlines with a double newline, and normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    
    doc_id = str(uuid.uuid4())
    doc_title = title or os.path.splitext(filename)[0]
    doc_author = author or "Unknown"
    
    # Save the file physical copy in uploads folder
    save_path = os.path.join(UPLOADS_DIR, f"{doc_id}{ext}")
    with open(save_path, "wb") as f:
        f.write(file_bytes)
        
    # Add to index
    uploaded = load_uploaded_docs()
    new_doc = {
        "id": doc_id,
        "title": doc_title,
        "author": doc_author,
        "type": "uploaded",
        "content": content,
        "bookmarked": False,
        "filename": filename,
        "path": save_path
    }
    uploaded.append(new_doc)
    save_uploaded_docs(uploaded)
    
    char_cnt, word_cnt = get_doc_stats(content)
    return {
        "id": doc_id,
        "title": doc_title,
        "author": doc_author,
        "type": "uploaded",
        "char_count": char_cnt,
        "word_count": word_cnt,
        "bookmarked": False
    }

@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: str):
    # Can only delete uploaded documents
    uploaded = load_uploaded_docs()
    for i, doc in enumerate(uploaded):
        if doc["id"] == doc_id:
            # Delete physical file
            path = doc.get("path")
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
            # Remove from index
            uploaded.pop(i)
            save_uploaded_docs(uploaded)
            return {"status": "success", "message": "Document deleted"}
            
    raise HTTPException(status_code=404, detail="Uploaded document not found or cannot be deleted")

# Serve Vue Frontend compiled files
DIST_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "frontend", "dist"))
assets_dir = os.path.join(DIST_DIR, "assets")
os.makedirs(assets_dir, exist_ok=True)

# Mount static assets directory
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/{fallback_path:path}")
def serve_frontend(fallback_path: str):
    # If API call, return 404 instead of serving HTML
    if fallback_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
        
    # Check if file exists in dist
    file_path = os.path.normpath(os.path.join(DIST_DIR, fallback_path))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
        
    # Otherwise serve index.html (SPA fallback)
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
        
    # If frontend is not built yet
    return {"message": "Backend is running. Please build the frontend (npm run build) to serve it."}
