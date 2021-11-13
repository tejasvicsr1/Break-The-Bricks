# Copy of Assignment Template

---

## Design and Analysis of Software Systems

---

### Tejasvi Chebrolu

2019114005

---

# Break The Bricks

A terminal game created without any curses libraries like `Pygame` for the course Design and Analysis of Software Systems. This is a recreation of the common *brick breaker game* in Python with additional *powerups* like multiple balls, etc.

The purpose of the game is to develop and understand skills related to **Object Oriented Programming**.

---

## Setup

To install libraries: 

```bash
pip3 install numpy
pip3 install colorama
pip3 install art
```

---

## Execution

```bash
python3 main.py
```

Make sure you are in the directory before running this command.

---

## Rules

**`a`**: To move left

**`d`**: To move right

**`Spacebar`**: To release the ball

**`q`**: To quit the game

- 10 points awarded for every destroyed brick.
- Life ends when the ball touches the floor.

---

## Features

- Multiple lives.
- Different kinds of bricks:
    - **OneTouch** - Explode with one hit
    - **TwoTouch** - Explode with two hits
    - **Exploding** - Destroy all blocks in the surrounding area
    - **Indestructible** - Cannot be destroyed
- Different Powerups:
    - **Expand** - Expand paddle size
    - **Shrink** - Shrink paddle size
    - **Multiple** - Multiple balls in play at the same time
    - **Grab** - Grab the ball onto the paddle
    - **Through** - Go through blocks
    - **Fast** - Increase ball speed

---

## Concepts

### Inheritance

Common attributes of the parent class is inherited by the child classes. This helps in avoiding redundant code.

```python
class Shrink(PowerUp):

    def __init__(self, x, y):
        text = "S"
        super().__init__( x, y)
        self._matrix = text

    def getPowerUp(self):
        text = "shrink"
        return text
```

### Polymorphism

Utilizing the same function of a parent class for different functionalities of child classes based on the list of parameters passed. This helps in avoiding redundancy.

```python
class Thru(PowerUp):
    
    def __init__(self, x, y):
        text = "T"
        super().__init__( x, y)
# Example of polymorphism
        self._matrix = text

    def getPowerUp(self):
        text = "thru"
        return text
```

### Encapsulation

Every component on the board is an object of a class. This instantiation encapsulates the methods and attributes of the objects.

### Abstraction

The functions of each class hide the inner details of the function enabling users to use just the function name.

```python
paddlewidth = self._paddle.getPositionX() + int(self._paddle.getWidth()/2)
```

---