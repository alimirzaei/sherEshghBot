# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:25:25 2016

@author: toranado
"""
#from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import Image
from bidi.algorithm import get_display
import arabic_reshaper
import colorsys
import glob
from random import randint

def getAvatar(poet):
    latinName = 'unknown'
    if(poet == 'نیما' or poet == 'نیما یوشیج'):
        latinName = 'nima'
    elif(poet =='حافظ'):
        latinName='hafez'
    elif(poet == 'سعدی'):
        latinName='sadi'
    elif(poet == 'فاضل نظری'):
        latinName='fazel_nazari'
    elif(poet == 'مولانا' or poet == 'مولوی'):
        latinName = 'molana'
    
        
        
    allAvatars = glob.glob('/home/ali/Pictures/avatars/'+latinName+'/*.png')
    selected = randint(0,len(allAvatars)-1)
    pic = allAvatars[selected]
    avatar = Image.open(pic)
    avatar = avatar.convert('RGBA')
    return avatar
    
def getPicture(poem,poet):
    allBGs = glob.glob('/home/ali/Pictures/background/*.*')
    selected = randint(0,len(allBGs)-1)
    pic = allBGs[selected]
    img = Image.open(pic)
    
    
    img= img.resize((800,300))
    offset = 200;
    draw = ImageDraw.Draw(img)
    sentences = poem
    maxSize = 0
    boundingSize = (550,300)
    for sent in sentences:
        if(len(sent) > maxSize):
            maxSize = len(sent)
            maxSent = sent
    t1 = arabic_reshaper.reshape(maxSent.decode('utf-8'))
    maxSent = get_display(t1)
    
    fontSize =2
    fontAddress = "/home/ali/Fonts/Mj_Sandbad.ttf"
    while(1):
        font = ImageFont.truetype(fontAddress, fontSize)
        draw.setfont(font)        
        width = draw.textsize(maxSent)[0]
        height = len(sentences)* draw.textsize(maxSent)[1]
        if(width<boundingSize[0] and height < boundingSize[1]):
            fontSize = fontSize+1
            continue
        else:
            break
    
    font = ImageFont.truetype(fontAddress, fontSize-1)
    draw.setfont(font)        
        
    i=0
    W,H = boundingSize
    color = (255,255,255)
    for sent in sentences:
        t1 = arabic_reshaper.reshape(sent.decode('utf-8'))
        text = get_display(t1)
        size = draw.textsize(text)
    ## draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((W/2-size[0]/2+offset, H/2-len(sentences)*size[1]/2-size[1]/4+i*size[1]),text, color)
        i=i+1
    font = ImageFont.truetype(fontAddress, 25)
    draw.setfont(font)        
    t1 = arabic_reshaper.reshape(poet.decode('utf-8'))
    ppoet = get_display(t1)
    size = draw.textsize(ppoet)
    position = (W/2-size[0]/2,H-size[1]-20)
    #pixel = img.getpixel(position)
    #hsv = colorsys.rgb_to_hsv(float(pixel[0])/255,float(pixel[1])/255,float(pixel[2])/255)
    #rgb = colorsys.hsv_to_rgb(((hsv[0]-.5)*360%360)/360,1-hsv[1],1-hsv[2])
    rgb = (1,1,1)
    draw.text(position,ppoet,(int(255*rgb[0]),int(255*rgb[1]),int(255*rgb[2])))
    avatar = getAvatar(poet)
    avatar = avatar.resize([offset,offset])
    img.paste(avatar, (0, img.size[1]-offset), avatar)
    return img
    #img.save('sample-out.jpg')
