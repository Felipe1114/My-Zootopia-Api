
DATAPATH = "./old_animal_data.txt"

def get_data():
  with open(DATAPATH, "r") as objfile:
    data = objfile.read()
  return data


def save_data(data):
  with open(DATAPATH, "w") as objfile:
      objfile.write(data)


def print_data(data):
    print(data)




