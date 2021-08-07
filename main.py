import os
import ujson as json
import aiofiles

from fastapi import FastAPI
from fastapi import  FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from config import Settings

from repositories import GitlabAPI

templates = Jinja2Templates(directory='templates')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
settings = Settings()
fetcher = GitlabAPI(settings.GITLAB_GROUP)


@app.get("/api/v1/projects")
async def projects():
    raw_projects = await fetcher.projects()
    target_projects = await read_conf()

    projects = []
    for project in raw_projects:
        if project['name'] in target_projects['projects']:
            project_propperties = target_projects['projects'][project['name']]
            try:
                project['web_url'] = target_projects['hosts'][project_propperties['host']].format(
                    **project_propperties['pattern']
                )
            except KeyError:
                pass
            projects.append(project)

    return JSONResponse(projects)


@app.get("/api/v1/projects/{project_id}/latest_pipelines")
async def project_pipelines(
    project_id: int
):
    pipelines = await fetcher.pipelines(project_id)
    return JSONResponse(pipelines)


@app.get("/api/v1/projects/{project_id}/pipelines/{pipeline_id}")
async def project_pipeline(
    project_id: int,
    pipeline_id: int
):
    pipeline = await fetcher.pipeline(project_id, pipeline_id)
    return JSONResponse(pipeline)


async def read_conf():
    try:
        async with aiofiles.open(os.path.join(BASE_DIR, 'config.json'), mode='r') as f:
            contents = await f.read()
            projects = json.loads(contents)
            return projects
    except FileNotFoundError:
        raise FileNotFoundError('config.json does not exist')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
