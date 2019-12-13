# rcpcs
RCPCS - Room Control and Puzzle Coordination System

# Elements of the system:

## Room Controller


## Media Controller


## Lighting Controller


## Puzzle Controller(s)

- **NFC-ALGO** :: A single NFC reader for an arbitrary number of tags in play.
In order to solve the puzzle, each tag must be read by the reader in the
correct order. Tags may be re-used multiple times in the pattern, but it's
not a good idea to use the same tag twice consecutively as that could cause
gameplay logic problems.

- **NFC-AND** :: Arbitrary number of NFC readers with one, and exactly one
matching tag. All tags must be in place and read in the same pass in order
to solve the puzzle. Referred to by some people as an "Einstein Puzzle".

- **ARDUINO Configurable Puzzle Controller** :: *need to commit* Built on an Arduino Mega2560
  platform, this one code-base can handle many different styles of puzzle
without require custom code.

- **Touchscreen Finger Puzzle** :: *need to commit* Works like an Android
  phone screen unlock interface.
