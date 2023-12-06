# Thinking thoughts to think this through

Podemos eliminar níveis de mapeamento e mapear do 1º para o 2º directamente? Acho que sim. Vejamos como.

seeds: 79 14 55 13
seed-to-soil map:
50 98 2
52 50 48

=>

79 - 79+14 = [79,93[

No primeiro nível temos:

[50, 98[ => 52
    50 está fora de [79,93[
    98 está fora de [79,93[

=>
    50 - 78 n interessa
    79 interessa
    

[98, 100[ => 50


79 mapeamos, range 1

se as extremidades estão todas num grupo, eg:
    59 < 79 < 98
    59 < 93 < 98

Podemos alterar o mapeamento, que fica então:

[79, 93[ -> 52

Agora vamos para o nível seguinte:

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

ou por outras palavras:

15 -> 15+37 => 0-36
52 -> 52+ 2 => 37-38
0  -> 15    => 39-53

o nosso mapeamento era:
[79, 93[ -> 52

olhando para os intervalos que temos:

15 -> 15+37 => 0-36
    - nenhuma das edges está no range acima (52-52+14)

52 -> 52+ 2 => 37-38
    - nenhuma das edges está no range acima (52-52+14)

0  -> 15    => 39-53




Logo basta testar o primeiro


* Este processamento tem de ser para cada seed, notar.

...

# Esquece. E se for bottom up partir aos bocados?

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4


[56, 56+37[ -> 60+37 (somar 4)
[93, 93+ 4[ -> 56+4 (somar -37)

...

não funciona por causa do que fica fora dos intervalos. Estes valores não têm boundaries...