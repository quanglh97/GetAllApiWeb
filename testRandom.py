import string
import random
def stringGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
print(stringGenerator())
print(stringGenerator(3, "6793YUIO"))

def stringGeneratorTopic():
    content = ["covid", 'bongda', 'thoi tiet', 'truyen tranh', 'phim', 'ảnh', 'youtube', 'facebook', 'giàu', 'biển đảo']
    r = random.randint(0, len(content))
    return content[r]

print(stringGeneratorTopic())