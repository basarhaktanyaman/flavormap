
def decode_message(encoded_string):
    stack = []
    queue = []
    i = 0
    
    while i < len(encoded_string):
        char = encoded_string[i]
        
        if char == '#':
            if stack:
                queue.append(stack.pop())
        elif char == '@':
            i += 1  
            i += 1  
            continue
        else:
            
            stack.append(char)
        
        i += 1
    
    queue.reverse()
    result = queue + stack
    
    return ''.join(result)


test_string = "ab#c@de#f#g"
result = decode_message(test_string)
print(f"Input: {test_string}")
print(f"Decoded message: {result}")

print("\nAdditional tests:")
print(f"decode_message('abc'): {decode_message('abc')}")
print(f"decode_message('ab#c'): {decode_message('ab#c')}")
print(f"decode_message('a@bc'): {decode_message('a@bc')}")

