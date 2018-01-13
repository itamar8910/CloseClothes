import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from closest_feat import get_KNN
from operator import itemgetter
from webbrowser import open_new_tab
import sys,os,click,subprocess

def plot_knn_with_html(groups,img_dir,title="vgg"):
    head = """<head>{}</head>
    <body>
    <table style="width:100%">\n
    """.format(title)
    tail = """
    </table>
    <p style="clear:both;">
    </body>\n"""
    body = ""
    for group in groups:
        print(group)
        group_leader = group[0][0] #name of first item which is (LEADER,0)
        group_names = map(itemgetter(0),group)
        group_distances = map(itemgetter(1),group)
        group_images = map(lambda x:os.path.join(img_dir,x.strip('npy') + 'jpg'),group_names)
        body+="<tr>"

        for image,distance in zip(group_images,group_distances):
            body+="""<th>
            <p>{image_name}</p>
            <IMG SRC="{image_path}" STYLE="FLOAT: LEFT; WIDTH: 30%; MARGIN-RIGHT: 1%; MARGIN-BOTTOM: 0.5EM;" />
            <p>{distance:.5}</p>
            </th>\n""".format(image_path=image,image_name = image.split('/')[-1],distance=distance)
        body+="</tr>"

    with open(title + ".html",'w') as html_file:
        html_file.write(head + body + tail)
    
@click.command()
@click.argument("feat_dir")
@click.argument("img_dir")
@click.option("-k","--k",default=1)
@click.option("--title","-t",default="plot")
def plot_knn(feat_dir,img_dir,k,title):
    plot_knn_with_html(get_KNN(feat_dir,k),img_dir,title)
    open_new_tab(title + '.html')



if __name__ == "__main__":
    plot_knn()
