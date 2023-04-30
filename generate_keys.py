import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names=["Pratham Kotian","Pujari Sanmith","Gautham Ghetia","Jash"]
usernames=["pratham","sanmith","gautham","jash"]
passwords=["XXX","XXX","XXX","XXX"]

hashed_passwords=stauth.Hasher(passwords).generate()

file_path=Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)