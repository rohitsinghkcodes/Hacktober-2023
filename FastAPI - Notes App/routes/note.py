from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from fastapi.responses import JSONResponse

note = APIRouter()
templates = Jinja2Templates(directory="templates")

# Home route
@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id" : doc["_id"],
            "title": doc["title"],
            "desc":doc["desc"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


# # get all notes route
@note.get("/get_all_notes")
async def get_all(request: Request):
    doc = conn.notes.notes.find({})
    return doc


# abouut page route
@note.get("/about", response_class=HTMLResponse)
async def display_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# add notes to db
@note.post("/")
async def add_note(request: Request):
    form = await request.form()
    note = conn.notes.notes.insert_one(dict(form))
    return {"msg": "Note has been added successfully."}
