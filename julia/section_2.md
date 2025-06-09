# Section 2

## Intro to functions

```julia
function youarethebest(x,y)
return x+y
end

youarethebest(3, 7)

func(x, y) = x + y
func(5,8)
```

## Implicit and explicit returns

```julia
function demo(x,y)
x+y
end

demo(6, 7)

function new(x,y)
return x*y
x+y
end

new(9, 4)
```

## Return multiple values

```julia
function a(x, y)
x+y, x*y
end

a(5, 6)

x,y = a(5,6)
x
y
```

## Operators as functions

```julia
+(2,3)

A = +

A(2,3)

function f(x, y=7)
x+y
end

f(3)
```