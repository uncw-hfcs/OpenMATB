from PySide import QtGui, QtCore
from numpy import linspace

class Communicate(QtCore.QObject):

    updateBW = QtCore.Signal(int)


class WScale(QtGui.QWidget):

    def __init__(self, parent, name, nbsteps, order, style):
        super(WScale, self).__init__(parent)
        self.style = style
        self.nbsteps = nbsteps
        self.middle = (self.nbsteps - 1) / 2

        self.uly = 0.3 * self.parent().height()
        self.scaleHeight = 0.55 * self.parent().height()

        self.borderSize = 0.50 / 6 * self.parent().width() / 15.
        hw_ratio = 0.50 / 2.8  # width = hw_ratio * height
        self.scaleWidth = hw_ratio * self.scaleHeight
        # ~ self.scaleWidth = 0.5 / 6 * self.parent().width() + self.borderSize * 2

        self.labelFont = QtGui.QFont("sans-serif", self.scaleWidth / 3., QtGui.QFont.Bold)

        self.scaleHeight = self.scaleWidth / hw_ratio
        self.partHeight = self.scaleHeight / self.nbsteps

        self.arrow = QtGui.QLabel(self)

        self.label = QtGui.QLabel(self)
        self.label.setText(name)
        self.label.setFont(self.labelFont)

        self.feedback = 0

        self.ulx = self.parent().width() * [i / 10. for i in range(0, 11, 2)][int(order)] - self.scaleWidth / 2

        self.label.setGeometry(QtCore.QRect(self.ulx - self.scaleWidth / 2, self.uly + self.scaleHeight + 10, self.scaleWidth * 2, 0.1 * self.parent().height()))
        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.position = self.middle
        self.feedback = 0
        self.tickposition_list = linspace(1, 0, self.nbsteps + 2).tolist()

        self.pen = QtGui.QPen(QtGui.QColor('#000000'), self.borderSize, QtCore.Qt.SolidLine)


    def paintEvent(self, e):
        if self.style==1:
            self.arrow.setText(u'\u25B6')
            self.arrowFont = QtGui.QFont("sans-serif", self.scaleWidth/5, QtGui.QFont.Bold)
        elif self.style==2:
            self.arrow.setText("<font color='#FFFF00'>>></font>")
            self.arrowFont = QtGui.QFont("sans-serif", self.scaleWidth/4., QtGui.QFont.Bold)

        self.arrow.setFont(self.arrowFont)

        if self.feedback:
            self.position = self.middle

        qp = QtGui.QPainter()
        qp.begin(self)
        if self.style==1:
            self.drawscaleI(qp)
        elif self.style==2:
            self.drawscaleII(qp)

        qp.end()


    # MATB-I style
    def drawscaleI(self, qp):
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setPen(self.pen)
        qp.setBrush(QtCore.Qt.white)
        qp.drawRect(self.ulx,self.uly, self.scaleWidth, self.scaleHeight)


        for thisTick in self.tickposition_list:
            if thisTick not in [0,1]: # not extreme values
                lineLenght = 0.3 * self.scaleWidth if thisTick != 0.5 else 0.5 * self.scaleWidth
                qp.drawLine(self.ulx + self.scaleWidth, self.uly + thisTick * self.scaleHeight, self.ulx + self.scaleWidth - lineLenght, self.uly + thisTick * self.scaleHeight)

        centerY = self.uly + self.scaleHeight - self.tickposition_list[self.position + 1] * self.scaleHeight
        self.arrow.setGeometry(QtCore.QRect(self.ulx + 0.1 * self.scaleWidth, centerY - 10, 0.4 * self.scaleWidth, 20))
        self.arrow.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        if self.feedback == 1:
            qp.setBrush(QtCore.Qt.yellow)
            qp.drawRect(self.ulx, self.uly + self.scaleHeight - self.partHeight, self.scaleWidth, self.partHeight)

        self.update()


    # MATB-II style
    def drawscaleII(self, qp):
        pen = QtGui.QPen(QtGui.QColor('#000000'), self.borderSize, QtCore.Qt.SolidLine)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        qp.setPen(pen)

        current_y = 0
        for thisPart in range(0, self.nbsteps):
            if thisPart in [self.position - 1, self.position, self.position + 1]:
                qp.setBrush(QtGui.QColor('#0066CC'))
                if thisPart == self.position:
                    self.arrow.setGeometry(
                        self.ulx - self.borderSize * 2, self.uly + current_y, self.scaleWidth, self.partHeight)
                    self.arrow.setAlignment(
                        QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            else:
                qp.setBrush(QtGui.QColor('#99CCFF'))

            if thisPart == self.nbsteps - 1 and self.feedback:
                qp.setBrush(QtGui.QColor('#FFFF00'))
            qp.drawRect(self.ulx, self.uly + current_y,
                        self.scaleWidth - self.borderSize, self.partHeight)
            current_y += self.partHeight

        self.update()
