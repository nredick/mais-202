import csv
import itertools
import time


def parse_lines(FILE):
    data = []

    rocks = ['biotit', 'feldspar', 'pyroxene', 'andesite', 'albite', 'dolomite', 'breccia', 'granite', 'corundum', 'magnetite',
             'basalt', 'concretion', 'tuff', 'biotite', 'xenolith', 'lapilli', 'tephra', 'sepiolite', 'shoshonite',
             'diogenite', 'gabbro', 'pegmatite', 'chert', 'limestone', 'conglomerate', 'shale', 'diorite', 'pumice',
             'copper', 'lead', 'cinnabar', 'smithsonite', 'willemite', 'syenite', 'talc', 'antimony', 'arkose',
             'asphalt', 'bornite', 'bournonite', 'breadcrus', 'chromite', 'clay', 'conglomerate', 'gneiss',
             'granophyre', 'graphite', 'hornblende', 'hornfels', 'iron', 'lava', 'limonite', 'marble', 'mesosiderite',
             'metamorphi', 'obsidian', 'oligoclase', 'ore', 'pallasite', 'pitchstone', 'propylite', 'proterobase',
             'radiolaria', 'sandstone', 'schist', 'sherg', 'shergottite', 'siliceou', 'sillimanit', 'silve', 'tufa',
             'ureilite', 'accretionar', 'adesit', 'altere', 'andesin', 'angrite', 'anorth', 'anthracite', 'aplite',
             'argillite', 'asbestos', 'ash', 'aub', 'bande', 'basal', 'bastnaesite', 'bastnäsite', 'bauxit', 'bauxite',
             'brachinite', 'calcareou', 'dacite', 'diabase', 'dio', 'eclogite', 'eclogitegarne', 'eucrit', 'felsite',
             'fumarol', 'graniti', 'hornblend', 'iab', 'iiiab', 'ii', 'iro', 'iva', 'ivb', 'komatiite', 'laterite',
             'lherzolite', 'mic', 'migmatite', 'muscovit', 'porphyrite', 'rhyoliti', 'rutile', 'sandston', 'slate',
             'unakite', 'ungr', 'variolite', 'volcani', 'welde']

    minerals = ['baryte', 'aurichalcite', 'auge', 'augelite', 'anhydrite', 'zeolite', 'quartz', 'calcite', 'elbaite', 'mica', 'apatite', 'lazurite', 'malachite', 'galena',
                'sphalerite', 'acanthite', 'heulandite', 'natrolite', 'thomsonite', 'penninite', 'azurite','chalcocite',
                'hematite', 'millerite', 'argentite', 'wolframite', 'tantalite', 'apophyllite', 'wulfenite','chabazite',
                'stilbite', 'muscovite', 'palermoite', 'goedkonite', 'chlorite', 'moschellandsbergite', 'goethite',
                'cubanite', 'enargite', 'sphorite', 'chlorite', 'stilbite', 'chabazite', 'cuprosklodowskite',
                'dyscrasite', 'clinchlore', 'fergusonite', 'gadolinite', 'shattuckite', 'hemimorphite', 'actinolite',
                'cervantite', 'clintonite', 'montecellite', 'vesuvianite', 'chromite', 'brochantite', 'aragonite',
                'lorenzenite', 'crocoite', 'banakite', 'tantalite', 'tellerium', 'tetrahedrite', 'acap',
                'acapulcoite', 'acho', 'adamite', 'analcime', 'anatase', 'aporhyolite', 'atacamite', 'aubrite', 'augit',
                'austinite', 'bertrandite', 'betafite', 'beyerite', 'bismuth', 'bixbyite', 'brazilianite', 'brucite',
                'buergerite', 'caudite', 'charoite', 'chrysocolla', 'chrysotile', 'columbite', 'connellite', 'eucrite',
                'genthelvite', 'gmelinite', 'goosecreekite', 'gree', 'greenockite', 'halite', 'harmotome', 'hematite',
                'hessite', 'how', 'howardite', 'kornerupine', 'laumonite', 'leidleite', 'lepidolite', 'leucite',
                'manganite', 'mesolite', 'metadacite', 'microcline', 'mimetite', 'monazite', 'monzonite', 'mud',
                'muscovite', 'nakhlite', 'neptunite', 'nicke', 'orphiment', 'papagoite', 'peridotite', 'perlite',
                'phenakite', 'phlogopite', 'phosgenite', 'platinum', 'prehnite', 'proustite', 'pyragyrite',
                'pyromorhpite', 'pyrophyllite', 'pyroxene', 'pyrrhotite', 'pyrrhottitesiderite', 'rhodonite',
                'riebeckite', 'scheelite', 'scolecite', 'scorocite', 'sepiolite', 'serpentinite', 'silver',
                'sperrylite', 'stalactite', 'staurolite', 'stannite', 'stibnite', 'strontianite', 'syenite', 'uvite',
                'vanadinite', 'vanadinitebaryte', 'variscite', 'vivianite', 'wavellite', 'wollastonite', 'zincite',
                'zoisite', 'afghanite', 'ajoite', 'alabandite', 'allemontite', 'allivalite', 'altaite', 'aluminum',
                'amalgamamalgam', 'baryteberthierite', 'baryteengland', 'baryterealgar', 'ben', 'bencubbinite',
                'brewsterite', 'celadonite', 'celestine', 'celestite', 'cerussite', 'chevkinite', 'cornubiteclinoclase',
                'cronstedtite', 'cummingtonite', 'cuprite', 'cuspidineilvaite', 'datolite', 'edingtonite', 'epidote',
                'fayalite', 'ferrarisite', 'franklinite', 'freieslebenite', 'gahnite', 'garne', 'garnieritegenthite',
                'geyserite', 'gigantolite', 'grunerite', 'gypsum', 'inesite', 'koechlinite', 'laumontite', 'legrandite',
                'liddicoatite', 'liparite', 'lodranite', 'magnesia', 'marcasit', 'marcasite', 'meionite', 'melonite' ,
                'merwinite', 'metatorbernite', 'metatorbernitemetatorbernite', 'metatorbernitetorbernite', 'mordenite',
                'novácekite', 'petalite', 'plazolite', 'powellite', 'pyrolusite', 'pyromorphite', 'realgar',
                'realgarlorándite', 'romanèchite', 'staurolit', 'stephanite', 'sérandite', 'tungste', 'volborthite',
                'väyrynenite', 'vésigniéite', 'weeksite', 'winonaite', 'yttrialite', 'zvyagintsevite']

    gemstones = ['jade', 'opal', 'rhodonite', 'pearl', 'garnet', 'grossular', 'almandine', 'almandite', 'beryl',
                 'diamond', 'topaz', 'pyrite', 'schorl', 'tourmaline', 'titatnite', 'fluorite', 'rhodochrosite',
                 'orthoclase', 'serpentine', 'diopside', 'wernerite', 'olivine', 'sulfur', 'chalcedony', 'forsterite',
                 'spodumene', 'zoisite', 'spinel', 'gold', 'amblygonite', 'andalusite', 'andesine', 'andradite',
                 'anglesite', 'antigorite', 'axinite', 'benitoite', 'boracite', 'clinohumite', 'colemanite', 'enstatite'
                 , 'euclase', 'glass', 'howlite', 'intarsia', 'jeremejevite', 'kyanite', 'labradorite', 'magnesite',
                 'narsarsukite', 'pharmacosiderite', 'phosphophyllite', 'pyrope', 'rhyolite', 'scapolite',
                 'sillimanite', 'sodalite', 'spessartine', 'stalagmite', 'tugtupite', 'turquoise', 'zircon',
                 'cordierite', 'fuchsit', 'ivory', 'kämmererite', 'nephrite', 'titanite', 'titanitelederite',
                 'titanitesphene']

    fossils = ['baculite', 'astrononio', 'astrodo', 'cythe', 'aganaste', 'aet', 'crinu', 'aege', 'aeo', 'acyl', 'act', 'acro', 'acriaste', 'acmarhachi', 'acimetopu', 'aciculolenu', 'acherontemy', 'acheilop', 'acheilu', 'aceratheriu', 'acanth', 'acantholambru', 'acantholabi', 'acanthocell', 'acantherpeste', 'abyssotherm', 'absarokiu', 'abditodentri', 'genu', 'aatocrinu', 'fossil', 'fulgurite', 'suppell', 'sullivanichthy', 'symbo', 'symbloc', 'synbathocrinu',
               'synerocrinu', 'synorichthy', 'taeniodu', 'taeniolabi', 'taeniopteri', 'talarocrinu', 'tanaodu',
               'tapiru', 'tappanell', 'taracyther', 'tatenecte', 'tautog', 'taxide', 'taxocrinu', 'technitell',
               'telocera', 'telepisz', 'telikosocrinu', 'tenontosauru', 'testud', 'tetrataxi', 'texacrinu', 'texasete',
               'textulari', 'textulariell', 'textulariopsi', 'thaerocyther', 'thalamocrinu', 'thalamoporell',
               'thalassocyther', 'thambetoche', 'thelxiop', 'thescelosauru', 'thespesiu', 'aacocrinu', 'abrocytherei',
               'abrotocrinu', 'absarokite', 'abyssamin', 'abyssocyther', 'acacocrinu', 'acaeniotylopsi',
               'acantharthropteru', 'acanthocera', 'acanthocrinu', 'acanthocytherei', 'acanthode', 'acanthodesi',
               'acanthoparyph', 'acanthosteg', 'acarinin', 'acarotrochu', 'acast', 'acervulin', 'acetabulastom',
               'acherorapto', 'achlysopsi', 'acidaspi', 'acidiphoru', 'acidiscu', 'acondylacanthu', 'acostinell',
               'acrocanthosaur', 'acrocephalite', 'acrocephalop', 'acrocrinu', 'acrodu', 'acrophoc', 'acrosaleni',
               'actinocrinite', 'actinocrinu', 'actinocytherei', 'actinolite', 'acyclocrinu', 'adelosin', 'adeon',
               'adercotrym', 'adjidaum', 'adocu', 'aelurodo', 'aeolomorphell', 'aeolostrepti', 'aesiocrinu',
               'affinocrinu', 'afrolloni', 'agaricocrinu', 'agassizi', 'agassizia', 'agassaizocrinu', 'agathammin',
               'agelacrinite', 'agladrillia', 'agnostu', 'agostopu', 'agraulo', 'agrenocyther', 'aguayoin', 'agull',
               'alabamin', 'alabamorni', 'alalcomenaeu', 'alamosaur', 'alatacyther', 'albansi', 'albertell',
               'albertelloide', 'albertosauru', 'alisocrinu', 'allacodo', 'allagecrinu', 'allocatillocrinu',
               'allocrinu', 'allomorphin', 'alloprosallocrinu', 'allosauru', 'allosocrinu', 'alokistocar',
               'alokistocarell', 'alopecia', 'alveolophragmiu', 'amblypteru', 'ambocyther', 'ambostraco', 'amecephalin',
               'amecysti', 'ami', 'amiaspi', 'amiskwi', 'ammoastut', 'ammobaculite', 'ammobaculoide', 'ammochilostom',
               'ammodiscoide', 'ammodiscu', 'ammofrondiculari', 'ammolagen', 'ammomarginulin', 'ammoni', 'ammoscalari',
               'ammovertell', 'ammosphaeroidin', 'ammotiu', 'ampelocrinu', 'amphelecrinu', 'amphiblestru', 'amphicoryn',
               'amphicrinu', 'amphicythereur', 'amphimorphin', 'amphisoru', 'amphissite', 'amphistegin',
               'ampheitremoid', 'amphoracrinu', 'amphoto', 'ampy', 'ampyxin', 'amyd', 'amyzo', 'analo', 'anancu',
               'anastomos', 'anataphru', 'anchitherium', 'anechocephalu', 'angulogavelinell', 'angulogerin',
               'anisonchu', 'anisopyg', 'ankour', 'ankylosauru', 'anomalin', 'anomalinoide', 'anomalocari',
               'anomalorthi', 'anomocar', 'anomocarell', 'anomoeodu', 'anori', 'anornithopor', 'anosteir', 'anoteropor',
               'antagmu', 'anulocrinu', 'aoji', 'aorocrinu', 'apateo', 'apatokephaloide', 'aphelaspi', 'aphelecrinu',
               'aphelop', 'aphelotoxo', 'apianuru', 'aplousin', 'apographiocrinu', 'apollocrinu', 'applinocrinu',
               'apsopeli', 'apteribi', 'apternodu', 'arachnocrinu', 'agoniatite', 'agomphu', 'agla', 'agathauma',
               'agassizodu', 'alce', 'both', 'bolivin', 'bonni', 'bos']
    # open input file as a csv reader,
    with open(f'/Users/nathalieredick/workspaces/mais202/datacollection/output_files/{FILE}', 'r') as r:
        read = csv.reader(r, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # convert the data to a list and enumerate
        for l, line in enumerate(list(read)):
            print(f'{time.ctime()}: Parsing data from line {l}.')
            # enumerate each line
            srcs = []
            for i, chunk in enumerate(line):
                # find image source links
                while chunk.find('https://collections.nmnh.si.edu') != -1:
                    index = chunk.find('https://collections.nmnh.si.edu')
                    if index != -1 and chunk.find('https://collections.nmnh.si.edu', index + 1) != -1:
                        srcs.append(chunk[index:chunk.find('https://collections.nmnh.si.edu', index + 1)])
                        chunk = chunk[chunk.find('https://collections.nmnh.si.edu', index + 1):]
                    elif index != -1:
                        srcs.append(chunk[index:])
                        break

                # get name of specimen in image
                if chunk.find('scientificName') != -1:

                    # make all names lower case for consistency
                    name = (chunk[chunk.find('scientificName') + 14:]).lower()

                    # ignore unlabeled/vague data points
                    if name != 'photograph' and name != 'unidentified' and name.find('unknown') == -1 and name.find(
                            'terr') == -1:

                        if name.find('(') != -1:
                            name = name[:name.find('(') - 1]

                        # simplify phrases to first name that occurs to generalize
                        if name.find(' ') != -1:
                            name = name[:name.find(' ') - 1]

                        # simplify names to names in the list of common names; i.e. "rose quartz" --> "quartz"
                        found = False
                        for j, k in enumerate(rocks):
                            if name.find(k) != -1:
                                name = 'rock'
                                found = True
                        if not found:
                            for l, m in enumerate(minerals):
                                if name.find(m) != -1:
                                    name = 'mineral'
                                    found = True
                        if not found:
                            for n, o in enumerate(gemstones):
                                if name.find(o) != -1:
                                    name = 'gemstone'
                                    found = True
                        for p, q in enumerate(fossils):
                            if name.find(q) != -1:
                                name = 'fossil'
                                found = True
                        if not found:
                            name = 'fossil'

                        # ignore data that is unnamed/includes hyphens, periods, numbers
                        if 1 < len(name) and name.find('-') == -1 and name.find('.') == -1 and not has_num(name):
                            for link in srcs:
                                data.append([name, link])
    return remove_duplicates(data)


# define a method to check if a string contains numbers
def has_num(str):
    return any(char.isdigit() for char in str)


def remove_duplicates(k):
    k.sort()
    return list(k for k, _ in itertools.groupby(k))


def main():
    print(f'{time.ctime()}: Retrieve names and image links from parsed data.')
    start_time = time.time()
    # define input and output files
    input_file = 'data.csv'
    output_file = 'parsed_data.csv'

    # parse data and get the returned list
    data = parse_lines(input_file)

    # write newly parsed data into a csv file
    with open(f'/Users/nathalieredick/workspaces/mais202/datacollection/output_files/{output_file}', 'w') as w:
        write = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        data.sort()
        for line in data:
            write.writerow(line)

    print(f'{time.ctime()}: Data collection process completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == "__main__":
    main()
