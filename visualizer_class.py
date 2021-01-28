import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.axes import Axes

class visualizer():
    def __init__(self, lines):
        self.x_pts = []
        self.y_pts = []

        self.pts = []

        self.fig = plt.figure()
        #self.ax = plt.axes(xlim = (0,500), ylim = (0,500))
        self.lines = lines
    
    #def Printing(self, pt1, pt2, line):
        
    def plot(self, p1):
        idx = 0
        clrs = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'w-']
        mark_pts = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']

        for line in self.lines:
            #print(len(line))
            x = list(line[i][0] for i in range(len(line)))
            y = list(line[i][1] for i in range(len(line)))

            p1.plot(y, x, clrs[idx])
            p1.plot(y, x, mark_pts[idx],  label = 'Robot'+ str(idx))
            
            idx = idx + 1

            if (idx == len(clrs)):
                idx = 0
        #plt.show()
    
    def points_on_line(self):
        time_print = []
        time_travel = []
        for line in self.lines:
            time_print_individual = 0
            time_travel_individual = 0
            lx = []
            ly = []
            for index in range(len(line) - 1):
                pt1 = line[index]
                pt2 = line[index+1]
                
                print(pt1, pt2)
                x1 = pt1[0]
                y1 = pt1[1]
                x2 = pt2[0]
                y2 = pt2[1]
                
                if index%2 ==0 :    #printing
                    num_btw = 3*int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))#Number of points btw 2 points   -- Adjust speed 
                    time_print_individual = time_print_individual + num_btw
                else:           #travelling
                    num_btw = 1*int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))#Number of points btw 2 points   -- Adjust speed
                    time_travel_individual = time_travel_individual + num_btw
                
                for t in range(num_btw):
                    x = x1 + (x2-x1) * (1/num_btw) * t
                    y = y1 + (y2-y1) * (1/num_btw) * t

                    lx.append(x)
                    ly.append(y)
                    
            #print (lx, ly)
            self.x_pts.append(lx)
            self.y_pts.append(ly)
            #print(line)
            time_print.append(time_print_individual)
            time_travel.append(time_travel_individual)
        time_bot = []
        for i, j in zip(time_print, time_travel):
            time_bot.append(i + j)

        return time_bot

    def animation(self):
        mark_pts = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        idx = 0
        Anim = []
        #self.fig = plt.figure()
        
        p1 = self.fig.add_subplot(111)
        
        self.plot(p1)

        #p1.set_xlim([0, 60])
        #p1.set_ylim([0, 60])
 
        #for the rest
        def next(index):
            #i = 0
            color_id = index

            if (color_id+1 == len(mark_pts)):
                color_id = 5 #yellow, so black is shown

            pt, = p1.plot([], [], mark_pts[color_id+1])
            
            def bot():
                i = 0
                while(True):
                    yield i
                    i += 1
                    
            def run(c):
                #Takes one more than original index
                pt.set_data(self.y_pts[index][c], self.x_pts[index][c])
                    
            Anim.append(animation.FuncAnimation(self.fig,run,bot,interval=1))
            
            if index == len(self.x_pts) :
                Axes.set_aspect(p1, 'equal')
                plt.axis([0, 500, 500, 0])
                plt.legend()
                plt.show()
            else:
                #print (index)
                index = index + 1
                next(index) #Recursive Function as a loop

        next(index = -1)

    def main(self):
        #self.plot()
        clr = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        clrdot = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        time_bot = self.points_on_line()
        self.animation()
        
        #frames to min
        for i in range(len(time_bot)):
            time_bot[i] = time_bot[i] * 0.1
            time_bot[i] = time_bot[i]/120

        xaxis_val = []
        val = np.arange(len(time_bot))
        for i in range(len(val)):
            xaxis_val.append('Robot ' + str(val[i]))
        
        for i,t in enumerate(time_bot):
            print('Robot',i,': ', t)
        
        p2=self.fig.add_subplot(111)
        barval = plt.bar( xaxis_val, time_bot, width = 0.5, align = 'center' )
        for i in range(len(time_bot)):
            barval[i].set_color(clr[i])  
        Axes.set_aspect(p2,'equal')
        plt.title('Elapsed Time')
        plt.ylabel('Time in Minutes')
        plt.show()

        p3 = self.fig.add_subplot(111)
        i = 0
        Axes.set_aspect(p2, 'equal')
        plt.axis([0, 500, 500, 0])
        print('25 percent')
        #plt.title('25% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx25 = ptx[0:int(len(ptx)/4)]
            pty25 = pty[0:int(len(ptx)/4)]

            plt.plot(pty25, ptx25, clr[i])
            plt.plot(pty25[-1], ptx25[-1], clrdot[i])
            i = i+1
            
        plt.show()
        
        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('50% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx50 = ptx[0:int(len(ptx)/2)]
            pty50 = pty[0:int(len(ptx)/2)]

            plt.plot(pty50, ptx50, clr[i])
            plt.plot(pty50[-1], ptx50[-1], clrdot[i])
            i = i+1
        plt.show()
        
        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('75% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            ptx75 = ptx[0:int(len(ptx)*0.75)]
            pty75 = pty[0:int(len(ptx)*0.75)]

            plt.plot(pty75, ptx75, clr[i])
            plt.plot(pty75[-1], ptx75[-1], clrdot[i])
            i = i+1
        plt.show()

        i = 0
        plt.axis([0, 500, 500, 0])
        #plt.title('100% Graph')
        for ptx, pty in zip(self.x_pts, self.y_pts):
            plt.plot(pty, ptx, clr[i])
            plt.plot(pty[-1], ptx[-1], clrdot[i])
            i = i+1
        plt.show()

if __name__ == '__main__':
    display = visualizer(lines = [(1,1), (1,4), (4,4), (4,1), (1,1)])
    display.main()
