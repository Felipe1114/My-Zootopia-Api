import requests

HTML_TEMPLATE_PATH = "./programm_files/animals_template.html"
OUTPUT_HTML_PATH = "./programm_files/new_animals.html"
API_KEY = {"X-Api-Key": "rPicwarm61jK9uOZ+wNI3A==3bUhKh0YiLMZm4ag"}
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def create_request():
  """Creates the API request based on user input."""
  animal = input("What animal do you want information for? (Animal name): ")
  url = "https://api.api-ninjas.com/v1/animals"
  full_request = f"{url}?name={animal}"
  return full_request, animal


def get_response():
  """Gets data from API."""
  full_request, animal = create_request()
  response = requests.get(full_request, headers=API_KEY)
  return response, animal


def get_json_from_request(response):
  """Converts response data to JSON format."""
  return response.json()


def get_animal_informations(response):
  """Extracts relevant information about animals."""
  data = get_json_from_request(response)
  all_animal_informations = []

  for animal in data:
    name = animal.get("name", "Unknown")
    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet", "No info")
    locations = animal.get("locations", [])
    location = locations[0] if locations else "Unknown location"
    animal_type = characteristics.get("type", "Unknown")

    animal_informations = {
      "name": name,
      "diet": diet,
      "location": location,
      "type": animal_type
    }
    all_animal_informations.append(animal_informations)

  return all_animal_informations


def generate_animal_html(response):
  """Generates HTML structure for animal information."""
  animal_data = get_animal_informations(response)

  if not animal_data:
    return "<li class='cards__item'><p class='card__text'>No data found for the requested animal.</p></li>"

  output = ""
  for animal in animal_data:
    output += (
      f"<li class='cards__item'>"
      f"<div class='card__title'>{animal['name']}</div>"
      f"<p class='card__text'>"
      f"<strong>Diet:</strong> {animal['diet']}<br/>"
      f"<strong>Location:</strong> {animal['location']}<br/>"
      f"<strong>Type:</strong> {animal['type']}<br/>"
      f"</p>"
      f"</li>\n"
    )
  return output


def generate_new_html():
  """Creates a new HTML file using the template and API data."""
  response, animal = get_response()
  animal_html = generate_animal_html(response)

  with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as template_file:
    template_content = template_file.read()

  new_html_content = template_content.replace(PLACEHOLDER, animal_html)

  with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as output_file:
    output_file.write(new_html_content)

  print("New HTML file 'new_animals.html' has been created successfully.")


def main():
  generate_new_html()


if __name__ == "__main__":
  main()
