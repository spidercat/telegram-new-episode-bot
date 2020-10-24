import sys
sys.path.append("..")
import config

from cryptography.fernet import Fernet
from pathlib import Path
from os.path import isfile
import argparse

def encrypt(db_file_name, encrypted_db_file_name):
  if not isfile(db_file_name):
    print(f'database file not found: {db_file_name}')
    exit(1)

  db_txt = Path(db_file_name).read_text()
  fernet = Fernet(config.DB_ENCRYPTION_KEY)
  cypher_text = fernet.encrypt(db_txt.encode())
  Path(encrypted_db_file_name).write_bytes(cypher_text)

def decrypt(encrypted_db_file_name, output_db_file_name):
  if not isfile(encrypted_db_file_name):
    print(f'encrypted file not found: {encrypted_db_file_name}')
    exit(1)

  cypher_bytes = Path(encrypted_db_file_name).read_bytes()
  fernet = Fernet(config.DB_ENCRYPTION_KEY)
  db_decrypted_bytes = fernet.decrypt(cypher_bytes)
  Path(output_db_file_name).write_text(db_decrypted_bytes.decode())

if __name__ == "__main__":
  # execute only if run as a script
  parser = argparse.ArgumentParser(description='Encrypt/Decrypt database file.')
  parser.add_argument('method', choices=['encrypt', 'decrypt'])
  parser.add_argument('-i', metavar='input_file', required=True,
                      help='input file')
  parser.add_argument('-o', metavar='output_file', required=True,
                      help='output file name')

  args = parser.parse_args()
  methods = {'encrypt': encrypt, 'decrypt': decrypt}
  methods[args.method](args.i, args.o)
