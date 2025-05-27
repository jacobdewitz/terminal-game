sprites = {

    "SPIKE":
        """   ^
         /   \\
        |_____|""",

    "small_spike_top": """/\\""",
    # needs at least one space between the left edge of the 'screen' to position correctly
    "small_spike_bottom": """/__\\""",  # two characters wider than the top

    'PLAYER':
        """
        """

}

my_string = f"{'' * 1}{sprites['small_spike_top']}{' ' * 10}{sprites['small_spike_top']}"
# the second string has 3 fewer spaces because the bottom spike sprite is 2 spaces wider
# and then also starts one character "earlier"
my_string2 = f"{sprites['small_spike_bottom']}{' ' * 8}{sprites['small_spike_bottom']}"
print(my_string, sep='', end='')
print()
print(my_string2, sep='', end='')
