import os
import shutil
import pathlib
import tempfile
import datetime
import collections
import zipfile

RESULTS_FOLDERS = ("images", "video", "documents", "audio", "archives", "unknown")


def normalize(name):
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'є': 'je', 'і': 'i', 'ї': 'ji', 'ґ': 'g'
    }
    
    result = ''.join(transliteration_dict.get(char, char) for char in name)
    result = ''.join([c if c.isalpha() or c.isdigit() or c == '.' else '_' for c in result])
    return result


def process_dir(result_path, element, extensions_info):
    res = False

    if element.name not in RESULTS_FOLDERS:
        folder_res = diver(result_path, element, extensions_info)

        if folder_res is False:
            element.rmdir()

        res |= folder_res

    return res



def process_file(result_path, element, extensions_info):

    table = (
        ('JPEG', 'PNG', 'JPG', 'SVG'),
        ('AVI', 'MP4', 'MOV', 'MKV'),
        ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        ('MP3', 'OGG', 'WAV', 'AMR'),
        ('ZIP', 'GZ', 'TAR')
    )

    suffixes_dict = {
        table[i][j]: RESULTS_FOLDERS[i]
        for i in range(len(table))
        for j in range(len(table[i]))
    }

    suffix = element.suffix[1:].upper()

    known = suffixes_dict.get(suffix) is not None

    dest_folder = suffixes_dict.get(suffix, 'unknown')
    result_path /= dest_folder

    if not result_path.is_dir():
        result_path.mkdir(parents=True)  # Створення всіх батьківських папок, якщо вони не існують

    extensions_info["known" if known else "unknown"].add(suffix)

    if dest_folder == "archives":
        result_path /= normalize(f"{element.stem}{element.suffix}") #!

        if known:
            # Перевірка, чи файл є архівом
            if element.suffix[1:].lower() in ('zip', 'gz', 'tar'):
                try:
                    with zipfile.ZipFile(str(element), 'r') as zip_ref:
                        zip_ref.extractall(str(result_path))
                except zipfile.BadZipFile:
                    print(f"Error: {element} is not a valid zip file. Deleting...")
                    element.unlink()  # Видалення невалідного архіву
                    pass
            else:
                shutil.copy(str(element), str(result_path))
    else:
        result_path /= f"{normalize(element.stem)}{element.suffix}" #!

        if known:
            shutil.copy(str(element), str(result_path))
        else:
            # Додавання невідомих розширень в окрему папку
            unknown_folder = result_path / "unknown"
            if not unknown_folder.is_dir():
                unknown_folder.mkdir(parents=True)
            shutil.copy(str(element), str(unknown_folder / f"unknown_{normalize(element.name)}")) #!

    return True

# ...


def diver(result_path, folder_path, extensions_info):
    res = False

    if not any(folder_path.iterdir()):
        return res

    for element in folder_path.iterdir():
        processor = process_dir if element.is_dir() else process_file
        res |= processor(result_path, element, extensions_info)

    return res


def post_processor(results_path, extensions_info):
    print(f"Known extensions: {extensions_info['known']}")
    if len(extensions_info['unknown']):
        print(f"Unknown extensions: {extensions_info['unknown']}")

    for folder in results_path.iterdir():
        print(f"{folder.name}:")
        for item in folder.iterdir():
            print(f"\t{item.name}")


def sorter(folder_platform_path):
    extensions_info = collections.defaultdict(set)
    folder_path = pathlib.Path(folder_platform_path)
    # folder_path = pathlib.Path(folder_platform_path[0])
    if not folder_path.is_dir():
        raise RuntimeError("error: no such directory")

    with tempfile.TemporaryDirectory() as tmp_platform_path:
        tmp_path = pathlib.Path(tmp_platform_path)

        if diver(tmp_path, folder_path, extensions_info) is False:
            raise RuntimeError("It's empty directory")

        os.makedirs("results", exist_ok=True)

        results_path = pathlib.Path(
            "results/"
            f"result_{datetime.datetime.now().strftime('%d.%m.%y_%H_%M_%S')}"
        )

        shutil.copytree(
            str(tmp_path),
            str(results_path)
        )

    post_processor(results_path, extensions_info)

def sorter_interaction():
    user_input = input(str("Enter path to folder: "))
    if user_input:
        try:
            sorter(user_input)
        except RuntimeError as e:
            print(e)
    else:
        print("No path was specified")
            

# if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     raise RuntimeError(f"usage: {sys.argv[0]} folder_platform_path")

    # sorter(sys.argv[1])

