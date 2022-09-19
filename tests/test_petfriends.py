#import pytest
from api import PetFriends
from settings import valid_mail, valid_pass

pf = PetFriends()

def test_get_api_key_for_valid_login (email=valid_mail, password=valid_pass):
    """Проверяем авторизацию с правильными е-мэйлом и паролем"""
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_wrong_login (email=valid_mail, password="678678"):
    """Проверяем авторизацию с неправильными паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_list_of_all_pets_with_valid_key(filter=""):
""" Проверка получения списка всех питомцев на сервере"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets'])>0

def test_get_list_of_my_pets (filter="my_pets"):
"""Проверка получения списка питомцев, заведенных данным пользователем"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets'])<15

def test_add_new_pet_with_valid_data():
    """Проверка добавления нового питомца с правильными данными"""
    """Определяем данные новго питомца"""
    name = 'Чебурашка'
    animal_type = 'неизвестен'
    age = '3'
    pet_photo = 'images/mypet.jpeg'

    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.add_new_pet(auth_key=auth_key, name=name, animal_type=animal_type,
                                    age=age, photo=pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type
    """Удаляем добавленного питомца"""
    _, _ = pf.delete_existing_pet(auth_key=auth_key, pet_id=result['id'])

def test_delete_existing_pet():
    """Проверка удаления питомца с заданным ID"""
    """Создаем новго питомца, которого потом удалим, 
    и получаем его ID"""
    name = 'Чебурашка'
    animal_type = 'неизвестен'
    age = '3'
    pet_photo = 'images/mypet.jpeg'
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, result0 = pf.add_new_pet(auth_key=auth_key, name=name, animal_type=animal_type,
                                    age=age, photo=pet_photo)
    new_id = result0['id']
    """Удаляем вновь созданного питомца"""
    status,_ = pf.delete_existing_pet(auth_key=auth_key,pet_id=new_id)
    assert status == 200

def test_add_new_pet_without_photo ():
    """Проверка добавления питомца без фотографии"""
    """Задаем данные новго питомца"""
    name = "Зевс"
    animal_type = "Аусси"
    age = 6
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.add_pet_without_photo(auth_key=auth_key, name=name,
                                              age=age, animal_type=animal_type)
    assert status == 200
    assert result['name'] == name
    assert result['age'] == str(age)
    assert result['animal_type'] == animal_type
    _, _ = pf.delete_existing_pet(auth_key=auth_key, pet_id=result['id'])

def test_update_pet_info():
    """Проверка обновления данных существующего питомуа"""
    """Создаем новго питомца, получаем его ID"""
    name = "Зевс"
    animal_type1 = "Австралийская овчарка"
    animal_type = "Аусси"
    age = "6"
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, res0 = pf.add_pet_without_photo(auth_key=auth_key, name=name,
                                              age=age, animal_type=animal_type)
    new_id = res0["id"]
    status, result = pf.update_pet_info(auth_key=auth_key, pet_id=new_id, name=name,
                                              age=age, animal_type=animal_type1)
    assert status == 200
    assert result['animal_type'] == "Австралийская овчарка"
    """Удаляем вновь созданного питомца"""
    _, _ = pf.delete_existing_pet(auth_key=auth_key, pet_id=new_id)

def test_add_photo_to_existing_pet():
    """Проверка добавления фотографии существующему питомцу"""
    """Создаем нового питомца в формате "без фото" """
    name = "Зевс"
    animal_type = "Австралийская овчарка"
    age = "6"
    new_photo="images/zevs.jpeg"
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, res0 = pf.add_pet_without_photo(auth_key=auth_key, name=name,
                                              age=age, animal_type=animal_type)
    new_id = res0["id"]
    status, result = pf.add_photo_to_existing_pet(auth_key=auth_key, pet_id=new_id,
                                                  photo=new_photo)
    assert status == 200
    """Удаляем вновь созданного питомца"""
    _, _ = pf.delete_existing_pet(auth_key=auth_key, pet_id=new_id)

def test_update_pet_info_with_partial_data():
    """Проверка обновления данных питомца в "укороченном" формате"""
    """Создаем нового питомца"""
    name = "Зевс"
    animal_type1 = "Австралийская овчарка"
    animal_type = "Аусси"
    age = 6
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, res0 = pf.add_pet_without_photo(auth_key=auth_key, name=name,
                                              age=age, animal_type=animal_type)
    new_id = res0["id"]
    """В запросе указываем только обновляемые данные"""
    status, result = pf.update_pet_info(auth_key=auth_key, pet_id=new_id,
                                        animal_type=animal_type1)
    assert status == 200
    assert result['animal_type'] == "Австралийская овчарка"
    """Удаляем созданного питомца"""
    _, _ = pf.delete_existing_pet(auth_key=auth_key, pet_id=new_id)



