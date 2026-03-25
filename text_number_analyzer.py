

def is_anagram(word1, word2):

    return sorted(word1.lower()) == sorted(word2.lower()) and word1.lower() != word2.lower()


def is_palindrome(word):    
    clean_word = ''.join(c for c in word if c.isalpha()).lower()
    return clean_word == clean_word[::-1]


def get_last_digit(word):
    digits = [c for c in word if c.isdigit()]
    return digits[-1] if digits else None


def caesar_cipher(word, shift=3):
    result = ""
    for char in word:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result


def find_anagrams(word, word_list):
    anagrams = []
    for other_word in word_list:
        if is_anagram(word, other_word):
            anagrams.append(other_word)
    return anagrams


def to_binary(num):
    return bin(num)[2:]


def gcd_euclid(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num ** 0.5) + 1, 2):
        if num % i == 0:
            return False
    return True


def analyze_words(words):
    results = {}
    
    for word in words:
        word_results = {
            'palindrome': is_palindrome(word),
            'anagrams': find_anagrams(word, words),
            'last_digit': get_last_digit(word),
            'caesar_cipher': caesar_cipher(word, 3)
        }
        results[word] = word_results
    
    return results


def analyze_numbers(num1, num2):
    results = {
        'number1': {
            'value': num1,
            'binary': to_binary(num1),
            'is_prime': is_prime(num1)
        },
        'number2': {
            'value': num2,
            'binary': to_binary(num2),
            'is_prime': is_prime(num2)
        },
        'gcd': gcd_euclid(num1, num2)
    }
    
    return results


def print_word_results(word_results):
    print("\n" + "=" * 50)
    print("📝 WORD ANALYSIS RESULTS")
    print("=" * 50)
    
    for word, data in word_results.items():
        print(f"\nWord: {word}")
        print(f"  Palindrome: {data['palindrome']}")
        
        if data['anagrams']:
            print(f"  Anagrams: {', '.join(data['anagrams'])}")
        else:
            print(f"  Anagrams: No")
        
        print(f"  Last digit: {data['last_digit'] if data['last_digit'] else 'None'}")
        print(f"  Caesar cipher: {data['caesar_cipher']}")


def print_number_results(number_results):
    print("\n" + "=" * 50)
    print("🔢 NUMBER ANALYSIS RESULTS")
    print("=" * 50)
    
    num1_data = number_results['number1']
    num2_data = number_results['number2']
    
    print(f"\nNumber 1: {num1_data['value']}")
    print(f"  Binary: {num1_data['binary']}")
    print(f"  Is Prime: {num1_data['is_prime']}")
    
    print(f"\nNumber 2: {num2_data['value']}")
    print(f"  Binary: {num2_data['binary']}")
    print(f"  Is Prime: {num2_data['is_prime']}")
    
    print(f"\nGCD of {num1_data['value']} and {num2_data['value']}: {number_results['gcd']}")


def main():
    print("=" * 50)
    print("  Multi-Feature Text & Number Analyzer")
    print("=" * 50)
    
    words = ["racecar", "arc", "car", "hello1", "noon"]
    num1 = 20
    num2 = 12
    
    print(f"\n📋 Input:")
    print(f"  Words: {words}")
    print(f"  Integers: {num1} and {num2}")
    
    word_results = analyze_words(words)
    print_word_results(word_results)
    
    number_results = analyze_numbers(num1, num2)
    print_number_results(number_results)
    
    print("\n" + "=" * 50)
    print("✅ Analysis Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()

