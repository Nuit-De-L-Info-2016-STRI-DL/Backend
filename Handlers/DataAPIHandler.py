# -*- coding: utf-8 -*-

import os
import tornado.web
from zipfile import ZipFile
from tools import ListingFiles

folder_path = 'data/'
zip_file = './export.zip'


def list_all_export_file():
    """
    Make a list of important 'data' files (important files to export).

    :return: important file list
    """
    temp = list_high_level_files()
    return temp


def list_high_level_files():
    return [os.path.normpath(os.path.join(folder_path, file))
            for file in ListingFiles.list_file_root_folder(folder_path)
            if file.endswith('.json')]


def create_zip(file_list: list):
    """
    Create a zip from list_export_file() returned file list.
    """
    with ZipFile(zip_file, 'w') as myzip:
        for file in file_list:
            myzip.write(file, arcname=file[len(folder_path):])


class DataAPIHandler(tornado.web.RequestHandler):
    """
    Class to handle '/data' endpoint.
    """

    def get(self, path_request):
        """
        Handle GET requests.

        :param path_request: request path ( < URI)
        """
        if path_request == 'all_export.zip':
            create_zip(list_all_export_file())
            with open(zip_file, mode='rb') as file:
                c = file.read()
                self.set_header('content-type', 'application/zip')
                self.write(c)
        else:
            self.send_error(status_code=400, reason='bad request')
        return

    def post(self, path_request):
        """
        Handle POST requests.

        :param path_request: request path ( < URI)
        """
        if path_request == 'import.zip':
            try:
                fileinfo = self.request.files['file'][0]
                # fname = fileinfo['filename']  # le nom du fichier recu
                with open(os.path.join(folder_path, 'imported.zip'), 'wb') as fh:
                    fh.write(fileinfo['body'])
                zip_2_extract = ZipFile(os.path.join(folder_path, 'imported.zip'), 'r')
                zip_2_extract.extractall(folder_path)
                zip_2_extract.close()
                os.remove(os.path.join(folder_path, 'imported.zip'))
            except KeyError:  # pas 'file' comme nom dans le formulaire pour le fichier recu
                self.send_error(status_code=400, reason='bad request')
        else:
            self.send_error(status_code=400, reason='bad request')
        return
