
## Common Pitfalls

- Garbage collection
- The compiler-generated machine code is suboptimal
- The CPU cores are insufficiently utilized
- The data is not cache friendly
- The code is not cache friendly
- The code is excessively abstracted

## CShape Specifically

- C# class instance
	- preallocated pool
- Mono Compiler or IL2CPP
- run all their code on the main thread
- a bunch of random objects scattered throughout memory
- code in a typical Unity project tends to not be cache friendly
	- object-oriented style of code
	- MonoBehaviour are invoked individually