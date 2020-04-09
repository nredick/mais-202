import os
from os import path
import os.path
import re
import random
import shutil
import time
import csv
from PIL import Image, UnidentifiedImageError, ImageChops


def resize(dirs):
    for p, name in dirs:
        if os.path.isfile(p):
            try:
                im = Image.open(p)
                resized = im.resize((128, 128), Image.ANTIALIAS)
                resized.save(p, 'JPEG', quality=300)
                print(f'{time.ctime()}: Resizing {p}.')
            except UnidentifiedImageError:
                out = '../output_files/Remainder'
                if not path.isdir(out):
                    os.makedirs(out)
                print(f'{time.ctime()}: UnidentifiedImageError --> deleting {name}')
                os.remove(p)


def duplicate(input, output):
    print(f'{time.ctime()}: Duplicating image set.')
    shutil.copytree(input, output)


def get_path_names(input):
    images = []
    for i in os.listdir(input):
        print(f'{time.ctime()}: Get path name for {i}.')
        name = re.findall('^[a-zA-Z]+', i)
        if len(name) > 0:
            images.append([os.path.join(input, i), *re.findall('^[a-zA-Z]+', i)])
    random.shuffle(images)
    return images


def separate(images, output_path):
    if not path.isdir(output_path):
        os.makedirs(output_path)
    print(images)

    for p, name in images:
        print(f'{time.ctime()}: Relocating {p}.')
        out = f'{output_path}/{name}'
        if not path.isdir(out):
            os.makedirs(out)
        shutil.move(p, out)


def remove_excess(output_path):
    tmp = sorted(os.listdir(output_path))  #INTERMEDIATE
    for f in tmp:
        print(f'{time.ctime()}: Removing excess data.')
        p = os.path.join(output_path, f)
        if len(os.listdir(p)) < 50:
            shutil.move(p, '../output_files/Remainder')


def consolidate(pathname, new_path):
    if not path.isdir(new_path):
        os.makedirs(new_path)

    for f in sorted(os.listdir(pathname)):
        print(f'{time.ctime()}: Consolidating cleaned data.')
        p = os.path.join(pathname, f)
        if len(os.listdir(p)) > 0:
            for i, img in enumerate(os.listdir(p)):
                if path.isfile(os.path.join(p, img)):
                    shutil.copyfile(os.path.join(p, img), os.path.join(new_path, img))


def split(input, output):
    if not path.isdir(f'{output}/X_train'):
        os.makedirs(f'{output}/X_train')
    if not path.isdir(f'{output}/X_test'):
        os.makedirs(f'{output}/X_test')

    images = [img for img in os.listdir(input)]

    random.shuffle(images)

    split_train = int(len(images) * .85)

    names_train = []
    names_test = []

    for i, img in enumerate(images):
        print(i, img)
        pathname = f'{input}/{img}'
        if i < split_train:
            print(f'{time.ctime()}: Adding {img} to train dataset.')
            names_train.append(*re.findall('^[a-zA-Z]+', img))
            shutil.move(pathname, f'{output}/X_train')

        elif i >= split_train:
            print(f'{time.ctime()}: Adding {img} to test dataset.')
            names_test.append(*re.findall('^[a-zA-Z]+', img))
            shutil.move(pathname, f'{output}/X_test')



def get_classes(input_dir, output):
    if not path.isdir(f'{output}'):
        os.makedirs(f'{output}')
    names = []
    print(f'{time.ctime()}: Locating class distinctions for data.')
    for x in os.listdir(input_dir):
        names.extend(re.findall('^[a-zA-Z]+', x))

    with open(f'{output}/classes.csv', 'a') as w:
        writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in sorted(set(names)):
            writer.writerow([item])


def main():
    # keep track of program runtime
    print(f'{time.ctime()}: Begin data preprocessing.')
    start_time = time.time()

    input = '../output_files/images_2.0'
    output = '../output_files/ImagesDuplicate'

    duplicate(input, output)
    images = get_path_names(output)
    resize(images)

    try:
        os.system(f'image-cleaner {output}')
    except FileNotFoundError:
        pass

    images = get_path_names(output)
    separate(images, '../output_files/Intermediate')
    #remove_excess('../output_files/Intermediate')
    consolidate('../output_files/Intermediate', '../output_files/Consolidated')
    get_classes('../output_files/Consolidated', '../datasets3')
    split('../output_files/Consolidated', '../datasets3')

    print(f'{time.ctime()}: Removing redundant directories and data.')
    shutil.rmtree('../output_files/Remainder')
    shutil.rmtree('../output_files/Intermediate')
    shutil.rmtree('../output_files/ImagesDuplicate')
    shutil.rmtree('../output_files/Consolidated')

    print(f'{time.ctime()}: Preprocessing completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == '__main__':
    main()
