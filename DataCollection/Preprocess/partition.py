import os
from os import path
import os.path
import re
import random
import shutil
import time
import csv


def get_path_names():
    directory = '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Images'
    newpath = '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/ImagesDuplicate'

    print(f'{time.ctime()}: Duplicating image set.')
    shutil.copytree(directory, newpath)

    images = []
    for i in os.listdir(newpath):
        print(f'{time.ctime()}: Get path name for {i}.')
        images.append([os.path.join(newpath, i), *re.findall('^[a-zA-Z]+', i)])
    random.shuffle(images)
    return images


def separate(images, output_path):
    for p, name in images:
        print(f'{time.ctime()}: Relocating {p}.')
        out = f'{output_path}/{name}'
        if not path.isdir(out):
            os.makedirs(out)
        shutil.move(p, f'{output_path}/{name}')


def remove_excess(output_path):
    tmp = sorted(os.listdir(output_path))
    for f in tmp:
        print(f'{time.ctime()}: Removing excess data.')
        p = os.path.join(output_path, f)
        if len(os.listdir(p)) < 50:
            shutil.move(p, '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Remainder')


def consolidate(pathname, newpath):
    if not path.isdir(newpath):
        os.makedirs(newpath)
    newpath = os.path.join(pathname, newpath)

    for f in sorted(os.listdir(pathname)):
        print(f'{time.ctime()}: Consolidating cleaned data.')
        p = os.path.join(pathname, f)
        if len(os.listdir(p)) > 0:
            for i in range(len(os.listdir(p))):
                if path.isfile(os.path.join(p, f+f'{i}'+'.jpeg')):
                    pass
                    shutil.copyfile((os.path.join(p, f+f'{i}'+'.jpeg')), newpath+'/'+f+f'{i}'+'.jpeg')


def split(input, output):
    if not path.isdir(output):
        os.makedirs(output)
        os.makedirs(f'{output}/X_train')
        os.makedirs(f'{output}/X_test')
        os.makedirs(f'{output}/X_valid')
    images = [img for img in os.listdir(input)]

    random.shuffle(images)

    split_train = int(len(images)*.65)
    split_valid = split_train + int(len(images)*.2)

    names_train = []
    names_valid = []
    names_test = []

    for i, img in enumerate(images):
        pathname = f'{input}/{img}'
        if i < split_train:
            print(f'{time.ctime()}: Adding {img} to train dataset.')
            names_train.append(*re.findall('^[a-zA-Z]+', img))
            shutil.move(pathname, f'{output}/X_train')
        elif split_train <= i < split_valid:
            print(f'{time.ctime()}: Adding {img} to validation dataset.')
            names_valid.append(*re.findall('^[a-zA-Z]+', img))
            shutil.move(pathname, f'{output}/X_valid')
        elif i >= split_valid:
            print(f'{time.ctime()}: Adding {img} to test dataset.')
            names_test.append(*re.findall('^[a-zA-Z]+', img))
            shutil.move(pathname, f'{output}/X_test')

        with open(f'{output}/y_test.csv', 'a') as w:
            writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in names_test:
                writer.writerow([line])
        with open(f'{output}/y_valid.csv', 'a') as w:
            writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in names_valid:
                writer.writerow([line])
        with open(f'{output}/y_train.csv', 'a') as w:
            writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in names_train:
                writer.writerow([line])


def get_classes(input_dir):
    names = []
    print(f'{time.ctime()}: Locating class distinctions for data.')
    for x in os.listdir(input_dir):
        names.extend(re.findall('^[a-zA-Z]+', x))

    with open('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/datasets/classes.csv', 'a') as w:
        writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(set(names)):
            writer.writerow([item])


def main():
    # keep track of program runtime
    print(f'{time.ctime()}: Begin data preprocessing.')
    start_time = time.time()

    output_path = '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Intermediate'
    if not path.isdir(output_path):
        os.makedirs(output_path)

    separate(get_path_names(), output_path)
    remove_excess(output_path)
    consolidate(output_path, '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Consolidated')
    get_classes('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Consolidated')
    split('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Consolidated',
          '/Users/nathalieredick/Workspaces/MAIS202/DataCollection/datasets')

    print(f'{time.ctime()}: Removing redundant directories and data.')
    shutil.rmtree('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Remainder')
    shutil.rmtree('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Intermediate')
    shutil.rmtree('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/ImagesDuplicate')
    shutil.rmtree('/Users/nathalieredick/Workspaces/MAIS202/DataCollection/output_files/Consolidated')

    print(f'{time.ctime()}: Preprocessing completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == '__main__':
    main()
