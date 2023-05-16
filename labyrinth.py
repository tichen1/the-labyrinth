import random

# obstacle: True if you cannot move to/through there
# state: 0 = none, 1 = theseus, 2 = minotaur
# coordinate: (1 <= x <= width, 1 <= y <= height)
class Space:
  def __init__(self, obstacle, state, coordinate):
    self.obstacle = obstacle
    self.state = state
    self.coordinate = coordinate

# spaces: list of Space
# width/height: labyrinth width and height
# num: labyrinth num
class Labyrinth:
  def __init__(self, spaces, obstacles, width, height, num):
    self.spaces = spaces
    self.obstacles = obstacles
    self.width = width
    self.height = height
    self.num = num

# name: Fighter's name (Theseus or Minotaur)
# health: Fighter's max health (15)
# coordinate: (1 <= x <= width, 1 <= y <= height)
# directions: dictionary of direction: bool (True if Fighter can move that way)
# sight: direction if opponent is in sight
# distance: spaces away opponent is (if in sight), -1 otherwise
class Fighter:
  def __init__(self, name, health, coordinate, directions, sight, distance):
    self.name = name
    self.health = health
    self.coordinate = coordinate
    self.directions = directions
    self.sight = sight
    self.distance = distance

class Cheats:
  def __init__(self, show_health, show_distance):
    self.show_health = show_health
    self.show_distance = show_distance

# creates generic labyrinth given its width and height
def init_labyrinth(width, height):
  labyrinth = Labyrinth([], [], width, height, 0)
  for x in range(width):
    for y in range(height):
      labyrinth.spaces.append(Space(False, 0, (x + 1, y + 1)))
#      labyrinth.append(Space(False, 0, (x + 1, y + 1)))
  return labyrinth

# sets obstacles for labyrinth1
def labyrinth1():
  width, height = 5, 5
  labyrinth = init_labyrinth(width, height)
  labyrinth.width = width
  labyrinth.height = height
  labyrinth.num = 1
  
  labyrinth.obstacles = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 4), (4, 2), (4, 4), (4, 5), (5, 4), (5, 5)]
  for x in range(width * height):
    if labyrinth.spaces[x].coordinate in labyrinth.obstacles:
      labyrinth.spaces[x].obstacle = True
  return labyrinth

# sets obstacles for labyrinth2
def labyrinth2():
  width, height = 3, 5
  labyrinth = init_labyrinth(width, height)
  labyrinth.width = width
  labyrinth.height = height
  labyrinth.num = 2
  
  labyrinth.obstacles = [(2, 2), (2, 4)]
  for x in range(width * height):
    if labyrinth.spaces[x].coordinate in labyrinth.obstacles:
      labyrinth.spaces[x].obstacle = True
  return labyrinth

def display_labyrinth(labyrinth):
  if labyrinth.num == 1:
    return

# prints list of labyrinth obstacles and coordinates
def print_labyrinth(labyrinth):
  print('Labyrinth number:', labyrinth.num)
  for x in range(labyrinth.width * labyrinth.height):
    print(labyrinth.spaces[x].obstacle, labyrinth.spaces[x].coordinate)

# new coordinate if moved one space in direction
def new_coordinate(coordinate, direction):
  x, y = coordinate[0], coordinate[1]
  if direction.upper() == 'N':
    y = coordinate[1] + 1
  if direction.upper() == 'E':
    x = coordinate[0] + 1
  if direction.upper() == 'S':
    y = coordinate[1] - 1
  if direction.upper() == 'W':
    x = coordinate[0] - 1
  return x, y

# returns bool determining whether a Fighter is in sight (modifies fighter.sight and fighter.distance)
def in_sight(labyrinth, fighter, opponent):
  coordinate = fighter.coordinate
  distance = 0
  # check north direction
  while coordinate[1] + 1 <= labyrinth.height:
    coordinate = new_coordinate(coordinate, 'N')
    distance += 1
    if coordinate == opponent.coordinate:
      fighter.sight = 'N'
      fighter.distance = distance
      return True
    elif coordinate in labyrinth.obstacles:
      break

  coordinate = fighter.coordinate
  distance = 0
  # check east direction
  while coordinate[0] + 1 <= labyrinth.width:
    coordinate = new_coordinate(coordinate, 'E')
    distance += 1
    if coordinate == opponent.coordinate:
      fighter.sight = 'E'
      fighter.distance = distance
      return True
    elif coordinate in labyrinth.obstacles:
      break

  coordinate = fighter.coordinate
  distance = 0
  # check south direction
  while 1 <= coordinate[1] - 1:
    coordinate = new_coordinate(coordinate, 'S')
    distance += 1
    if coordinate == opponent.coordinate:
      fighter.sight = 'S'
      fighter.distance = distance
      return True
    elif coordinate in labyrinth.obstacles:
      break

  coordinate = fighter.coordinate
  distance = 0
  # check west direction
  while 1 <= coordinate[0] - 1:
    coordinate = new_coordinate(coordinate, 'W')
    distance += 1
    if coordinate == opponent.coordinate:
      fighter.sight = 'W'
      fighter.distance = distance
      return True
    elif coordinate in labyrinth.obstacles:
      break
  
  fighter.sight = ''
  fighter.distance = -1
  return False

# determines the directions a Fighter may move
def move(labyrinth, fighter, opponent, sight):
  fighter.directions = {'N': False, 'E': False, 'S': False, 'W': False}
  coordinate = fighter.coordinate
  
  # north
  x, y = new_coordinate(coordinate, 'N')[0], new_coordinate(coordinate, 'N')[1]
  if (x, y) not in labyrinth.obstacles: # not in obstacles
    if (x, y) != opponent.coordinate: # not where opponent is
      if 1 <= y <= labyrinth.height: # not out of bounds
        fighter.directions['N'] = True

  # east
  x, y = new_coordinate(coordinate, 'E')[0], new_coordinate(coordinate, 'E')[1]
  if (x, y) not in labyrinth.obstacles:
    if (x, y) != opponent.coordinate:
      if 1 <= x <= labyrinth.width:
        fighter.directions['E'] = True
    
  # south
  x, y = new_coordinate(coordinate, 'S')[0], new_coordinate(coordinate, 'S')[1]
  if (x, y) not in labyrinth.obstacles:
    if (x, y) != opponent.coordinate:
      if 1 <= y <= labyrinth.height:
        fighter.directions['S'] = True
  
  # west
  x, y = new_coordinate(coordinate, 'W')[0], new_coordinate(coordinate, 'W')[1]
  if (x, y) not in labyrinth.obstacles:
    if (x, y) != opponent.coordinate:
      if 1 <= x <= labyrinth.width:
        fighter.directions['W'] = True

  # determine Theseus' move
  if fighter.name == 'THESEUS':
    print('Which direction would you like to move? [ ', end="")
    for x in fighter.directions.keys():
      if fighter.directions[x] == True:
        print(x, end=" ")
    print(']')
    
    direction = input('Enter direction here: ')
    while direction.upper() not in fighter.directions.keys() or fighter.directions[direction.upper()] == False:
      print('Not a valid direction! Please enter in one of:')
      for x in fighter.directions.keys():
        if fighter.directions[x] == True:
          print(x, end=" ")
      direction = input('\nEnter direction here: ')
  
  # determine Minotaur's random move
  if fighter.name == 'THE MINOTAUR':
    if fighter.sight != '':
      if fighter.distance == 1:
        print('ISSUE: fighter.distance should not be 1 here')
      else:
        direction = fighter.sight
        
    else:
      direction = random.choice(list(fighter.directions.keys()))
      while fighter.directions[direction] == False:
        direction = random.choice(list(fighter.directions.keys()))
      
  # actual move
  if direction.upper() == 'N':
    fighter.coordinate = new_coordinate(coordinate, 'N')
  if direction.upper() == 'E':
    fighter.coordinate = new_coordinate(coordinate, 'E')
  if direction.upper() == 'S':
    fighter.coordinate = new_coordinate(coordinate, 'S')
  if direction.upper() == 'W':
    fighter.coordinate = new_coordinate(coordinate, 'W')

  print(fighter.name, 'moved 1 space', direction.upper())

# attack
def attack(fighter, opponent):
  if fighter.name == 'THESEUS':
    dice = random.randint(1, 6)
    
    if dice == 6:
      multiplier = 2
      print('CRITICAL HIT! ', end="")
    else:
      multiplier = 1
    print('THESEUS shot an arrow at the THE MINOTAUR.')
    if fighter.distance == 1:
      opponent.health -= 3 * multiplier
    if fighter.distance == 2:
      opponent.health -= 2 * multiplier
    if fighter.distance == 3:
      opponent.health -= 1 * multiplier
    if fighter.distance > 3:
      opponent.health -= 0 * multiplier
    
  if fighter.name == 'THE MINOTAUR':
    dice = random.randint(1,6)
    if dice == 6:
      damage = 5
      print('CRITICAL HIT! ', end="")
    else:
      damage = 3
    opponent.health -= damage
    print('THE MINOTAUR struck THESEUS with his bare fists.')
    

# generates random start positions
def generate_random_start(width, height):
  return (random.randint(1, width), random.randint(1, height))

def print_line():
  print('-----------------------------------------------------------')

# starts the game
def start_game():
  labyrinth_num = random.randint(1, 2)
  if labyrinth_num == 1:
    labyrinth = labyrinth1()
  elif labyrinth_num == 2:
    labyrinth = labyrinth2()
  
  start1 = generate_random_start(labyrinth.width, labyrinth.height)
  start2 = generate_random_start(labyrinth.width, labyrinth.height)
  
  while start1 in labyrinth.obstacles:
    start1 = generate_random_start(labyrinth.width, labyrinth.height)
  
  while (start2 in labyrinth.obstacles) or ((abs(start1[0] - start2[0]) + abs(start1[1] - start2[1])) <= 1):
    start2 = start2 = (random.randint(1, labyrinth.width), random.randint(1, labyrinth.height))
  
  Theseus = Fighter('THESEUS', 15, start1, {}, '', -1)
  Minotaur = Fighter('THE MINOTAUR', 20, start2, {}, '', -1)
  cheats = Cheats(False, False)
  
  print_line()
  print('Welcome to THE LABYRINTH! You are THESEUS: son of Aegeus, the king of Athens.',
        'You have recently heard that Minos, the king of Crete, has been sacrificing his enemies',
        'by sending them to by killed by THE MINOTAUR, a half-human half-bull monster.\n')
  print('You decide to take the challenge of slaying THE MINOTAUR in order to end Minos\' inhumane',
        'sacrifices once and for all. You sail from Athens to Crete and head towards THE LABYRINTH...\n')
  option = input('Enter any key to start: ')
  
  # GAME STARTS HERE
  while True:
    print('1: START GAME', '        2: CHEATS')
    option = input('Enter an option: ')
    if option == '1':
      break
    if option == '2':
      print('1: SHOW HEALTH:', cheats.show_health, '        2: SHOW HEALTH:', cheats.show_distance, '       3: MAIN MENU')
      option = input('Enter an option: ')
      while option != '3':
        print('1: SHOW HEALTH:', cheats.show_health, '        2: SHOW HEALTH:', cheats.show_distance, '       3: MAIN MENU')
        option = input('Enter an option: ')
        if option == '1':
          cheats.show_health = not cheats.show_health
          continue
        elif option == '2':
          cheats.show_distance = not cheats.show_distance
          continue
        elif option != '3':
          print('Please enter a valid option.')
          continue
      continue
    else:
      print('Please enter a valid option.')
      continue
        
  print('\nYou find THE LABYRINTH. Taking a deep breath, you delve into its mist, seeking THE MINOTAUR.')
  print_line()

  while True:
    # game actions
    if cheats.show_health:
      print('THESEUS:', str(Theseus.health) + 'HP       THE MINOTAUR:', str(Minotaur.health) + 'HP')
    
    #theseus action
    sight = in_sight(labyrinth, Theseus, Minotaur)
    if sight:
      print('THE MINOTAUR is in sight! Would you like to move or attack?')
      if cheats.show_distance and sight:
        if Theseus.distance == 1:
          print('THE MINOTAUR is', Theseus.distance, 'space away.')
        else:
          print('THE MINOTAUR is', Theseus.distance, 'spaces away.')
      action = input('Enter 1 to move or 2 to attack: ')
      while (action != '1' and action != '2'):
        action = input('Invalid entry! Please enter 1 to move or 2 to attack: ')
      
      if action == '1':
        move(labyrinth, Theseus, Minotaur, sight)
      elif action == '2':
        attack(Theseus, Minotaur)
    
    elif not sight:
      print('You do not see THE MINOTAUR.')
      move(labyrinth, Theseus, Minotaur, sight)

    if Minotaur.health <= 0:
      break
    
    # minotaur action
    sight = in_sight(labyrinth, Minotaur, Theseus)
    if Minotaur.distance == 1:
      attack(Minotaur, Theseus)
    else:
      move(labyrinth, Minotaur, Theseus, sight)
    
    print()
    
    if Theseus.health <= 0:
      break
    
  if Minotaur.health <= 0:
    print('THESEUS has bested THE MINOTAUR! He escapes THE LABYRINTH with the help of Ariadne\'s thread,',
          'and returns home to Athens with pride, glory and fame. Congratulations!')
    
  if Theseus.health <= 0:
    print('THE MINOTAUR has defeated THESEUS! You earn no pride, glory, or fame. In fact,',
          'you have earned death. THE MINOTAUR lives to kill another day.')

start_game()
