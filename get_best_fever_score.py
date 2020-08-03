import numpy as np

myBoardNums = [4, 5, 6, 9, 9, 14, 14, 12, 15]

# myBoardNums = [5, 5, 9]

class FeverBoard:
    def __init__(self, nums):
        self.nums = nums
        self.threshold_value = 0

    def get_best_fever_score(self):
        my_nums = np.sort(self.nums)
        j = 0
        while j < len(my_nums) - 1:
            if my_nums[j] == my_nums[j + 1] and my_nums[j] + 2 > my_nums[-1]:
                my_nums = np.delete(my_nums, [j, j + 1])
                j = j - 1
            j = j + 1
        my_value = self.get_best_fever_score_recurse(my_nums, False, 0, 0)
        while my_value > self.threshold_value:
            print("Could not meet the score of " + str(self.threshold_value) + ". Incrementing.")
            self.threshold_value += 1
            my_value = self.get_best_fever_score_recurse(my_nums, False, 0, 0)
        return my_value

    def get_best_fever_score_recurse(self, my_nums, tile_is_saved, depth, accumulated_score):
        if len(my_nums) == 1:
            if tile_is_saved:
                return 10000
            else:
                return my_nums[0] + accumulated_score
            '''
            if len(my_nums) == 3:
                if my_nums[0] + my_nums[1] == my_nums[2]:
                    return my_nums[0] + accumulated_score
                # All tiles must be matched off if we have already saved a tile.
                elif tile_is_saved:
                    return 10000
                elif my_nums[0] + my_nums[1] > my_nums[2]:
                    return my_nums[0] + my_nums[1] + accumulated_score
                else:
                    return my_nums[2] + accumulated_score
            '''
        elif len(my_nums) == 0:
            return accumulated_score
        else:
            best_score = 10000
            # Try matching off the lowest valued tile.
            for i in range(1, len(my_nums)):
                # If we have multiple copies of a tile, we only
                # need to consider matching the lowest valued tile to just
                # one of these tiles.
                if i > 1 and my_nums[i] == my_nums[i - 1]:
                    continue
                # Calculate how many points we are going to lose on the move we are considering. It is either
                # going to be 0 points or equal to the lowest valued tile.
                points_lost_on_move = 0 if my_nums[0] == my_nums[i] else my_nums[0]
                my_accumulated_score = points_lost_on_move + accumulated_score
                # Remove the two tiles that we are matching.
                temp_nums = np.delete(my_nums, [0, i])
                if points_lost_on_move:
                    if my_accumulated_score > self.threshold_value:
                        # If we have reached here, then all other moves we can consider will score us points
                        # which will send us over the threshold, so we don't need to consider the remaining moves.
                        return best_score
                    # Insert the newly formed tile into the sorted array
                    temp_nums = np.sort(np.insert(temp_nums, 0, my_nums[i] - my_nums[0]))
                    j = 0
                    while j < len(temp_nums) - 1:
                        if temp_nums[j] == temp_nums[j + 1] and temp_nums[j] + 2 > temp_nums[-1]:
                            temp_nums = np.delete(temp_nums, [j, j + 1])
                            j = j - 1
                        j = j + 1
                other_score = self.get_best_fever_score_recurse(temp_nums, tile_is_saved, depth + 1,
                                                                my_accumulated_score)
                # If we have a better score, change it.
                if best_score > other_score:
                    # If we have a score that meets the threshold value, immediately return out
                    if depth == 0 and other_score == self.threshold_value:
                        return other_score
                    best_score = other_score

            # Try saving the lowest valued tile for the very end.
            if not tile_is_saved:
                other_score = self.get_best_fever_score_recurse(np.delete(my_nums, 0), True, depth + 1,
                                                                accumulated_score + my_nums[0])
                if best_score > other_score:
                    best_score = other_score

            return best_score


if __name__ == "__main__":
    print(FeverBoard(myBoardNums).get_best_fever_score())
