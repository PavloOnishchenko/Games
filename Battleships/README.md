Video on https://www.youtube.com/@DaddyWithPython/shorts coming soon...

->link will be here<-

============================================================================================

This is Demo of Sea Battle game. The goal is to show practical examples of Matrix and Collections usage.

There are three classes with constants and eleven functions: ten secondary and one main.

Among the constants: messages used in the game, ship position and markers used on the battlefield.

The first three functions are to get data from user: ship length, ship position and ship start coordinate.

Function used for taking ship start coordinate also used for taking fire coordinate. It contains an example of how to avoid regular expression, which checks entered coordinate to be allowed, by using simple String slicing and Dictionary.

Next function tries to add new ship to the battlefield if provided ship length is not out of the field range and if needed space on the field is not occupied by another ship, coming from ship start coordinate and position (vertical or horizontal).

If provided data by user was correct and ship has been placed, we mark margin around ship, not to allow place another ship closer than one square between ships. Current function checks all possible corner cases not to catch out of range exceptions. Btw, the same function is used to mark margin around ship when it was destroyed.

Then a function which reduces amount of available ships is used, to let user know which ships are still available to be placed on the battlefield.

After all ships were placed on the battlefield, all markers around ships as safe margin not needed anymore and removed by one of the functions.

When all ships are placed, we can start the game and function which will perform fire on ships is needed. Only this one function needs all types of Collections: Dictionary for provided coordinate of the fire and taking data if the ship is destroyed; Set which will collects all unique coordinates of all hit ships; Tuple because Set is immutable and we need an immutable pair for coordinate inside it; and finally fire function takes and returns modified 2D Matrix as List inside the List.

As we don't know if the ship was already destroyed after we hit it, fire function contains different cases how to check it. And while checking it fire function is working with a copy of 2D Matrix, not to mess up results with failed attempts to mark ship as destroyed.

If a ship was destroyed, fire function provides the needed data to another function, which marks margin around ship as destroyed one.

The last two secondary functions print one of the messages mentioned before in constants above, calculating dynamically changeable frame around it and the last one prints 2D Matrix as List inside the List, deciding which data will be shown or hidden on it.

Finally, the main game function executes inside it all ten secondary functions mentioned above.

Calling the main function in a special IF statement allows execution only if it was called inside the main program file. Thus, it won't be called in cases of import for testing and so on. Also, the main function isolates all its variables from being global and gives clear point of program execution.

============================================================================================

Examples of program execution:

Start from console:
<img width="1110" height="70" alt="image" src="https://github.com/user-attachments/assets/45e00658-34fb-49ad-820b-4c2bc18d2fe5" />

Read this:
<img width="1110" height="506" alt="image" src="https://github.com/user-attachments/assets/2e430001-bdb6-445c-86b5-aa9da3250d9d" />

Adding first ship:
<img width="1110" height="206" alt="image" src="https://github.com/user-attachments/assets/d679d227-3c30-41f7-a3bc-00658c4a3c0b" />

Adding next ship:
<img width="1110" height="587" alt="image" src="https://github.com/user-attachments/assets/9c5bdda7-8375-48e0-bdf9-bd3272035fc0" />

When all ships are placed:
<img width="1110" height="600" alt="image" src="https://github.com/user-attachments/assets/6b6c1c08-cf2b-4be2-960c-d500483ea312" />

Game started. First fire coordinate is needed:
<img width="1110" height="70" alt="image" src="https://github.com/user-attachments/assets/fdbb4fb2-9452-4989-946b-8358cc2d7e65" />

Game continues. Next fire coordinate is needed:
<img width="1110" height="490" alt="image" src="https://github.com/user-attachments/assets/bb3a1815-b440-497f-b56f-fa0b93ec74c6" />

Last message when all ships were destroyed:
<img width="1110" height="582" alt="image" src="https://github.com/user-attachments/assets/426b9c78-3c4c-4b8b-8798-3e1045f65a4a" />

============================================================================================

Possible wrong inputs:

<img width="1110" height="584" alt="image" src="https://github.com/user-attachments/assets/3651ca77-d4a4-4dc4-879a-4ef06f51a989" />

<img width="1110" height="603" alt="image" src="https://github.com/user-attachments/assets/2bfc3845-9f9a-48a4-8e16-70519c8caa47" />

<img width="1110" height="316" alt="image" src="https://github.com/user-attachments/assets/e6188de3-6eeb-43fe-8399-49e84736f8ef" />

<img width="1110" height="374" alt="image" src="https://github.com/user-attachments/assets/22f94b0d-0d87-40da-9528-fdc48007197a" />

<img width="1110" height="623" alt="image" src="https://github.com/user-attachments/assets/899e8b46-e0cf-4f14-a3b4-657d850559ca" />

<img width="1110" height="623" alt="image" src="https://github.com/user-attachments/assets/848141a5-8354-4908-aa93-b624ce19670a" />

<img width="1110" height="222" alt="image" src="https://github.com/user-attachments/assets/7b1a5d41-cceb-4ed3-a7d0-7507db9ca41e" />

<img width="1110" height="223" alt="image" src="https://github.com/user-attachments/assets/ab5f0bfa-c024-46b2-a667-919c58a9f745" />

<img width="1110" height="241" alt="image" src="https://github.com/user-attachments/assets/b446bf10-bd62-4d46-80ce-bb0817916df0" />
