from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from affine.Affine import executeFact, encrypt_text, decrypt_text, qualify_msg, get_force_keys, build_decrypt_text, \
    normalize_msg, build_decrypt_text_with_keys, force_decrypt

app = FastAPI()


class KeysModel(BaseModel):
    a: int
    b: int


class RequestModel(BaseModel):
    keys: Optional[KeysModel]
    plain_text: Optional[str]
    crypt_text: Optional[str]


class ResponseModel(BaseModel):
    plain_text: Optional[str]
    encrypt_text: Optional[str]
    decrypt_text: list[str]
    force_crypt: list[str]


@app.post("/crypt_and_decrypt", response_model=ResponseModel)
async def root(request: RequestModel):
    plain_msg = None
    crypt_msg = None

    if request.crypt_text is not None:
        crypt_msg = normalize_msg(msg=request.crypt_text)
    elif request.plain_text is not None:
        plain_msg = normalize_msg(msg=request.plain_text)

    # valid_keys = executeFact(1, 10)
    # if not valid_keys:
    #   return {"error": "invalid keys"}

    if plain_msg is None:
        a, b = get_force_keys(msg=crypt_msg)
        decrypt_result = build_decrypt_text(msg=crypt_msg, key_a=a, key_b=b)
    else:
        encrypt_result = encrypt_text(msg=plain_msg, key_a=request.keys.a, key_b=request.keys.b)
        decrypt_result = build_decrypt_text_with_keys(msg=encrypt_result, key_a=request.keys.a, key_b=request.keys.b)
        return ResponseModel(plain_text=plain_msg, encrypt_text=encrypt_result, decrypt_text=decrypt_result,
                             force_crypt=[])

    # encrypt_result = ""
    # get_keys = get_force_keys(msg=msg)
    # decrypt_result = decrypt_text(msg=msg, key_a=11, key_b=17)

    return ResponseModel(decrypt_text=decrypt_result, force_crypt=force_decrypt(msg=crypt_msg))
