import logging
import torch
import torch.nn.functional as F
from ts.torch_handler.image_classifier import ImageClassifier as PImageClassifier
from ts.utils.util import map_class_to_label


logger = logging.getLogger(__name__)

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
    'UTILITY', 'backpack': 'UTILITY', 'bolo_tie':
    'UTILITY', 'bow_tie': 'UTILITY', 'buckle': 'UTILITY',
    'feather_boa': 'UTILITY', 'gasmask': 'UTILITY',
    'hair_slide': 'UTILITY', 'handkerchief': 'UTILITY',
    'lipstick': 'UTILITY', 'mailbag': 'UTILITY',
    'neck_brace': 'UTILITY', 'necklace': 'UTILITY', 'purse':
    'UTILITY', 'sleeping_bag': 'UTILITY', 'stole':
    'UTILITY', 'umbrella': 'UTILITY', 'wallet':
    'UTILITY', 'airliner': 'TRAVEL', 'airship': 'TRAVEL',
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
    'barrel': 'UTILITY', 'carton': 'UTILITY', 'chest':
    'UTILITY', 'crate': 'UTILITY', 'medicine_chest':
    'UTILITY', 'milk_can': 'UTILITY', 'packet':
    'UTILITY', 'pill_bottle': 'UTILITY', 'plastic_bag':
    'UTILITY', 'rain_barrel': 'UTILITY', 'safe':
    'UTILITY', 'shopping_basket': 'UTILITY', 'shopping_cart':
    'UTILITY', 'vault': 'UTILITY', 'washbasin':
    'UTILITY', 'water_bottle': 'UTILITY', 'water_jug':
    'UTILITY', 'whiskey_jug': 'UTILITY', 'Crock_Pot':
    'UTILITY', 'Dutch_oven': 'UTILITY', 'caldron':
    'UTILITY', 'cleaver': 'UTILITY', 'cocktail_shaker':
    'UTILITY', 'coffee_mug': 'UTILITY', 'coffeepot':
    'UTILITY', 'corkscrew': 'UTILITY', 'cup': 'UTILITY',
    'espresso_maker': 'UTILITY', 'frying_pan': 'UTILITY',
    'goblet': 'UTILITY', 'hot_pot': 'UTILITY', 'ladle':
    'UTILITY', 'measuring_cup': 'UTILITY', 'mixing_bowl':
    'UTILITY', 'mortar': 'UTILITY', 'pitcher': 'UTILITY',
    'plate': 'UTILITY', 'pot': 'UTILITY', 'rotisserie':
    'UTILITY', 'soup_bowl': 'UTILITY', 'spatula':
    'UTILITY', 'strainer': 'UTILITY', 'teapot':
    'UTILITY', 'wok': 'UTILITY', 'wooden_spoon':
    'UTILITY', 'Christmas_stocking': 'UTILITY', 'analog_clock':
    'UTILITY', 'bath_towel': 'UTILITY', 'brass':
    'UTILITY', 'dishrag': 'UTILITY', 'doormat':
    'UTILITY', 'hamper': 'UTILITY', 'lampshade':
    'UTILITY', 'piggy_bank': 'UTILITY', 'pillow':
    'UTILITY', 'plate_rack': 'UTILITY', 'prayer_rug':
    'UTILITY', 'quilt': 'UTILITY', 'screen': 'UTILITY',
    'shower_curtain': 'UTILITY', 'soap_dispenser': 'UTILITY',
    'table_lamp': 'UTILITY', 'theater_curtain': 'UTILITY',
    'tray': 'UTILITY', 'vase': 'UTILITY',
    'window_screen': 'UTILITY', 'window_shade': 'UTILITY',
    'CD_player': 'UTILITY', 'Polaroid_camera': 'UTILITY',
    'cassette_player': 'UTILITY', 'cellular_telephone':
    'UTILITY', 'computer_keyboard': 'UTILITY', 'desktop_computer':
    'UTILITY', 'dial_telephone': 'UTILITY', 'digital_clock':
    'UTILITY', 'digital_watch': 'UTILITY', 'dishwasher':
    'UTILITY', 'electric_fan': 'UTILITY', 'hand-held_computer':
    'UTILITY', 'hand_blower': 'UTILITY', 'hard_disc':
    'UTILITY', 'iPod': 'UTILITY', 'joystick': 'UTILITY',
    'laptop': 'UTILITY', 'loudspeaker': 'UTILITY',
    'microphone': 'UTILITY', 'microwave': 'UTILITY',
    'modem': 'UTILITY', 'monitor': 'UTILITY',
    'odometer': 'UTILITY', 'oscilloscope': 'UTILITY',
    'parking_meter': 'UTILITY', 'pay-phone': 'UTILITY',
    'photocopier': 'UTILITY', 'power_drill': 'UTILITY',
    'printer': 'UTILITY', 'projector': 'UTILITY',
    'radiator': 'UTILITY', 'radio': 'UTILITY',
    'reflex_camera': 'UTILITY', 'remote_control': 'UTILITY',
    'scale': 'UTILITY', 'slot': 'UTILITY', 'space_bar':
    'UTILITY', 'space_heater': 'UTILITY', 'spotlight':
    'UTILITY', 'stopwatch': 'UTILITY', 'switch':
    'UTILITY', 'tape_player': 'UTILITY', 'television':
    'UTILITY', 'toaster': 'UTILITY', 'traffic_light':
    'UTILITY', 'typewriter_keyboard': 'UTILITY', 'vacuum':
    'UTILITY', 'waffle_iron': 'UTILITY', 'washer':
    'UTILITY', 'chainlink_fence': 'HOUSES', 'picket_fence':
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
    'wine_bottle': 'FOOD', 'altar': 'UTILITY', 'ashcan':
    'UTILITY', 'bannister': 'UTILITY', 'barber_chair':
    'UTILITY', 'bassinet': 'UTILITY', 'bathtub':
    'UTILITY', 'bookcase': 'UTILITY', 'chiffonier':
    'UTILITY', 'china_cabinet': 'UTILITY', 'cradle':
    'UTILITY', 'crib': 'UTILITY', 'desk': 'UTILITY',
    'dining_table': 'UTILITY', 'entertainment_center':
    'UTILITY', 'file': 'UTILITY', 'fire_screen':
    'UTILITY', 'folding_chair': 'UTILITY', 'four-poster':
    'UTILITY', 'mailbox': 'UTILITY', 'park_bench':
    'UTILITY', 'pedestal': 'UTILITY', 'pool_table':
    'UTILITY', 'refrigerator': 'UTILITY', 'rocking_chair':
    'UTILITY', 'shoji': 'UTILITY', 'sliding_door':
    'UTILITY', 'stage': 'UTILITY', 'stove': 'UTILITY',
    'stretcher': 'UTILITY', 'studio_couch': 'UTILITY',
    'throne': 'UTILITY', 'toilet_seat': 'UTILITY',
    'tub': 'UTILITY', 'wardrobe': 'UTILITY',
    'bathing_cap': 'UTILITY', 'bearskin': 'UTILITY',
    'bonnet': 'UTILITY', 'crash_helmet': 'UTILITY',
    'mortarboard': 'UTILITY', 'shower_cap': 'UTILITY',
    'sombrero': 'UTILITY', 'pickelhaube': 'UTILITY',
    'French_horn': 'UTILITY', 'accordion': 'UTILITY',
    'acoustic_guitar': 'UTILITY', 'banjo': 'UTILITY', 'bassoon':
    'UTILITY', 'cello': 'UTILITY', 'chime': 'UTILITY',
    'cornet': 'UTILITY', 'drum': 'UTILITY', 'drumstick':
    'UTILITY', 'electric_guitar': 'UTILITY', 'flute':
    'UTILITY', 'gong': 'UTILITY', 'grand_piano':
    'UTILITY', 'harmonica': 'UTILITY', 'harp': 'UTILITY',
    'maraca': 'UTILITY', 'marimba': 'UTILITY', 'oboe':
    'UTILITY', 'ocarina': 'UTILITY', 'organ': 'UTILITY',
    'panpipe': 'UTILITY', 'pick': 'UTILITY', 'sax':
    'UTILITY', 'steel_drum': 'UTILITY', 'trombone':
    'UTILITY', 'upright': 'UTILITY', 'violin': 'UTILITY',
    'Petri_dish': 'UTILITY', 'beaker': 'UTILITY',
    'Band_Aid': 'UTILITY', 'bottlecap': 'UTILITY',
    'bubble': 'UTILITY', 'face_powder': 'UTILITY',
    'hair_spray': 'UTILITY', 'hay': 'UTILITY', 'honeycomb':
    'UTILITY', 'knot': 'UTILITY', 'lotion': 'UTILITY',
    'mosquito_net': 'UTILITY', 'muzzle': 'UTILITY', 'nipple':
    'UTILITY', 'pencil_box': 'UTILITY', 'perfume':
    'UTILITY', 'sunscreen': 'UTILITY', 'toilet_tissue':
    'UTILITY', 'velvet': 'UTILITY', 'wing': 'UTILITY',
    'wool': 'UTILITY', 'alp': 'LANDSCAPES', 'apiary':
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
    'UTILITY', 'book_jacket': 'UTILITY', 'comic_book':
    'UTILITY', 'crossword_puzzle': 'UTILITY', 'envelope':
    'UTILITY', 'jigsaw_puzzle': 'UTILITY', 'menu':
    'UTILITY', 'notebook': 'UTILITY', 'paper_towel':
    'UTILITY', 'balance_beam': 'SPORT', 'barbell':
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
    'ballpoint': 'UTILITY', 'barrow': 'UTILITY',
    'binoculars': 'UTILITY', 'broom': 'UTILITY', 'bucket':
    'UTILITY', 'can_opener': 'UTILITY', 'candle':
    'UTILITY', "carpenter's_kit": 'UTILITY', 'chain':
    'UTILITY', 'chain_saw': 'UTILITY', 'crutch':
    'UTILITY', 'dumbbell': 'UTILITY', 'fountain_pen':
    'UTILITY', 'hammer': 'UTILITY', 'hatchet': 'UTILITY',
    'hook': 'UTILITY', 'iron': 'UTILITY',
    'letter_opener': 'UTILITY', 'lighter': 'UTILITY', 'loupe':
    'UTILITY', 'magnetic_compass': 'UTILITY', 'matchstick':
    'UTILITY', 'nail': 'UTILITY', 'paintbrush':
    'UTILITY', 'pencil_sharpener': 'UTILITY', 'plane':
    'UTILITY', 'plunger': 'UTILITY', "potter's_wheel":
    'UTILITY', 'quill': 'UTILITY', 'rubber_eraser':
    'UTILITY', 'rule': 'UTILITY', 'safety_pin':
    'UTILITY', 'screw': 'UTILITY', 'screwdriver':
    'UTILITY', 'shield': 'UTILITY', 'shovel': 'UTILITY',
    'stethoscope': 'UTILITY', 'sunglass': 'UTILITY', 'swab':
    'UTILITY', 'syringe': 'UTILITY', 'thimble':
    'UTILITY', 'torch': 'UTILITY', 'whistle': 'UTILITY',
    'balloon': 'BIRTHDAYS', 'pinwheel': 'BIRTHDAYS', 'swing':
    'BIRTHDAYS', 'teddy': 'BIRTHDAYS', 'bullet_train':
    'TRAVEL', 'electric_locomotive': 'TRAVEL', 'freight_car':
    'TRAVEL', 'steam_locomotive': 'TRAVEL', 'Model_T':
    'UTILITY', 'ambulance': 'UTILITY', 'amphibian':
    'UTILITY', 'beach_wagon': 'UTILITY', 'bicycle-built-for-two':
    'UTILITY', 'bobsled': 'UTILITY', 'cab': 'UTILITY',
    'convertible': 'UTILITY', 'crane': 'UTILITY', 'dogsled':
    'UTILITY', 'fire_engine': 'UTILITY', 'forklift':
    'UTILITY', 'garbage_truck': 'UTILITY', 'go-kart':
    'UTILITY', 'golfcart': 'UTILITY', 'grille':
    'UTILITY', 'half_track': 'UTILITY', 'harvester':
    'UTILITY', 'horse_cart': 'UTILITY', 'jeep':
    'UTILITY', 'jinrikisha': 'UTILITY', 'lawn_mower':
    'UTILITY', 'limousine': 'UTILITY', 'minibus':
    'UTILITY', 'minivan': 'UTILITY', 'moped': 'UTILITY',
    'motor_scooter': 'UTILITY', 'mountain_bike': 'UTILITY',
    'moving_van': 'UTILITY', 'oxcart': 'UTILITY',
    'passenger_car': 'UTILITY', 'pickup': 'UTILITY', 'plow':
    'UTILITY', 'police_van': 'UTILITY', 'racer':
    'UTILITY', 'recreational_vehicle': 'UTILITY', 'school_bus':
    'UTILITY', 'snowmobile': 'UTILITY', 'snowplow':
    'UTILITY', 'sports_car': 'UTILITY', 'streetcar':
    'UTILITY', 'tank': 'UTILITY', 'thresher': 'UTILITY',
    'tow_truck': 'UTILITY', 'tractor': 'UTILITY',
    'trailer_truck': 'UTILITY', 'tricycle': 'UTILITY',
    'trolleybus': 'UTILITY', 'unicycle': 'UTILITY',
    'assault_rifle': 'UTILITY', 'bow': 'UTILITY', 'cannon':
    'UTILITY', 'guillotine': 'UTILITY', 'holster':
    'UTILITY', 'missile': 'UTILITY', 'projectile':
    'UTILITY', 'revolver': 'UTILITY', 'rifle': 'UTILITY',
    'scabbard': 'UTILITY',
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
    logger.info(f'classified_categories: {results}')
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
