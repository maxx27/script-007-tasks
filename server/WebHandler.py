import json
import os.path

from aiohttp import web

import server.FileService as FileService
import utils.StrUtils
import utils.Config


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self) -> None:
        FileService.change_dir(utils.Config.data.dir,
                               utils.Config.data.autocreate)

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        return WebHandler._get_json_response({
            'status': 'success',
        })

    async def change_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        payload = ''
        stream = request.content
        while not stream.at_eof():
            line = await stream.read()
            payload += line.decode()

        data = json.loads(payload)
        path = data.get('path')

        try:
            new_path = os.path.join(utils.Config.data.dir, path)
            FileService.change_dir(new_path, utils.Config.data.autocreate)
            return WebHandler._get_json_response({
                'status': 'success',
            })
        except (RuntimeError, ValueError) as err:
            data = {
                'status': 'error',
                'message': str(err),
            }
            raise web.HTTPBadRequest(text=utils.StrUtils.to_json(data))

    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """

        files = FileService.get_files()
        return WebHandler._get_json_response({
            'status': 'success',
            'data': files,
        })

    async def get_file_data(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        if (filename := request.match_info.get('filename')) is None:
            raise web.HTTPBadRequest(text="No filename specified")

        try:
            filedata = FileService.get_file_data(filename)
            return WebHandler._get_json_response({
                'status': 'success',
                'data': filedata,
            })
        except (RuntimeError, ValueError) as err:
            data = {
                'status': 'error',
                'message': str(err),
            }
            raise web.HTTPBadRequest(text=utils.StrUtils.to_json(data))

    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        payload = ''
        stream = request.content
        while not stream.at_eof():
            line = await stream.read()
            payload += line.decode()

        try:
            data = json.loads(payload)
            filename = data.get('filename')
            content = utils.StrUtils.str2bytes(data.get('content'))

            FileService.create_file(filename, content)
            return WebHandler._get_json_response({
                'status': 'success',
                # TODO: Add resource link
            })
        except json.JSONDecodeError as err:
            raise web.HTTPBadRequest(text=f"cannot parse json: {str(err)}")
        except (RuntimeError, ValueError) as err:
            data = {
                'status': 'error',
                'message': str(err),
            }
            raise web.HTTPBadRequest(text=utils.StrUtils.to_json(data))

    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        if (filename := request.match_info.get('filename')) is None:
            raise web.HTTPBadRequest(text="No filename specified")

        try:
            FileService.delete_file(filename)
            return WebHandler._get_json_response({
                'status': 'success',
            })
        except (RuntimeError, ValueError) as err:
            data = {
                'status': 'error',
                'message': str(err),
            }
            raise web.HTTPBadRequest(text=utils.StrUtils.to_json(data))

    @staticmethod
    def _get_json_response(data: dict) -> web.Response:
        return web.json_response(data=data, dumps=utils.StrUtils.to_json)


def get_aiohttp_server():
    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/change_dir', handler.change_dir),
        web.get('/files', handler.get_files),
        web.get('/files/{filename}', handler.get_file_data),
        web.post('/files', handler.create_file),
        web.delete('/files/{filename}', handler.delete_file),
    ])
    return app
