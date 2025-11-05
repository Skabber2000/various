import random
from enum import Enum
from typing import List, Optional, Tuple, Dict

class Team(Enum):
    KNIGHTS = "knights"
    ASSASSINS = "assassins"

class UnitType(Enum):
    INFANTRY = "infantry"
    CAVALRY = "cavalry"
    SPECIAL = "special"

class Unit:
    def __init__(self, name: str, team: Team, unit_type: UnitType,
                 health: int, attack: int, defense: int, move_range: int, attack_range: int):
        self.name = name
        self.team = team
        self.unit_type = unit_type
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.move_range = move_range
        self.attack_range = attack_range
        self.has_moved = False
        self.has_attacked = False
        self.x = 0
        self.y = 0

    def reset_turn(self):
        """Reset unit actions for new turn"""
        self.has_moved = False
        self.has_attacked = False

    def take_damage(self, damage: int):
        """Apply damage to unit"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        return self.health > 0

    def can_attack(self, target: 'Unit', distance: int) -> bool:
        """Check if this unit can attack the target"""
        if not self.is_alive() or not target.is_alive():
            return False
        if self.team == target.team:
            return False
        if self.has_attacked:
            return False
        if distance > self.attack_range:
            return False
        return True

    def to_dict(self):
        """Convert unit to dictionary for JSON"""
        return {
            'name': self.name,
            'team': self.team.value,
            'unit_type': self.unit_type.value,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'defense': self.defense,
            'move_range': self.move_range,
            'attack_range': self.attack_range,
            'has_moved': self.has_moved,
            'has_attacked': self.has_attacked,
            'x': self.x,
            'y': self.y
        }

# Unit templates
def create_knight_infantry() -> Unit:
    return Unit("Knight Swordsman", Team.KNIGHTS, UnitType.INFANTRY,
                health=100, attack=20, defense=8, move_range=2, attack_range=1)

def create_knight_cavalry() -> Unit:
    return Unit("Knight Rider", Team.KNIGHTS, UnitType.CAVALRY,
                health=80, attack=25, defense=5, move_range=4, attack_range=1)

def create_knight_special() -> Unit:
    return Unit("Paladin", Team.KNIGHTS, UnitType.SPECIAL,
                health=120, attack=30, defense=10, move_range=2, attack_range=2)

def create_assassin_infantry() -> Unit:
    return Unit("Shadow Blade", Team.ASSASSINS, UnitType.INFANTRY,
                health=90, attack=25, defense=5, move_range=3, attack_range=1)

def create_assassin_cavalry() -> Unit:
    return Unit("Dark Rider", Team.ASSASSINS, UnitType.CAVALRY,
                health=75, attack=30, defense=4, move_range=4, attack_range=1)

def create_assassin_special() -> Unit:
    return Unit("Master Assassin", Team.ASSASSINS, UnitType.SPECIAL,
                health=100, attack=35, defense=6, move_range=3, attack_range=2)

class GameBoard:
    def __init__(self, width: int = 10, height: int = 8):
        self.width = width
        self.height = height
        self.grid: List[List[Optional[Unit]]] = [[None for _ in range(width)] for _ in range(height)]

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_unit(self, x: int, y: int) -> Optional[Unit]:
        """Get unit at position"""
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]

    def place_unit(self, unit: Unit, x: int, y: int) -> bool:
        """Place unit at position"""
        if not self.is_valid_position(x, y):
            return False
        if self.grid[y][x] is not None:
            return False

        # Remove from old position if exists
        if unit.x >= 0 and unit.y >= 0:
            self.grid[unit.y][unit.x] = None

        self.grid[y][x] = unit
        unit.x = x
        unit.y = y
        return True

    def move_unit(self, unit: Unit, to_x: int, to_y: int) -> bool:
        """Move unit to new position"""
        if not self.is_valid_position(to_x, to_y):
            return False
        if self.grid[to_y][to_x] is not None:
            return False

        distance = abs(unit.x - to_x) + abs(unit.y - to_y)
        if distance > unit.move_range or unit.has_moved:
            return False

        # Check if path is clear (simple Manhattan distance check)
        self.grid[unit.y][unit.x] = None
        self.grid[to_y][to_x] = unit
        unit.x = to_x
        unit.y = to_y
        unit.has_moved = True
        return True

    def get_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance"""
        return abs(x1 - x2) + abs(y1 - y2)

    def get_units_in_range(self, x: int, y: int, range_val: int) -> List[Tuple[Unit, int]]:
        """Get all units within range of position"""
        units = []
        for dy in range(-range_val, range_val + 1):
            for dx in range(-range_val, range_val + 1):
                tx, ty = x + dx, y + dy
                if self.is_valid_position(tx, ty):
                    unit = self.grid[ty][tx]
                    if unit:
                        distance = abs(dx) + abs(dy)
                        if distance <= range_val:
                            units.append((unit, distance))
        return units

class Game:
    def __init__(self):
        self.board = GameBoard()
        self.current_turn = Team.KNIGHTS
        self.turn_number = 1
        self.selected_unit = None
        self.game_over = False
        self.winner = None
        self.knights_units: List[Unit] = []
        self.assassins_units: List[Unit] = []
        self.initialize_units()

    def initialize_units(self):
        """Initialize starting units for both teams"""
        # Knights (bottom)
        knight_units = [
            (create_knight_infantry(), 1, 7),
            (create_knight_infantry(), 3, 7),
            (create_knight_infantry(), 5, 7),
            (create_knight_infantry(), 7, 7),
            (create_knight_cavalry(), 0, 6),
            (create_knight_cavalry(), 8, 6),
            (create_knight_special(), 4, 6),
        ]

        for unit, x, y in knight_units:
            self.knights_units.append(unit)
            self.board.place_unit(unit, x, y)

        # Assassins (top)
        assassin_units = [
            (create_assassin_infantry(), 2, 0),
            (create_assassin_infantry(), 4, 0),
            (create_assassin_infantry(), 6, 0),
            (create_assassin_infantry(), 8, 0),
            (create_assassin_cavalry(), 1, 1),
            (create_assassin_cavalry(), 9, 1),
            (create_assassin_special(), 5, 1),
        ]

        for unit, x, y in assassin_units:
            self.assassins_units.append(unit)
            self.board.place_unit(unit, x, y)

    def get_current_team_units(self) -> List[Unit]:
        """Get units for current team"""
        if self.current_turn == Team.KNIGHTS:
            return [u for u in self.knights_units if u.is_alive()]
        else:
            return [u for u in self.assassins_units if u.is_alive()]

    def get_enemy_team_units(self) -> List[Unit]:
        """Get enemy units"""
        if self.current_turn == Team.ASSASSINS:
            return [u for u in self.knights_units if u.is_alive()]
        else:
            return [u for u in self.assassins_units if u.is_alive()]

    def attack(self, attacker: Unit, defender: Unit) -> Dict:
        """Execute attack from one unit to another"""
        distance = self.board.get_distance(attacker.x, attacker.y, defender.x, defender.y)

        if not attacker.can_attack(defender, distance):
            return {'success': False, 'message': 'Cannot attack this target'}

        # Calculate damage with some randomness
        base_damage = attacker.attack
        damage_variance = random.randint(-5, 5)
        total_damage = max(1, base_damage + damage_variance)

        actual_damage = defender.take_damage(total_damage)
        attacker.has_attacked = True

        result = {
            'success': True,
            'damage': actual_damage,
            'defender_health': defender.health,
            'defender_alive': defender.is_alive(),
            'attacker': attacker.name,
            'defender': defender.name
        }

        if not defender.is_alive():
            result['message'] = f"{defender.name} has been defeated!"

        self.check_victory()

        return result

    def check_victory(self):
        """Check if one team has won"""
        knights_alive = any(u.is_alive() for u in self.knights_units)
        assassins_alive = any(u.is_alive() for u in self.assassins_units)

        if not knights_alive:
            self.game_over = True
            self.winner = Team.ASSASSINS
        elif not assassins_alive:
            self.game_over = True
            self.winner = Team.KNIGHTS

    def end_turn(self):
        """End current turn and switch to other team"""
        # Reset all units of current team
        for unit in self.get_current_team_units():
            unit.reset_turn()

        # Switch team
        if self.current_turn == Team.KNIGHTS:
            self.current_turn = Team.ASSASSINS
        else:
            self.current_turn = Team.KNIGHTS
            self.turn_number += 1

        self.selected_unit = None

    def get_state(self) -> Dict:
        """Get current game state as dictionary"""
        return {
            'board_width': self.board.width,
            'board_height': self.board.height,
            'current_turn': self.current_turn.value,
            'turn_number': self.turn_number,
            'game_over': self.game_over,
            'winner': self.winner.value if self.winner else None,
            'knights_units': [u.to_dict() for u in self.knights_units if u.is_alive()],
            'assassins_units': [u.to_dict() for u in self.assassins_units if u.is_alive()],
        }

    def ai_take_turn(self):
        """Simple AI for computer player"""
        units = self.get_current_team_units()
        enemy_units = self.get_enemy_team_units()

        actions = []

        for unit in units:
            if not unit.is_alive():
                continue

            # Find closest enemy
            closest_enemy = None
            min_distance = float('inf')

            for enemy in enemy_units:
                distance = self.board.get_distance(unit.x, unit.y, enemy.x, enemy.y)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

            if closest_enemy:
                # Try to attack if in range
                if min_distance <= unit.attack_range and not unit.has_attacked:
                    result = self.attack(unit, closest_enemy)
                    actions.append(result)

                # Try to move closer if not already moved
                elif not unit.has_moved:
                    # Calculate direction to enemy
                    dx = 1 if closest_enemy.x > unit.x else (-1 if closest_enemy.x < unit.x else 0)
                    dy = 1 if closest_enemy.y > unit.y else (-1 if closest_enemy.y < unit.y else 0)

                    # Try to move in that direction
                    target_x = unit.x + dx * unit.move_range
                    target_y = unit.y + dy * unit.move_range

                    # Clamp to board
                    target_x = max(0, min(self.board.width - 1, target_x))
                    target_y = max(0, min(self.board.height - 1, target_y))

                    # Find closest empty spot
                    moved = False
                    for radius in range(unit.move_range + 1):
                        for dy_offset in range(-radius, radius + 1):
                            for dx_offset in range(-radius, radius + 1):
                                if abs(dx_offset) + abs(dy_offset) > unit.move_range:
                                    continue
                                new_x = unit.x + dx_offset
                                new_y = unit.y + dy_offset
                                if self.board.move_unit(unit, new_x, new_y):
                                    actions.append({
                                        'action': 'move',
                                        'unit': unit.name,
                                        'from': (unit.x - dx_offset, unit.y - dy_offset),
                                        'to': (new_x, new_y)
                                    })
                                    moved = True
                                    break
                            if moved:
                                break
                        if moved:
                            break

                    # Try to attack after moving
                    new_distance = self.board.get_distance(unit.x, unit.y, closest_enemy.x, closest_enemy.y)
                    if new_distance <= unit.attack_range and not unit.has_attacked:
                        result = self.attack(unit, closest_enemy)
                        actions.append(result)

        return actions
