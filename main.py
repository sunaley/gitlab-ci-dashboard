import os
import ujson as json
import asyncio
import aiofiles

from functools import lru_cache

from fastapi import FastAPI
from fastapi import Depends, FastAPI
from fastapi_versioning import VersionedFastAPI, version
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from config import Settings

from repositories import GitlabAPI

templates = Jinja2Templates(directory='templates')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
settings = Settings()
fetcher = GitlabAPI(settings.GITLAB_GROUP)


@app.get("/")
async def root(
    request: Request,
):
    raw_projects = await fetcher.projects()
    target_projects = await read_conf()
    projects = []
    tasks = []

    for project in raw_projects:
        if project['name'] in target_projects['projects']:
            tasks.append(fetcher.pipelines(project['id']))
            project_propperties = target_projects['projects'][project['name']]
            project['web_url'] = target_projects['hosts'][project_propperties['host']].format(
                **project_propperties['pattern']
            )
            projects.append(project)

    responses = await asyncio.gather(*tasks)
    for idx, project in enumerate(projects):
        project['latest_pipeline'] = responses[idx][0] if responses[idx] else {}

    return templates.TemplateResponse('index.html', {
        'request': request,
        'projects': projects
    })


async def read_conf():
    try:
        async with aiofiles.open(os.path.join(BASE_DIR, 'config.json'), mode='r') as f:
            contents = await f.read()
            projects = json.loads(contents)
            return projects
    except FileNotFoundError:
        raise FileNotFoundError('config.json does not exist')


# app = VersionedFastAPI(app,
#     version_format='{major}',
#     prefix_format='/v{major}')
