from django.test import TestCase


# Create your tests here.
class Solution:
    def isCircularSentence(self, sentence: str) -> bool:
        words = sentence.split()
        
        if sentence[0] != sentence[-1]:
            return False

        for i in range(1, len(words)):
            if words[i - 1][-1] != words[i][0]:
                return False

        return True
