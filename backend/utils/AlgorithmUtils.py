from functools import cache


class AlgorithmUtils():
    def minDistanceString(self, word1: str, word2: str) -> int:
        n, m = len(word1), len(word2)
        @cache
        def dfs(i, j):
            if i < 0:
                return j+1
            if j < 0:
                return i+1
            if word1[i] == word2[j]:
                return dfs(i-1, j-1)
            return min(dfs(i-1, j), dfs(i, j-1), dfs(i-1, j-1)) + 1
        
        return dfs(n-1, m-1)

    def minDistanceTag(self, word1: list, word2: list) -> int:
        n, m = len(word1), len(word2)
        @cache
        def dfs(i, j):
            if i < 0:
                return j+1
            if j < 0:
                return i+1
            if word1[i] == word2[j]:
                return dfs(i-1, j-1)
            return min(dfs(i-1, j), dfs(i, j-1), dfs(i-1, j-1)) + 1
        
        return dfs(n-1, m-1)
