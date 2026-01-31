# --- Distance Constants ---
BASE_DISTANCE_PENALTY = 1000
INTRA_SYSTEM_DISTANCE = 5
DISTANCE_DIVISOR = 35000

# --- Speed Constants ---
# Using 10% speed for maximum fuel efficiency (0.1)
# Formula uses (Speed + 1)^2 -> (0.1 + 1)^2 = 1.21
SELECTED_SPEED_FACTOR = 0.1
SPEED_SQUARE_COEFFICIENT = (SELECTED_SPEED_FACTOR + 1) ** 2

# --- Server & Class Modifiers (Pluto s271-en) ---
PLUTO_CONSUMPTION_RATE = 0.5
PLUTO_PEACEFUL_SPEED_MULT = 4
DISCOVERER_FUEL_DISCOUNT = 1

IS_DISCVERER_CLASS = True

# 1. Calculate Distance
FURTHER_SYSTEM_DISTANCE_FOR_EXPEDITION = 5