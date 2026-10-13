import unittest
from src.astar import astar


class AStarTests(unittest.TestCase):
    def test_finds_path_around_obstacle(self):
        grid = [
            [0, 0, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 0],
        ]
        path = astar(grid, (0, 0), (3, 2))
        self.assertTrue(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (3, 2))
        self.assertTrue(all(grid[y][x] == 0 for x, y in path))

    def test_no_path(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]
        self.assertEqual(astar(grid, (0, 0), (2, 0)), [])

    def test_start_equals_goal(self):
        self.assertEqual(astar([[0]], (0, 0), (0, 0)), [(0, 0)])

    def test_replans_when_new_obstacle_blocks_old_path(self):
        grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        start = (0, 1)
        goal = (3, 1)
        original_path = astar(grid, start, goal)
        self.assertTrue(original_path)

        blocked_cell = original_path[1]
        x, y = blocked_cell
        grid[y][x] = 1
        new_path = astar(grid, start, goal)

        self.assertTrue(new_path)
        self.assertEqual(new_path[0], start)
        self.assertEqual(new_path[-1], goal)
        self.assertNotIn(blocked_cell, new_path)
        self.assertTrue(all(grid[py][px] == 0 for px, py in new_path))


if __name__ == "__main__":
    unittest.main()