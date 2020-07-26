from gl import Render, color

from obj import Obj

r = Render(1000, 800)


poly1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
poly2 = [(321, 335),  (288, 286),  (339, 251),  (374, 302)]
poly3 = [(377, 249),  (411, 197),  (436, 249)]
poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
        (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
        (597, 215), (552, 214), (517, 144), (466, 180)]
poly5 = [(682, 175),  (708, 120),  (735, 148),  (739, 170)]

r.glColor(0,1,1)
r.glDrawPolygon(poly1)
r.glFillPolygon(poly1)

r.glColor(1,0,0)
r.glDrawPolygon(poly2)
r.glFillPolygon(poly2)

r.glColor(1,0,1)
r.glDrawPolygon(poly3)
r.glFillPolygon(poly3)

r.glColor(0.5,1,0)
r.glDrawPolygon(poly4)
r.glFillPolygon(poly4)

r.glColor(0.5,0.5,0)
r.glDrawPolygon(poly5)
r.glFillPolygon(poly5)


r.glFinish('output.bmp')