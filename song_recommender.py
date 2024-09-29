import random
from tree_node import TreeNode
import csv

#set up empty dictionary for songs
song_dictionary = {}
#set up root for data tree
music = TreeNode('Song Tree')

#builds genre dictionary using csv file
def dictionary_builder():
  with open('songs.csv', 'r') as file:
    read = csv.DictReader(file)
    for row in read:
      if row['genre'] not in song_dictionary:
        song_dictionary[row['genre']] = {row['artist']: [row['songs']]}
      elif row['artist'] not in song_dictionary[row['genre']]:
        song_dictionary[row['genre']].update({row['artist']: [row['songs']]})
      elif row['songs'] not in song_dictionary[row['genre']][row['artist']]:
        song_dictionary[row['genre']][row['artist']].append(row['songs'])

#comparison method for strings for quicksort
def text_comparison(text_a, text_b):
  if text_a.lower() > text_b.lower():
    return True
  else:
    return False

#comparison method for lists of nodes based on node values for quicksort
def string_node_comparison(node_a, node_b):
  if node_a.value.lower() > node_b.value.lower():
    return True
  else:
    return False

#quicksort implementation
def quicksort(list, start, end, comparison_function = text_comparison):
  if start >= end:
    return
  pivot_idx = random.randrange(start, end + 1)
  pivot_element = list[pivot_idx]
  list[end], list[pivot_idx] = list[pivot_idx], list[end]
  less_than_pointer = start
  for i in range(start, end):
    if comparison_function(pivot_element, list[i]):
      list[i], list[less_than_pointer] = list[less_than_pointer], list[i]
      less_than_pointer += 1
  list[end], list[less_than_pointer] = list[less_than_pointer], list[end]
  quicksort(list, start, less_than_pointer - 1, comparison_function)
  quicksort(list, less_than_pointer + 1, end, comparison_function)

#This function assumes that the data is in a well-constructed dictionary (the correct data structure for what the program needs to do).
#However, in the name of computer science education, the data will be transferred into a data tree (not a supported Python data structure type).
#It probably goes without saying that if this weren't an implied project requirement, it would be left out completely and the rest of the program
#would just go ahead with the dictionary.
def tree_builder():
  #because the dictionary is set up as a roughly analogous data structure, it is straightforward to iterate through to set up the data tree
  for genre in song_dictionary.keys():
    genre_node = TreeNode(genre)
    music.add_child(genre_node)
    for artist in song_dictionary[genre].keys():
      artist_node = TreeNode(artist)
      genre_node.add_child(artist_node)
      song_list_node = TreeNode(song_dictionary[genre][artist])
      artist_node.add_child(song_list_node)
  #list values for genres and artists are quicksorted into alphabetical order
  quicksort(music.children, 0, len(music.children)-1, string_node_comparison)
  for child in music.children:
    quicksort(child.children, 0, len(child.children)-1, string_node_comparison)

#user interactions will be handled through menus, taking advantage of data being stored within orderly data structure:
def node_children_to_menu(menu_node):
  for i in range(len(menu_node.children)):
    print("{} - {}".format(i, menu_node.children[i].value))

#menu inputs will return nodes.  The purpose of user inputs is to move to different points on the data tree.
def get_menu_input(menu_node):
  #establish a list of valid user inputs to check against:
  valid_inputs = [str(i) for i in range(len(menu_node.children))]
  #User input should correspond to a number from a menu:
  user_choice = input('\nEnter a number corresponding to one of the menu choices above\n')
  while user_choice not in valid_inputs:
    user_choice = input("Uh oh.  Let's try again.  Enter a number from {} to {}.\n".format(valid_inputs[0], valid_inputs[-1]))

  return menu_node.children[int(user_choice)]

#genre choice function:
def genre_choice():
  print("\n('working title for song recommender') has the following musical genres:\n")
  node_children_to_menu(music)
  genre_pick = get_menu_input(music)
  print("\nVery cool!  You might want to check out music by the following artists:\n")
  node_children_to_menu(genre_pick)
  song_request = input("\nWould you like to get a list of songs from one of these artists? (y/n)\n")
  if song_request == 'y':
    artist_choice(genre_pick)
  again = input("\nWould you like to check out some recommendations from other genres? (y/n)\n")
  if again == 'y':
    return genre_choice()

#function to access song lists from genre artists:
def artist_choice(genre_node):
  artist_pick = get_menu_input(genre_node)
  #each artist node has a single child node, with the value of a list of songs by the artist:
  song_list = artist_pick.children[0].value
  #once selected, the list is quicksorted:
  quicksort(song_list, 0, len(song_list) - 1)
  print("Great choice! {}'s best {} song(s): ".format(artist_pick.value, genre_node.value))
  for song in song_list:
    print(song)
  again = input("\nDo you want to check out song recommendations from other {} artists? (y/n)\n".format(genre_node.value))
  if again == 'y':
    refresh_menu = input("Let's keep going.  Do you want to see the artist menu again? (y/n)\n")
    if refresh_menu == 'y':
      node_children_to_menu(genre_node)
    return artist_choice(genre_node)

#say hi to the people:
def welcome():
  print("Welcome to ('working title for song recommender')!  Let's get started.\n")

#say goodbye to the people:
def goodbye():
  print("\nThank you for using ('working title for song recommender').  Goodbye.")

#main function
def main():

  welcome()
  dictionary_builder()
  tree_builder()
  genre_choice()
  goodbye()

main()