# TODO

- win screen with statistics
  - accuracy
  - time
  - hardest pokemon
- skip button
- settings menu:
  - json file storing user's default settings, gitignored
  - first 5 letters vs full name
  - symbol exclusion
  - enter/automatic
  - sets
  - hints
  - skips
  - unordered, ordered, ordered where for a set you must name the first pokemon
  - arrow key selection menu for start screen/settings screen
- visible timer
- pause
- only take in normal keys
- control keys for special features, message at top explaining features
- prevent entire terminal from reprinting (possible?)
- update readme
- cmd + delete to delete entire line; cmd + delete glitch
- name every 25 pokemon; every 10
- continue program after finishing a game
- keep track of records

## Design Issues

- 6th character problem: if I type bulbas, then it gets bulba and then gives me the s for the next pokemon
- 5 character spoilers: nidoran-f vs nidoran-m, hitmonlee vs hitmonchan, kabuto vs kabutops, mew vs mewtwo
- Sets with evolution splits:
  - slowpoke, slowbro, ... , slowking: how to verify you knew slowking was a different generation? If you have to name each individually, it will spoil that something is wrong with this evolution line
  - burmy, wormadam, mothin: burmy not autocompleting spoils that there are two split evolutions
  - nincada same as above
