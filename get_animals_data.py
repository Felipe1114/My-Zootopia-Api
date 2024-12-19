"""
get link: https://api.api-ninjas.com/v1/animals
beispiel für cheetah: https://api.api-ninjas.com/v1/animals?name=cheetah
                                                          ^^^^^^^^^^^^^^

api key<.

aufgaben:
- neues git repository anlegen
- code dort hintransferieren
- api in code einfügen (dass das html dokument die daten aus der json dort hineinfügt)
- wenn es das tier nicht gibt, einen text in das html dokuemtn schreiben: 'das tier ... ist nicht in den daten enthalten'.
- wie erstezte ich das alte tier mit den alten?

"""
import requests

API_KEY = {"X-Api-Key": "rPicwarm61jK9uOZ+wNI3A==3bUhKh0YiLMZm4ag"}


def create_request():
  """creates the HTML request"""
  animal = input("what animal, you want information for?(animal name):")

  url = "https://api.api-ninjas.com/v1/animals"
  get_request = f"?name={animal}"

  full_request = url + get_request

  return full_request


def get_response():
  """gets data from api"""
  full_request = create_request()

  response = requests.get(full_request, params=API_KEY)
  return response


def get_json_from_request():
  response = get_response()
  data = response.json()

  return data


def main():
  data = get_json_from_request()
  print(data)


if __name__ == "__main__":
  main()










