from __future__ import annotations

import pytest


class Character:
    def __init__(self):
        self._alive = True
        self._level = 1
        self._health = 1000

    pass

    def attack(self, character: Character, damage: float):
        character._health -= damage
        if character._health < 0:
            character._health = 0
            character._alive = False

    def heal(self, character: Character, heal_amount: float):
        if not character._alive:
            return

        character._health += heal_amount

        if character._health > 1000:
            character._health = 1000


class TestCharacter:

    # 1. All Characters, when created, have:
    #   - Health, starting at 1000
    #   - Level, starting at 1
    #   - May be Alive or Dead, starting Alive (Alive may be a true/false)
    @pytest.mark.parametrize("initial_health,initial_level,initial_alive_status", [(1000, 1, True)])
    def test_character_is_created_with_initial_values(self, initial_health, initial_level, initial_alive_status):
        character = Character()

        assert character._health == initial_health
        assert character._level == initial_level
        assert character._alive == initial_alive_status

    # 2. Characters can Deal Damage to Characters.
    #   - Damage is subtracted from Health
    #   - When damage received exceeds current Health, Health becomes 0 and the character dies
    def test_character1_attacks_character2(self):
        character1 = Character()
        character2 = Character()

        character1.attack(character2, 50)

        assert character2._health == 950

    def test_character_dies_after_damage_exceeds_current_health(self):
        character1 = Character()
        character2 = Character()

        character1.attack(character2, 1050)

        assert character2._health == 0
        assert character2._alive == False

    # 3. A Character can Heal a Character.
    #   - Dead characters cannot be healed
    #   - Healing cannot raise health above 1000
    @pytest.mark.parametrize(
        "damage,expected_health,expected_alive_status",
        [
            (200, 900, True),
            (1050, 0, False),
            (50, 1000, True)
        ]
    )
    def test_character1_heals_character2(self, damage, expected_health, expected_alive_status):
        character1 = Character()
        character2 = Character()

        character1.attack(character2, damage)
        character2.heal(character2, 100)

        assert character2._health == expected_health
        assert character2._alive == expected_alive_status
