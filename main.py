import random
import requests
from bs4 import BeautifulSoup
import os

def fetchListContent(parentURL, listContent, names):
    response = requests.get(parentURL)
    soup = BeautifulSoup(response.content, "html.parser")
    targetClass = soup.find_all(class_="exo-ol no-bullets site-footer__linklist")
    for element in targetClass:
        targetListItems = element.find_all("li")
        for item in targetListItems:
            targetListItemLinks = item.find_all("a")
            for link in targetListItemLinks:
                href = link["href"]
                listContent.append(f"https://www.simplyfitness.com{href}")
                names.append(href.strip("/pages/"))
    finalListContent = list(set(listContent))
    print("The list of content has been fetched")

def fixURLs(src):
    if src.startswith("//"):
        return f"https:{src}"
    else:
        return src

def fetchContent(listContent, contentURLs):
    for contentURL in listContent:
        response = requests.get(contentURL)
        soup = BeautifulSoup(response.content, "html.parser")
        targetClass = soup.find_all("header")
        for _ in targetClass:
            targetDiv = _.find_all("div")
            for div in targetDiv:
                targetImg = div.find_all("img")
                for img in targetImg:
                    finalURL = fixURLs(img["src"])
                    print(finalURL)
                    contentURLs.append(finalURL)
    finalContent = list(set(contentURLs))
    print("The content has been fetched")
  
def createDirectory():
    os.mkdir('workouts')

def downloadImages( content):
    os.chdir('workouts')
    for image in content:
        response = requests.get(image)
        random_number = random.randint(1, 9999999)
        with open(f"image_{random_number}.png", "wb") as f:
            f.write(response.content)
    os.chdir("..")
    print("The images have been downloaded")

def main():
    parentURL = "https://www.simplyfitness.com/pages/workout-exercise-guides"
    listContent = []
    names = []
    contentURLs = []
    fetchListContent(parentURL, listContent, names)
    createDirectory()
    fetchContent(listContent, contentURLs)
    listContent = list(set(listContent))
    contentURLs = list(set(contentURLs))
    downloadImages(contentURLs)
    print("The program has finished running")

if __name__ == "__main__":
    main()
