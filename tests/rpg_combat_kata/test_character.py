from __future__ import annotations

import pytest


class Character:
    def __init__(self, level=1):
        self._alive = True
        self._level = level
        self._health = 1000

    pass

    def attack(self, target: Character, damage: float):
        if target == self:
            return

        if target._level - self._level >= 5:
            damage *= 0.5
        elif self._level - target._level >= 5:
            damage *= 1.5

        target._health -= damage

        if target._health < 0:
            target._health = 0
            target._alive = False

    def heal(self, character: Character, heal_amount: float):
        if character != self or not character._alive:
            return

        character._health += heal_amount

        if character._health > 1000:
            character._health = 1000


class TestCharacter:

    # Iteration one

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

    # Iteration two

    # A Character cannot Deal Damage to itself.

    def test_character_cannot_damage_itself(self):
        character = Character()

        character.attack(character, 300)

        assert character._health == 1000

    # A Character can only Heal itself.
    def test_character_can_only_heal_itself(self):
        character1 = Character()
        character2 = Character()
        character1.attack(character2, 100)

        character1.heal(character2, 50)

        assert character2._health == 900

    # If the target is 5 or more Levels above the attacker, Damage is reduced by 50%
    @pytest.mark.parametrize("target_level", [6, 10])
    def test_reduce_damage_when_target_is_5_or_more_levels_above_attacker(self, target_level):
        character = Character()
        target = Character(level=target_level)

        character.attack(target, 100)

        assert target._health == 950

    # If the target is 5 or more Levels below the attacker, Damage is increased by 50%
    @pytest.mark.parametrize("character_level", [6, 10])
    def test_increase_damage_when_character_is_5_or_more_levels_above_target(self, character_level):
        character = Character(level=character_level)
        target = Character()

        character.attack(target, 100)

        assert target._health == 850
