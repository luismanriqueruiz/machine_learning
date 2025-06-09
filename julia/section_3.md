# Section 3

## Conditional statements: If else

```julia
x = 5

if x < 0
print("Negative")
else
print("Positive")
end


if x<0
print("Negative")
elseif x > 0
print("Positive")
else
print("Zero")
end
```

## Ternary operator

```julia

x = 5

print(x>0 ? "pos" : "neg")