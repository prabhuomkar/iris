import torch
import torch.nn.functional as F
from ts.torch_handler.image_classifier import ImageClassifier as PImageClassifier
from ts.utils.util import map_class_to_label


class ImageClassifier(PImageClassifier):
  """Image Classifier"""
  IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY = {
    'barn_spider': 'ANIMALS', 'black_and_gold_garden_spider':
    'ANIMALS', 'black_widow': 'ANIMALS', 'garden_spider':
    'ANIMALS', 'harvestman': 'ANIMALS', 'scorpion':
    'ANIMALS', 'tarantula': 'ANIMALS', 'wolf_spider':
    'ANIMALS', 'armadillo': 'ANIMALS', 'American_black_bear':
    'ANIMALS', 'brown_bear': 'ANIMALS', 'ice_bear':
    'ANIMALS', 'giant_panda': 'ANIMALS', 'lesser_panda':
    'ANIMALS', 'African_grey': 'ANIMALS', 'American_coot':
    'ANIMALS', 'American_egret': 'ANIMALS', 'European_gallinule':
    'ANIMALS', 'albatross': 'ANIMALS', 'bald_eagle':
    'ANIMALS', 'bee_eater': 'ANIMALS', 'bittern':
    'ANIMALS', 'black_grouse': 'ANIMALS', 'black_stork':
    'ANIMALS', 'black_swan': 'ANIMALS', 'brambling':
    'ANIMALS', 'bulbul': 'ANIMALS', 'bustard': 'ANIMALS',
    'chickadee': 'ANIMALS', 'cock': 'ANIMALS', 'coucal':
    'ANIMALS', 'crane (bird)': 'ANIMALS', 'dowitcher':
    'ANIMALS', 'drake': 'ANIMALS', 'flamingo': 'ANIMALS',
    'goldfinch': 'ANIMALS', 'goose': 'ANIMALS',
    'great_grey_owl': 'ANIMALS', 'hen': 'ANIMALS', 'hornbill':
    'ANIMALS', 'house_finch': 'ANIMALS', 'hummingbird':
    'ANIMALS', 'indigo_bunting': 'ANIMALS', 'jacamar':
    'ANIMALS', 'jay': 'ANIMALS', 'junco': 'ANIMALS',
    'king_penguin': 'ANIMALS', 'kite': 'ANIMALS', 'limpkin':
    'ANIMALS', 'little_blue_heron': 'ANIMALS', 'lorikeet':
    'ANIMALS', 'macaw': 'ANIMALS', 'magpie': 'ANIMALS',
    'ostrich': 'ANIMALS', 'oystercatcher': 'ANIMALS',
    'partridge': 'ANIMALS', 'peacock': 'ANIMALS', 'pelican':
    'ANIMALS', 'prairie_chicken': 'ANIMALS', 'ptarmigan':
    'ANIMALS', 'quail': 'ANIMALS', 'red-backed_sandpiper':
    'ANIMALS', 'red-breasted_merganser': 'ANIMALS', 'redshank':
    'ANIMALS', 'robin': 'ANIMALS', 'ruddy_turnstone':
    'ANIMALS', 'ruffed_grouse': 'ANIMALS', 'spoonbill':
    'ANIMALS', 'sulphur-crested_cockatoo': 'ANIMALS', 'toucan':
    'ANIMALS', 'vulture': 'ANIMALS', 'water_ouzel':
    'ANIMALS', 'white_stork': 'ANIMALS', 'ant': 'ANIMALS',
    'bee': 'ANIMALS', 'centipede': 'ANIMALS', 'cicada':
    'ANIMALS', 'cockroach': 'ANIMALS', 'cricket':
    'ANIMALS', 'damselfly': 'ANIMALS', 'dragonfly':
    'ANIMALS', 'flatworm': 'ANIMALS', 'fly': 'ANIMALS',
    'grasshopper': 'ANIMALS', 'ground_beetle': 'ANIMALS',
    'lacewing': 'ANIMALS', 'ladybug': 'ANIMALS',
    'long-horned_beetle': 'ANIMALS', 'mantis': 'ANIMALS', 'nematode':
    'ANIMALS', 'rhinoceros_beetle': 'ANIMALS', 'tick':
    'ANIMALS', 'tiger_beetle': 'ANIMALS', 'weevil':
    'ANIMALS', 'dung_beetle': 'ANIMALS', 'leaf_beetle':
    'ANIMALS', 'leafhopper': 'ANIMALS', 'walking_stick':
    'ANIMALS', 'admiral': 'ANIMALS', 'cabbage_butterfly':
    'ANIMALS', 'lycaenid': 'ANIMALS', 'monarch': 'ANIMALS',
    'ringlet': 'ANIMALS', 'sulphur_butterfly': 'ANIMALS',
    'Egyptian_cat': 'ANIMALS', 'Persian_cat': 'ANIMALS',
    'Siamese_cat': 'ANIMALS', 'tabby': 'ANIMALS',
    'brain_coral': 'ANIMALS', 'coral_fungus': 'ANIMALS',
    'coral_reef': 'ANIMALS', 'rock_beauty': 'ANIMALS',
    'sea_anemone': 'ANIMALS', 'African_crocodile': 'ANIMALS',
    'American_alligator': 'ANIMALS', 'American_lobster': 'ANIMALS',
    'Dungeness_crab': 'ANIMALS', 'crayfish': 'ANIMALS',
    'fiddler_crab': 'ANIMALS', 'hermit_crab': 'ANIMALS',
    'isopod': 'ANIMALS', 'king_crab': 'ANIMALS',
    'rock_crab': 'ANIMALS', 'spiny_lobster': 'ANIMALS',
    'triceratops': 'ANIMALS', 'Afghan_hound': 'ANIMALS',
    'African_hunting_dog': 'ANIMALS', 'Airedale': 'ANIMALS',
    'American_Staffordshire_terrier': 'ANIMALS', 'Appenzeller': 'ANIMALS',
    'Australian_terrier': 'ANIMALS', 'Bedlington_terrier': 'ANIMALS',
    'Bernese_mountain_dog': 'ANIMALS', 'Blenheim_spaniel': 'ANIMALS',
    'Border_collie': 'ANIMALS', 'Border_terrier': 'ANIMALS',
    'Boston_bull': 'ANIMALS', 'Bouvier_des_Flandres':
    'ANIMALS', 'Brabancon_griffon': 'ANIMALS', 'Brittany_spaniel':
    'ANIMALS', 'Cardigan': 'ANIMALS', 'Chesapeake_Bay_retriever':
    'ANIMALS', 'Chihuahua': 'ANIMALS', 'Dandie_Dinmont':
    'ANIMALS', 'Doberman': 'ANIMALS', 'English_foxhound':
    'ANIMALS', 'English_setter': 'ANIMALS', 'English_springer':
    'ANIMALS', 'EntleBucher': 'ANIMALS', 'Eskimo_dog':
    'ANIMALS', 'French_bulldog': 'ANIMALS', 'German_shepherd':
    'ANIMALS', 'German_short-haired_pointer': 'ANIMALS', 'Gordon_setter':
    'ANIMALS', 'Great_Dane': 'ANIMALS', 'Great_Pyrenees':
    'ANIMALS', 'Greater_Swiss_Mountain_dog': 'ANIMALS', 'Ibizan_hound':
    'ANIMALS', 'Irish_setter': 'ANIMALS', 'Irish_terrier':
    'ANIMALS', 'Irish_water_spaniel': 'ANIMALS', 'Irish_wolfhound':
    'ANIMALS', 'Italian_greyhound': 'ANIMALS', 'Japanese_spaniel':
    'ANIMALS', 'Kerry_blue_terrier': 'ANIMALS', 'Labrador_retriever':
    'ANIMALS', 'Lakeland_terrier': 'ANIMALS', 'Leonberg':
    'ANIMALS', 'Lhasa': 'ANIMALS', 'Maltese_dog':
    'ANIMALS', 'Mexican_hairless': 'ANIMALS', 'Newfoundland':
    'ANIMALS', 'Norfolk_terrier': 'ANIMALS', 'Norwegian_elkhound':
    'ANIMALS', 'Norwich_terrier': 'ANIMALS', 'Old_English_sheepdog':
    'ANIMALS', 'Pekinese': 'ANIMALS', 'Pembroke':
    'ANIMALS', 'Pomeranian': 'ANIMALS', 'Rhodesian_ridgeback':
    'ANIMALS', 'Rottweiler': 'ANIMALS', 'Saint_Bernard':
    'ANIMALS', 'Saluki': 'ANIMALS', 'Samoyed': 'ANIMALS',
    'Scotch_terrier': 'ANIMALS', 'Scottish_deerhound': 'ANIMALS',
    'Sealyham_terrier': 'ANIMALS', 'Shetland_sheepdog': 'ANIMALS',
    'Shih-Tzu': 'ANIMALS', 'Siberian_husky': 'ANIMALS',
    'Staffordshire_bullterrier': 'ANIMALS', 'Sussex_spaniel': 'ANIMALS',
    'Tibetan_mastiff': 'ANIMALS', 'Tibetan_terrier': 'ANIMALS',
    'Walker_hound': 'ANIMALS', 'Weimaraner': 'ANIMALS',
    'Welsh_springer_spaniel': 'ANIMALS', 'West_Highland_white_terrier':
    'ANIMALS', 'Yorkshire_terrier': 'ANIMALS', 'affenpinscher':
    'ANIMALS', 'basenji': 'ANIMALS', 'basset': 'ANIMALS',
    'beagle': 'ANIMALS', 'black-and-tan_coonhound':
    'ANIMALS', 'bloodhound': 'ANIMALS', 'bluetick':
    'ANIMALS', 'borzoi': 'ANIMALS', 'boxer': 'ANIMALS',
    'briard': 'ANIMALS', 'bull_mastiff': 'ANIMALS',
    'cairn': 'ANIMALS', 'chow': 'ANIMALS', 'clumber':
    'ANIMALS', 'cocker_spaniel': 'ANIMALS', 'collie':
    'ANIMALS', 'curly-coated_retriever': 'ANIMALS', 'dalmatian':
    'ANIMALS', 'flat-coated_retriever': 'ANIMALS', 'giant_schnauzer':
    'ANIMALS', 'golden_retriever': 'ANIMALS', 'groenendael':
    'ANIMALS', 'keeshond': 'ANIMALS', 'kelpie': 'ANIMALS',
    'komondor': 'ANIMALS', 'kuvasz': 'ANIMALS', 'malamute':
    'ANIMALS', 'malinois': 'ANIMALS', 'miniature_pinscher':
    'ANIMALS', 'miniature_poodle': 'ANIMALS', 'miniature_schnauzer':
    'ANIMALS', 'otterhound': 'ANIMALS', 'papillon':
    'ANIMALS', 'pug': 'ANIMALS', 'redbone': 'ANIMALS',
    'schipperke': 'ANIMALS', 'silky_terrier': 'ANIMALS',
    'soft-coated_wheaten_terrier': 'ANIMALS', 'standard_poodle': 'ANIMALS',
    'standard_schnauzer': 'ANIMALS', 'toy_poodle': 'ANIMALS',
    'toy_terrier': 'ANIMALS', 'vizsla': 'ANIMALS', 'whippet':
    'ANIMALS', 'wire-haired_fox_terrier': 'ANIMALS', 'sea_cucumber':
    'ANIMALS', 'sea_urchin': 'ANIMALS', 'starfish':
    'ANIMALS', 'badger': 'ANIMALS', 'black-footed_ferret':
    'ANIMALS', 'mink': 'ANIMALS', 'otter': 'ANIMALS',
    'polecat': 'ANIMALS', 'skunk': 'ANIMALS', 'weasel':
    'ANIMALS', 'anemone_fish': 'ANIMALS', 'barracouta':
    'ANIMALS', 'eel': 'ANIMALS', 'electric_ray': 'ANIMALS',
    'gar': 'ANIMALS', 'goldfish': 'ANIMALS',
    'lionfish': 'ANIMALS', 'puffer': 'ANIMALS', 'sea_snake':
    'ANIMALS', 'sturgeon': 'ANIMALS', 'tench': 'ANIMALS',
    'jellyfish': 'ANIMALS', 'stingray': 'ANIMALS', 'cardoon':
    'FLOWERS', 'daisy': 'FLOWERS', 'hip': 'FLOWERS',
    'rapeseed': 'FLOWERS', "yellow_lady's_slipper":
    'FLOWERS', 'bullfrog': 'ANIMALS', 'tailed_frog':
    'ANIMALS', 'tree_frog': 'ANIMALS', 'Granny_Smith':
    'FOOD', 'acorn_squash': 'FOOD', 'banana':
    'FOOD', 'custard_apple': 'FOOD', 'fig':
    'FOOD', "jack-o'-lantern": 'FOOD', 'jackfruit':
    'FOOD', 'lemon': 'FOOD', 'orange': 'FOOD',
    'pineapple': 'FOOD', 'pomegranate': 'FOOD',
    'spaghetti_squash': 'FOOD', 'strawberry': 'FOOD',
    'zucchini': 'FOOD', 'agaric': 'GARDENS', 'bolete':
    'GARDENS', 'earthstar': 'GARDENS', 'gyromitra':
    'GARDENS', 'hen-of-the-woods': 'GARDENS', 'mushroom':
    'GARDENS', 'stinkhorn': 'GARDENS', 'hog': 'ANIMALS',
    'warthog': 'ANIMALS', 'wild_boar': 'ANIMALS',
    'African_chameleon': 'ANIMALS', 'American_chameleon': 'ANIMALS',
    'Gila_monster': 'ANIMALS', 'Komodo_dragon': 'ANIMALS',
    'agama': 'ANIMALS', 'alligator_lizard': 'ANIMALS',
    'banded_gecko': 'ANIMALS', 'common_iguana': 'ANIMALS',
    'frilled_lizard': 'ANIMALS', 'green_lizard': 'ANIMALS',
    'whiptail': 'ANIMALS', 'dugong': 'ANIMALS', 'sea_lion':
    'ANIMALS', 'grey_whale': 'ANIMALS', 'killer_whale':
    'ANIMALS', 'koala': 'ANIMALS', 'wallaby': 'ANIMALS',
    'wombat': 'ANIMALS', 'chambered_nautilus': 'ANIMALS',
    'chiton': 'ANIMALS', 'conch': 'ANIMALS', 'sea_slug':
    'ANIMALS', 'slug': 'ANIMALS', 'snail': 'ANIMALS',
    'Madagascar_cat': 'ANIMALS', 'meerkat': 'ANIMALS', 'mongoose':
    'ANIMALS', 'echidna': 'ANIMALS', 'platypus': 'ANIMALS',
    'ballplayer': 'PEOPLE', 'groom': 'PEOPLE', 'pirate':
    'PEOPLE', 'scuba_diver': 'PEOPLE', 'acorn':
    'FOOD', 'buckeye': 'FOOD', 'sorrel': 'FOOD',
    'baboon': 'ANIMALS', 'capuchin': 'ANIMALS',
    'chimpanzee': 'ANIMALS', 'colobus': 'ANIMALS', 'gibbon':
    'ANIMALS', 'gorilla': 'ANIMALS', 'guenon': 'ANIMALS',
    'howler_monkey': 'ANIMALS', 'indri': 'ANIMALS', 'langur':
    'ANIMALS', 'macaque': 'ANIMALS', 'marmoset': 'ANIMALS',
    'orangutan': 'ANIMALS', 'patas': 'ANIMALS',
    'proboscis_monkey': 'ANIMALS', 'siamang': 'ANIMALS',
    'spider_monkey': 'ANIMALS', 'squirrel_monkey': 'ANIMALS',
    'titi': 'ANIMALS', 'Angora': 'ANIMALS', 'hare':
    'ANIMALS', 'wood_rabbit': 'ANIMALS', 'beaver':
    'ANIMALS', 'fox_squirrel': 'ANIMALS', 'guinea_pig':
    'ANIMALS', 'hamster': 'ANIMALS', 'marmot': 'ANIMALS',
    'mouse': 'ANIMALS', 'porcupine': 'ANIMALS',
    'European_fire_salamander': 'ANIMALS', 'axolotl': 'ANIMALS',
    'common_newt': 'ANIMALS', 'eft': 'ANIMALS',
    'spotted_salamander': 'ANIMALS', 'coho': 'ANIMALS',
    'great_white_shark': 'ANIMALS', 'hammerhead': 'ANIMALS',
    'tiger_shark': 'ANIMALS', 'sloth_bear': 'ANIMALS',
    'three-toed_sloth': 'ANIMALS', 'Indian_cobra': 'ANIMALS',
    'boa_constrictor': 'ANIMALS', 'diamondback': 'ANIMALS',
    'garter_snake': 'ANIMALS', 'green_mamba': 'ANIMALS',
    'green_snake': 'ANIMALS', 'hognose_snake': 'ANIMALS',
    'horned_viper': 'ANIMALS', 'king_snake': 'ANIMALS',
    'night_snake': 'ANIMALS', 'ringneck_snake': 'ANIMALS',
    'rock_python': 'ANIMALS', 'sidewinder': 'ANIMALS',
    'thunder_snake': 'ANIMALS', 'vine_snake': 'ANIMALS',
    'water_snake': 'ANIMALS', 'trilobite': 'ANIMALS',
    'box_turtle': 'ANIMALS', 'leatherback_turtle': 'ANIMALS',
    'loggerhead': 'ANIMALS', 'mud_turtle': 'ANIMALS',
    'terrapin': 'ANIMALS', 'African_elephant': 'ANIMALS',
    'Arabian_camel': 'ANIMALS', 'Indian_elephant': 'ANIMALS',
    'bighorn': 'ANIMALS', 'bison': 'ANIMALS', 'gazelle':
    'ANIMALS', 'hartebeest': 'ANIMALS', 'hippopotamus':
    'ANIMALS', 'ibex': 'ANIMALS', 'impala': 'ANIMALS',
    'llama': 'ANIMALS', 'ox': 'ANIMALS', 'ram':
    'ANIMALS', 'tusker': 'ANIMALS', 'zebra': 'ANIMALS',
    'water_buffalo': 'ANIMALS', 'artichoke': 'FOOD',
    'bell_pepper': 'FOOD', 'broccoli': 'FOOD',
    'butternut_squash': 'FOOD', 'cauliflower': 'FOOD',
    'cucumber': 'FOOD', 'head_cabbage': 'FOOD',
    'cheetah': 'ANIMALS', 'cougar': 'ANIMALS', 'jaguar':
    'ANIMALS', 'leopard': 'ANIMALS', 'lion': 'ANIMALS',
    'lynx': 'ANIMALS', 'snow_leopard': 'ANIMALS',
    'tiger': 'ANIMALS', 'tiger_cat': 'ANIMALS',
    'Arctic_fox': 'ANIMALS', 'coyote': 'ANIMALS', 'dingo':
    'ANIMALS', 'grey_fox': 'ANIMALS', 'hyena': 'ANIMALS',
    'kit_fox': 'ANIMALS', 'red_fox': 'ANIMALS', 'red_wolf':
    'ANIMALS', 'timber_wolf': 'ANIMALS', 'white_wolf':
    'ANIMALS', 'dhole': 'ANIMALS', 'Windsor_tie':
    'PETS', 'backpack': 'PETS', 'bolo_tie':
    'PETS', 'bow_tie': 'PETS', 'buckle': 'PETS',
    'feather_boa': 'PETS', 'gasmask': 'PETS',
    'hair_slide': 'PETS', 'handkerchief': 'PETS',
    'lipstick': 'PETS', 'mailbag': 'PETS',
    'neck_brace': 'PETS', 'necklace': 'PETS', 'purse':
    'PETS', 'sleeping_bag': 'PETS', 'stole':
    'PETS', 'umbrella': 'PETS', 'wallet':
    'PETS', 'airliner': 'TRAVEL', 'airship': 'TRAVEL',
    'parachute': 'TRAVEL', 'space_shuttle': 'TRAVEL',
    'warplane': 'TRAVEL', 'baseball': 'SPORT',
    'basketball': 'SPORT', 'croquet_ball': 'SPORT',
    'golf_ball': 'SPORT', 'ping-pong_ball': 'SPORT',
    'rugby_ball': 'SPORT', 'soccer_ball': 'SPORT',
    'tennis_ball': 'SPORT', 'volleyball': 'SPORT',
    'aircraft_carrier': 'TRAVEL', 'canoe': 'TRAVEL', 'catamaran':
    'TRAVEL', 'container_ship': 'TRAVEL', 'fireboat':
    'TRAVEL', 'gondola': 'TRAVEL', 'lifeboat': 'TRAVEL',
    'liner': 'TRAVEL', 'paddlewheel': 'TRAVEL',
    'schooner': 'TRAVEL', 'speedboat': 'TRAVEL',
    'submarine': 'TRAVEL', 'trimaran': 'TRAVEL', 'wreck':
    'TRAVEL', 'yawl': 'TRAVEL', 'bakery': 'CITYSCAPES',
    'barbershop': 'CITYSCAPES', 'barn': 'CITYSCAPES', 'beacon':
    'CITYSCAPES', 'bell_cote': 'CITYSCAPES', 'boathouse':
    'CITYSCAPES', 'bookshop': 'CITYSCAPES', 'butcher_shop':
    'CITYSCAPES', 'carousel': 'CITYSCAPES', 'castle':
    'CITYSCAPES', 'church': 'CITYSCAPES', 'cinema': 'CITYSCAPES',
    'cliff_dwelling': 'CITYSCAPES', 'confectionery': 'CITYSCAPES',
    'dome': 'CITYSCAPES', 'greenhouse': 'CITYSCAPES',
    'grocery_store': 'CITYSCAPES', 'home_theater': 'CITYSCAPES',
    'library': 'CITYSCAPES', 'lumbermill': 'CITYSCAPES',
    'mobile_home': 'CITYSCAPES', 'monastery': 'CITYSCAPES',
    'mosque': 'CITYSCAPES', 'mountain_tent': 'CITYSCAPES',
    'obelisk': 'CITYSCAPES', 'palace': 'CITYSCAPES', 'patio':
    'CITYSCAPES', 'planetarium': 'CITYSCAPES', 'prison':
    'CITYSCAPES', 'restaurant': 'CITYSCAPES', 'shoe_shop':
    'CITYSCAPES', 'stupa': 'CITYSCAPES', 'thatch': 'CITYSCAPES',
    'tile_roof': 'CITYSCAPES', 'tobacco_shop': 'CITYSCAPES',
    'toyshop': 'CITYSCAPES', 'yurt': 'CITYSCAPES', 'Loafer':
    'FASHION', 'abaya': 'FASHION', 'academic_gown':
    'FASHION', 'apron': 'FASHION', 'bib': 'FASHION',
    'bikini': 'FASHION', 'brassiere': 'FASHION',
    'breastplate': 'FASHION', 'bulletproof_vest': 'FASHION',
    'cardigan': 'FASHION', 'chain_mail': 'FASHION',
    'cloak': 'FASHION', 'clog': 'FASHION',
    'cowboy_boot': 'FASHION', 'cowboy_hat': 'FASHION',
    'cuirass': 'FASHION', 'diaper': 'FASHION',
    'fur_coat': 'FASHION', 'gown': 'FASHION', 'hoopskirt':
    'FASHION', 'jean': 'FASHION', 'jersey': 'FASHION',
    'kimono': 'FASHION', 'knee_pad': 'FASHION',
    'lab_coat': 'FASHION', 'maillot': 'FASHION', 'mask':
    'FASHION', 'military_uniform': 'FASHION', 'miniskirt':
    'FASHION', 'mitten': 'FASHION', 'overskirt':
    'FASHION', 'oxygen_mask': 'FASHION', 'pajama':
    'FASHION', 'poncho': 'FASHION', 'running_shoe':
    'FASHION', 'sandal': 'FASHION', 'sarong': 'FASHION',
    'ski_mask': 'FASHION', 'sock': 'FASHION', 'suit':
    'FASHION', 'sunglasses': 'FASHION', 'sweatshirt':
    'FASHION', 'swimming_trunks': 'FASHION', 'trench_coat':
    'FASHION', 'vestment': 'FASHION', 'wig': 'FASHION',
    'barrel': 'PETS', 'carton': 'PETS', 'chest':
    'PETS', 'crate': 'PETS', 'medicine_chest':
    'PETS', 'milk_can': 'PETS', 'packet':
    'PETS', 'pill_bottle': 'PETS', 'plastic_bag':
    'PETS', 'rain_barrel': 'PETS', 'safe':
    'PETS', 'shopping_basket': 'PETS', 'shopping_cart':
    'PETS', 'vault': 'PETS', 'washbasin':
    'PETS', 'water_bottle': 'PETS', 'water_jug':
    'PETS', 'whiskey_jug': 'PETS', 'Crock_Pot':
    'PETS', 'Dutch_oven': 'PETS', 'caldron':
    'PETS', 'cleaver': 'PETS', 'cocktail_shaker':
    'PETS', 'coffee_mug': 'PETS', 'coffeepot':
    'PETS', 'corkscrew': 'PETS', 'cup': 'PETS',
    'espresso_maker': 'PETS', 'frying_pan': 'PETS',
    'goblet': 'PETS', 'hot_pot': 'PETS', 'ladle':
    'PETS', 'measuring_cup': 'PETS', 'mixing_bowl':
    'PETS', 'mortar': 'PETS', 'pitcher': 'PETS',
    'plate': 'PETS', 'pot': 'PETS', 'rotisserie':
    'PETS', 'soup_bowl': 'PETS', 'spatula':
    'PETS', 'strainer': 'PETS', 'teapot':
    'PETS', 'wok': 'PETS', 'wooden_spoon':
    'PETS', 'Christmas_stocking': 'PETS', 'analog_clock':
    'PETS', 'bath_towel': 'PETS', 'brass':
    'PETS', 'dishrag': 'PETS', 'doormat':
    'PETS', 'hamper': 'PETS', 'lampshade':
    'PETS', 'piggy_bank': 'PETS', 'pillow':
    'PETS', 'plate_rack': 'PETS', 'prayer_rug':
    'PETS', 'quilt': 'PETS', 'screen': 'PETS',
    'shower_curtain': 'PETS', 'soap_dispenser': 'PETS',
    'table_lamp': 'PETS', 'theater_curtain': 'PETS',
    'tray': 'PETS', 'vase': 'PETS',
    'window_screen': 'PETS', 'window_shade': 'PETS',
    'CD_player': 'PETS', 'Polaroid_camera': 'PETS',
    'cassette_player': 'PETS', 'cellular_telephone':
    'PETS', 'computer_keyboard': 'PETS', 'desktop_computer':
    'PETS', 'dial_telephone': 'PETS', 'digital_clock':
    'PETS', 'digital_watch': 'PETS', 'dishwasher':
    'PETS', 'electric_fan': 'PETS', 'hand-held_computer':
    'PETS', 'hand_blower': 'PETS', 'hard_disc':
    'PETS', 'iPod': 'PETS', 'joystick': 'PETS',
    'laptop': 'PETS', 'loudspeaker': 'PETS',
    'microphone': 'PETS', 'microwave': 'PETS',
    'modem': 'PETS', 'monitor': 'PETS',
    'odometer': 'PETS', 'oscilloscope': 'PETS',
    'parking_meter': 'PETS', 'pay-phone': 'PETS',
    'photocopier': 'PETS', 'power_drill': 'PETS',
    'printer': 'PETS', 'projector': 'PETS',
    'radiator': 'PETS', 'radio': 'PETS',
    'reflex_camera': 'PETS', 'remote_control': 'PETS',
    'scale': 'PETS', 'slot': 'PETS', 'space_bar':
    'PETS', 'space_heater': 'PETS', 'spotlight':
    'PETS', 'stopwatch': 'PETS', 'switch':
    'PETS', 'tape_player': 'PETS', 'television':
    'PETS', 'toaster': 'PETS', 'traffic_light':
    'PETS', 'typewriter_keyboard': 'PETS', 'vacuum':
    'PETS', 'waffle_iron': 'PETS', 'washer':
    'PETS', 'chainlink_fence': 'HOUSES', 'picket_fence':
    'HOUSES', 'worm_fence': 'HOUSES', 'French_loaf':
    'FOOD', 'bagel': 'FOOD', 'beer_bottle':
    'FOOD', 'beer_glass': 'FOOD', 'burrito':
    'FOOD', 'carbonara': 'FOOD', 'cheeseburger':
    'FOOD', 'chocolate_sauce': 'FOOD', 'consomme':
    'FOOD', 'corn': 'FOOD', 'dough': 'FOOD',
    'ear': 'FOOD', 'eggnog': 'FOOD', 'espresso':
    'FOOD', 'guacamole': 'FOOD', 'hotdog': 'FOOD',
    'ice_cream': 'FOOD', 'ice_lolly': 'FOOD',
    'mashed_potato': 'FOOD', 'meat_loaf': 'FOOD', 'pizza':
    'FOOD', 'pop_bottle': 'FOOD', 'potpie':
    'FOOD', 'pretzel': 'FOOD', 'red_wine': 'FOOD',
    'saltshaker': 'FOOD', 'trifle': 'FOOD',
    'wine_bottle': 'FOOD', 'altar': 'PETS', 'ashcan':
    'PETS', 'bannister': 'PETS', 'barber_chair':
    'PETS', 'bassinet': 'PETS', 'bathtub':
    'PETS', 'bookcase': 'PETS', 'chiffonier':
    'PETS', 'china_cabinet': 'PETS', 'cradle':
    'PETS', 'crib': 'PETS', 'desk': 'PETS',
    'dining_table': 'PETS', 'entertainment_center':
    'PETS', 'file': 'PETS', 'fire_screen':
    'PETS', 'folding_chair': 'PETS', 'four-poster':
    'PETS', 'mailbox': 'PETS', 'park_bench':
    'PETS', 'pedestal': 'PETS', 'pool_table':
    'PETS', 'refrigerator': 'PETS', 'rocking_chair':
    'PETS', 'shoji': 'PETS', 'sliding_door':
    'PETS', 'stage': 'PETS', 'stove': 'PETS',
    'stretcher': 'PETS', 'studio_couch': 'PETS',
    'throne': 'PETS', 'toilet_seat': 'PETS',
    'tub': 'PETS', 'wardrobe': 'PETS',
    'bathing_cap': 'PETS', 'bearskin': 'PETS',
    'bonnet': 'PETS', 'crash_helmet': 'PETS',
    'mortarboard': 'PETS', 'shower_cap': 'PETS',
    'sombrero': 'PETS', 'pickelhaube': 'PETS',
    'French_horn': 'PETS', 'accordion': 'PETS',
    'acoustic_guitar': 'PETS', 'banjo': 'PETS', 'bassoon':
    'PETS', 'cello': 'PETS', 'chime': 'PETS',
    'cornet': 'PETS', 'drum': 'PETS', 'drumstick':
    'PETS', 'electric_guitar': 'PETS', 'flute':
    'PETS', 'gong': 'PETS', 'grand_piano':
    'PETS', 'harmonica': 'PETS', 'harp': 'PETS',
    'maraca': 'PETS', 'marimba': 'PETS', 'oboe':
    'PETS', 'ocarina': 'PETS', 'organ': 'PETS',
    'panpipe': 'PETS', 'pick': 'PETS', 'sax':
    'PETS', 'steel_drum': 'PETS', 'trombone':
    'PETS', 'upright': 'PETS', 'violin': 'PETS',
    'Petri_dish': 'PETS', 'beaker': 'PETS',
    'Band_Aid': 'PETS', 'bottlecap': 'PETS',
    'bubble': 'PETS', 'face_powder': 'PETS',
    'hair_spray': 'PETS', 'hay': 'PETS', 'honeycomb':
    'PETS', 'knot': 'PETS', 'lotion': 'PETS',
    'mosquito_net': 'PETS', 'muzzle': 'PETS', 'nipple':
    'PETS', 'pencil_box': 'PETS', 'perfume':
    'PETS', 'sunscreen': 'PETS', 'toilet_tissue':
    'PETS', 'velvet': 'PETS', 'wing': 'PETS',
    'wool': 'PETS', 'alp': 'LANDSCAPES', 'apiary':
    'LANDSCAPES', 'birdhouse': 'LANDSCAPES', 'breakwater':
    'LANDSCAPES', 'cliff': 'LANDSCAPES', 'dam': 'LANDSCAPES',
    'dock': 'LANDSCAPES', 'drilling_platform': 'LANDSCAPES',
    'flagpole': 'LANDSCAPES', 'fountain': 'LANDSCAPES', 'geyser':
    'LANDSCAPES', 'lakeside': 'LANDSCAPES', 'manhole_cover':
    'LANDSCAPES', 'maypole': 'LANDSCAPES', 'maze': 'LANDSCAPES',
    'megalith': 'LANDSCAPES', 'pier': 'LANDSCAPES', 'promontory':
    'LANDSCAPES', 'sandbar': 'LANDSCAPES', 'seashore': 'LANDSCAPES',
    'spider_web': 'LANDSCAPES', 'steel_arch_bridge': 'LANDSCAPES',
    'stone_wall': 'LANDSCAPES', 'street_sign': 'LANDSCAPES',
    'sundial': 'LANDSCAPES', 'suspension_bridge': 'LANDSCAPES',
    'totem_pole': 'LANDSCAPES', 'triumphal_arch': 'LANDSCAPES',
    'valley': 'LANDSCAPES', 'viaduct': 'LANDSCAPES', 'volcano':
    'LANDSCAPES', 'water_tower': 'LANDSCAPES', 'binder':
    'PETS', 'book_jacket': 'PETS', 'comic_book':
    'PETS', 'crossword_puzzle': 'PETS', 'envelope':
    'PETS', 'jigsaw_puzzle': 'PETS', 'menu':
    'PETS', 'notebook': 'PETS', 'paper_towel':
    'PETS', 'balance_beam': 'SPORT', 'barbell':
    'SPORT', 'football_helmet': 'SPORT', 'horizontal_bar':
    'SPORT', 'paddle': 'SPORT', 'parallel_bars':
    'SPORT', 'pole': 'SPORT', 'puck': 'SPORT',
    'punching_bag': 'SPORT', 'racket': 'SPORT',
    'scoreboard': 'SPORT', 'ski': 'SPORT', 'snorkel':
    'SPORT', 'abacus': 'ANIMALS', 'barometer': 'ANIMALS',
    'car_mirror': 'ANIMALS', 'car_wheel': 'ANIMALS',
    'cash_machine': 'ANIMALS', 'cassette': 'ANIMALS', 'coil':
    'ANIMALS', 'combination_lock': 'ANIMALS', 'disk_brake':
    'ANIMALS', 'gas_pump': 'ANIMALS', 'hourglass':
    'ANIMALS', 'lens_cap': 'ANIMALS', 'mousetrap':
    'ANIMALS', 'oil_filter': 'ANIMALS', 'padlock':
    'ANIMALS', 'radio_telescope': 'ANIMALS', 'reel':
    'ANIMALS', 'seat_belt': 'ANIMALS', 'sewing_machine':
    'ANIMALS', 'slide_rule': 'ANIMALS', 'solar_dish':
    'ANIMALS', 'spindle': 'ANIMALS', 'tripod': 'ANIMALS',
    'turnstile': 'ANIMALS', 'vending_machine': 'ANIMALS',
    'wall_clock': 'ANIMALS', 'web_site': 'ANIMALS',
    'ballpoint': 'PETS', 'barrow': 'PETS',
    'binoculars': 'PETS', 'broom': 'PETS', 'bucket':
    'PETS', 'can_opener': 'PETS', 'candle':
    'PETS', "carpenter's_kit": 'PETS', 'chain':
    'PETS', 'chain_saw': 'PETS', 'crutch':
    'PETS', 'dumbbell': 'PETS', 'fountain_pen':
    'PETS', 'hammer': 'PETS', 'hatchet': 'PETS',
    'hook': 'PETS', 'iron': 'PETS',
    'letter_opener': 'PETS', 'lighter': 'PETS', 'loupe':
    'PETS', 'magnetic_compass': 'PETS', 'matchstick':
    'PETS', 'nail': 'PETS', 'paintbrush':
    'PETS', 'pencil_sharpener': 'PETS', 'plane':
    'PETS', 'plunger': 'PETS', "potter's_wheel":
    'PETS', 'quill': 'PETS', 'rubber_eraser':
    'PETS', 'rule': 'PETS', 'safety_pin':
    'PETS', 'screw': 'PETS', 'screwdriver':
    'PETS', 'shield': 'PETS', 'shovel': 'PETS',
    'stethoscope': 'PETS', 'sunglass': 'PETS', 'swab':
    'PETS', 'syringe': 'PETS', 'thimble':
    'PETS', 'torch': 'PETS', 'whistle': 'PETS',
    'balloon': 'BIRTHDAYS', 'pinwheel': 'BIRTHDAYS', 'swing':
    'BIRTHDAYS', 'teddy': 'BIRTHDAYS', 'bullet_train':
    'TRAVEL', 'electric_locomotive': 'TRAVEL', 'freight_car':
    'TRAVEL', 'steam_locomotive': 'TRAVEL', 'Model_T':
    'PETS', 'ambulance': 'PETS', 'amphibian':
    'PETS', 'beach_wagon': 'PETS', 'bicycle-built-for-two':
    'PETS', 'bobsled': 'PETS', 'cab': 'PETS',
    'convertible': 'PETS', 'crane': 'PETS', 'dogsled':
    'PETS', 'fire_engine': 'PETS', 'forklift':
    'PETS', 'garbage_truck': 'PETS', 'go-kart':
    'PETS', 'golfcart': 'PETS', 'grille':
    'PETS', 'half_track': 'PETS', 'harvester':
    'PETS', 'horse_cart': 'PETS', 'jeep':
    'PETS', 'jinrikisha': 'PETS', 'lawn_mower':
    'PETS', 'limousine': 'PETS', 'minibus':
    'PETS', 'minivan': 'PETS', 'moped': 'PETS',
    'motor_scooter': 'PETS', 'mountain_bike': 'PETS',
    'moving_van': 'PETS', 'oxcart': 'PETS',
    'passenger_car': 'PETS', 'pickup': 'PETS', 'plow':
    'PETS', 'police_van': 'PETS', 'racer':
    'PETS', 'recreational_vehicle': 'PETS', 'school_bus':
    'PETS', 'snowmobile': 'PETS', 'snowplow':
    'PETS', 'sports_car': 'PETS', 'streetcar':
    'PETS', 'tank': 'PETS', 'thresher': 'PETS',
    'tow_truck': 'PETS', 'tractor': 'PETS',
    'trailer_truck': 'PETS', 'tricycle': 'PETS',
    'trolleybus': 'PETS', 'unicycle': 'PETS',
    'assault_rifle': 'PETS', 'bow': 'PETS', 'cannon':
    'PETS', 'guillotine': 'PETS', 'holster':
    'PETS', 'missile': 'PETS', 'projectile':
    'PETS', 'revolver': 'PETS', 'rifle': 'PETS',
    'scabbard': 'PETS',
  }

  def postprocess(self, data):
    # get results from pytorch inferencing
    ps = F.softmax(data, dim=1)
    probs, classes = torch.topk(ps, self.topk, dim=1) # pylint: disable=no-member
    probs = probs.tolist()
    classes = classes.tolist()
    results = map_class_to_label(probs, self.mapping, classes)
    # customizing based on iris requirements
    results = results[0]
    result_classes = []
    content_categories = []
    results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    for i, key in enumerate(results):
      if results[key] > 0.80:
        result_classes.append(key)
        if results[key] > 0.95:
          break
      if i == 2: # in future, configure with topK sent via request
        break
    for ic_class in result_classes:
      category = self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY[ic_class]
      if category not in content_categories:
        content_categories.append(category)
    return [{
      "content_categories": content_categories,
      "classes": result_classes
    }]
