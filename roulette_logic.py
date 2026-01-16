import random

def choose_winner(players):
    """
    Memilih satu pemenang dari daftar peserta menggunakan
    metode weighted random.

    Parameter :
    - players (list): daftar peserta berisi dictionary
      { "name": str, "weight": int, "wins": int }

    Return: 
    - dict: data peserta yang terpilih sebagai pemenang
    """

    total_weight = sum(p["weight"] for p in players)
    r = random.uniform(0, total_weight)

    upto = 0
    for p in players:
        upto += p["weight"]
        if r <= upto:
            return p
        

def update_wins(winner, stats):
    """
    Menambah jumlah kemenangan pemenang
    dan mencatat total spin yang sudah dilakukan.

    Parameter:
    - winner (dict): peserta yang menang
    - stats (dict): jumlah total spin { "total_spins": int }
    """
    winner["wins"] += 1
    stats["total_spins"] += 1

def force_winner(players, name):
    """
    Memilih peserta tertentu sebagai pemenang secara langsung.

    Parameter:
    - players (list): daftar peserta
    - name (str): nama peserta yang ingin dipaksa menang

    Return:
    - dict | None: data peserta jika ditemukan,
    """

    for p in players:
        if p["name"] == name:
            return p
    return None
