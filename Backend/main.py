from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse 
from services.recommender import Recommend
import pickle
import requests

templates=Jinja2Templates(directory="templates")
movie_list=pickle.load(open("movie_list.pkl","rb"))
movie_list=movie_list.tolist()
app=FastAPI()


@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"movies": movie_list}
)
@app.post("/recommend",response_class=HTMLResponse)
def getrecommend(request:Request,movie:str =Form(...)):
    recommended=Recommend(movie)
    return templates.TemplateResponse(
        name="recommend.html",
        request=request,
        context={"recommend":recommended}
    )

