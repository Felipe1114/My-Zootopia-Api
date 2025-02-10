import requests
from porgramm_modules import CRD_data

HTML_DATAPATH = "./programm_files/animals_template.html"
API_KEY = {"X-Api-Key": "rPicwarm61jK9uOZ+wNI3A==3bUhKh0YiLMZm4ag"}
#Backup Platzhalter zum kopieren für python code: "__REPLACE_ANIMALS_INFO__"

def create_request():
  """creates the API request, on base of the user input"""
  animal = input("what animal, you want information for?(animal name):")

  url = "https://api.api-ninjas.com/v1/animals"
  get_request = f"?name={animal}"

  full_request = url + get_request

  return full_request, animal


def get_response():
  """gets data from api"""
  full_request, animal = create_request()

  response = requests.get(full_request, params=API_KEY)

  return response, animal


def get_json_from_request(response):
  """changes response data, to json structure"""
  data = response.json()
  return data


def get_HTML_data():
  """gets the data from the HTML file"""
  with open(HTML_DATAPATH, "r") as htmlfile:
    data = htmlfile.read()

    return data


def save_HTML_data(data):
  """Saves data to HTML file"""
  try:
    with open(HTML_DATAPATH, "w") as objfile:
      objfile.write(data)
    print("Website was successfully generated to the file animals_template.html.")
  except FileNotFoundError as e:
    print(e)


def generate_new_HTML_code():
  """
  """
  response, animal = get_response()
  # hier wird der response code gecheckt, bevor er in eine json umgewandelt wird
  output = validade_response(response, animal)

  return output


def validade_response(response, animal):
  """Checks the status code. If status_code is 200, it gives back response,
  if not, it gives back an error string

  """
  response_len = len(response.json())
  if response_len > 0:
    output = generate_animal_informations(response)

  else:
    output = (f"<li class='cards__item'>\n"
              f"<div class='card__title'>{animal}</div>\n"
              f"<p class='card__text'>the animal {animal} does not exist</p>\n"
              f"</li>\n")

  return output



def get_animal_informations(response):
  data = get_json_from_request(response)

  all_animal_informations = []
  for animal in data:
    name = animal.get("name", "Unbekannt")  # Falls "name" nicht existiert, wird "Unbekannt" verwendet
    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet", "Keine Info")

    locations = animal.get("locations", [])
    location = locations[0] if locations else "Ort unbekannt"  # Falls keine Locations vorhanden sind

    animal_type = characteristics.get("type", None)  # Falls "type" nicht existiert, None zurückgeben

    animal_informations = [name, diet, location]

    # if animal_type is None
    if animal_type:
      animal_informations.append(animal_type)

    all_animal_informations.append(animal_informations)
  return all_animal_informations


def generate_animal_informations(response):
  """Generates for each list of animal-information HTML-code and wirtes it into a HTML file

  Args:
    data(dict): contains all informations about animals of a specific type
  """
  animal_informations = get_animal_informations(response)
  output = ""

  for animal in animal_informations:
    output += "<li class='cards__item'>"

    name = animal[0]
    diet = animal[1]
    location = animal[2]

    # text, if animal has a "type"
    if len(animal) == 4:
      type = animal[3]
      output += (f"<div class='card__title'>{name}</div>\n"
                 f"<p class='card__text'>\n<strong>Diet:</strong> {diet}<br/>\n"
                 f"<strong>Location:</strong> {location}<br/>\n<strong>Type:</strong> {type}<br/>"
                 f"\n</p>\n</li>\n")
    # text, if animal has no "type"
    else:
      output += (f"<div class='card__title'>{name}</div>\n"
                 f"<p class='card__text'>\n<strong>Diet:</strong> {diet}<br/>\n"
                 f"<strong>Location:</strong> {location}<br/>"
                 f"\n</p>\n</li>\n")

  return output


def update_HTML_data(old_data="__REPLACE_ANIMALS_INFO__"):
  """
  updates HTML data. Gets the placeholder from a .txt file.
  replaces the placeholder with the new HTML data and saves the new HMTL data as the new placeholder
  """
  old_data = CRD_data.get_data()

  html = get_HTML_data()
  new_html_data = generate_new_HTML_code()

  html = html.replace(old_data, new_html_data)

  save_HTML_data(html)

  CRD_data.save_data(new_html_data)

def main():
  update_HTML_data()


if __name__ == "__main__":
  main()