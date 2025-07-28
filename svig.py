
_KEY_ROTATIONS = [2,3,5,7,11,13,17,23,27]


def encr(input: str, keys: list[str], n_subkeys: int = 7) -> str:
    """
    EXPERIMENTAL
    """
    assert isinstance(input, str), "input must be a string"
    assert isinstance(keys, list), "key must be a list"
    assert len(keys)>=n_subkeys, "key must be a list of length at least " + str(n_subkeys)
    for k in keys:
        assert isinstance(k, str), "all key indices must be strings"
        assert len(k)>0, "all key indices must have positive length"
        for c in k:
            assert 97 <= ord(c) <= 122, "all key indices must be strings of lowercase English ASCII characters"
    

    effective_keys = []
    for k in range(n_subkeys):
        new_subkey = ""
        
        while len(new_subkey) < _KEY_ROTATIONS[k]:
            new_subkey += keys[k]

        effective_keys.append(new_subkey[:_KEY_ROTATIONS[k]])


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



def decr(input: str, keys: list[str], n_subkeys: int = 7) -> str:
    """
    EXPERIMENTAL
    """
    assert isinstance(input, str), "input must be a string"
    assert isinstance(keys, list), "key must be a list"
    assert len(keys)>=n_subkeys, "key must be a list of length at least " + str(n_subkeys)
    for k in keys:
        assert isinstance(k, str), "all key indices must be strings"
        assert len(k)>0, "all key indices must have positive length"
        for c in k:
            assert 97 <= ord(c) <= 122, "all key indices must be strings of lowercase English ASCII characters"

    effective_keys = []
    for k in range(n_subkeys):
        new_subkey = ""
        
        while len(new_subkey) < _KEY_ROTATIONS[k]:
            new_subkey += keys[k]

        effective_keys.append(new_subkey[:_KEY_ROTATIONS[k]])
    

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
            for k in range(n_subkeys):
                k_char = effective_keys[k][n_alpha_chars % len(effective_keys[k])]
                composite_value += ord(k_char)-97
                
            composite_value = composite_value % 26

            output_value = (input_value - composite_value) % 26
            if output_value < 0:
                output_value += 26

            output += chr(output_value + 65) if is_upper else chr(output_value + 97)     
            

    return output



if __name__ == '__main__':
    ct = encr('aaaa aaaa', ['ab', 'cde', 'fghij', 'zyx'], n_subkeys=4)
    print(ct)

    pt = decr(ct, ['ab', 'cde', 'fghij', 'zyx'], n_subkeys=4)
    print(pt)