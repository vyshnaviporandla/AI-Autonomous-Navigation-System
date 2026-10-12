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


if __name__ == "__main__":
    unittest.main()
