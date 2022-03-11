# Cifrado afine por fuerza bruta y  estadistico

En la siguiente API rest se encuentra un metodo post expuesto que permite cifrar, descifrar(con llaves, o por analisis estadistico), el api se encuentra expuesta en el siguiente [Link](https://cryptrestapi.herokuapp.com/docs)  

1. Para cifrar con clave se requiere enviar el siguiente objeto json en el request
```
{
  "keys": {
    "a": 0,
    "b": 0
  },
  "plain_text": "string"
}
```
2. Para descifrar con clave se requiere enviar el siguiente objeto json en el request
```
{
  "keys": {
    "a": 0,
    "b": 0
  },
  "crypt_text": "string"
}
```
3. Para descifrar por analisis estadistico o fuerza bruta se requiere enviar el siguiente objeto json en el request
```
{
  "crypt_text": "string"
}
```

Para cada uno de estos escenarios el servicio responde lo siguiente
```
{
  "plain_text": "STRING",
  "encrypt_text": "AAAAAA",
  "decrypt_text": [
    ""
  ],
  "force_crypt": []
}
```

