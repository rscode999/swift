_KEY_LENGTHS = [2,3,5,7,11,13,17,23,27]



def _assert_preconditions(input: str, keys: list[str], n_subkeys: int) -> None:
    """
    Raises an AssertionError if any operation preconditions are broken.
    """
    assert isinstance(input, str), "input must be a string"
    assert isinstance(keys, list), "key must be a list"
    assert isinstance(n_subkeys, int) and n_subkeys>0, "number of subkeys must be a positive integer"
    assert len(keys)>=n_subkeys, "key must be a list of length at least " + str(n_subkeys)
    for k in keys:
        assert isinstance(k, str), "all key indices must be strings"
        assert len(k)>0, "all key indices must have positive length"
        for c in k:
            assert 97 <= ord(c) <= 122, "all key indices must be strings of lowercase English ASCII characters"



def encr(input: str, keys: list[str], n_subkeys: int = 7) -> str:
    """
    Encrypts `input` using the keys `keys`, using the first `n_used_keys` of the keys in `keys`.

    Parameters:
        input (str): input text to encrypt
        keys (list[str]): keys to use. Must have nonzero length. Strings must not be empty and contain only English lowercase letters.
        n_used_keys (int): amount of keys to use in the given keys. Must be at least the length of the `keys` list.
    Returns:
        `input` encrypted with `keys`
    """
    _assert_preconditions(input, keys, n_subkeys)


    effective_key_lengths = [] #make a deep copy
    while(len(effective_key_lengths) < n_subkeys):
        effective_key_lengths.append(_KEY_LENGTHS[len(effective_key_lengths) % len(_KEY_LENGTHS)])


    effective_keys = []
    for k in range(n_subkeys):
        new_subkey = ""
        
        while len(new_subkey) < effective_key_lengths[k]:
            new_subkey += keys[k]

        effective_keys.append(new_subkey[:effective_key_lengths[k]])


    n_alpha_chars = 0

    output = ""
    for input_char in input:

        if not (65<=ord(input_char)<=90 or 97<=ord(input_char)<=122):
            output += input_char
        
        else:
            is_upper = 65 <= ord(input_char) <= 90

            input_value = (ord(input_char) - 65) if is_upper else (ord(input_char) - 97)
            
            composite_value = 0
            for k in range(n_subkeys):
                k_char = effective_keys[k][n_alpha_chars % len(effective_keys[k])]
                composite_value += ord(k_char)-97
                
            composite_value = composite_value % 26

            output_value = (input_value + composite_value) % 26

            output += chr(output_value + 65) if is_upper else chr(output_value + 97)
            
            n_alpha_chars += 1

    return output



def decr(input: str, keys: list[str], n_used_keys: int = 7) -> str:
    """
    Decrypts `input` using the keys `keys`, using the first `n_used_keys` of the keys in `keys`.

    Parameters:
        input (str): input text to decrypt
        keys (list[str]): keys to use. Must have nonzero length. Strings must not be empty and contain only English lowercase letters.
        n_used_keys (int): amount of keys to use in the given keys. Must be at least the length of the `keys` list.
    Returns:
        `input` decrypted with `keys`
    """
    _assert_preconditions(input, keys, n_used_keys)


    effective_key_lengths = [] #make a deep copy
    while(len(effective_key_lengths) < n_used_keys):
        effective_key_lengths.append(_KEY_LENGTHS[len(effective_key_lengths) % len(_KEY_LENGTHS)])


    effective_keys = []
    for k in range(n_used_keys):
        new_subkey = ""
        
        while len(new_subkey) < effective_key_lengths[k]:
            new_subkey += keys[k]

        effective_keys.append(new_subkey[:effective_key_lengths[k]])
    

    n_alpha_chars = 0
    for i in input:
        if 65<=ord(i)<=90 or 97<=ord(i)<=122:
            n_alpha_chars += 1

    output = ""
    for input_char in reversed(input):

        if not (65<=ord(input_char)<=90 or 97<=ord(input_char)<=122):
            output += input_char
        
        else:
            n_alpha_chars -= 1

            is_upper = 65 <= ord(input_char) <= 90

            input_value = (ord(input_char) - 65) if is_upper else (ord(input_char) - 97)
            
            composite_value = 0
            for k in range(n_used_keys):
                k_char = effective_keys[k][n_alpha_chars % len(effective_keys[k])]
                composite_value += ord(k_char)-97
                
            composite_value = composite_value % 26

            output_value = (input_value - composite_value) % 26
            if output_value < 0:
                output_value += 26

            output += chr(output_value + 65) if is_upper else chr(output_value + 97)     
            
    return output[::-1]



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--decr', '-d', action='store_true', help='Flag to decrypt the given input')
    parser.add_argument('--in-file', default="", type=str, help='Input filepath to use. Must lead to a *.txt file')
    parser.add_argument('--out-file', default="", type=str, help='Output filepath to use. Must lead to a *.txt file')
    parser.add_argument('--keys', '-k', default="", type=str, help='Comma-separated list of keys to use during the operation. Must contain English lowercase characters only (no spaces anywhere).')
    parser.add_argument('--n-keys', '-nsk', default=7, type=int, help='The first N keys to use in the list of given keys. Must be an integer greater than or equal to the number of keys used. Default 7')
    args = parser.parse_args()
    #Note: If the --in-file and --out-file are not set, their lengths are 0

    #File extension checks
    if len(args.in_file)>0 and not args.in_file.endswith('.txt'):
        parser.error(f'Input file "({args.in_file})" must end in ".txt"')
    if len(args.out_file)>0 and not args.out_file.endswith('.txt'):
        parser.error(f'Output file "({args.out_file})" must end in ".txt"')

    #Ensure the input file exists
    if len(args.in_file) > 0:
        try:
            with open(args.in_file, 'r') as check:
                pass
        except FileNotFoundError:
            parser.error(f'The input file "{args.in_file}" does not exist')


    #Make the key, as a list
    keys = None
    if len(args.keys) > 0:
        keys = args.keys.replace(' ', '').split(",")
        #Check the key
        for k, key in enumerate(keys):
            if len(key)==0:
                parser.error(f"Subkey {k+1} cannot be the empty string")
            for l, letter in enumerate(key):
                if not 97<=ord(letter)<=122:
                    parser.error(f"Character {l+1} in subkey {k+1} ('{letter}') must be an English lowercase letter")
        
        #Check number of subkeys
        if args.n_keys < len(keys):
            parser.error(f"Number of keys used ({args.n_keys}) must be at least {len(keys)}, the number of keys used")


    #Take the input
    text = ""
    if len(args.in_file)>0:
        #File read
        with open(args.in_file, 'r') as f:
            text = f.read()
    else:
        #Standard input read
        text = input("Enter ciphertext: " if args.decr else "Enter plaintext: ")
    

    #Take the keys (if not defined yet)
    if not keys:
        keys = input("Enter keys (comma-separated): ").replace(' ', '').split(',')

        #Check the key. Redundant, but I feel like this is the best option
        for k, key in enumerate(keys):
            if len(key)==0:
                parser.error(f"Subkey {k+1} cannot be the empty string")
            for l, letter in enumerate(key):
                if not 97<=ord(letter)<=122:
                    parser.error(f"Character {l+1} in subkey {k+1} ('{letter}') must be an English lowercase letter")

        #Check number of keys
        if len(keys) < args.n_keys:
            parser.error(f"Number of keys used ({args.n_keys}) must be at most {len(keys)}, the actual number of keys used. Use the option `--n-subkeys [N]`")


    #Do the operation
    text = decr(text, keys, n_used_keys=args.n_keys) if args.decr else encr(text, keys, n_subkeys=args.n_keys)


    #Make the output
    if len(args.out_file) > 0:
        #File write
        with open(args.out_file, 'w') as f:
            f.write(text)
        print(f'Output printed to "{args.out_file}"')
    else:
        #Standard output print
        print()
        print("Plaintext: " if args.decr else "Ciphertext: ", end='', flush=True)
        print(text, flush=True)

    print()