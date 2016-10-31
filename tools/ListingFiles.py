# -*- coding: utf-8 -*-

import os


def list_file_root_folder(folder_path: str = '.'):
    """
    List files from a folder

    :param folder_path: folder to list from
    :return: listed files (and sorted)
    """
    return sorted([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
