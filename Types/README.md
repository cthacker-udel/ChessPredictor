
# Types Directory
> This is the directory that houses all the types we will be using throughout the implementation of this project.
> - We have each chess piece inheriting from the base class **ChessPiece** to standardize the fields, 
> - We have classes for detailing the move-sets of each individual chess piece with the **MoveSet** class 
>   - The **MoveSet** class also has an extra class called **InfiniteDirection**, that allows for the backend to know if a piece can move infinitely in either the x|y plane, or both simultaneously (aka diagonally)