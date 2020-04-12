import requests
import yadisk

API_KEY = "trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0"

URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_DISK = "https://cloud-api.yandex.net/v1/disk/resources/upload"

def translate_it(read_from, write_to, from_lang, into_lang='ru'):
    text = read_file(read_from)

    params = {
        'key': API_KEY,
        'text': text,
        'lang': "{}-{}".format(from_lang, into_lang),
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    text_tr = json_['text']
    write_file(read_from, write_to, text_tr)
    # ya_save(write_to)
    ya_save2(write_to)
    return text_tr

def read_file(read_from):
    with open(read_from) as f:
        return f.read()

def write_file(read_from, write_to, text_tr):
    with open(write_to, 'w') as file:
        for line in text_tr:
            file.write(line)
            print(f'Файл {read_from} успешно переведен.')

# Второй вариант решения загрузки
def ya_save(write_to):
    y = yadisk.YaDisk(token="AgAAAAA2-fK0AADLWz4chNQ4Xkgfk6yZCeN8dmo")
    try:
        y.upload(write_to, "/{}".format(write_to))
        print(f'Файл {write_to} успешно сохранен на диск.')
    except yadisk.exceptions.PathExistsError as Exception:
        print('Не удалось сохранить файл. Файл с данным именем уже существует на диске.')

# Основной вариант решения загрузки
def ya_save2(write_to):
    
    headers = {"Authorization": "OAuth AgAAAAA2-fK0AADLWz4chNQ4Xkgfk6yZCeN8dmo", "Accept": "application/json", "Content-Type": "application/json"}

    params = {
    'path': "/{}".format(write_to),
    'overwrite': 'true'
    }

    response = requests.get(URL_DISK, headers=headers, params=params)
    json_ = response.json()
    link = json_['href']
    with open (write_to) as f:
        data =  f.read()

    upload = requests.put(link, data=data.encode("utf-8"))
    print(f'Файл {write_to} успешно сохранен на диск.')

if __name__ == '__main__':
    translate_it('DE.txt', 'tr_de.txt', 'de')
    translate_it('ES.txt', 'tr_es.txt', 'es')
    translate_it('FR.txt', 'tr_fr.txt', 'fr')
