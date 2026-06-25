import json
from pathlib import Path
from urllib.parse import parse_qs

from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse 
from services.recommender import Recommend

BASE_DIR = Path(__file__).resolve().parent

templates=Jinja2Templates(directory=str(BASE_DIR / "templates"))
movie_list=json.loads((BASE_DIR / "movie_list.json").read_text(encoding="utf-8"))
app=FastAPI()


@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"movies": movie_list}
)
@app.post("/recommend",response_class=HTMLResponse)
async def getrecommend(request:Request):
    form_data = parse_qs((await request.body()).decode("utf-8"))
    movie = form_data.get("movie", [""])[0]
    recommended=Recommend(movie)
    return templates.TemplateResponse(
        name="recommend.html",
        request=request,
        context={"recommend":recommended, "selected_movie": movie}
    )

