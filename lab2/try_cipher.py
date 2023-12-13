from stream import StreamCipher

msg = "Hello Vilag"

cypher = StreamCipher()

encoded = cypher.encrypt(msg)

encoded = encoded.decode('utf-8')
print(f'ENCODED : {encoded}')

decoded = cypher.decrypt(encoded)

print(f'DECODED : {decoded.decode()}')