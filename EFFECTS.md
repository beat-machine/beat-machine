# Effects
            
This auto-generated document contains a list of effects defined in the `beatmachine` module available for loading from
JSON.

## cut
A periodic effect that cuts beats in half.

### Optional Parameters
`period`: **int**

## randomize
An effect that randomizes the order of every single beat of a song.

## remove
A periodic effect that completely removes beats.

### Optional Parameters
`period`: **int**

## repeat
A periodic effect that repeats beats a specified number of times.

### Optional Parameters
`period`: **int**

`times`: **int**

## reverse
A periodic effect that reverses beats.

### Optional Parameters
`period`: **int**

## silence
A periodic effect that silences beats, retaining their length.

### Optional Parameters
`period`: **int**

## swap
An effect that swaps every two specified beats. For example, specifying periods 2 and 4 would result in every
    second and fourth beats being swapped.

### Required Parameters
`x_period`: **int**

`y_period`: **int**

