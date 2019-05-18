# First project of Processing and Recognition of Images course
This project was about matching parts of rectangles to their corresponding part.
We used following algorithm to do that:
1. Find contours of a rectangle's fragment.
2. Choose two vertices of a base.
3. Find start and end of a cut.
4. Transform the cut to a one-dimensional array.
5. Do the Fourrier transform and normalize it's results.
6. Find another fragment that fits the most.
