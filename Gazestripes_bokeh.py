import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bokeh.plotting import figure
from bokeh.embed import components
from HelperFunctions import get_data_user, get_data_map, get_array_fixations, get_x_fixation, get_y_fixation, get_duration_fixation, random_color


FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


def get_cropped_images(user_name, name_map):
    string_folder='static/stimuli/'
    image_source = string_folder+name_map
    im = plt.imread(image_source)
    img = Image.fromarray(im)
    width, height = img.size

    images=[]
    for i in get_array_fixations(user_name, name_map):
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        #cropped_img.save("{0}.jpg".format(type))
        images.append(cropped_img)
    return images, len(images)
    #return(cropped_img)

def draw_gaze_stripes(user_name, name_map):

    if user_name == 'ALL':
        max_amount_images = 0
        ListUser = get_data_map(name_map).user.unique()

        for i in range(len(ListUser)):
            images, amount_images = get_cropped_images(ListUser[i], name_map)
            max_amount_images = max(max_amount_images, amount_images)
        
        fig = figure(plot_width = 25*max_amount_images, plot_height = 25*len(ListUser), x_range=(0,max_amount_images-1), y_range=(-1,len(ListUser)-1), x_axis_location=None, y_axis_location=None, title = 'Gaze stripes all users')
        for i in range(len(ListUser)):
            images, amount_images = get_cropped_images(ListUser[i], name_map)
            amount_images -= 1
            for j in range(amount_images):
                #This must be changed
                fig.image_url(['1.jpg'], j, i, 1, 1)
        
    else:
        images, amount_images = get_cropped_images(user_name, name_map)
        #we need to work on the x axis (duration scale)
        fig = figure(plot_width=75*amount_images, plot_height=75, x_range=(0,amount_images), y_range=(0,1), x_axis_location=None, y_axis_location=None, title = 'Gaze stripes user '+ str(user_name[1:]))
        for i in range(amount_images):
            im = images[i].convert("RGBA")
            imarray = np.array(im)
            fig.image_rgba(image=[imarray], x=i, y=0, dw=1, dh=1)

    script, div = components(fig)
    return [script, div]

#get_cropped_images('p1', '01_Antwerpen_S1.jpg')
