import sys

import imagematrix


class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        dp = {}
        energy_dict = {}
        for j in range(0, self.height):
            for i in range(0, self.width):
                if (i, j) not in energy_dict:
                    energy_dict[i, j] = self.energy(i, j)
                if j == 0:
                    dp[i, j] = energy_dict[i, j]
                elif i == 0:
                    dp[i, j] = min(dp[i, j - 1], dp[i + 1, j - 1]) + energy_dict[i, j]
                elif i == self.width - 1:
                    dp[i, j] = min(dp[i, j - 1], dp[i - 1, j - 1]) + energy_dict[i, j]
                else:
                    dp[i, j] = min(dp[i, j - 1], dp[i - 1, j - 1], dp[i + 1, j - 1]) + energy_dict[i, j]
        min_val = sys.maxint
        for i in range(0, self.width):
            if min_val > dp[i, self.height - 1]:
                min_val = dp[i, self.height - 1]
                seam_end = (i, self.height - 1)

        seam = []
        current = seam_end
        for i in range(0, self.height):
            seam.append(current)
            if current[1] == 0:
                break
            min_val = min(dp[current[0], current[1] - 1], dp[current[0] - 1, current[1] - 1],
                          dp[current[0] + 1, current[1] - 1])
            if min_val == dp[current[0], current[1] - 1]:
                current = (current[0], current[1] - 1)
            elif min_val == dp[current[0] - 1, current[1] - 1]:
                current = (current[0] - 1, current[1] - 1)
            elif min_val == dp[current[0] + 1, current[1] - 1]:
                current = (current[0] + 1, current[1] - 1)
        seam.reverse()
        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
