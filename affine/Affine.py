import math
import unicodedata

alphaWithValue = {"A": 0, "B": 1, "C": 2, "D": 3,
                  "E": 4, "F": 5, "G": 6, "H": 7,
                  "I": 8, "J": 9, "K": 10, "L": 11,
                  "M": 12, "N": 13, "Ñ": 14, "O": 15,
                  "P": 16, "Q": 17, "R": 18, "S": 19,
                  "T": 20, "U": 21, "V": 22, "W": 23,
                  "X": 24, "Y": 25, "Z": 26}

valueByAlphabet = {0: "A", 1: "B", 2: "C", 3: "D",
                   4: "E", 5: "F", 6: "G", 7: "H",
                   8: "I", 9: "J", 10: "K", 11: "L",
                   12: "M", 13: "N", 14: "Ñ", 15: "O",
                   16: "P", 17: "Q", 18: "R", 19: "S",
                   20: "T", 21: "U", 22: "V", 23: "W",
                   24: "X", 25: "Y", 26: "Z"}


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def fact(n):
    fact_n = []
    for num in range(1, n + 1):
        if n % num == 0:
            fact_n.append(num)
    return fact_n


def encrypt_text(msg: str, key_a: int, key_b: int) -> str:
    new_msg = []
    for ch in msg:
        char = ((key_a * alphaWithValue[ch]) + key_b) % (len(alphaWithValue))
        new_msg.append(valueByAlphabet[char])
    return "".join(new_msg)


def normalize_msg(msg: str) -> str:
    normalized = unicodedata.normalize('NFD', msg.replace("\n", ""))
    new_msg = u"".join([c for c in normalized if not unicodedata.combining(c)])
    return "".join(e for e in new_msg if e.isalnum()).upper()


def decrypt_text(msg: str, key_a: int, key_b: int) -> str:
    new_msg = []
    inv_a_m = modinv(key_a, len(alphaWithValue))
    if inv_a_m is None:
        return ""
    for ch in msg:
        char = (inv_a_m * (alphaWithValue[ch] - key_b)) % (len(alphaWithValue))
        new_msg.append(valueByAlphabet[char])
    return "".join(new_msg) + "\n key_a=" + str(key_a) + " key_b=" + str(key_b)


def build_decrypt_text(msg: str, key_a: int, key_b: int) -> [str]:
    if key_a == key_b:
        return [decrypt_text(msg, key_a, key_b)]
    else:
        return [decrypt_text(msg, key_a, key_b), decrypt_text(msg, key_b, key_a)]


def build_decrypt_text_with_keys(msg: str, key_a: int, key_b: int) -> [str]:
    return [decrypt_text(msg, key_a, key_b)]


def executeFact(a: int, b: int) -> bool:
    values_for_a = fact(a)
    values_for_b = fact(b)
    print("Factores de {} = {}".format(a, values_for_a))
    print("Factores de {} = {}".format(b, values_for_b))
    equals_items = []

    for vA in values_for_a:
        for vB in values_for_b:
            if vA == vB:
                equals_items.append(vA)

    print("equal items", equals_items)

    # Checar cuáles números del 1 al 26 son coprimos
    probables = []
    for i in range(a, b + 1):
        if math.gcd(i, b) == 1:
            probables.append(i)
    print("Números que se pueden usar: ", probables)

    return len(equals_items) == 1


def get_force_keys(msg: str) -> (int, int):
    letters = qualify_msg(msg)
    a_dict = list(letters['a'])[0]
    e_dict = list(letters['e'])[0]
    a_key = 0
    b = int((alphaWithValue[a_dict] - (a_key * 0)) / 1 % 27)
    a = ((alphaWithValue[e_dict] - b) * modinv(alphaWithValue['E'], 27)) % 27
    return a, b


def force_decrypt(msg: str) -> [str]:
    results: [str] = []
    for a in alphaWithValue:
        for b in alphaWithValue:
            dec_msg = decrypt_text(msg, alphaWithValue[a], alphaWithValue[b])
            if len(dec_msg) > 0:
                results.append(dec_msg)
    return results


def qualify_msg(msg: str) -> dict:
    new_dic = {}
    sorted_dic = []
    e = ""
    a = ""
    for ch in msg:
        if ch in new_dic:
            new_dic[ch] = new_dic[ch] + 1
        else:
            new_dic[ch] = 1

    print("------------------------------------------")
    for p_item in new_dic:
        p_value = round((new_dic[p_item] * 100) / len(msg), 2)
        new_dic[p_item] = p_value
        sorted_dic.append(p_value)
        print(p_item, new_dic[p_item])
    print("------------------------------------------")

    sorted_dic = sorted(sorted_dic)

    for p_item in new_dic:
        if new_dic[p_item] == sorted_dic[len(sorted_dic) - 1]:
            e = p_item
        elif new_dic[p_item] == sorted_dic[len(sorted_dic) - 2]:
            a = p_item
    return {"e": {e: sorted_dic[len(sorted_dic) - 1]}, "a": {a: sorted_dic[len(sorted_dic) - 2]}}
