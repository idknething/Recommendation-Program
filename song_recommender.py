import random
from tree_node import TreeNode
import csv

#set up root for data tree
music = TreeNode('Song Tree')

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

#function to read csv data into a data tree structure
def new_tree_builder():
    with open('songs.csv', 'r') as file:
      read = csv.DictReader(file)
      for row in read:
        if music.is_in(row['genre']) == False:
          genre_node = TreeNode(row['genre'])
          music.add_child(genre_node)
          artist_node = TreeNode(row['artist'])
          genre_node.add_child(artist_node)
          song_node = TreeNode([row['songs']])
          artist_node.add_child(song_node)
        else:
          genre_node = music.get_child_node(row['genre'])
          if genre_node.is_in(row['artist']) == False:
            artist_node = TreeNode(row['artist'])
            genre_node.add_child(artist_node)
            song_node = TreeNode([row['songs']])
            artist_node.add_child(song_node)
          else:
            artist_node = genre_node.get_child_node(row['artist'])
            song_node = artist_node.children[0]
            if row['songs'] not in song_node.value:
              song_node.value.append(row['songs'])
    #quicksort the list of genre nodes
    quicksort(music.children, 0, len(music.children) -1, string_node_comparison)

#function to compile list of songs in genre and print it:
def print_songlist(genre_node):
  songlist = []
  for artist_node in genre_node.children:
    for song in artist_node.children[0].value:
      songlist += [song + ', by ' + artist_node.value]

  quicksort(songlist, 0, len(songlist)-1)
  print(f"\nElectronic Music Finder recommends:\n")
  for song in songlist:
    print(song)

#genre choice function:
def genre_choice():

  selected_genre = None
  genre_list = [child.value for child in music.children]
  print("What genre of electronic music are you interested in?  Type in the start of the genre name to search.")
  while selected_genre is None:
    user_input = str(input("\n")).lower()
    matchlist = [genre for genre in genre_list if genre.lower().startswith(user_input)]

    print("\nThese genres match your search:")
    for match in matchlist:
      print(match)

    if len(matchlist) == 1:
      user_input = str(input(f"\nDo you want to see {matchlist[0]} song recommendations? (y/n) ")).lower()
      if user_input == 'y':
        selected_genre = music.get_child_node(matchlist[0])
      else:
        print("\nSorry this wasn't what you were looking for.  Type in a new search to keep looking.")
    else:
      print("\nEnter more of the genre name to narrow down the search options, or start a new search for something else.\n")

  print_songlist(selected_genre)

  again = input("\nWould you like to check out some recommendations from other genres? (y/n)\n")
  if again == 'y':
    return genre_choice()

#say hi to the people:
def welcome():
  print("Welcome to Electronic Music Finder!  Let's get started.\n")

#say goodbye to the people:
def goodbye():
  print("\nThank you for using Electronic Music Finder!  Goodbye.")

#main function
def main():

  welcome()
  new_tree_builder()
  genre_choice()
  goodbye()

main()