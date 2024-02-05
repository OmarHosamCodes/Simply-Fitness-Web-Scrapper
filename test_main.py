import unittest
from main import fetchListContent

class TestFetchListContent(unittest.TestCase):
    def test_fetchListContent(self):
        parentURL = "https://www.simplyfitness.com"
        listContent = []
        names = []
        fetchListContent(parentURL, listContent, names)
        
        # Check if listContent and names are not empty
        self.assertTrue(listContent)
        self.assertTrue(names)
        
        # Check if all URLs in listContent start with "https://www.simplyfitness.com"
        for url in listContent:
            self.assertTrue(url.startswith("https://www.simplyfitness.com"))
        
        # Check if all names in names list are stripped of "/pages/"
        for name in names:
            self.assertFalse("/pages/" in name)
        
if __name__ == '__main__':
    unittest.main()