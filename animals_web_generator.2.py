import requests
from porgramm_modules import CRD_data

HTML_DATAPATH = "./programm_files/animals_template.html"
API_KEY = {"X-Api-Key": "rPicwarm61jK9uOZ+wNI3A==3bUhKh0YiLMZm4ag"}
# Backup Platzhalter zum Kopieren für Python-Code: "__REPLACE_ANIMALS_INFO__"

def create_request():
    """Creates the API request based on user input."""
    animal = input("What animal do you want information for? (Animal name): ")
    url = "https://api.api-ninjas.com/v1/animals"
    get_request = f"?name={animal}"
    full_request = url + get_request
    return full_request, animal

def get_response():
    """Gets data from API."""
    full_request, animal = create_request()
    response = requests.get(full_request, params=API_KEY)
    return response, animal

def get_json_from_request(response):
    """Converts response data to JSON format."""
    return response.json()

def generate_new_HTML_code():
    """Generates a new HTML file with animal data from the API."""
    response, animal = get_response()
    output = validade_response(response, animal)
    create_new_HTML(output)

def validade_response(response, animal):
    """Checks response status and processes data."""
    response_len = len(response.json())
    if response_len > 0:
        return generate_animal_informations(response)
    else:
        return (f"<li class='cards__item'>\n"
                f"<div class='card__title'>{animal}</div>\n"
                f"<p class='card__text'>The animal {animal} does not exist</p>\n"
                f"</li>\n")

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
        animal_type = characteristics.get("type", None)
        animal_informations = [name, diet, location]
        if animal_type:
            animal_informations.append(animal_type)
        all_animal_informations.append(animal_informations)
    return all_animal_informations

def generate_animal_informations(response):
    """Generates HTML structure for animal information."""
    animal_informations = get_animal_informations(response)
    output = ""
    for animal in animal_informations:
        output += "<li class='cards__item'>"
        name, diet, location = animal[:3]
        if len(animal) == 4:
            type_ = animal[3]
            output += (f"<div class='card__title'>{name}</div>\n"
                       f"<p class='card__text'>\n<strong>Diet:</strong> {diet}<br/>\n"
                       f"<strong>Location:</strong> {location}<br/>\n"
                       f"<strong>Type:</strong> {type_}<br/>\n</p>\n</li>\n")
        else:
            output += (f"<div class='card__title'>{name}</div>\n"
                       f"<p class='card__text'>\n<strong>Diet:</strong> {diet}<br/>\n"
                       f"<strong>Location:</strong> {location}<br/>\n</p>\n</li>\n")
    return output

def create_new_HTML(content):
    """Creates a new HTML file with animal data."""
    html_template = """
        <html>
            <head>
                <style>
                    html {{ background-color: #ffe9e9; }}
                    h1 {{ text-align: center; font-size: 40pt; font-weight: normal; }}
                    body {{
                        font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                        font-style: normal; font-weight: 400; padding: 1rem;
                        width: 900px; margin: auto;
                    }}
                    .cards {{ list-style: none; margin: 0; padding: 0; }}
                    .cards__item {{
                        background-color: white; border-radius: 0.25rem;
                        box-shadow: 0 20px 40px -14px rgba(0,0,0,0.25);
                        overflow: hidden; padding: 1rem; margin: 50px;
                    }}
                    .card__title {{
                        font-size: 1.25rem; font-weight: 300;
                        letter-spacing: 2px; text-transform: uppercase;
                    }}
                    .card__text {{
                        flex: 1 1 auto; font-size: 0.95rem;
                        line-height: 2; margin-bottom: 1.25rem;
                    }}
                </style>
            </head>
            <body>
                <h1>My Animal Repository</h1>
                <ul class="cards">
                    {content}
                </ul>
            </body>
        </html>
        """.format(content=content)
    with open("./programm_files/new_animals.html", "w") as file:
        file.write(html_template)
    print("New HTML file 'new_animals.html' has been created successfully.")

def main():
    generate_new_HTML_code()

if __name__ == "__main__":
    main()
