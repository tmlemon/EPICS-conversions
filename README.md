# opi2edl
**Python script to convert OPI files to EDL files.**

*Development of this script is ongoing as of December 6, 2018.*

Program is designed to run from Linux command line. Format of command is `python opi2edl.py <opi file>`


### Widgets able to be converted: ###

- Text Update

- Static Text / Label

- Image
  - PNG or GIF only

- Line
  - Can be polyline

- Rectangle

- Circle / Ellipse

- Arc
  - Arc conversion is a little buggy.
  - It does not always convert the angles spanned by the arc correctly.

- Bar Monitor
  - Wiget conversion added, but yet to be fully tested.
