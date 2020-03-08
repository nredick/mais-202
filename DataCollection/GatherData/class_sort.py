import itertools
import re
import os
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import time
from os import path
import shutil

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
         'unakite', 'ungr', 'variolite', 'volcani', 'welde', 'igneou', 'scoria', 'kyanit']

minerals = ['baryte', 'aurichalcite', 'auge', 'augelite', 'anhydrite', 'zeolite', 'quartz', 'calcite', 'elbaite',
            'mica', 'apatite', 'lazurite', 'malachite', 'galena',
            'sphalerite', 'acanthite', 'heulandite', 'natrolite', 'thomsonite', 'penninite', 'azurite' ,'chalcocite',
            'hematite', 'millerite', 'argentite', 'wolframite', 'tantalite', 'apophyllite', 'wulfenite' ,'chabazite',
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
             'anglesite', 'antigorite', 'axinite', 'benitoite', 'boracite', 'clinohumite', 'colemanite', 'enstatite',
             'euclase', 'glass', 'howlite', 'intarsia', 'jeremejevite', 'kyanite', 'labradorite', 'magnesite',
             'narsarsukite', 'pharmacosiderite', 'phosphophyllite', 'pyrope', 'rhyolite', 'scapolite',
             'sillimanite', 'sodalite', 'spessartine', 'stalagmite', 'tugtupite', 'turquoise', 'zircon',
             'cordierite', 'fuchsit', 'ivory', 'kämmererite', 'nephrite', 'titanite', 'titanitelederite',
             'titanitesphene']

fossils = ['baculite', 'astrononio', 'astrodo', 'cythe', 'aganaste', 'aet', 'crinu', 'aege', 'aeo', 'acyl', 'act',
           'acro', 'acriaste', 'acmarhachi', 'acimetopu', 'aciculolenu', 'acherontemy', 'acheilop', 'acheilu',
           'aceratheriu', 'acanth', 'acantholambru', 'acantholabi', 'acanthocell', 'acantherpeste', 'abyssotherm',
           'absarokiu', 'abditodentri', 'genu', 'aatocrinu', 'fossil', 'fulgurite', 'suppell', 'sullivanichthy',
           'symbo', 'symbloc', 'synbathocrinu',
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
           'agassizodu', 'alce', 'both', 'bolivin', 'bonni', 'bos', 'pleurostomell', 'valvulineri', 'cribroelphidiu',
           'olenellu', 'echinocyamu', 'pegidi', 'pronemobiu', 'symploc', 'bulimin', 'uvigerin', 'cyathocrinite']


def rename(directory):
    files = os.listdir(directory)
    for i, f in enumerate(files):
        name = re.findall('^[a-zA-Z]+', f)[0]
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
        if not found:
            for p, q in enumerate(fossils):
                if name.find(q) != -1:
                    name = 'fossil'
                    found = True
        if not found:
            name = 'fossil'

        old_path = os.path.join('../output_files/Images_zip', f)
        new_path = os.path.join('../output_files/images_2.0', f'{name}{i}.jpeg')

        Path(new_path).touch(exist_ok=True)
        print(old_path, '------->', new_path)
        shutil.move(old_path, new_path)


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


def main():
    print(f'{time.ctime()}: Sorting images into classes and resizing images.')
    start_time = time.time()

    directory = '../output_files/Images_zip'
    rename(directory)

    print(f'{time.ctime()}: Sorting process completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == "__main__":
    main()