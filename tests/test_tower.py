from unittest import TestCase

from ed_utils.decorators import number, visibility, advanced
from ed_utils.timeout import timeout
from random_gen import RandomGen

from battle import Battle
from elements import Element
from team import MonsterTeam
from tower import BattleTower, tournament_balanced
from helpers import Flamikin, Faeboa

from data_structures.referential_array import ArrayR

class GoodFlamikin(Flamikin):

    def get_attack(self):
        return 10000000

    def get_speed(self):
        return 10000000

    def get_defense(self):
        return 10000000

    def get_max_hp(self):
        return 10000000

    def ready_to_evolve(self):
        # Never evolve = never stats
        return False


class BadFlamikin(Flamikin):

    def get_attack(self):
        return 0

    def get_speed(self):
        return 0

    def get_defense(self):
        return 0

    def get_max_hp(self):
        return 1

class TestTower(TestCase):

    @number("5.1")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_random_elements(self):
        RandomGen.set_seed(123456789)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([BadFlamikin])
        ))
        # The only random number generated at this point is the lives of our team member
        # We have 4 lives
        bt.generate_teams(2)
        # 1 Opposing team - there's some random elements here but they should always beat our team.
        # In terms of random generation, the next use of random numbers is:
            # Selecting the team, then
            # Selecting the lives.
        # This is repeated twice.
        lives_expected = [
            (3, 7),
            (2, 5),
            (1, 7),
            (0, 5),
        ]
        lives_genned_early = [
            (3, 10),
            (2, 7),
            (1, 10),
            (0, 7),
        ]
        lives_genned_at_the_end = [
            (3, 5),
            (2, 8),
            (1, 5),
            (0, 8),
        ]
        lives_got = []
        while bt.battles_remaining():
            result, team1, team2, lives1, lives2 = bt.next_battle()
            lives_got.append((lives1, lives2))

        self.assertNotEqual(lives_got, lives_genned_at_the_end, "You need to generate the first enemy teams lives before the second enemy team object.")
        self.assertNotEqual(lives_got, lives_genned_early, "You are generating the enemy lives before the enemy team")
        self.assertListEqual(lives_got, lives_expected)


    @number("5.2")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_simple_iter(self):
        # Now give us an overpowered team so we can test the enemy losing lives.
        RandomGen.set_seed(123456789)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([GoodFlamikin])
        ))
        bt.generate_teams(3)
        # They have lives 7 5 and 3

        expected = [
            (Battle.Result.TEAM1, 4, 6),
            (Battle.Result.TEAM1, 4, 4),
            (Battle.Result.TEAM1, 4, 2),
            (Battle.Result.TEAM1, 4, 5),
            (Battle.Result.TEAM1, 4, 3),
            (Battle.Result.TEAM1, 4, 1),
            (Battle.Result.TEAM1, 4, 4),
            (Battle.Result.TEAM1, 4, 2),
            (Battle.Result.TEAM1, 4, 0), # Player 3 Eliminated
            (Battle.Result.TEAM1, 4, 3),
            (Battle.Result.TEAM1, 4, 1),
            (Battle.Result.TEAM1, 4, 2),
            (Battle.Result.TEAM1, 4, 0), # Player 2 Eliminated
            (Battle.Result.TEAM1, 4, 1),
            (Battle.Result.TEAM1, 4, 0), # Player 1 Eliminated
        ]

        got = []
        while bt.battles_remaining():
            result, team1, team2, lives1, lives2 = bt.next_battle()
            got.append((result, lives1, lives2))

        self.assertListEqual(got, expected)

    @number("5.3")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_out_of_meta(self):
        RandomGen.set_seed(123456789)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([Faeboa])
        ))
        bt.generate_teams(3)
        # The following teams should have been generated:
        # 1 (7 lives): Strikeon, Faeboa, Shockserpent, Gustwing, Vineon, Pythondra
            # Fighting, Fairy, Electricity, Flying, Grass, Dragon
        # 2 (5 lives): Iceviper, Thundrake, Groundviper, Iceviper, Metalhorn
            # Ice, Electric, Ground, Steel
        # 3 (3 lives): Strikeon
            # Fighting

        # When no games have been played, noone is outside of the meta.
        self.assertListEqual(bt.out_of_meta().to_list(), [])
        result, t1, t2, l1, l2 = bt.next_battle()
        # After the first game, Fighting, Flying, Grass and Dragon are no longer in the meta.
        # Electric & Fairy are still present in the battle between the two.
        self.assertListEqual(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.FIGHTING, Element.FLYING])
        result, t1, t2, l1, l2 = bt.next_battle()
        # After the second game, Flying, Grass, Dragon, Ice, Electric, Ground, Steel are no longer present.
        self.assertListEqual(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.ELECTRIC, Element.FLYING, Element.GROUND, Element.ICE, Element.STEEL])
        result, t1, t2, l1, l2 = bt.next_battle()
        # After the third game, We are just missing Ice, Ground and Steel.
        self.assertListEqual(bt.out_of_meta().to_list(), [Element.GROUND, Element.ICE, Element.STEEL])
        result, t1, t2, l1, l2 = bt.next_battle()
        # After the fourth game, We are back to missing Grass, Dragon, Fighting and Flying
        self.assertListEqual(bt.out_of_meta().to_list(), [Element.GRASS, Element.DRAGON, Element.FIGHTING, Element.FLYING])