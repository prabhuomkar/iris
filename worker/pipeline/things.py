"""Things"""
import requests
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from .utils import get_image_classification_classes, get_object_detection_classes
from .component import Component


class Things(Component):
  """Things Component"""
  def __init__(self, db, oid, image_url, mime_type):
    super().__init__('things', db, oid, image_url, mime_type)
    self.INFERENCE_TYPES = [
      'object_detection', 'image_classification'
    ]
    self.MODELS = [
      'maskrcnn', 'resnet152'
    ]
    self.CONTENT_CATEGORIES = [
      'ANIMALS', 'FOOD', 'GARDENS', 'SPORT', 'PEOPLE', 'TRAVEL', 'WEDDINGS',
      'LANDSCAPES', 'SCREENSHOTS', 'WHITEBOARDS', 'BIRTHDAYS', 'NIGHT', 'FLOWERS',
      'SELFIES', 'CITYSCAPES', 'ARTS', 'CRAFTS', 'HOLIDAYS', 'FASHION', 'LANDMARKS',
      'PERFORMANCES', 'RECEIPTS', 'DOCUMENTS', 'HOUSES', 'PETS', 'UTILITY',
    ]
    self.OBJECT_DETECTION_CLASSES_TO_CATEGORY = {
      'bird': self.CONTENT_CATEGORIES[0], 'cat': self.CONTENT_CATEGORIES[0],
      'dog': self.CONTENT_CATEGORIES[0], 'horse': self.CONTENT_CATEGORIES[0],
      'sheep': self.CONTENT_CATEGORIES[0], 'cow': self.CONTENT_CATEGORIES[0],
      'elephant': self.CONTENT_CATEGORIES[0], 'bear': self.CONTENT_CATEGORIES[0],
      'zebra': self.CONTENT_CATEGORIES[0], 'giraffe': self.CONTENT_CATEGORIES[0],
      'banana': self.CONTENT_CATEGORIES[1], 'apple': self.CONTENT_CATEGORIES[1],
      'sandwich': self.CONTENT_CATEGORIES[1], 'orange': self.CONTENT_CATEGORIES[1],
      'broccoli': self.CONTENT_CATEGORIES[1], 'carrot': self.CONTENT_CATEGORIES[1],
      'hot dog': self.CONTENT_CATEGORIES[1], 'pizza': self.CONTENT_CATEGORIES[1],
      'donut': self.CONTENT_CATEGORIES[1], 'cake': self.CONTENT_CATEGORIES[1],
      'potted plant': self.CONTENT_CATEGORIES[2],
      'frisbee': self.CONTENT_CATEGORIES[3], 'skis': self.CONTENT_CATEGORIES[3],
      'snowboard': self.CONTENT_CATEGORIES[3], 'sports ball': self.CONTENT_CATEGORIES[3],
      'kite': self.CONTENT_CATEGORIES[3], 'baseball bat': self.CONTENT_CATEGORIES[3],
      'baseball glove': self.CONTENT_CATEGORIES[3], 'skateboard': self.CONTENT_CATEGORIES[3],
      'surfboard': self.CONTENT_CATEGORIES[3], 'tennis racket': self.CONTENT_CATEGORIES[3],
      'person': self.CONTENT_CATEGORIES[4],
      'bicycle': self.CONTENT_CATEGORIES[5], 'car': self.CONTENT_CATEGORIES[5],
      'motorcycle': self.CONTENT_CATEGORIES[5], 'airplane': self.CONTENT_CATEGORIES[5],
      'bus': self.CONTENT_CATEGORIES[5], 'train': self.CONTENT_CATEGORIES[5],
      'truck': self.CONTENT_CATEGORIES[5], 'boat': self.CONTENT_CATEGORIES[5]
    }
    self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY = {
      'barn_spider': self.CONTENT_CATEGORIES[0], 'black_and_gold_garden_spider':
      self.CONTENT_CATEGORIES[0], 'black_widow': self.CONTENT_CATEGORIES[0], 'garden_spider':
      self.CONTENT_CATEGORIES[0], 'harvestman': self.CONTENT_CATEGORIES[0], 'scorpion':
      self.CONTENT_CATEGORIES[0], 'tarantula': self.CONTENT_CATEGORIES[0], 'wolf_spider':
      self.CONTENT_CATEGORIES[0], 'armadillo': self.CONTENT_CATEGORIES[0], 'American_black_bear':
      self.CONTENT_CATEGORIES[0], 'brown_bear': self.CONTENT_CATEGORIES[0], 'ice_bear':
      self.CONTENT_CATEGORIES[0], 'giant_panda': self.CONTENT_CATEGORIES[0], 'lesser_panda':
      self.CONTENT_CATEGORIES[0], 'African_grey': self.CONTENT_CATEGORIES[0], 'American_coot':
      self.CONTENT_CATEGORIES[0], 'American_egret': self.CONTENT_CATEGORIES[0], 'European_gallinule':
      self.CONTENT_CATEGORIES[0], 'albatross': self.CONTENT_CATEGORIES[0], 'bald_eagle':
      self.CONTENT_CATEGORIES[0], 'bee_eater': self.CONTENT_CATEGORIES[0], 'bittern':
      self.CONTENT_CATEGORIES[0], 'black_grouse': self.CONTENT_CATEGORIES[0], 'black_stork':
      self.CONTENT_CATEGORIES[0], 'black_swan': self.CONTENT_CATEGORIES[0], 'brambling':
      self.CONTENT_CATEGORIES[0], 'bulbul': self.CONTENT_CATEGORIES[0], 'bustard': self.CONTENT_CATEGORIES[0],
      'chickadee': self.CONTENT_CATEGORIES[0], 'cock': self.CONTENT_CATEGORIES[0], 'coucal':
      self.CONTENT_CATEGORIES[0], 'crane (bird)': self.CONTENT_CATEGORIES[0], 'dowitcher':
      self.CONTENT_CATEGORIES[0], 'drake': self.CONTENT_CATEGORIES[0], 'flamingo': self.CONTENT_CATEGORIES[0],
      'goldfinch': self.CONTENT_CATEGORIES[0], 'goose': self.CONTENT_CATEGORIES[0],
      'great_grey_owl': self.CONTENT_CATEGORIES[0], 'hen': self.CONTENT_CATEGORIES[0], 'hornbill':
      self.CONTENT_CATEGORIES[0], 'house_finch': self.CONTENT_CATEGORIES[0], 'hummingbird':
      self.CONTENT_CATEGORIES[0], 'indigo_bunting': self.CONTENT_CATEGORIES[0], 'jacamar':
      self.CONTENT_CATEGORIES[0], 'jay': self.CONTENT_CATEGORIES[0], 'junco': self.CONTENT_CATEGORIES[0],
      'king_penguin': self.CONTENT_CATEGORIES[0], 'kite': self.CONTENT_CATEGORIES[0], 'limpkin':
      self.CONTENT_CATEGORIES[0], 'little_blue_heron': self.CONTENT_CATEGORIES[0], 'lorikeet':
      self.CONTENT_CATEGORIES[0], 'macaw': self.CONTENT_CATEGORIES[0], 'magpie': self.CONTENT_CATEGORIES[0],
      'ostrich': self.CONTENT_CATEGORIES[0], 'oystercatcher': self.CONTENT_CATEGORIES[0],
      'partridge': self.CONTENT_CATEGORIES[0], 'peacock': self.CONTENT_CATEGORIES[0], 'pelican':
      self.CONTENT_CATEGORIES[0], 'prairie_chicken': self.CONTENT_CATEGORIES[0], 'ptarmigan':
      self.CONTENT_CATEGORIES[0], 'quail': self.CONTENT_CATEGORIES[0], 'red-backed_sandpiper':
      self.CONTENT_CATEGORIES[0], 'red-breasted_merganser': self.CONTENT_CATEGORIES[0], 'redshank':
      self.CONTENT_CATEGORIES[0], 'robin': self.CONTENT_CATEGORIES[0], 'ruddy_turnstone':
      self.CONTENT_CATEGORIES[0], 'ruffed_grouse': self.CONTENT_CATEGORIES[0], 'spoonbill':
      self.CONTENT_CATEGORIES[0], 'sulphur-crested_cockatoo': self.CONTENT_CATEGORIES[0], 'toucan':
      self.CONTENT_CATEGORIES[0], 'vulture': self.CONTENT_CATEGORIES[0], 'water_ouzel':
      self.CONTENT_CATEGORIES[0], 'white_stork': self.CONTENT_CATEGORIES[0], 'ant': self.CONTENT_CATEGORIES[0],
      'bee': self.CONTENT_CATEGORIES[0], 'centipede': self.CONTENT_CATEGORIES[0], 'cicada':
      self.CONTENT_CATEGORIES[0], 'cockroach': self.CONTENT_CATEGORIES[0], 'cricket':
      self.CONTENT_CATEGORIES[0], 'damselfly': self.CONTENT_CATEGORIES[0], 'dragonfly':
      self.CONTENT_CATEGORIES[0], 'flatworm': self.CONTENT_CATEGORIES[0], 'fly': self.CONTENT_CATEGORIES[0],
      'grasshopper': self.CONTENT_CATEGORIES[0], 'ground_beetle': self.CONTENT_CATEGORIES[0],
      'lacewing': self.CONTENT_CATEGORIES[0], 'ladybug': self.CONTENT_CATEGORIES[0],
      'long-horned_beetle': self.CONTENT_CATEGORIES[0], 'mantis': self.CONTENT_CATEGORIES[0], 'nematode':
      self.CONTENT_CATEGORIES[0], 'rhinoceros_beetle': self.CONTENT_CATEGORIES[0], 'tick':
      self.CONTENT_CATEGORIES[0], 'tiger_beetle': self.CONTENT_CATEGORIES[0], 'weevil':
      self.CONTENT_CATEGORIES[0], 'dung_beetle': self.CONTENT_CATEGORIES[0], 'leaf_beetle':
      self.CONTENT_CATEGORIES[0], 'leafhopper': self.CONTENT_CATEGORIES[0], 'walking_stick':
      self.CONTENT_CATEGORIES[0], 'admiral': self.CONTENT_CATEGORIES[0], 'cabbage_butterfly':
      self.CONTENT_CATEGORIES[0], 'lycaenid': self.CONTENT_CATEGORIES[0], 'monarch': self.CONTENT_CATEGORIES[0],
      'ringlet': self.CONTENT_CATEGORIES[0], 'sulphur_butterfly': self.CONTENT_CATEGORIES[0],
      'Egyptian_cat': self.CONTENT_CATEGORIES[0], 'Persian_cat': self.CONTENT_CATEGORIES[0],
      'Siamese_cat': self.CONTENT_CATEGORIES[0], 'tabby': self.CONTENT_CATEGORIES[0],
      'brain_coral': self.CONTENT_CATEGORIES[0], 'coral_fungus': self.CONTENT_CATEGORIES[0],
      'coral_reef': self.CONTENT_CATEGORIES[0], 'rock_beauty': self.CONTENT_CATEGORIES[0],
      'sea_anemone': self.CONTENT_CATEGORIES[0], 'African_crocodile': self.CONTENT_CATEGORIES[0],
      'American_alligator': self.CONTENT_CATEGORIES[0], 'American_lobster': self.CONTENT_CATEGORIES[0],
      'Dungeness_crab': self.CONTENT_CATEGORIES[0], 'crayfish': self.CONTENT_CATEGORIES[0],
      'fiddler_crab': self.CONTENT_CATEGORIES[0], 'hermit_crab': self.CONTENT_CATEGORIES[0],
      'isopod': self.CONTENT_CATEGORIES[0], 'king_crab': self.CONTENT_CATEGORIES[0],
      'rock_crab': self.CONTENT_CATEGORIES[0], 'spiny_lobster': self.CONTENT_CATEGORIES[0],
      'triceratops': self.CONTENT_CATEGORIES[0], 'Afghan_hound': self.CONTENT_CATEGORIES[0],
      'African_hunting_dog': self.CONTENT_CATEGORIES[0], 'Airedale': self.CONTENT_CATEGORIES[0],
      'American_Staffordshire_terrier': self.CONTENT_CATEGORIES[0], 'Appenzeller': self.CONTENT_CATEGORIES[0],
      'Australian_terrier': self.CONTENT_CATEGORIES[0], 'Bedlington_terrier': self.CONTENT_CATEGORIES[0],
      'Bernese_mountain_dog': self.CONTENT_CATEGORIES[0], 'Blenheim_spaniel': self.CONTENT_CATEGORIES[0],
      'Border_collie': self.CONTENT_CATEGORIES[0], 'Border_terrier': self.CONTENT_CATEGORIES[0],
      'Boston_bull': self.CONTENT_CATEGORIES[0], 'Bouvier_des_Flandres':
      self.CONTENT_CATEGORIES[0], 'Brabancon_griffon': self.CONTENT_CATEGORIES[0], 'Brittany_spaniel':
      self.CONTENT_CATEGORIES[0], 'Cardigan': self.CONTENT_CATEGORIES[0], 'Chesapeake_Bay_retriever':
      self.CONTENT_CATEGORIES[0], 'Chihuahua': self.CONTENT_CATEGORIES[0], 'Dandie_Dinmont':
      self.CONTENT_CATEGORIES[0], 'Doberman': self.CONTENT_CATEGORIES[0], 'English_foxhound':
      self.CONTENT_CATEGORIES[0], 'English_setter': self.CONTENT_CATEGORIES[0], 'English_springer':
      self.CONTENT_CATEGORIES[0], 'EntleBucher': self.CONTENT_CATEGORIES[0], 'Eskimo_dog':
      self.CONTENT_CATEGORIES[0], 'French_bulldog': self.CONTENT_CATEGORIES[0], 'German_shepherd':
      self.CONTENT_CATEGORIES[0], 'German_short-haired_pointer': self.CONTENT_CATEGORIES[0], 'Gordon_setter':
      self.CONTENT_CATEGORIES[0], 'Great_Dane': self.CONTENT_CATEGORIES[0], 'Great_Pyrenees':
      self.CONTENT_CATEGORIES[0], 'Greater_Swiss_Mountain_dog': self.CONTENT_CATEGORIES[0], 'Ibizan_hound':
      self.CONTENT_CATEGORIES[0], 'Irish_setter': self.CONTENT_CATEGORIES[0], 'Irish_terrier':
      self.CONTENT_CATEGORIES[0], 'Irish_water_spaniel': self.CONTENT_CATEGORIES[0], 'Irish_wolfhound':
      self.CONTENT_CATEGORIES[0], 'Italian_greyhound': self.CONTENT_CATEGORIES[0], 'Japanese_spaniel':
      self.CONTENT_CATEGORIES[0], 'Kerry_blue_terrier': self.CONTENT_CATEGORIES[0], 'Labrador_retriever':
      self.CONTENT_CATEGORIES[0], 'Lakeland_terrier': self.CONTENT_CATEGORIES[0], 'Leonberg':
      self.CONTENT_CATEGORIES[0], 'Lhasa': self.CONTENT_CATEGORIES[0], 'Maltese_dog':
      self.CONTENT_CATEGORIES[0], 'Mexican_hairless': self.CONTENT_CATEGORIES[0], 'Newfoundland':
      self.CONTENT_CATEGORIES[0], 'Norfolk_terrier': self.CONTENT_CATEGORIES[0], 'Norwegian_elkhound':
      self.CONTENT_CATEGORIES[0], 'Norwich_terrier': self.CONTENT_CATEGORIES[0], 'Old_English_sheepdog':
      self.CONTENT_CATEGORIES[0], 'Pekinese': self.CONTENT_CATEGORIES[0], 'Pembroke':
      self.CONTENT_CATEGORIES[0], 'Pomeranian': self.CONTENT_CATEGORIES[0], 'Rhodesian_ridgeback':
      self.CONTENT_CATEGORIES[0], 'Rottweiler': self.CONTENT_CATEGORIES[0], 'Saint_Bernard':
      self.CONTENT_CATEGORIES[0], 'Saluki': self.CONTENT_CATEGORIES[0], 'Samoyed': self.CONTENT_CATEGORIES[0],
      'Scotch_terrier': self.CONTENT_CATEGORIES[0], 'Scottish_deerhound': self.CONTENT_CATEGORIES[0],
      'Sealyham_terrier': self.CONTENT_CATEGORIES[0], 'Shetland_sheepdog': self.CONTENT_CATEGORIES[0],
      'Shih-Tzu': self.CONTENT_CATEGORIES[0], 'Siberian_husky': self.CONTENT_CATEGORIES[0],
      'Staffordshire_bullterrier': self.CONTENT_CATEGORIES[0], 'Sussex_spaniel': self.CONTENT_CATEGORIES[0],
      'Tibetan_mastiff': self.CONTENT_CATEGORIES[0], 'Tibetan_terrier': self.CONTENT_CATEGORIES[0],
      'Walker_hound': self.CONTENT_CATEGORIES[0], 'Weimaraner': self.CONTENT_CATEGORIES[0],
      'Welsh_springer_spaniel': self.CONTENT_CATEGORIES[0], 'West_Highland_white_terrier':
      self.CONTENT_CATEGORIES[0], 'Yorkshire_terrier': self.CONTENT_CATEGORIES[0], 'affenpinscher':
      self.CONTENT_CATEGORIES[0], 'basenji': self.CONTENT_CATEGORIES[0], 'basset': self.CONTENT_CATEGORIES[0],
      'beagle': self.CONTENT_CATEGORIES[0], 'black-and-tan_coonhound':
      self.CONTENT_CATEGORIES[0], 'bloodhound': self.CONTENT_CATEGORIES[0], 'bluetick':
      self.CONTENT_CATEGORIES[0], 'borzoi': self.CONTENT_CATEGORIES[0], 'boxer': self.CONTENT_CATEGORIES[0],
      'briard': self.CONTENT_CATEGORIES[0], 'bull_mastiff': self.CONTENT_CATEGORIES[0],
      'cairn': self.CONTENT_CATEGORIES[0], 'chow': self.CONTENT_CATEGORIES[0], 'clumber':
      self.CONTENT_CATEGORIES[0], 'cocker_spaniel': self.CONTENT_CATEGORIES[0], 'collie':
      self.CONTENT_CATEGORIES[0], 'curly-coated_retriever': self.CONTENT_CATEGORIES[0], 'dalmatian':
      self.CONTENT_CATEGORIES[0], 'flat-coated_retriever': self.CONTENT_CATEGORIES[0], 'giant_schnauzer':
      self.CONTENT_CATEGORIES[0], 'golden_retriever': self.CONTENT_CATEGORIES[0], 'groenendael':
      self.CONTENT_CATEGORIES[0], 'keeshond': self.CONTENT_CATEGORIES[0], 'kelpie': self.CONTENT_CATEGORIES[0],
      'komondor': self.CONTENT_CATEGORIES[0], 'kuvasz': self.CONTENT_CATEGORIES[0], 'malamute':
      self.CONTENT_CATEGORIES[0], 'malinois': self.CONTENT_CATEGORIES[0], 'miniature_pinscher':
      self.CONTENT_CATEGORIES[0], 'miniature_poodle': self.CONTENT_CATEGORIES[0], 'miniature_schnauzer':
      self.CONTENT_CATEGORIES[0], 'otterhound': self.CONTENT_CATEGORIES[0], 'papillon':
      self.CONTENT_CATEGORIES[0], 'pug': self.CONTENT_CATEGORIES[0], 'redbone': self.CONTENT_CATEGORIES[0],
      'schipperke': self.CONTENT_CATEGORIES[0], 'silky_terrier': self.CONTENT_CATEGORIES[0],
      'soft-coated_wheaten_terrier': self.CONTENT_CATEGORIES[0], 'standard_poodle': self.CONTENT_CATEGORIES[0],
      'standard_schnauzer': self.CONTENT_CATEGORIES[0], 'toy_poodle': self.CONTENT_CATEGORIES[0],
      'toy_terrier': self.CONTENT_CATEGORIES[0], 'vizsla': self.CONTENT_CATEGORIES[0], 'whippet':
      self.CONTENT_CATEGORIES[0], 'wire-haired_fox_terrier': self.CONTENT_CATEGORIES[0], 'sea_cucumber':
      self.CONTENT_CATEGORIES[0], 'sea_urchin': self.CONTENT_CATEGORIES[0], 'starfish':
      self.CONTENT_CATEGORIES[0], 'badger': self.CONTENT_CATEGORIES[0], 'black-footed_ferret':
      self.CONTENT_CATEGORIES[0], 'mink': self.CONTENT_CATEGORIES[0], 'otter': self.CONTENT_CATEGORIES[0],
      'polecat': self.CONTENT_CATEGORIES[0], 'skunk': self.CONTENT_CATEGORIES[0], 'weasel':
      self.CONTENT_CATEGORIES[0], 'anemone_fish': self.CONTENT_CATEGORIES[0], 'barracouta':
      self.CONTENT_CATEGORIES[0], 'eel': self.CONTENT_CATEGORIES[0], 'electric_ray': self.CONTENT_CATEGORIES[0],
      'gar': self.CONTENT_CATEGORIES[0], 'goldfish': self.CONTENT_CATEGORIES[0],
      'lionfish': self.CONTENT_CATEGORIES[0], 'puffer': self.CONTENT_CATEGORIES[0], 'sea_snake':
      self.CONTENT_CATEGORIES[0], 'sturgeon': self.CONTENT_CATEGORIES[0], 'tench': self.CONTENT_CATEGORIES[0],
      'jellyfish': self.CONTENT_CATEGORIES[0], 'stingray': self.CONTENT_CATEGORIES[0], 'cardoon':
      self.CONTENT_CATEGORIES[12], 'daisy': self.CONTENT_CATEGORIES[12], 'hip': self.CONTENT_CATEGORIES[12],
      'rapeseed': self.CONTENT_CATEGORIES[12], "yellow_lady's_slipper":
      self.CONTENT_CATEGORIES[12], 'bullfrog': self.CONTENT_CATEGORIES[0], 'tailed_frog':
      self.CONTENT_CATEGORIES[0], 'tree_frog': self.CONTENT_CATEGORIES[0], 'Granny_Smith':
      self.CONTENT_CATEGORIES[1], 'acorn_squash': self.CONTENT_CATEGORIES[1], 'banana':
      self.CONTENT_CATEGORIES[1], 'custard_apple': self.CONTENT_CATEGORIES[1], 'fig':
      self.CONTENT_CATEGORIES[1], "jack-o'-lantern": self.CONTENT_CATEGORIES[1], 'jackfruit':
      self.CONTENT_CATEGORIES[1], 'lemon': self.CONTENT_CATEGORIES[1], 'orange': self.CONTENT_CATEGORIES[1],
      'pineapple': self.CONTENT_CATEGORIES[1], 'pomegranate': self.CONTENT_CATEGORIES[1],
      'spaghetti_squash': self.CONTENT_CATEGORIES[1], 'strawberry': self.CONTENT_CATEGORIES[1],
      'zucchini': self.CONTENT_CATEGORIES[1], 'agaric': self.CONTENT_CATEGORIES[2], 'bolete':
      self.CONTENT_CATEGORIES[2], 'earthstar': self.CONTENT_CATEGORIES[2], 'gyromitra':
      self.CONTENT_CATEGORIES[2], 'hen-of-the-woods': self.CONTENT_CATEGORIES[2], 'mushroom':
      self.CONTENT_CATEGORIES[2], 'stinkhorn': self.CONTENT_CATEGORIES[2], 'hog': self.CONTENT_CATEGORIES[0],
      'warthog': self.CONTENT_CATEGORIES[0], 'wild_boar': self.CONTENT_CATEGORIES[0],
      'African_chameleon': self.CONTENT_CATEGORIES[0], 'American_chameleon': self.CONTENT_CATEGORIES[0],
      'Gila_monster': self.CONTENT_CATEGORIES[0], 'Komodo_dragon': self.CONTENT_CATEGORIES[0],
      'agama': self.CONTENT_CATEGORIES[0], 'alligator_lizard': self.CONTENT_CATEGORIES[0],
      'banded_gecko': self.CONTENT_CATEGORIES[0], 'common_iguana': self.CONTENT_CATEGORIES[0],
      'frilled_lizard': self.CONTENT_CATEGORIES[0], 'green_lizard': self.CONTENT_CATEGORIES[0],
      'whiptail': self.CONTENT_CATEGORIES[0], 'dugong': self.CONTENT_CATEGORIES[0], 'sea_lion':
      self.CONTENT_CATEGORIES[0], 'grey_whale': self.CONTENT_CATEGORIES[0], 'killer_whale':
      self.CONTENT_CATEGORIES[0], 'koala': self.CONTENT_CATEGORIES[0], 'wallaby': self.CONTENT_CATEGORIES[0],
      'wombat': self.CONTENT_CATEGORIES[0], 'chambered_nautilus': self.CONTENT_CATEGORIES[0],
      'chiton': self.CONTENT_CATEGORIES[0], 'conch': self.CONTENT_CATEGORIES[0], 'sea_slug':
      self.CONTENT_CATEGORIES[0], 'slug': self.CONTENT_CATEGORIES[0], 'snail': self.CONTENT_CATEGORIES[0],
      'Madagascar_cat': self.CONTENT_CATEGORIES[0], 'meerkat': self.CONTENT_CATEGORIES[0], 'mongoose':
      self.CONTENT_CATEGORIES[0], 'echidna': self.CONTENT_CATEGORIES[0], 'platypus': self.CONTENT_CATEGORIES[0],
      'ballplayer': self.CONTENT_CATEGORIES[4], 'groom': self.CONTENT_CATEGORIES[4], 'pirate':
      self.CONTENT_CATEGORIES[4], 'scuba_diver': self.CONTENT_CATEGORIES[4], 'acorn':
      self.CONTENT_CATEGORIES[1], 'buckeye': self.CONTENT_CATEGORIES[1], 'sorrel': self.CONTENT_CATEGORIES[1],
      'baboon': self.CONTENT_CATEGORIES[0], 'capuchin': self.CONTENT_CATEGORIES[0],
      'chimpanzee': self.CONTENT_CATEGORIES[0], 'colobus': self.CONTENT_CATEGORIES[0], 'gibbon':
      self.CONTENT_CATEGORIES[0], 'gorilla': self.CONTENT_CATEGORIES[0], 'guenon': self.CONTENT_CATEGORIES[0],
      'howler_monkey': self.CONTENT_CATEGORIES[0], 'indri': self.CONTENT_CATEGORIES[0], 'langur':
      self.CONTENT_CATEGORIES[0], 'macaque': self.CONTENT_CATEGORIES[0], 'marmoset': self.CONTENT_CATEGORIES[0],
      'orangutan': self.CONTENT_CATEGORIES[0], 'patas': self.CONTENT_CATEGORIES[0],
      'proboscis_monkey': self.CONTENT_CATEGORIES[0], 'siamang': self.CONTENT_CATEGORIES[0],
      'spider_monkey': self.CONTENT_CATEGORIES[0], 'squirrel_monkey': self.CONTENT_CATEGORIES[0],
      'titi': self.CONTENT_CATEGORIES[0], 'Angora': self.CONTENT_CATEGORIES[0], 'hare':
      self.CONTENT_CATEGORIES[0], 'wood_rabbit': self.CONTENT_CATEGORIES[0], 'beaver':
      self.CONTENT_CATEGORIES[0], 'fox_squirrel': self.CONTENT_CATEGORIES[0], 'guinea_pig':
      self.CONTENT_CATEGORIES[0], 'hamster': self.CONTENT_CATEGORIES[0], 'marmot': self.CONTENT_CATEGORIES[0],
      'mouse': self.CONTENT_CATEGORIES[0], 'porcupine': self.CONTENT_CATEGORIES[0],
      'European_fire_salamander': self.CONTENT_CATEGORIES[0], 'axolotl': self.CONTENT_CATEGORIES[0],
      'common_newt': self.CONTENT_CATEGORIES[0], 'eft': self.CONTENT_CATEGORIES[0],
      'spotted_salamander': self.CONTENT_CATEGORIES[0], 'coho': self.CONTENT_CATEGORIES[0],
      'great_white_shark': self.CONTENT_CATEGORIES[0], 'hammerhead': self.CONTENT_CATEGORIES[0],
      'tiger_shark': self.CONTENT_CATEGORIES[0], 'sloth_bear': self.CONTENT_CATEGORIES[0],
      'three-toed_sloth': self.CONTENT_CATEGORIES[0], 'Indian_cobra': self.CONTENT_CATEGORIES[0],
      'boa_constrictor': self.CONTENT_CATEGORIES[0], 'diamondback': self.CONTENT_CATEGORIES[0],
      'garter_snake': self.CONTENT_CATEGORIES[0], 'green_mamba': self.CONTENT_CATEGORIES[0],
      'green_snake': self.CONTENT_CATEGORIES[0], 'hognose_snake': self.CONTENT_CATEGORIES[0],
      'horned_viper': self.CONTENT_CATEGORIES[0], 'king_snake': self.CONTENT_CATEGORIES[0],
      'night_snake': self.CONTENT_CATEGORIES[0], 'ringneck_snake': self.CONTENT_CATEGORIES[0],
      'rock_python': self.CONTENT_CATEGORIES[0], 'sidewinder': self.CONTENT_CATEGORIES[0],
      'thunder_snake': self.CONTENT_CATEGORIES[0], 'vine_snake': self.CONTENT_CATEGORIES[0],
      'water_snake': self.CONTENT_CATEGORIES[0], 'trilobite': self.CONTENT_CATEGORIES[0],
      'box_turtle': self.CONTENT_CATEGORIES[0], 'leatherback_turtle': self.CONTENT_CATEGORIES[0],
      'loggerhead': self.CONTENT_CATEGORIES[0], 'mud_turtle': self.CONTENT_CATEGORIES[0],
      'terrapin': self.CONTENT_CATEGORIES[0], 'African_elephant': self.CONTENT_CATEGORIES[0],
      'Arabian_camel': self.CONTENT_CATEGORIES[0], 'Indian_elephant': self.CONTENT_CATEGORIES[0],
      'bighorn': self.CONTENT_CATEGORIES[0], 'bison': self.CONTENT_CATEGORIES[0], 'gazelle':
      self.CONTENT_CATEGORIES[0], 'hartebeest': self.CONTENT_CATEGORIES[0], 'hippopotamus':
      self.CONTENT_CATEGORIES[0], 'ibex': self.CONTENT_CATEGORIES[0], 'impala': self.CONTENT_CATEGORIES[0],
      'llama': self.CONTENT_CATEGORIES[0], 'ox': self.CONTENT_CATEGORIES[0], 'ram':
      self.CONTENT_CATEGORIES[0], 'tusker': self.CONTENT_CATEGORIES[0], 'zebra': self.CONTENT_CATEGORIES[0],
      'water_buffalo': self.CONTENT_CATEGORIES[0], 'artichoke': self.CONTENT_CATEGORIES[1],
      'bell_pepper': self.CONTENT_CATEGORIES[1], 'broccoli': self.CONTENT_CATEGORIES[1],
      'butternut_squash': self.CONTENT_CATEGORIES[1], 'cauliflower': self.CONTENT_CATEGORIES[1],
      'cucumber': self.CONTENT_CATEGORIES[1], 'head_cabbage': self.CONTENT_CATEGORIES[1],
      'cheetah': self.CONTENT_CATEGORIES[0], 'cougar': self.CONTENT_CATEGORIES[0], 'jaguar':
      self.CONTENT_CATEGORIES[0], 'leopard': self.CONTENT_CATEGORIES[0], 'lion': self.CONTENT_CATEGORIES[0],
      'lynx': self.CONTENT_CATEGORIES[0], 'snow_leopard': self.CONTENT_CATEGORIES[0],
      'tiger': self.CONTENT_CATEGORIES[0], 'tiger_cat': self.CONTENT_CATEGORIES[0],
      'Arctic_fox': self.CONTENT_CATEGORIES[0], 'coyote': self.CONTENT_CATEGORIES[0], 'dingo':
      self.CONTENT_CATEGORIES[0], 'grey_fox': self.CONTENT_CATEGORIES[0], 'hyena': self.CONTENT_CATEGORIES[0],
      'kit_fox': self.CONTENT_CATEGORIES[0], 'red_fox': self.CONTENT_CATEGORIES[0], 'red_wolf':
      self.CONTENT_CATEGORIES[0], 'timber_wolf': self.CONTENT_CATEGORIES[0], 'white_wolf':
      self.CONTENT_CATEGORIES[0], 'dhole': self.CONTENT_CATEGORIES[0], 'Windsor_tie':
      self.CONTENT_CATEGORIES[25], 'backpack': self.CONTENT_CATEGORIES[25], 'bolo_tie':
      self.CONTENT_CATEGORIES[25], 'bow_tie': self.CONTENT_CATEGORIES[25], 'buckle': self.CONTENT_CATEGORIES[25],
      'feather_boa': self.CONTENT_CATEGORIES[25], 'gasmask': self.CONTENT_CATEGORIES[25],
      'hair_slide': self.CONTENT_CATEGORIES[25], 'handkerchief': self.CONTENT_CATEGORIES[25],
      'lipstick': self.CONTENT_CATEGORIES[25], 'mailbag': self.CONTENT_CATEGORIES[25],
      'neck_brace': self.CONTENT_CATEGORIES[25], 'necklace': self.CONTENT_CATEGORIES[25], 'purse':
      self.CONTENT_CATEGORIES[25], 'sleeping_bag': self.CONTENT_CATEGORIES[25], 'stole':
      self.CONTENT_CATEGORIES[25], 'umbrella': self.CONTENT_CATEGORIES[25], 'wallet':
      self.CONTENT_CATEGORIES[25], 'airliner': self.CONTENT_CATEGORIES[5], 'airship': self.CONTENT_CATEGORIES[5],
      'parachute': self.CONTENT_CATEGORIES[5], 'space_shuttle': self.CONTENT_CATEGORIES[5],
      'warplane': self.CONTENT_CATEGORIES[5], 'baseball': self.CONTENT_CATEGORIES[3],
      'basketball': self.CONTENT_CATEGORIES[3], 'croquet_ball': self.CONTENT_CATEGORIES[3],
      'golf_ball': self.CONTENT_CATEGORIES[3], 'ping-pong_ball': self.CONTENT_CATEGORIES[3],
      'rugby_ball': self.CONTENT_CATEGORIES[3], 'soccer_ball': self.CONTENT_CATEGORIES[3],
      'tennis_ball': self.CONTENT_CATEGORIES[3], 'volleyball': self.CONTENT_CATEGORIES[3],
      'aircraft_carrier': self.CONTENT_CATEGORIES[5], 'canoe': self.CONTENT_CATEGORIES[5], 'catamaran':
      self.CONTENT_CATEGORIES[5], 'container_ship': self.CONTENT_CATEGORIES[5], 'fireboat':
      self.CONTENT_CATEGORIES[5], 'gondola': self.CONTENT_CATEGORIES[5], 'lifeboat': self.CONTENT_CATEGORIES[5],
      'liner': self.CONTENT_CATEGORIES[5], 'paddlewheel': self.CONTENT_CATEGORIES[5],
      'schooner': self.CONTENT_CATEGORIES[5], 'speedboat': self.CONTENT_CATEGORIES[5],
      'submarine': self.CONTENT_CATEGORIES[5], 'trimaran': self.CONTENT_CATEGORIES[5], 'wreck':
      self.CONTENT_CATEGORIES[5], 'yawl': self.CONTENT_CATEGORIES[5], 'bakery': self.CONTENT_CATEGORIES[14],
      'barbershop': self.CONTENT_CATEGORIES[14], 'barn': self.CONTENT_CATEGORIES[14], 'beacon':
      self.CONTENT_CATEGORIES[14], 'bell_cote': self.CONTENT_CATEGORIES[14], 'boathouse':
      self.CONTENT_CATEGORIES[14], 'bookshop': self.CONTENT_CATEGORIES[14], 'butcher_shop':
      self.CONTENT_CATEGORIES[14], 'carousel': self.CONTENT_CATEGORIES[14], 'castle':
      self.CONTENT_CATEGORIES[14], 'church': self.CONTENT_CATEGORIES[14], 'cinema': self.CONTENT_CATEGORIES[14],
      'cliff_dwelling': self.CONTENT_CATEGORIES[14], 'confectionery': self.CONTENT_CATEGORIES[14],
      'dome': self.CONTENT_CATEGORIES[14], 'greenhouse': self.CONTENT_CATEGORIES[14],
      'grocery_store': self.CONTENT_CATEGORIES[14], 'home_theater': self.CONTENT_CATEGORIES[14],
      'library': self.CONTENT_CATEGORIES[14], 'lumbermill': self.CONTENT_CATEGORIES[14],
      'mobile_home': self.CONTENT_CATEGORIES[14], 'monastery': self.CONTENT_CATEGORIES[14],
      'mosque': self.CONTENT_CATEGORIES[14], 'mountain_tent': self.CONTENT_CATEGORIES[14],
      'obelisk': self.CONTENT_CATEGORIES[14], 'palace': self.CONTENT_CATEGORIES[14], 'patio':
      self.CONTENT_CATEGORIES[14], 'planetarium': self.CONTENT_CATEGORIES[14], 'prison':
      self.CONTENT_CATEGORIES[14], 'restaurant': self.CONTENT_CATEGORIES[14], 'shoe_shop':
      self.CONTENT_CATEGORIES[14], 'stupa': self.CONTENT_CATEGORIES[14], 'thatch': self.CONTENT_CATEGORIES[14],
      'tile_roof': self.CONTENT_CATEGORIES[14], 'tobacco_shop': self.CONTENT_CATEGORIES[14],
      'toyshop': self.CONTENT_CATEGORIES[14], 'yurt': self.CONTENT_CATEGORIES[14], 'Loafer':
      self.CONTENT_CATEGORIES[18], 'abaya': self.CONTENT_CATEGORIES[18], 'academic_gown':
      self.CONTENT_CATEGORIES[18], 'apron': self.CONTENT_CATEGORIES[18], 'bib': self.CONTENT_CATEGORIES[18],
      'bikini': self.CONTENT_CATEGORIES[18], 'brassiere': self.CONTENT_CATEGORIES[18],
      'breastplate': self.CONTENT_CATEGORIES[18], 'bulletproof_vest': self.CONTENT_CATEGORIES[18],
      'cardigan': self.CONTENT_CATEGORIES[18], 'chain_mail': self.CONTENT_CATEGORIES[18],
      'cloak': self.CONTENT_CATEGORIES[18], 'clog': self.CONTENT_CATEGORIES[18],
      'cowboy_boot': self.CONTENT_CATEGORIES[18], 'cowboy_hat': self.CONTENT_CATEGORIES[18],
      'cuirass': self.CONTENT_CATEGORIES[18], 'diaper': self.CONTENT_CATEGORIES[18],
      'fur_coat': self.CONTENT_CATEGORIES[18], 'gown': self.CONTENT_CATEGORIES[18], 'hoopskirt':
      self.CONTENT_CATEGORIES[18], 'jean': self.CONTENT_CATEGORIES[18], 'jersey': self.CONTENT_CATEGORIES[18],
      'kimono': self.CONTENT_CATEGORIES[18], 'knee_pad': self.CONTENT_CATEGORIES[18],
      'lab_coat': self.CONTENT_CATEGORIES[18], 'maillot': self.CONTENT_CATEGORIES[18], 'mask':
      self.CONTENT_CATEGORIES[18], 'military_uniform': self.CONTENT_CATEGORIES[18], 'miniskirt':
      self.CONTENT_CATEGORIES[18], 'mitten': self.CONTENT_CATEGORIES[18], 'overskirt':
      self.CONTENT_CATEGORIES[18], 'oxygen_mask': self.CONTENT_CATEGORIES[18], 'pajama':
      self.CONTENT_CATEGORIES[18], 'poncho': self.CONTENT_CATEGORIES[18], 'running_shoe':
      self.CONTENT_CATEGORIES[18], 'sandal': self.CONTENT_CATEGORIES[18], 'sarong': self.CONTENT_CATEGORIES[18],
      'ski_mask': self.CONTENT_CATEGORIES[18], 'sock': self.CONTENT_CATEGORIES[18], 'suit':
      self.CONTENT_CATEGORIES[18], 'sunglasses': self.CONTENT_CATEGORIES[18], 'sweatshirt':
      self.CONTENT_CATEGORIES[18], 'swimming_trunks': self.CONTENT_CATEGORIES[18], 'trench_coat':
      self.CONTENT_CATEGORIES[18], 'vestment': self.CONTENT_CATEGORIES[18], 'wig': self.CONTENT_CATEGORIES[18],
      'barrel': self.CONTENT_CATEGORIES[25], 'carton': self.CONTENT_CATEGORIES[25], 'chest':
      self.CONTENT_CATEGORIES[25], 'crate': self.CONTENT_CATEGORIES[25], 'medicine_chest':
      self.CONTENT_CATEGORIES[25], 'milk_can': self.CONTENT_CATEGORIES[25], 'packet':
      self.CONTENT_CATEGORIES[25], 'pill_bottle': self.CONTENT_CATEGORIES[25], 'plastic_bag':
      self.CONTENT_CATEGORIES[25], 'rain_barrel': self.CONTENT_CATEGORIES[25], 'safe':
      self.CONTENT_CATEGORIES[25], 'shopping_basket': self.CONTENT_CATEGORIES[25], 'shopping_cart':
      self.CONTENT_CATEGORIES[25], 'vault': self.CONTENT_CATEGORIES[25], 'washbasin':
      self.CONTENT_CATEGORIES[25], 'water_bottle': self.CONTENT_CATEGORIES[25], 'water_jug':
      self.CONTENT_CATEGORIES[25], 'whiskey_jug': self.CONTENT_CATEGORIES[25], 'Crock_Pot':
      self.CONTENT_CATEGORIES[25], 'Dutch_oven': self.CONTENT_CATEGORIES[25], 'caldron':
      self.CONTENT_CATEGORIES[25], 'cleaver': self.CONTENT_CATEGORIES[25], 'cocktail_shaker':
      self.CONTENT_CATEGORIES[25], 'coffee_mug': self.CONTENT_CATEGORIES[25], 'coffeepot':
      self.CONTENT_CATEGORIES[25], 'corkscrew': self.CONTENT_CATEGORIES[25], 'cup': self.CONTENT_CATEGORIES[25],
      'espresso_maker': self.CONTENT_CATEGORIES[25], 'frying_pan': self.CONTENT_CATEGORIES[25],
      'goblet': self.CONTENT_CATEGORIES[25], 'hot_pot': self.CONTENT_CATEGORIES[25], 'ladle':
      self.CONTENT_CATEGORIES[25], 'measuring_cup': self.CONTENT_CATEGORIES[25], 'mixing_bowl':
      self.CONTENT_CATEGORIES[25], 'mortar': self.CONTENT_CATEGORIES[25], 'pitcher': self.CONTENT_CATEGORIES[25],
      'plate': self.CONTENT_CATEGORIES[25], 'pot': self.CONTENT_CATEGORIES[25], 'rotisserie':
      self.CONTENT_CATEGORIES[25], 'soup_bowl': self.CONTENT_CATEGORIES[25], 'spatula':
      self.CONTENT_CATEGORIES[25], 'strainer': self.CONTENT_CATEGORIES[25], 'teapot':
      self.CONTENT_CATEGORIES[25], 'wok': self.CONTENT_CATEGORIES[25], 'wooden_spoon':
      self.CONTENT_CATEGORIES[25], 'Christmas_stocking': self.CONTENT_CATEGORIES[25], 'analog_clock':
      self.CONTENT_CATEGORIES[25], 'bath_towel': self.CONTENT_CATEGORIES[25], 'brass':
      self.CONTENT_CATEGORIES[25], 'dishrag': self.CONTENT_CATEGORIES[25], 'doormat':
      self.CONTENT_CATEGORIES[25], 'hamper': self.CONTENT_CATEGORIES[25], 'lampshade':
      self.CONTENT_CATEGORIES[25], 'piggy_bank': self.CONTENT_CATEGORIES[25], 'pillow':
      self.CONTENT_CATEGORIES[25], 'plate_rack': self.CONTENT_CATEGORIES[25], 'prayer_rug':
      self.CONTENT_CATEGORIES[25], 'quilt': self.CONTENT_CATEGORIES[25], 'screen': self.CONTENT_CATEGORIES[25],
      'shower_curtain': self.CONTENT_CATEGORIES[25], 'soap_dispenser': self.CONTENT_CATEGORIES[25],
      'table_lamp': self.CONTENT_CATEGORIES[25], 'theater_curtain': self.CONTENT_CATEGORIES[25],
      'tray': self.CONTENT_CATEGORIES[25], 'vase': self.CONTENT_CATEGORIES[25],
      'window_screen': self.CONTENT_CATEGORIES[25], 'window_shade': self.CONTENT_CATEGORIES[25],
      'CD_player': self.CONTENT_CATEGORIES[25], 'Polaroid_camera': self.CONTENT_CATEGORIES[25],
      'cassette_player': self.CONTENT_CATEGORIES[25], 'cellular_telephone':
      self.CONTENT_CATEGORIES[25], 'computer_keyboard': self.CONTENT_CATEGORIES[25], 'desktop_computer':
      self.CONTENT_CATEGORIES[25], 'dial_telephone': self.CONTENT_CATEGORIES[25], 'digital_clock':
      self.CONTENT_CATEGORIES[25], 'digital_watch': self.CONTENT_CATEGORIES[25], 'dishwasher':
      self.CONTENT_CATEGORIES[25], 'electric_fan': self.CONTENT_CATEGORIES[25], 'hand-held_computer':
      self.CONTENT_CATEGORIES[25], 'hand_blower': self.CONTENT_CATEGORIES[25], 'hard_disc':
      self.CONTENT_CATEGORIES[25], 'iPod': self.CONTENT_CATEGORIES[25], 'joystick': self.CONTENT_CATEGORIES[25],
      'laptop': self.CONTENT_CATEGORIES[25], 'loudspeaker': self.CONTENT_CATEGORIES[25],
      'microphone': self.CONTENT_CATEGORIES[25], 'microwave': self.CONTENT_CATEGORIES[25],
      'modem': self.CONTENT_CATEGORIES[25], 'monitor': self.CONTENT_CATEGORIES[25],
      'odometer': self.CONTENT_CATEGORIES[25], 'oscilloscope': self.CONTENT_CATEGORIES[25],
      'parking_meter': self.CONTENT_CATEGORIES[25], 'pay-phone': self.CONTENT_CATEGORIES[25],
      'photocopier': self.CONTENT_CATEGORIES[25], 'power_drill': self.CONTENT_CATEGORIES[25],
      'printer': self.CONTENT_CATEGORIES[25], 'projector': self.CONTENT_CATEGORIES[25],
      'radiator': self.CONTENT_CATEGORIES[25], 'radio': self.CONTENT_CATEGORIES[25],
      'reflex_camera': self.CONTENT_CATEGORIES[25], 'remote_control': self.CONTENT_CATEGORIES[25],
      'scale': self.CONTENT_CATEGORIES[25], 'slot': self.CONTENT_CATEGORIES[25], 'space_bar':
      self.CONTENT_CATEGORIES[25], 'space_heater': self.CONTENT_CATEGORIES[25], 'spotlight':
      self.CONTENT_CATEGORIES[25], 'stopwatch': self.CONTENT_CATEGORIES[25], 'switch':
      self.CONTENT_CATEGORIES[25], 'tape_player': self.CONTENT_CATEGORIES[25], 'television':
      self.CONTENT_CATEGORIES[25], 'toaster': self.CONTENT_CATEGORIES[25], 'traffic_light':
      self.CONTENT_CATEGORIES[25], 'typewriter_keyboard': self.CONTENT_CATEGORIES[25], 'vacuum':
      self.CONTENT_CATEGORIES[25], 'waffle_iron': self.CONTENT_CATEGORIES[25], 'washer':
      self.CONTENT_CATEGORIES[25], 'chainlink_fence': self.CONTENT_CATEGORIES[23], 'picket_fence':
      self.CONTENT_CATEGORIES[23], 'worm_fence': self.CONTENT_CATEGORIES[23], 'French_loaf':
      self.CONTENT_CATEGORIES[1], 'bagel': self.CONTENT_CATEGORIES[1], 'beer_bottle':
      self.CONTENT_CATEGORIES[1], 'beer_glass': self.CONTENT_CATEGORIES[1], 'burrito':
      self.CONTENT_CATEGORIES[1], 'carbonara': self.CONTENT_CATEGORIES[1], 'cheeseburger':
      self.CONTENT_CATEGORIES[1], 'chocolate_sauce': self.CONTENT_CATEGORIES[1], 'consomme':
      self.CONTENT_CATEGORIES[1], 'corn': self.CONTENT_CATEGORIES[1], 'dough': self.CONTENT_CATEGORIES[1],
      'ear': self.CONTENT_CATEGORIES[1], 'eggnog': self.CONTENT_CATEGORIES[1], 'espresso':
      self.CONTENT_CATEGORIES[1], 'guacamole': self.CONTENT_CATEGORIES[1], 'hotdog': self.CONTENT_CATEGORIES[1],
      'ice_cream': self.CONTENT_CATEGORIES[1], 'ice_lolly': self.CONTENT_CATEGORIES[1],
      'mashed_potato': self.CONTENT_CATEGORIES[1], 'meat_loaf': self.CONTENT_CATEGORIES[1], 'pizza':
      self.CONTENT_CATEGORIES[1], 'pop_bottle': self.CONTENT_CATEGORIES[1], 'potpie':
      self.CONTENT_CATEGORIES[1], 'pretzel': self.CONTENT_CATEGORIES[1], 'red_wine': self.CONTENT_CATEGORIES[1],
      'saltshaker': self.CONTENT_CATEGORIES[1], 'trifle': self.CONTENT_CATEGORIES[1],
      'wine_bottle': self.CONTENT_CATEGORIES[1], 'altar': self.CONTENT_CATEGORIES[25], 'ashcan':
      self.CONTENT_CATEGORIES[25], 'bannister': self.CONTENT_CATEGORIES[25], 'barber_chair':
      self.CONTENT_CATEGORIES[25], 'bassinet': self.CONTENT_CATEGORIES[25], 'bathtub':
      self.CONTENT_CATEGORIES[25], 'bookcase': self.CONTENT_CATEGORIES[25], 'chiffonier':
      self.CONTENT_CATEGORIES[25], 'china_cabinet': self.CONTENT_CATEGORIES[25], 'cradle':
      self.CONTENT_CATEGORIES[25], 'crib': self.CONTENT_CATEGORIES[25], 'desk': self.CONTENT_CATEGORIES[25],
      'dining_table': self.CONTENT_CATEGORIES[25], 'entertainment_center':
      self.CONTENT_CATEGORIES[25], 'file': self.CONTENT_CATEGORIES[25], 'fire_screen':
      self.CONTENT_CATEGORIES[25], 'folding_chair': self.CONTENT_CATEGORIES[25], 'four-poster':
      self.CONTENT_CATEGORIES[25], 'mailbox': self.CONTENT_CATEGORIES[25], 'park_bench':
      self.CONTENT_CATEGORIES[25], 'pedestal': self.CONTENT_CATEGORIES[25], 'pool_table':
      self.CONTENT_CATEGORIES[25], 'refrigerator': self.CONTENT_CATEGORIES[25], 'rocking_chair':
      self.CONTENT_CATEGORIES[25], 'shoji': self.CONTENT_CATEGORIES[25], 'sliding_door':
      self.CONTENT_CATEGORIES[25], 'stage': self.CONTENT_CATEGORIES[25], 'stove': self.CONTENT_CATEGORIES[25],
      'stretcher': self.CONTENT_CATEGORIES[25], 'studio_couch': self.CONTENT_CATEGORIES[25],
      'throne': self.CONTENT_CATEGORIES[25], 'toilet_seat': self.CONTENT_CATEGORIES[25],
      'tub': self.CONTENT_CATEGORIES[25], 'wardrobe': self.CONTENT_CATEGORIES[25],
      'bathing_cap': self.CONTENT_CATEGORIES[25], 'bearskin': self.CONTENT_CATEGORIES[25],
      'bonnet': self.CONTENT_CATEGORIES[25], 'crash_helmet': self.CONTENT_CATEGORIES[25],
      'mortarboard': self.CONTENT_CATEGORIES[25], 'shower_cap': self.CONTENT_CATEGORIES[25],
      'sombrero': self.CONTENT_CATEGORIES[25], 'pickelhaube': self.CONTENT_CATEGORIES[25],
      'French_horn': self.CONTENT_CATEGORIES[25], 'accordion': self.CONTENT_CATEGORIES[25],
      'acoustic_guitar': self.CONTENT_CATEGORIES[25], 'banjo': self.CONTENT_CATEGORIES[25], 'bassoon':
      self.CONTENT_CATEGORIES[25], 'cello': self.CONTENT_CATEGORIES[25], 'chime': self.CONTENT_CATEGORIES[25],
      'cornet': self.CONTENT_CATEGORIES[25], 'drum': self.CONTENT_CATEGORIES[25], 'drumstick':
      self.CONTENT_CATEGORIES[25], 'electric_guitar': self.CONTENT_CATEGORIES[25], 'flute':
      self.CONTENT_CATEGORIES[25], 'gong': self.CONTENT_CATEGORIES[25], 'grand_piano':
      self.CONTENT_CATEGORIES[25], 'harmonica': self.CONTENT_CATEGORIES[25], 'harp': self.CONTENT_CATEGORIES[25],
      'maraca': self.CONTENT_CATEGORIES[25], 'marimba': self.CONTENT_CATEGORIES[25], 'oboe':
      self.CONTENT_CATEGORIES[25], 'ocarina': self.CONTENT_CATEGORIES[25], 'organ': self.CONTENT_CATEGORIES[25],
      'panpipe': self.CONTENT_CATEGORIES[25], 'pick': self.CONTENT_CATEGORIES[25], 'sax':
      self.CONTENT_CATEGORIES[25], 'steel_drum': self.CONTENT_CATEGORIES[25], 'trombone':
      self.CONTENT_CATEGORIES[25], 'upright': self.CONTENT_CATEGORIES[25], 'violin': self.CONTENT_CATEGORIES[25],
      'Petri_dish': self.CONTENT_CATEGORIES[25], 'beaker': self.CONTENT_CATEGORIES[25],
      'Band_Aid': self.CONTENT_CATEGORIES[25], 'bottlecap': self.CONTENT_CATEGORIES[25],
      'bubble': self.CONTENT_CATEGORIES[25], 'face_powder': self.CONTENT_CATEGORIES[25],
      'hair_spray': self.CONTENT_CATEGORIES[25], 'hay': self.CONTENT_CATEGORIES[25], 'honeycomb':
      self.CONTENT_CATEGORIES[25], 'knot': self.CONTENT_CATEGORIES[25], 'lotion': self.CONTENT_CATEGORIES[25],
      'mosquito_net': self.CONTENT_CATEGORIES[25], 'muzzle': self.CONTENT_CATEGORIES[25], 'nipple':
      self.CONTENT_CATEGORIES[25], 'pencil_box': self.CONTENT_CATEGORIES[25], 'perfume':
      self.CONTENT_CATEGORIES[25], 'sunscreen': self.CONTENT_CATEGORIES[25], 'toilet_tissue':
      self.CONTENT_CATEGORIES[25], 'velvet': self.CONTENT_CATEGORIES[25], 'wing': self.CONTENT_CATEGORIES[25],
      'wool': self.CONTENT_CATEGORIES[25], 'alp': self.CONTENT_CATEGORIES[7], 'apiary':
      self.CONTENT_CATEGORIES[7], 'birdhouse': self.CONTENT_CATEGORIES[7], 'breakwater':
      self.CONTENT_CATEGORIES[7], 'cliff': self.CONTENT_CATEGORIES[7], 'dam': self.CONTENT_CATEGORIES[7],
      'dock': self.CONTENT_CATEGORIES[7], 'drilling_platform': self.CONTENT_CATEGORIES[7],
      'flagpole': self.CONTENT_CATEGORIES[7], 'fountain': self.CONTENT_CATEGORIES[7], 'geyser':
      self.CONTENT_CATEGORIES[7], 'lakeside': self.CONTENT_CATEGORIES[7], 'manhole_cover':
      self.CONTENT_CATEGORIES[7], 'maypole': self.CONTENT_CATEGORIES[7], 'maze': self.CONTENT_CATEGORIES[7],
      'megalith': self.CONTENT_CATEGORIES[7], 'pier': self.CONTENT_CATEGORIES[7], 'promontory':
      self.CONTENT_CATEGORIES[7], 'sandbar': self.CONTENT_CATEGORIES[7], 'seashore': self.CONTENT_CATEGORIES[7],
      'spider_web': self.CONTENT_CATEGORIES[7], 'steel_arch_bridge': self.CONTENT_CATEGORIES[7],
      'stone_wall': self.CONTENT_CATEGORIES[7], 'street_sign': self.CONTENT_CATEGORIES[7],
      'sundial': self.CONTENT_CATEGORIES[7], 'suspension_bridge': self.CONTENT_CATEGORIES[7],
      'totem_pole': self.CONTENT_CATEGORIES[7], 'triumphal_arch': self.CONTENT_CATEGORIES[7],
      'valley': self.CONTENT_CATEGORIES[7], 'viaduct': self.CONTENT_CATEGORIES[7], 'volcano':
      self.CONTENT_CATEGORIES[7], 'water_tower': self.CONTENT_CATEGORIES[7], 'binder':
      self.CONTENT_CATEGORIES[25], 'book_jacket': self.CONTENT_CATEGORIES[25], 'comic_book':
      self.CONTENT_CATEGORIES[25], 'crossword_puzzle': self.CONTENT_CATEGORIES[25], 'envelope':
      self.CONTENT_CATEGORIES[25], 'jigsaw_puzzle': self.CONTENT_CATEGORIES[25], 'menu':
      self.CONTENT_CATEGORIES[25], 'notebook': self.CONTENT_CATEGORIES[25], 'paper_towel':
      self.CONTENT_CATEGORIES[25], 'balance_beam': self.CONTENT_CATEGORIES[3], 'barbell':
      self.CONTENT_CATEGORIES[3], 'football_helmet': self.CONTENT_CATEGORIES[3], 'horizontal_bar':
      self.CONTENT_CATEGORIES[3], 'paddle': self.CONTENT_CATEGORIES[3], 'parallel_bars':
      self.CONTENT_CATEGORIES[3], 'pole': self.CONTENT_CATEGORIES[3], 'puck': self.CONTENT_CATEGORIES[3],
      'punching_bag': self.CONTENT_CATEGORIES[3], 'racket': self.CONTENT_CATEGORIES[3],
      'scoreboard': self.CONTENT_CATEGORIES[3], 'ski': self.CONTENT_CATEGORIES[3], 'snorkel':
      self.CONTENT_CATEGORIES[3], 'abacus': self.CONTENT_CATEGORIES[0], 'barometer': self.CONTENT_CATEGORIES[0],
      'car_mirror': self.CONTENT_CATEGORIES[0], 'car_wheel': self.CONTENT_CATEGORIES[0],
      'cash_machine': self.CONTENT_CATEGORIES[0], 'cassette': self.CONTENT_CATEGORIES[0], 'coil':
      self.CONTENT_CATEGORIES[0], 'combination_lock': self.CONTENT_CATEGORIES[0], 'disk_brake':
      self.CONTENT_CATEGORIES[0], 'gas_pump': self.CONTENT_CATEGORIES[0], 'hourglass':
      self.CONTENT_CATEGORIES[0], 'lens_cap': self.CONTENT_CATEGORIES[0], 'mousetrap':
      self.CONTENT_CATEGORIES[0], 'oil_filter': self.CONTENT_CATEGORIES[0], 'padlock':
      self.CONTENT_CATEGORIES[0], 'radio_telescope': self.CONTENT_CATEGORIES[0], 'reel':
      self.CONTENT_CATEGORIES[0], 'seat_belt': self.CONTENT_CATEGORIES[0], 'sewing_machine':
      self.CONTENT_CATEGORIES[0], 'slide_rule': self.CONTENT_CATEGORIES[0], 'solar_dish':
      self.CONTENT_CATEGORIES[0], 'spindle': self.CONTENT_CATEGORIES[0], 'tripod': self.CONTENT_CATEGORIES[0],
      'turnstile': self.CONTENT_CATEGORIES[0], 'vending_machine': self.CONTENT_CATEGORIES[0],
      'wall_clock': self.CONTENT_CATEGORIES[0], 'web_site': self.CONTENT_CATEGORIES[0],
      'ballpoint': self.CONTENT_CATEGORIES[25], 'barrow': self.CONTENT_CATEGORIES[25],
      'binoculars': self.CONTENT_CATEGORIES[25], 'broom': self.CONTENT_CATEGORIES[25], 'bucket':
      self.CONTENT_CATEGORIES[25], 'can_opener': self.CONTENT_CATEGORIES[25], 'candle':
      self.CONTENT_CATEGORIES[25], "carpenter's_kit": self.CONTENT_CATEGORIES[25], 'chain':
      self.CONTENT_CATEGORIES[25], 'chain_saw': self.CONTENT_CATEGORIES[25], 'crutch':
      self.CONTENT_CATEGORIES[25], 'dumbbell': self.CONTENT_CATEGORIES[25], 'fountain_pen':
      self.CONTENT_CATEGORIES[25], 'hammer': self.CONTENT_CATEGORIES[25], 'hatchet': self.CONTENT_CATEGORIES[25],
      'hook': self.CONTENT_CATEGORIES[25], 'iron': self.CONTENT_CATEGORIES[25],
      'letter_opener': self.CONTENT_CATEGORIES[25], 'lighter': self.CONTENT_CATEGORIES[25], 'loupe':
      self.CONTENT_CATEGORIES[25], 'magnetic_compass': self.CONTENT_CATEGORIES[25], 'matchstick':
      self.CONTENT_CATEGORIES[25], 'nail': self.CONTENT_CATEGORIES[25], 'paintbrush':
      self.CONTENT_CATEGORIES[25], 'pencil_sharpener': self.CONTENT_CATEGORIES[25], 'plane':
      self.CONTENT_CATEGORIES[25], 'plunger': self.CONTENT_CATEGORIES[25], "potter's_wheel":
      self.CONTENT_CATEGORIES[25], 'quill': self.CONTENT_CATEGORIES[25], 'rubber_eraser':
      self.CONTENT_CATEGORIES[25], 'rule': self.CONTENT_CATEGORIES[25], 'safety_pin':
      self.CONTENT_CATEGORIES[25], 'screw': self.CONTENT_CATEGORIES[25], 'screwdriver':
      self.CONTENT_CATEGORIES[25], 'shield': self.CONTENT_CATEGORIES[25], 'shovel': self.CONTENT_CATEGORIES[25],
      'stethoscope': self.CONTENT_CATEGORIES[25], 'sunglass': self.CONTENT_CATEGORIES[25], 'swab':
      self.CONTENT_CATEGORIES[25], 'syringe': self.CONTENT_CATEGORIES[25], 'thimble':
      self.CONTENT_CATEGORIES[25], 'torch': self.CONTENT_CATEGORIES[25], 'whistle': self.CONTENT_CATEGORIES[25],
      'balloon': self.CONTENT_CATEGORIES[10], 'pinwheel': self.CONTENT_CATEGORIES[10], 'swing':
      self.CONTENT_CATEGORIES[10], 'teddy': self.CONTENT_CATEGORIES[10], 'bullet_train':
      self.CONTENT_CATEGORIES[5], 'electric_locomotive': self.CONTENT_CATEGORIES[5], 'freight_car':
      self.CONTENT_CATEGORIES[5], 'steam_locomotive': self.CONTENT_CATEGORIES[5], 'Model_T':
      self.CONTENT_CATEGORIES[25], 'ambulance': self.CONTENT_CATEGORIES[25], 'amphibian':
      self.CONTENT_CATEGORIES[25], 'beach_wagon': self.CONTENT_CATEGORIES[25], 'bicycle-built-for-two':
      self.CONTENT_CATEGORIES[25], 'bobsled': self.CONTENT_CATEGORIES[25], 'cab': self.CONTENT_CATEGORIES[25],
      'convertible': self.CONTENT_CATEGORIES[25], 'crane': self.CONTENT_CATEGORIES[25], 'dogsled':
      self.CONTENT_CATEGORIES[25], 'fire_engine': self.CONTENT_CATEGORIES[25], 'forklift':
      self.CONTENT_CATEGORIES[25], 'garbage_truck': self.CONTENT_CATEGORIES[25], 'go-kart':
      self.CONTENT_CATEGORIES[25], 'golfcart': self.CONTENT_CATEGORIES[25], 'grille':
      self.CONTENT_CATEGORIES[25], 'half_track': self.CONTENT_CATEGORIES[25], 'harvester':
      self.CONTENT_CATEGORIES[25], 'horse_cart': self.CONTENT_CATEGORIES[25], 'jeep':
      self.CONTENT_CATEGORIES[25], 'jinrikisha': self.CONTENT_CATEGORIES[25], 'lawn_mower':
      self.CONTENT_CATEGORIES[25], 'limousine': self.CONTENT_CATEGORIES[25], 'minibus':
      self.CONTENT_CATEGORIES[25], 'minivan': self.CONTENT_CATEGORIES[25], 'moped': self.CONTENT_CATEGORIES[25],
      'motor_scooter': self.CONTENT_CATEGORIES[25], 'mountain_bike': self.CONTENT_CATEGORIES[25],
      'moving_van': self.CONTENT_CATEGORIES[25], 'oxcart': self.CONTENT_CATEGORIES[25],
      'passenger_car': self.CONTENT_CATEGORIES[25], 'pickup': self.CONTENT_CATEGORIES[25], 'plow':
      self.CONTENT_CATEGORIES[25], 'police_van': self.CONTENT_CATEGORIES[25], 'racer':
      self.CONTENT_CATEGORIES[25], 'recreational_vehicle': self.CONTENT_CATEGORIES[25], 'school_bus':
      self.CONTENT_CATEGORIES[25], 'snowmobile': self.CONTENT_CATEGORIES[25], 'snowplow':
      self.CONTENT_CATEGORIES[25], 'sports_car': self.CONTENT_CATEGORIES[25], 'streetcar':
      self.CONTENT_CATEGORIES[25], 'tank': self.CONTENT_CATEGORIES[25], 'thresher': self.CONTENT_CATEGORIES[25],
      'tow_truck': self.CONTENT_CATEGORIES[25], 'tractor': self.CONTENT_CATEGORIES[25],
      'trailer_truck': self.CONTENT_CATEGORIES[25], 'tricycle': self.CONTENT_CATEGORIES[25],
      'trolleybus': self.CONTENT_CATEGORIES[25], 'unicycle': self.CONTENT_CATEGORIES[25],
      'assault_rifle': self.CONTENT_CATEGORIES[25], 'bow': self.CONTENT_CATEGORIES[25], 'cannon':
      self.CONTENT_CATEGORIES[25], 'guillotine': self.CONTENT_CATEGORIES[25], 'holster':
      self.CONTENT_CATEGORIES[25], 'missile': self.CONTENT_CATEGORIES[25], 'projectile':
      self.CONTENT_CATEGORIES[25], 'revolver': self.CONTENT_CATEGORIES[25], 'rifle': self.CONTENT_CATEGORIES[25],
      'scabbard': self.CONTENT_CATEGORIES[25],
    }

  def class_to_category(self, inference_type, class_name):
    """Converts result class from dataset to content category"""
    if inference_type == self.INFERENCE_TYPES[0] and class_name in self.OBJECT_DETECTION_CLASSES_TO_CATEGORY:
      return self.OBJECT_DETECTION_CLASSES_TO_CATEGORY[class_name]
    if inference_type == self.INFERENCE_TYPES[1] and class_name in self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY:
      return self.IMAGE_CLASSIFICATION_CLASSES_TO_CATEGORY[class_name]
    return None

  def get_inference_results(self, inference_type):
    """Calls torchserve inference api and returns response"""
    result_classes = []
    model_name = self.MODELS[0] if inference_type == self.INFERENCE_TYPES[0] else self.MODELS[1]
    data = None
    with open(self.file_name, 'rb') as f:
      data = f.read()
    headers = {'Content-Type': self.mime_type}
    res = requests.post(f'http://ml:5002/predictions/{model_name}', data=data, headers=headers)
    if res.status_code == 200:
      data = res.json()
      print(data)
      if inference_type == self.INFERENCE_TYPES[0]:
        return get_object_detection_classes(data)
      if inference_type == self.INFERENCE_TYPES[1]:
        return get_image_classification_classes(data)
    else:
      print(f'error while making inference request, status code: {res.status_code}')
    return result_classes

  def upsert_things(self, things):
    """Upserts things for future usage"""
    for thing in things:
      self.db['things'].find_one_and_update({ 'name': thing }, {'$set': { 'name': thing }}, upsert=True, return_document=ReturnDocument.AFTER)

  def upsert_entity(self, data):
    """Upserts things entity"""
    entity_oids = []
    for cat_class in data:
      cat_class = cat_class.replace('_', ' ')
      result = self.db['entities'].find_one_and_update(
        {'name': cat_class, 'entityType': 'things'},
        {'$set': { 'name': cat_class, 'imageUrl': self.image_url }},
        upsert=True,
        return_document=ReturnDocument.AFTER
      )
      self.db['entities'].update_one(
        {'_id': result['_id']},
        {'$addToSet': {'mediaItems': ObjectId(self.oid)}},
      )
      entity_oids.append(result['_id'])
    return entity_oids

  def process(self):
    content_categories = []
    # make inference call for object detection
    od_classes = self.get_inference_results(self.INFERENCE_TYPES[0])
    for od_class in od_classes:
      category = self.class_to_category(self.INFERENCE_TYPES[0], od_class)
      if category not in content_categories:
        content_categories.append(category)

    # make inference call for image classification
    ic_classes = self.get_inference_results(self.INFERENCE_TYPES[1])
    for ic_class in ic_classes:
      category = self.class_to_category(self.INFERENCE_TYPES[1], ic_class)
      if category not in content_categories:
        content_categories.append(category)

    self.upsert_things(od_classes + ic_classes)
    entity_oids = self.upsert_entity(od_classes + ic_classes)
    self.update({ '$set': { 'contentCategories': content_categories }, '$addToSet': { 'entities': { '$each': entity_oids } } })
