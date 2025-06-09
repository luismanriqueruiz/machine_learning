# Section 1

## 1. Introduction

## 2. Setup

### Execution
```bash
julia
```

### execute selected text in vscode
workbench.action.terminal.runSelectedText

```
ctrl + alt + s
```

## 3. Variables

```julia
x = 2

typeof(x)

x = "ok"

#=
x = 'ok' #not possible
=#

pi

sqrt(49)
```

## 4. Mathematical calculations

```julia
x = 5.4
typeof(x)

5+6

6/7

5/2
result = 2.5

div(5, 2)
result = 2

5%2

3^8
```

## 5. Bitwise operations

```julia
Binary instead of bits

bitstring(3)

bitstring(7)

and operation
3 & 7

or operation
3 | 7
```

## 7. Polynomial equation

```julia
x = 5

3*x*x + 5*x + 6

3*x*x + 5*x + 6

3x^2 + 5x + 6
```

## 10. ASCII and UNICODE

```julia
'A'

typeof('A')

'\u2665'

Int('A')
```

## 11. Strings and memory indexing

```julia
text = "Hello world"

text[2]

text[end]

text[end-1]
```

## 12. String to substring

```julia
x = """Hello World"""

x[1:5]

x[7:end]
```