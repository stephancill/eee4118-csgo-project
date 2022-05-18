# CSGO Spray Control via Reinforcement Learning

## Game client
Launch options
```
-insecure -novid -netconport 2121 -w 1024 -h 768 -windowed
```

## Game state
The model relies on the variation in the player camera angle. The camera angle is 
read with a script via pymem. 

The memory address of the camera angle is found with ReClass.NET:
- Run CSGO with the `-insecure` launch flag
- In CSGO, load into a map
- In console, execute `cl_showpos 1`
- Download ReClass.NET
- Run the x86 version (Source is a 32-bit engine)
- Attach to the 'csgo.exe' process
- Open 'Process > Memory Searcher...'
- Check the first angle value in CSGO showpos
- In memory searcher, enter the value to be the first value in CSGO
- Set value type to be `Float`
- Press First Scan
- In CSGO, move the mouse to change the value and observe which values in the address scanner match the updated value
- Record the address of the first value
- Repeat for second angle value

With the known memory addresses, you can read the values via pymem in a script.

## Input
Ensure the raw_input setting is off

## Trained model comments
### A2C_4
Model peaks and then falls off because the learning rate is too high (0.1), each change makes it overshoot by far because it chooses an action on the boundaries [-1, 1], constantly overshooting the target.

### A2C_10 `ak47_1652911551.zip`
Lower learning rate (0.001) makes it converge much more quickly. One note is that the it cannot reach the target in one step because the action space is too small. I.e. it has to correct by a distance of > 1 but can only move 1 unit.