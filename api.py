import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email:str, password:str)->json:
        """Получение уникального ключа для зарегистрованного пользователя"""
        headers = {
            'email': email,
            'password': password
        }
        result = ""
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key:str, filter:str):
        """Получение списка всех питомцев на сервер, Возможно получение "своих"
        питомцкв при использовании фильтра "my_pets" """

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get (self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, photo: str):
    """ Добавление нового питомца на сереерю, Возвращется ссылка на нового питомца
    в формате JSON """
        data = MultipartEncoder(
            fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (photo, open(photo, 'rb'),'image/jpeg')
        })
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        result = ""
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_without_photo (self, auth_key: str, name:str, age:str, animal_type: str):
        """ Добавление на сервер нового питомца, если нет фотографии.
        Возвращаются данные добавленного питомца в вофрмате JSON"""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        headers = {
            'auth_key': auth_key['key'],
        }
        result = ""
        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_to_existing_pet(self, auth_key: str, pet_id: str, photo: str):
        """Добавление фото существуюему питомцу с указанным ID"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (photo, open(photo, 'rb'), 'image/jpeg')
            })
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }
        result = ""
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_existing_pet(self, auth_key: json, pet_id: str):
        """ Удаление питомца с указанным ID """
        header = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'/api/pets/'+pet_id, headers=header)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name="", animal_type="",age=""):
        """ Обновление информации о питомце с с указанным ID
        Можно указать только обновляемые поля, тогда остальные данные будут сохранены
        аатоматически """

        header = {
            'auth_key': auth_key['key'],
        }
        pet = {}
        res = requests.get(self.base_url+'api/pets', params='my_pets', headers=header)
        my_pets = res.json()
        if (len(my_pets['pets'])==0):
            print ("No pets in list, update not available\nНет питомцев в списке, обновление невозможномё\n")
        else:
            for pet in my_pets['pets']:
                if pet['id'] == pet_id:
        """У найденнго питомца считыываем значения, которые не будут обновляться"""
                    if name == "": name = pet['name']
                    if age == "": age = pet['age']
                    if animal_type == "": animal_type = pet['animal_type']
                    break # и выходим из цаила
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        result = ""
        res = requests.put(self.base_url+'api/pets/'+pet_id, headers=header, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
