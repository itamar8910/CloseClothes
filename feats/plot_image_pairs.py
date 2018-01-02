import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from closest_feat import closest_pairs
import sys,os,click,subprocess

def plot_pairs_with_html(pairs,dir_path,title="vgg"):
    head = """<head>{}</head>
    <body>
    <table style="width:100%">\n
    """.format(title)
    tail = """
    </table>
    <p style="clear:both;">
    </body>\n"""
    body = ""
    for pair in pairs:
        body+="<tr>"
        body+="""<th><IMG SRC="{}" STYLE="FLOAT: LEFT; WIDTH: 30%; MARGIN-RIGHT: 1%; MARGIN-BOTTOM: 0.5EM;" ></th>\n""".format(os.path.join(dir_path,pair[0].strip(".npy") + ".jpg"))
        body+="""<th><img src="{}" style="float: left; width: 30%; margin-right: 1%; margin-bottom: 0.5em;" ></th>\n""".format(os.path.join(dir_path,pair[1].strip(".npy") + ".jpg"))
        body+="</tr>"

    with open("plot.html",'w') as html_file:
        html_file.write(head + body + tail)
    
def plot_pairs(pairs,dir_path):
    f, subplots= plt.subplots(len(pairs) , 2)
    print(pairs)
    for plot,pair in zip(subplots,pairs):
        plot[0].imshow(mpimg.imread(os.path.join(dir_path,pair[0].strip(".npy") + ".jpg")))
        plot[1].imshow(mpimg.imread(os.path.join(dir_path,pair[1].strip(".npy") + ".jpg")))
        plot[0].axes.get_xaxis().set_visible(False)
        plot[0].axes.get_yaxis().set_visible(False)
        plot[1].axes.get_xaxis().set_visible(False)
        plot[1].axes.get_yaxis().set_visible(False)
        plt.axis('off')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        plot_pairs_with_html(closest_pairs(sys.argv[1]),sys.argv[2])
    else:
        print("Missing path to features and/or images")
