import os
import pathlib
import shutil


def main():
    path_to_factorio_saves = get_path_to_factorio_saves()
    list_of_factorio_saves = get_list_of_saves_from_(path_to_factorio_saves)
    path_to_backup_location = get_path_to_backup_location()
    copy_to_backup_location_(path_to_backup_location, list_of_factorio_saves)


def get_path_to_factorio_saves():
    appdata = os.getenv('APPDATA')
    return pathlib.Path(appdata, 'Factorio', 'saves')


def get_list_of_saves_from_(path_to_factorio_saves):
    if not os.path.exists(path_to_factorio_saves):
        print(f'path {path_to_factorio_saves} not exist')
        exit()
    list_of_factorio_saves = list()
    for root, dirs, files in os.walk(path_to_factorio_saves):
        for file in files:
            if is_a_save_(file):
                list_of_factorio_saves.append(pathlib.Path(root, file))
    return list_of_factorio_saves


def is_a_save_(file):
    file_ext = file.split('.')[-1]
    if 'zip' in file_ext:
        return True
    return False


def copy_to_backup_location_(backup_location, list_of_factorio_saves):
    for factorio_save in list_of_factorio_saves:
        if destination_contains_save(destination=backup_location,
                                     save=factorio_save):
            print(f'already backed up, skipping {factorio_save}..')
            continue  # already backed up
        backup_save = build_path_to_(backup_location, factorio_save)
        print(f'new file found, backing up {factorio_save}')
        shutil.copy(src=factorio_save,
                    dst=backup_save)


def destination_contains_save(destination, save):
    for root, dirs, files in os.walk(destination):
        for file in files:
            if save.name in file:
                return True
    return False


def build_path_to_(backup_location, factorio_save):
    return pathlib.Path(backup_location, factorio_save.name)


def get_path_to_backup_location():
    home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    backup_location = pathlib.Path(home, 'OneDrive', 'Factorio', 'saves_backup')
    if not os.path.exists(backup_location):
        print(f'backup location {backup_location} does not exist')
        exit()
    return backup_location


if __name__ == '__main__':
    main()
