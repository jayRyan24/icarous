"""
    MAVProxy geofence module
"""
import os, time, platform, math
from pymavlink import mavutil
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.mavproxy_map import mp_slipmap
from MAVProxy.modules.lib import mp_settings
from MAVProxy.modules.lib.mp_menu import *  # popup menus

if mp_util.has_wxpython:
    from MAVProxy.modules.lib.mp_menu import *

class SlipEllipse(mp_slipmap.SlipObject):
    def __init__(self, key, layer, center, axes, angle, startAngle, endAngle, colour, linewidth, popup_menu=None):
        mp_slipmap.SlipObject.__init__(self, key, layer, popup_menu=popup_menu)
        self.center = center
        self.axes = axes
        self.angle = angle
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.colour = colour
        self.linewidth = linewidth
        self._pix_points = []

    def bounds(self):
        '''return bounding box'''
        if self.hidden:
            return None
        return (self.center[0],self.center[1],0,0)

    def draw(self, img, pixmapper, bounds):
        '''draw a polygon on the image'''
        if self.hidden:
            return

        center = pixmapper(self.center)
        mp_slipmap.cv.Ellipse(img,center,self.axes,self.angle,self.startAngle,self.endAngle,self.colour,self.linewidth)


class Traffic:
    def __init__(self,x,y,z,vx,vy,vz,tstart):
        self.x0 = x;
        self.y0 = y;
        self.z0 = z;

        self.vx0 = vx;
        self.vy0 = vy;
        self.vz0 = vz;

        self.x = self.x0;
        self.y = self.y0;
        self.z = self.z0;

        self.tstart = tstart

    def get_pos(self,t):
        dt = t-self.tstart
        
        self.x = self.x0 + self.vx0*(dt)
        self.y = self.y0 + self.vy0*(dt)
        self.z = self.z0 + self.vz0*(dt)
    
class TrafficModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(TrafficModule, self).__init__(mpstate, "traffic", "traffic management", public = True)
        
        self.add_command('traffic', self.load_traffic,
                         "start traffic",
                         ["load <x,y,z,vx,vy,vz>"])
 
        self.menu_added_console = False
        self.menu_added_map = False
        self.traffic_list = [];
        self.traffic_on_map = [];
        self.WCV = False;
        self.radius = 10.0;


        self.numBands = 0;
        self.Bands = [];


        
        
    def idle_task(self):
        '''called on idle'''
        if self.module('console') is not None and not self.menu_added_console:
            self.menu_added_console = True
            self.module('console').add_menu(self.menu)
        if self.module('map') is not None and not self.menu_added_map:
            self.menu_added_map = True
            self.module('map').add_menu(self.menu)

        
            
                                
    def mavlink_packet(self, m):
        '''handle and incoming mavlink packet'''                        

        
        self.Update_traffic()

        if(len(self.traffic_list) > 0):
            wcv_volume = mp_slipmap.SlipCircle("well_clear_volume", 3,\
                                               (self.module('map').lat,self.module('map').lon),\
                                               self.radius,\
                                               (0, 0, 255), linewidth=2)
        
            self.mpstate.map.add_object(wcv_volume)

            self.numBands = 1

            if self.numBands > 0:
                colour = (0,255,0,100)
                center = (self.module('map').lat,self.module('map').lon)
                axes = (50,50)
                angle = -90
                startAngle = 0
                stopAngle = 270
                thickness = -1
                band_guidance = SlipEllipse("band",1,center,axes,angle,startAngle,stopAngle,colour,thickness)
                self.mpstate.map.add_object(band_guidance)
                
        if m.get_type() == "TRAFFIC_INFO":
            print m.breach_status

        if m.get_type() == "SPATIAL_USER_1":
            self.numBands = m.param1

            numBands = 0
            numBands = numBands + 1

            self.Bands = []

            if(numBands <= self.numBands):
                low    = (float)(m.params2/10000)/10
                high   = (float)(m.params2%10000)/10
                bands = [low,high]
                self.Bands.append(bands)
                numBands = numBands + 1

            if (numBands <= self.numBands):
                low = (float)(m.params3 / 10000) / 10
                high = (float)(m.params3 % 10000) / 10
                bands = [low, high]
                self.Bands.append(bands)
                numBands = numBands + 1

            if (numBands <= self.numBands):
                low = (float)(m.params4 / 10000) / 10
                high = (float)(m.params4 % 10000) / 10
                bands = [low, high]
                self.Bands.append(bands)
                numBands = numBands + 1

            if (numBands <= self.numBands):
                low = (float)(m.params5 / 10000) / 10
                high = (float)(m.params5 % 10000) / 10
                bands = [low, high]
                self.Bands.append(bands)
                numBands = numBands + 1

            if (numBands <= self.numBands):
                low = (float)(m.params6 / 10000) / 10
                high = (float)(m.params6 % 10000) / 10
                bands = [low, high]
                self.Bands.append(bands)
                numBands = numBands + 1

            if (numBands <= self.numBands):
                low = (float)(m.params7 / 10000) / 10
                high = (float)(m.params7 % 10000) / 10
                bands = [low, high]
                self.Bands.append(bands)
                numBands = numBands + 1


    def load_traffic(self, args):
        '''fence commands'''
        if len(args) < 1:
            self.print_usage()
            return        
        elif args[0] == "load":
            if len(args) != 7:
                print len(args)
                self.print_usage();                
                return
            else:
                start_time = time.time();
                tffc = Traffic(float(args[1]),float(args[2]),float(args[3]), \
                               float(args[4]),float(args[5]),float(args[6]),start_time)
                self.traffic_list.append(tffc)
                self.start_lat = self.module('map').lat
                self.start_lon = self.module('map').lon
                print len(self.traffic_list)
        elif args[0] == "radius":
            if len(args) == 2:
                self.radius = float(args[1]);
            
        
        else:
            self.print_usage()

    def Update_traffic(self):
        '''Update traffic icon on map'''
        
        #from MAVProxy.modules.mavproxy_map import mp_slipmap
        t = time.time()
        
        for i,tffc in enumerate(self.traffic_list):
            vehicle = 'Traffic%d' % i
            
            if(vehicle not in self.traffic_on_map):
                
                colour = "blue"
                vehicle_type = "copter"
                icon = self.mpstate.map.icon(colour + vehicle_type + '.png')
                
                self.mpstate.map.add_object(mp_slipmap.SlipIcon(vehicle, (0,0), icon, layer=3, rotation=0, follow=False, \
                                                                trail=mp_slipmap.SlipTrail()))
                self.traffic_on_map.append(vehicle)
                                                        
            self.traffic_list[i].get_pos(t)
            (lat, lon) = mp_util.gps_offset(self.start_lat,self.start_lon, self.traffic_list[i].y, self.traffic_list[i].x)
            heading = math.degrees(math.atan2(self.traffic_list[i].vy0, self.traffic_list[i].vx0))            
            self.mpstate.map.set_position(vehicle, (lat, lon), rotation=heading)

            self.master.mav.command_long_send(
                1,  # target_system
                0, # target_component
                mavutil.mavlink.MAV_CMD_SPATIAL_USER_1, # command
                0, # confirmation
                i, # param1
                self.traffic_list[i].vx0, # param2
                self.traffic_list[i].vy0, # param3
                self.traffic_list[i].vz0, # param4
                lat, # param5
                lon, # param6
                self.traffic_list[i].z0) # param7
            

    def print_usage(self):
        print("usage: traffic load x y z vx vy vz")
        

def init(mpstate):
    '''initialise module'''
    return TrafficModule(mpstate)
