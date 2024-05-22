import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup


class SimplyFitnessWebScrapper:
    parentURL = "https://www.simplyfitness.com/pages/workout-exercise-guides"

    async def get_list_content(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.parentURL) as response:
                text = await response.text()
                document = BeautifulSoup(text, "html.parser")
                content_and_name = set()

                target_class = document.select(
                    ".exo-ol.no-bullets.site-footer__linklist li a"
                )

                for element in target_class:
                    href = element.get("href")
                    content_and_name.add(
                        (
                            f"https://www.simplyfitness.com{href}",
                            href.replace("/pages/", "") if href else "",
                        )
                    )

                print(f"The list of content has been fetched: {content_and_name}")
                return content_and_name

    def fix_urls(self, src):
        return f"https:{src}" if src.startswith("//") else src

    async def get_content(self, list_content):
        content_urls_and_names = set()

        async with aiohttp.ClientSession() as session:
            for content_url, name in list_content:
                async with session.get(content_url) as response:
                    text = await response.text()
                    document = BeautifulSoup(text, "html.parser")

                    target_class = document.select("header div img")

                    for element in target_class:
                        final_url = self.fix_urls(element.get("src", ""))
                        print(final_url)
                        content_urls_and_names.add((final_url, name))

        print(f"The content has been fetched: {content_urls_and_names}")
        return content_urls_and_names

    async def create_folders(self):
        os.makedirs("workouts", exist_ok=True)

    async def download_images(self, content):
        os.chdir("workouts")
        list_of_content = list(content)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for final_url, name in list_of_content:
                tasks.append(self.download_image(session, final_url, name))
            await asyncio.gather(*tasks)
        print("The images have been downloaded")

    async def download_image(self, session, url, name):
        async with session.get(url) as response:
            content = await response.read()
            file_name = f"{name}.png"
            with open(file_name, "wb") as file:
                file.write(content)
            print(f"Downloaded {file_name}")


async def main():
    scrapper = SimplyFitnessWebScrapper()
    await scrapper.create_folders()
    content = await scrapper.get_list_content()
    content_urls_and_names = await scrapper.get_content(content)
    await scrapper.download_images(content_urls_and_names)
    print("The process has been completed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except aiohttp.ServerDisconnectedError:
        exit("Script Ended")
    except:
        exit("Script Ended")
