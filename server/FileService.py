import os


# path = 'C:\script007\server\ForFile'

def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """


    if os.path.exists(path):
        print("Директория есть")
        pass
    else:
        print("Создали директорию ")
        autocreate = os.mkdir(path, mode=0o777)
        return autocreate

    pass


def get_files(path) -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    # Словарь
    FileInfoDict = {
        'name':"",
        'create_date':"",
        'edit_date':"",
        'size': "",
    }


    AllFiles = os.listdir(path) # получить список файлов в каталоге

    returnlist =[]

    for i in AllFiles: # проходим по всем файлам

        statinfo = os.stat(path + i) # получаем инфу по файлу

        FileInfoDict['name'] = i
        FileInfoDict['create_date'] = statinfo.st_ctime
        FileInfoDict['edit_date'] = statinfo.st_mtime
        FileInfoDict['size'] = statinfo.st_size

        returnlist.append(FileInfoDict) # добавляеем кортеж в список


    return returnlist


def get_file_data(filename: str) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """


    try:
        with open(filename, 'r') as file:
            data = file.read()

        FileInfoDict = {}
        statinfo = os.stat(filename)
        FileInfoDict['name'] = filename
        FileInfoDict['content'] = data
        FileInfoDict['create_date'] = statinfo.st_ctime
        FileInfoDict['edit_date'] = statinfo.st_mtime
        FileInfoDict['size'] = statinfo.st_size

        return FileInfoDict

    except:
        print("Файл не найден")




def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """
    try:
        with open(filename, '+r') as file:
            file.write(content)
    except:
        print("Ошибка")
        pass


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    os.remove(filename)
    print("Done!")


