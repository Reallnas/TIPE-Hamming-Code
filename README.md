# Hamming Code implementation comparison

## Presentation

Comparison of multiple hamming code implementation done in python.
Three methods are compared (both encoding and decoding): 
- a naive method where we calculate all parity bits kind of manually.
- a standard method in linear code theory where we use a parity matrix.
- a more clever approach where we do the xor of the position of every 
bit set to one.

We also compare the standard Hamming code with the extended Hamming Code 
(where we add a global parity bit to increase the error detection capacity).

We compare the time that it takes to encode and decode a block of data, 
how time efficients the methods are compared to one another and their 
error detection and correction capacity.

Project done for the TIPE ("Travail d'Initiative Personelle Encadré" or 
"Self-Directed Supervised Work") exam of the french preparatory classes.

## Sources

Refer to `rapport/slides.pdf` for an extensive list of sources.

## Credits

Done by Reallnas in 2021.
