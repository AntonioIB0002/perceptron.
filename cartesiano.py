import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene,QMessageBox
from PyQt5.QtGui import QPainter, QPen,QColor
from PyQt5.QtCore import Qt,QLineF
from mw import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 740, 740)

        self.coordenadas = []
        self.w1 = 0
        self.w2 = 0
        self.bias = 0
        self.Cartesiano()
        self.ui.graphicsView.mousePressEvent = self.mousePressEvent
        self.ui.pushButton_graficar.clicked.connect(self.grafica)
        self.ui.pushButton_reset.clicked.connect(self.reset)

    def perseptron(self):
        w = np.array([self.bias,self.w1,self.w2])
        x = np.array(self.coordenadas)
        print(x)
        z = np.hstack((np.ones((x.shape[0],1)),x))

        y = np.array(np.dot(w,z.T) >= 0)

        print(y)
        m = -w[1]/w[2]
        c = -w[0]/w[2]

        x1 = -20
        y1 = m * x1 + c
        x2 = 20  
        y2 = m * x2 + c

        # Juste para cuadrar en el plano
        y1 = -y1 * 20 + self.scene.height() / 2
        y2 = -y2 * 20 + self.scene.height() / 2
        x1 = x1 * 20 + self.scene.width() / 2
        x2 = x2 * 20 + self.scene.width() / 2

        
        
        self.scene.clear()
        self.Cartesiano()
        for i in range(len(y)):
            if y[i] == 0:
                plt.plot(x[i][0], x[i][1],'or')
                self.scene.addEllipse((x[i][0])*20+self.scene.width()/2-2, -(x[i][1])*20+self.scene.height()/2-2, 4, 4, QPen(Qt.red), Qt.red)

            else:
                plt.plot(x[i][0], x[i][1],'ob')
                self.scene.addEllipse((x[i][0])*20+self.scene.width()/2-2, -(x[i][1])*20+self.scene.height()/2-2, 4, 4, QPen(Qt.blue), Qt.blue)
        line = QLineF(x1, y1, x2, y2)
        pen = QPen(Qt.green)
        pen.setWidth(2)
        self.scene.addLine(line, pen)

        plt.axline((0, c), slope = m, linewidth=4)

        plt.title('Perceptrón')
        plt.grid('on')


        plt.xlabel(r'x1')
        plt.ylabel(r'x2')

        plt.show()


    def reset(self):
        self.scene.clear()
        self.coordenadas.clear()
        self.Cartesiano()
        self.ui.lineEdit_bias.clear()
        self.ui.lineEdit_w1.clear()
        self.ui.lineEdit_w2.clear()

    def grafica(self):
        try:
            self.w1 = float(self.ui.lineEdit_w1.text())
            self.w2 = float(self.ui.lineEdit_w2.text())
            self.bias = float(self.ui.lineEdit_bias.text())
            
        except ValueError:
            QMessageBox.warning(self, 'Captura no Valida', 'ingrese solo números enteros o reales.')

        try:
            self.perseptron()
        
        except ValueError:
            QMessageBox.warning(self,'Ingrese entradas','Seleccione entradas en el plano')
        



    def Cartesiano(self):
        gris = QColor(238, 223, 220)
        for x in range(-20, 21):
            self.scene.addLine(self.scene.width() / 2 + x * 20,0,self.scene.width() / 2 + x * 20,self.scene.height(),gris)
            self.scene.addLine(self.scene.width() / 2 + x * 20, self.scene.height() / 2 - 5,
                               self.scene.width() / 2 + x * 20, self.scene.height() / 2 + 5, Qt.black)
            
            

      
        for y in range(-20, 21):
            self.scene.addLine(0, self.scene.height() / 2 + y * 20,self.scene.width(),self.scene.height() / 2 + y * 20,gris)
            self.scene.addLine(self.scene.width() / 2 - 5, self.scene.height() / 2 + y * 20,
                               self.scene.width() / 2 + 5, self.scene.height() / 2 + y * 20, Qt.black)
            

            

        self.scene.addLine(0,self.scene.height() / 2,self.scene.width(),self.scene.height() / 2,Qt.black)
        self.scene.addLine(self.scene.width()/2,0,self.scene.width()/2,self.scene.height())

        self.ui.graphicsView.setScene(self.scene)


    def mousePressEvent(self, event):
        pos = self.ui.graphicsView.mapToScene(event.pos())

        pen = QPen(Qt.red)
        brush = Qt.red
        point = self.scene.addEllipse(pos.x() - 2, pos.y() - 2, 4, 4, pen, brush)
        
        x = pos.x()
        y = pos.y()
        if x <= 750 and y <= 750:
            #ajuste hecho para cuadrar en el plano cartesiano dado que no tiene cuadrantes negativos se busco
            #el centro y se ajusto a que cada 20 pixeles representa una unidad
            ajustex = (pos.x()-370)/20
            ajustey = (pos.y()-370)/20 *-1
            self.coordenadas.append((ajustex, ajustey))
            print("Coordenadas del punto:", ajustex,ajustey )







app = QApplication(sys.argv)
ventana = Window()
ventana.show()
sys.exit(app.exec_())
