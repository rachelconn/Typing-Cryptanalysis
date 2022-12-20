from collections import defaultdict

character_class_idx = {
    'a': 0,
    'A': 0,
    'b': 1,
    'B': 1,
    'c': 2,
    'C': 2,
    'd': 3,
    'D': 3,
    'e': 4,
    'E': 4,
    'f': 5,
    'F': 5,
    'g': 6,
    'G': 6,
    'h': 7,
    'H': 7,
    'i': 8,
    'I': 8,
    'j': 9,
    'J': 9,
    'k': 10,
    'K': 10,
    'l': 11,
    'L': 11,
    'm': 12,
    'M': 12,
    'n': 13,
    'N': 13,
    'o': 14,
    'O': 14,
    'p': 15,
    'P': 15,
    'q': 16,
    'Q': 16,
    'r': 17,
    'R': 17,
    's': 18,
    'S': 18,
    't': 19,
    'T': 19,
    'u': 20,
    'U': 20,
    'v': 21,
    'V': 21,
    'w': 22,
    'W': 22,
    'x': 23,
    'X': 23,
    'y': 24,
    'Y': 24,
    'z': 25,
    'Z': 25,
    '1': 26,
    '!': 26,
    '2': 27,
    '@': 28,
    '3': 28,
    '#': 28,
    '4': 29,
    '$': 29,
    '5': 30,
    '%': 30,
    '6': 31,
    '^': 31,
    '7': 32,
    '&': 32,
    '8': 33,
    '*': 33,
    '9': 34,
    '(': 34,
    '0': 35,
    ')': 35,
    '-': 36,
    '_': 36,
    '=': 37,
    '+': 37,
    'backspace': 38,
    'tab': 39,
    '[': 40,
    '{': 40,
    ']': 41,
    '}': 41,
    'capslock': 42,
    ':': 43,
    ';': 43,
    "'": 44,
    '"': 44,
    '\\': 45,
    '|': 45,
    'enter': 46,
    'shift': 47,
    'rightshift': 47,
    ',': 48,
    '<': 48,
    '.': 49,
    '>': 49,
    '/': 50,
    '?': 50,
    'ctrl': 51,
    'rightctrl': 51,
    'leftwindows': 52,
    'rightwindows': 52,
    'alt': 53,
    'rightalt': 53,
    'insert': 54,
    'home': 55,
    'pageup': 56,
    'delete': 57,
    'end': 58,
    'pagedown': 59,
    'f1': 60,
    'f2': 60,
    'f3': 60,
    'f4': 60,
    'f5': 60,
    'f6': 60,
    'f7': 60,
    'f8': 60,
    'f9': 60,
    'f10': 60,
    'f11': 60,
    'f12': 60,
    'up': 61,
    'right': 62,
    'down': 63,
    'left': 64,
    'esc': 65,
    '`': 66,
    '~': 66,
    'space': 67,
}

character_class_idx_reduced = defaultdict(lambda: 26)
character_class_idx_reduced.update(
    {
        'a': 0,
        'A': 0,
        'b': 1,
        'B': 1,
        'c': 2,
        'C': 2,
        'd': 3,
        'D': 3,
        'e': 4,
        'E': 4,
        'f': 5,
        'F': 5,
        'g': 6,
        'G': 6,
        'h': 7,
        'H': 7,
        'i': 8,
        'I': 8,
        'j': 9,
        'J': 9,
        'k': 10,
        'K': 10,
        'l': 11,
        'L': 11,
        'm': 12,
        'M': 12,
        'n': 13,
        'N': 13,
        'o': 14,
        'O': 14,
        'p': 15,
        'P': 15,
        'q': 16,
        'Q': 16,
        'r': 17,
        'R': 17,
        's': 18,
        'S': 18,
        't': 19,
        'T': 19,
        'u': 20,
        'U': 20,
        'v': 21,
        'V': 21,
        'w': 22,
        'W': 22,
        'x': 23,
        'X': 23,
        'y': 24,
        'Y': 24,
        'z': 25,
        'Z': 25,
    }
)

character_for_idx = {v: k for k, v in character_class_idx_reduced.items()}

def get_character_class(character: str) -> int:
    if character == 'space':
        return ord('|')
    # Add 0x20 to skip utf-8 control characters and space
    return character_class_idx_reduced[character.lower()] + 0x21

def decode(transcription: str) -> str:
    decoded = []
    for character in transcription:
        if character == '|':
            decoded.append(' ')
        elif character == ';':
            decoded.append('$')
        else:
            decoded.append(character_for_idx[ord(character) - 0x21])
    return ''.join(decoded)
