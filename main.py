import streamlit as st
import time
import matplotlib.pyplot as plt

from roulette_logic import choose_winner, update_wins

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Roulette Edukatif Non-Gambling",
    layout="centered"
)

st.title("🎯 Roulette Non-Gambling")
st.caption(
    "Simulasi edukatif untuk menggambarkan sistem Weighted Random "
    "seperti judi online."
)

# --------------------------------
# STATISTIK GLOBAL
# --------------------------------
if "stats" not in st.session_state:
    st.session_state.stats = {
        "total_spins": 0
    }

stats = st.session_state.stats

# --------------------------------
# INPUT PESERTA
# --------------------------------
st.subheader("⚙️ Input Peserta & Bobot Kemenangan (%)")

num_players = st.number_input(
    "Jumlah Peserta",
    min_value=2,
    max_value=10,
    value=4,
    step=1
)

players = []
total_weight = 0

for i in range(num_players):
    col1, col2 = st.columns([3, 1])

    with col1:
        name = st.text_input(
            f"Nama Peserta {i+1}",
            key=f"name_{i}"
        )

    with col2:
        weight = st.number_input(
            f"Bobot (%)",
            min_value=0,
            max_value=100,
            value=0,
            key=f"weight_{i}"
        )

    if name.strip() != "":
        players.append({
            "name": name,
            "weight": weight,
            "wins": st.session_state.get(f"wins_{name}", 0)
        })
        total_weight += weight

# --------------------------------
# VALIDASI TOTAL BOBOT
# --------------------------------
st.markdown(f"### Total Bobot: **{total_weight}%**")

if total_weight > 100:
    st.error("❌ Total bobot melebihi 100%. Kurangi bobot peserta.")
    can_spin = False
elif total_weight == 0:
    st.warning("⚠️ Total bobot masih 0%. Tambahkan bobot.")
    can_spin = False
else:
    can_spin = True

# --------------------------------
# TAMPILKAN PELUANG
# --------------------------------
st.subheader("📊 Peluang Peserta")
if total_weight > 0:
    for p in players:
        chance = (p["weight"] / total_weight) * 100
        st.write(f"• **{p['name']}** → {chance:.2f}%")

# --------------------------------
# DRAW ROULETTE
# --------------------------------
def draw_roulette(players, rotation_angle=0, highlight=None):
    labels = [p["name"] for p in players]
    sizes = [1] * len(players)

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, _ = ax.pie(
        sizes,
        labels=labels,
        startangle=rotation_angle,
        wedgeprops=dict(edgecolor="black")
    )

    # Highlight pemenang
    if highlight:
        idx = labels.index(highlight)
        wedges[idx].set_facecolor("gold")

    # Set Panah Pointer
    ax.annotate(
        "",
        xy=(0, 1.05),
        xytext=(0, 1.25),
        arrowprops=dict(
            facecolor="red",
            edgecolor="red",
            width=6,
            headwidth=18
        )
    )

    ax.set_aspect("equal")
    ax.axis("off")
    return fig

# --------------------------------
# SPIN BUTTON
# --------------------------------
st.divider()
placeholder = st.empty()

if st.button("🎯 SPIN", disabled=not can_spin):

    # Tentukan pemenang (weighted random)
    winner = choose_winner(players)
    winner_index = players.index(winner)

    total_players = len(players)
    angle_per_slice = 360 / total_players

    # Angle panah
    target_angle = 90 - (winner_index + 0.5) * angle_per_slice
    total_rotation = 360 * 5 + target_angle

    steps = 40
    for step in range(steps):
        current_angle = (total_rotation / steps) * step
        placeholder.pyplot(
            draw_roulette(players, rotation_angle=current_angle)
        )
        time.sleep(0.06)

    # Update jumlah kemenangan
    update_wins(winner, stats)
    st.session_state[f"wins_{winner['name']}"] = winner["wins"]

    # Final render
    placeholder.pyplot(
        draw_roulette(
            players,
            rotation_angle=total_rotation,
            highlight=winner["name"]
        )
    )

    st.success(f"🏆 Pemenang: **{winner['name']}**")

# --------------------------------
# STATISTIK
# --------------------------------
st.divider()
st.subheader("📊 Statistik")
st.write(f"🔄 Total Spin: **{stats['total_spins']}** kali")

for p in players:
    st.write(f"• {p['name']} → {p['wins']} kemenangan")

# --------------------------------
# DISCLAIMER
# --------------------------------
st.divider()
st.info(
    "⚠️ Aplikasi ini adalah simulasi edukatif (non-gambling).\n\n"
    "Digunakan untuk edukasi probabilitas dan pencegahan judi online."
)
