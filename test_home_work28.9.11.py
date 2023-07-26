from pydantic import BaseModel, Field, EmailStr
import pytest

class get_auth_key(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3)

class pet_animal(BaseModel):
    name: str = Field(min_length=2, max_length=15)
    animal_type: str = Field(min_length=3, max_length=15)
    age: int = Field(ge=0)


def test_valid_get_auth_key():
    request = {'email': "test1@mail.com", 'password': "test1"}
    get_auth_key(**request)

def test_not_valid_pass():
    request = {'email': "test1@mail.com", 'password': "t"}
    with pytest.raises(ValueError):
        get_auth_key(**request)

def test_not_valid_email():
    request = {'email': "test1@mail", 'password': "t"}
    with pytest.raises(ValueError):
        get_auth_key(**request)

def test_empty_get_auth_key():
    request = {}
    with pytest.raises(ValueError):
        get_auth_key(**request)

def test_valid_data_pet():
    request = {'name': "Muhtar", 'animal_type': "Dog", 'age': 5}
    pet_animal(**request)

def test_not_valid_data_name():
    request = {'name': "M", 'animal_type': "Dog", 'age': 2}
    with pytest.raises(ValueError):
        pet_animal(**request)

def test_not_valid_data_animal_type():
    request = {'name': "Muhtar", 'animal_type': "D", 'age': 2}
    with pytest.raises(ValueError):
        pet_animal(**request)


def test_not_valid_data_age():
    request = {'name': "Muhtar", 'animal_type': "Dog", 'age': 'f'}
    with pytest.raises(ValueError):
        pet_animal(**request)

def test_valid_data_response():
    response = [{'name': "Drug", 'animal_type': "Cat", 'age': 1},
                {'name': "Muhtar", 'animal_type': "Dog", 'age': 5} ]
    animals = [pet_animal(**animal) for animal in response]
    assert len(animals) != 1
    assert animals[1].name == 'Muhtar'
    assert animals[1].animal_type == 'Dog'
    assert animals[1].age == 5

def test_valid_data_response_not_animal():
    response = []
    animals = [pet_animal(**animal) for animal in response]
    assert len(animals) == 0

def test_not_valid_data_response():
    response = [{'ValidationError': 'Data'}]
    with pytest.raises(ValueError):
        animals = [pet_animal(**animal) for animal in response]
