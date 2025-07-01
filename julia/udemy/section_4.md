# Section 4

## For loop

```julia

for i = 1:10
println(i)
end


for arr in [2,7,9]
println(arr)
end


for c in ["carlos", "luis", "hello"]
println(c)
end


for c in ["carlos", "luis", "hello"]
println(c, " our output is this")
end
```

## While loop

```julia

x = 1

while x < 6
println(x)
x += 1
end
```

## Continue

```julia

for x in 1:10
if x%2 == 0
continue
end
println(x)
end


for x in 1:10
if x%2 == 0
continue
end
println(x*x)
end
```
