import cv2
import pandas as pd

img_path = 'Color detection/Color detection/pic2.jpg'
csv_path = 'Color detection/Color detection/colors.csv'

"""
CSV File Has 6 Columns, Namely,
1. Color
2. Color Name
3. Hex Value of Color
4. R value
5. G Value
6. B Value
"""

index = ['color','color_name','hex','R','G','B']
df = pd.read_csv(csv_path, names=index, header=None)

img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))  # Resizing of an Image

clicked = False  # I have assumed left button isn't clicked Twice
r = g = b = xpos = ypos = 0    # Initializing Five Variables with Zero

def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        """
        Here I am trying to find which color values best matches the color in the image
        with Addition of Difference in Absolute Values

        First of all we try to find the minimum difference of RGB Components Stored in the
        CSV File (We will do it for all 865 Rows in the Dataset)
        """
        d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i,'color_name']  # Finding Color Name

    return cname


# Now We need to find the Co-ordinates on the image where we will click to get the color
def draw_function(event, x, y, flags, params):
    """

    :param event:  Left click, right click, double Right / left click etc are the events
    :param x:  X Co-ordinate of the position where we will click to get the color
    :param y:  Y Co-ordinate of the position where we will click to get the color
    :param flags:
    :param params:
    :return:
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked, r, g, b, xpos, ypos
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]   # Since OpenCV Works with BGR Color Format not with RGB Format
        b = int(b)   # Since Originally it is in Numpy uint8
        g = int(g)
        r = int(r)


cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_function)

while True:
    cv2.imshow('Image', img)
    if clicked:
        cv2.rectangle(img, (20,20), (600, 60), (b, g, r), -1)
        """
        Above Line Will create a rectangle / strip on the top of our image on which we can write some text
        """
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)  # If Color is too light then write in Black Color

    if cv2.waitKey(20) & 0xFF == 27:
        """
        If Anything doesn't Happen or If We Press the Escape key then break the Loop
        0xFF == 27 Checks Whether the Esc Key is pressed
        """
        break


cv2.destroyAllWindows()
