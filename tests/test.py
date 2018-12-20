#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

s = cv2.imread('s.png')
s_gray = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)

t = cv2.imread('t.png')
t_gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)

res = cv2.matchTemplate(s_gray, t_gray, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(min_val, max_val, min_loc, max_loc)

h, w = t.shape[:2]
print(w, h)

# cv2.rectangle(s, (int(max_loc[0] - w / 2), int(max_loc[1] - h / 2)), (int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)),
#               (0, 0, 255), 2)

cv2.rectangle(s, (int(max_loc[0]), int(max_loc[1])), (int(max_loc[0] + w), int(max_loc[1] + h)),
              (0, 0, 255), 2)

cv2.imwrite('r.png', s)
