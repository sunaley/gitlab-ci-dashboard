import aiohttp
import requests
from typing import List
from urllib.parse import urljoin
from config import get_settings
from log.log import get_logger

logger = get_logger(__file__)

Settings = get_settings()


def uurljoin(*args: List[str], **kwargs):
    _arg = args[0]
    if not args[0].endswith('/'):
        _arg += '/'
    if len(args) == 2:
        return urljoin(str(_arg), str(args[1]), **kwargs)
    if len(args) > 2:
        return uurljoin(urljoin(str(_arg), str(args[1]), **kwargs), *args[2:])


class GitlabAPI:
    API_URL = Settings.GITLAB_API_URL
    TOKEN = Settings.GITLAB_API_TOKEN

    def __init__(self, namespace: str, token: str = ''):
        self.token = token or self.TOKEN
        self.namespace = namespace
        groups = self.get_group_id()
        assert len(groups) == 1, 'Multiple groups found.'
        try:
            self.group_id = groups[0].get('id')
        except IndexError:
            raise ValueError(f'Group {self.namespace} not found.')

    def get_group_id(self):
            url = uurljoin(self.API_URL, 'groups', f'?search={self.namespace}')
            with requests.get(url, headers=self.get_headers()) as resp:
                if response := resp.json():
                    return response

    @classmethod
    def get_headers(cls):
        return {
            'PRIVATE-TOKEN': cls.TOKEN
        }

    async def projects(self):
        async with aiohttp.ClientSession() as session:
            url = uurljoin(self.API_URL, 'groups', self.group_id, 'projects')
            logger.debug(f'URL: {url}')
            async with session.get(url, headers=self.get_headers(), params={
                'pagination': 'keyset',
                'per_page': 100,
                'order_by': 'last_activity_at',
                'sort': 'desc'
            }) as resp:
                if pipelines_status := await resp.json():
                    return pipelines_status

    async def pipelines(self, project: int):
        async with aiohttp.ClientSession() as session:
            url = uurljoin(self.API_URL, 'projects', project, 'pipelines')
            async with session.get(
                url,
                headers=self.get_headers(),
                params={
                    'per_page': 1,
                    'page': 1
                }
            ) as resp:
                if pipelines_status := await resp.json():
                    return pipelines_status

    async def pipeline(self, project_id: int, pipeline_id: int):
        async with aiohttp.ClientSession() as session:
            url = uurljoin(self.API_URL, 'projects', project_id, 'pipelines', pipeline_id)
            async with session.get(
                url,
                headers=self.get_headers()
            ) as resp:
                if pipelines_status := await resp.json():
                    return pipelines_status
