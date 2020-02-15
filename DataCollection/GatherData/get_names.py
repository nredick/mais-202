import csv
import time
import threading
from multiprocessing import JoinableQueue


def parse_lines(FILE):
    data = []
    common = ['quartz', 'jade', 'opal', 'calcite', 'rhodonite', 'pearl', 'garnet', 'elbaite', 'feldspar',
              'pyroxene', 'mica', 'andesite', 'grossular', 'almandine', 'almandite', 'apatite', 'lazurite',
              'beryl', 'diamond', 'topaz', 'malachite', 'galena', 'sphalerite', 'acanthite', 'heulandite',
              'natrolite', 'thomsonite', 'penninite', 'azurite', 'pyrite', 'chalcocite', 'hematite', 'millerite',
              'copper', 'lead', 'argentite', 'wolframite', 'tantalite', 'apophyllite', 'wulfenite',
              'natrolite', 'schorl', 'chabazite', 'stilbite', 'muscovite', 'palermoite', 'goedkonite', 'chlorite',
              'titanite', 'albite', 'dolomite', 'cinnabar', 'moschellandsbergite', 'goethite', 'cubanite',
              'enargite', 'smithsonite', 'sphorite', 'breccia', 'fluorite', 'chlorite', 'rhodochrosite', 'stilbite',
              'chabazite', 'cuprosklodowskite', 'dyscrasite', 'orthoclase', 'clinochlore', 'granite',
              'corundum', 'fergusonite', 'gadolinite', 'willemite', 'shattuckite', 'hemimorphite', 'actinolite',
              'cervantite', 'montecellite', 'vesuvianite', 'serpentine', 'clintonite', 'chromite', 'bronchantite',
              'aragonite', 'diopside', 'magnetite', 'lorenzenite', 'crocoite', 'chalcite', 'wernerite',
              'antigorite', 'olivine', 'basalt', 'fossil', 'concretion', 'sulfur', 'chalcedony', 'tuff', 'biotite',
              'forsterite', 'spodumene', 'xenolith', 'lapilli', 'sepiolite', 'banakite', 'shoshonite', 'zoisite',
              'diogenite', 'gabbro', 'pegmatite', 'spinel', 'chert', 'limestone', 'conglomerate', 'gold', 'shale',
              'fulgerite', 'diorite', 'pumice']
    # open input file as a csv reader
    with open(f'../DataCollection/output_files/{FILE}', 'r') as r:
        read = csv.reader(r, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # convert the data to a list and enumerate
        for l, line in enumerate(list(read)):
            print(f'{time.ctime()}: Parsing data from line {l}.')

            # enumerate each line
            for i, chunk in enumerate(line):

                # find first image source link
                index = chunk.find('https')
                if index != -1 and chunk.find('https', index + 1) != -1:
                    src = (chunk[index:chunk.find('https', index + 1)])

                # get name of specimen in image
                if chunk.find('scientificName') != -1:

                    # make all names lower case for consistency
                    name = (chunk[chunk.find('scientificName') + 14:]).lower()

                    # ignore unlabeled/vague data points
                    if name != 'photograph' and name != 'unidentified' and name.find('unknown') == -1 and name.find(
                            'terr') == -1:

                        # if the name contains a str from the common names, replace the name with the common name
                        if name.find('(') != -1:
                            name = name[:name.find('(') - 1]

                        # simplify names to names in the list of common names; i.e. "rose quartz" --> "quartz"
                        for j, n in enumerate(common):
                            if name.find(n) != -1:
                                name = common[j]
                                break

                        # simplify phrases to first name that occurs to generalize
                        if name.find(' ') != -1:
                            name = name[:name.find(' ') - 1]

                        # ignore data that is unnamed/includes hyphens, periods, numbers
                        if 1 < len(name) and name.find('-') == -1 and name.find('.') == -1 and not has_num(name):
                            data.append([name, src])
    return data


# define a method to check if a string contains numbers
def has_num(str):
    return any(char.isdigit() for char in str)


def main():
    print(f'{time.ctime()}: Retrieve names and image links from parsed data.')
    start_time = time.time()
    # define input and output files
    input_file = 'data.csv'
    output_file = 'parsed_data.csv'

    # parse data and get the returned list
    data = parse_lines(input_file)

    # write newly parsed data into a csv file
    with open(f'../DataCollection/output_files/{output_file}', 'w') as w:
        write = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        data.sort()
        for line in data:
            write.writerow(line)

    print(f'{time.ctime()}: Data collection process completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == "__main__":
    main()
