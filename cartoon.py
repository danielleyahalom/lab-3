import wikipedia
import cv2
import os
from images import get_wikipedia_page_thumbnail_url, download_image_from_url

def prompt_for_image():
    """
    Prompts the user for the name of a Wikipedia page and obtains the URL of the thumbnail image of the page.
    
    return url, page_name: str, str
    """
    search_query = input("Enter name of a personality: ")
    try:
        # Search Wikipedia for pages related to the query
        search_results = wikipedia.search(search_query, results=3)

        if not search_results:
            print("No results found. Please try again.")
            return None, None

        print("Select a name from the following list:")
        for i, result in enumerate(search_results, start=1):
            print(f"{i}. {result}")

        # Prompt the user to choose from the search results
        choice = int(input("Enter the number of the desired name: ")) - 1
        if choice < 0 or choice >= len(search_results):
            print("Invalid choice. Please try again.")
            return None, None

        page_name = search_results[choice]
        url = get_wikipedia_page_thumbnail_url(page_name)

        if url:
            return url, page_name
        else:
            print("No image found for the selected Wikipedia page.")
            return None, None

    except Exception as e:
        print(f"Error: Unable to find image for the given name: {e}")
        return None, None

def convert_image_to_cartoon(image_path):
    """
    Converts an image to a cartoon given the image_path.
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Unable to load image. Check the file path.")
            return

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply median blur
        gray = cv2.medianBlur(gray, 5)

        # Detect edges
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)

        # Apply bilateral filter for color smoothing
        color = cv2.bilateralFilter(img, 9, 200, 200)

        # Combine edges and color
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        # Save the cartoonified image
        cartoon_path = f"cartoon_{os.path.basename(image_path)}"
        cv2.imwrite(cartoon_path, cartoon)
        print(f"Cartoon image saved as: {cartoon_path}")

    except Exception as e:
        print(f"Error while converting image to cartoon: {e}")

if __name__ == "__main__":
    # Prompt for an image URL and page name
    image_url, page_name = prompt_for_image()

    if image_url and page_name:
        # Download the image
        image_path = download_image_from_url(image_url, page_name)

        if image_path:
            print(f"Image downloaded and saved as: {image_path}")

            # Convert the image to a cartoon
            convert_image_to_cartoon(image_path)
