import math
import CalculateVOC


R_10d, R_10c, R_11d, R_11c, R_12d, R_12c, T_ref_R1d, T_ref_R1c, T_shift_R1d, T_shift_R1c = 7.1135e-4, 0.0016, -4.3865e-4, -0.0032, 2.3788e-4, 0.0045, 347.4707, 159.2819, -79.5816, -41.4548
R_20d, R_20c, R_21d, R_21c, R_22d, R_22c, T_ref_R2d, T_ref_R2c = 0.0288, 0.0113, -0.073, -0.027, 0.0605, 0.0339, 16.6712, 17.0224
C_10d, C_10c, C_11d, C_11c, C_12d, C_12c, C_13d, C_13c, C_14d, C_14c, C_15d, C_15c = 335.4518, 523.215, 3.1712e+3, 6.4171e+3, -1.3214e+3, -7.5555e+3, 53.2138, 50.7107, -65.4786, -131.2298, 44.3761, 162.4688
C_20d, C_20c, C_21d, C_21c, C_22d, C_22c, C_23d, C_23c, C_24d, C_24c, C_25d, C_25c = 3.1887e+4, 6.2449e+4, -1.1593e+5, -1.055e+5, 1.0493e+5, 4.4432e+4, 60.3114, 198.9753, 1.0175e+4, 7.5621e+3, -9.5924e+3, -6.9365e+3
R_s0d, R_s0c, T_ref_Rsd, T_ref_Rsc, T_shift_R_sd, T_shift_R_sc = 0.0048, 0.0055, 31.0494, 22.2477, -15.3253, -11.5943
C_s = 4.5
C_c = 62.7
R_c = 1.94
R_u = 3.08

class Battery:
    # Should I set T_c, T_s, and T_f to 25 deg celsius, assert they should be 25 deg celsius, etc
    # C_bat in amp/h
    # I'm not sure about V_oc being 3.6 volts but couldn't find equation and saw "Charging or discharging V profile can be used for V_oc"
    def __init__(self, soh = 1, soc = 1, C_bat = 2.3, V_oc = 3.6, V_max = 3.6):
        self.V_1 = 0
        self.V_2 = 0
        self.soh = soh
        self.soc = soc
        self.C_bat = C_bat * 3600
        self.max_voc = V_max
        self.V_oc = CalculateVOC.get_voc_from_soc(soc = self.soc, max_voc = self.max_voc)

    def electrical_update(self, I, T_f):
        self.I = I
        self.T_f = T_f
        self.T_s = T_f 
        self.T_c = T_f
        self.T_m = (self.T_s + self.T_c)/2
        
        # Discharge
        if self.I >= 0:
            self.C_1 = C_10d + C_11d*(self.soc) + C_12d*(self.soc**2) + (C_13d + C_14d*(self.soc) + C_15d*(self.soc**2)) * self.T_m    
            self.C_2 = C_20d + C_21d*(self.soc) + C_22d*(self.soc**2) + (C_23d + C_24d*(self.soc) + C_25d*(self.soc**2)) * self.T_m 
            self.R_1 = (R_10d + R_11d * self.soc + R_12d * (self.soc**2)) * math.exp(T_ref_R1d/(self.T_m - T_shift_R1d))
            self.R_2 = (R_20d + R_21d * self.soc + R_22d * (self.soc**2)) * math.exp(T_ref_R2d/self.T_m)
            self.R_0 = R_s0d * math.exp(T_ref_Rsd/(self.T_m - T_shift_R_sd))
            self.soc -= self.I/self.C_bat            
            self.V_1 += -self.V_1/(self.R_1*self.C_1) + self.I/self.C_1
            self.V_2 += -self.V_2/(self.R_2*self.C_2) + self.I/self.C_2
            self.V_t = self.V_oc - self.V_1 - self.V_2 - self.R_0 * self.I

        # Charge
        else: 
            self.C_1 = C_10c + C_11c * (self.soc) + C_12c * (self.soc**2) + (C_13c + C_14c*(self.soc) + C_15c*(self.soc**2)) * self.T_m 
            self.C_2 = C_20c + C_21c*(self.soc) + C_22c*(self.soc**2) + (C_23c + C_24c*(self.soc) + C_25c*(self.soc**2)) * self.T_m
            self.R_1 = (R_10c + R_11c * self.soc + R_12c * (self.soc**2))* math.exp(T_ref_R1c/(self.T_m - T_shift_R1c)) 
            self.R_2 = (R_20c + R_21c * self.soc + R_22c * (self.soc**2)) * math.exp(T_ref_R2c/self.T_m)
            self.R_0 = R_s0c * math.exp(T_ref_Rsc/(self.T_m - T_shift_R_sc))
            self.soc -= self.I/self.C_bat
            self.V_1 += -self.V_1/(self.R_1*self.C_1) + self.I/self.C_1
            self.V_2 += -self.V_2/(self.R_2*self.C_2) + self.I/self.C_2
            self.V_t = self.V_oc + self.V_1 + self.V_2 + self.R_0 * self.I
            
     
    """Calculates changes to surface and core temperatures where T_s and T_c begin at equilibrium"""
    # Where do I get surface/core temp, R_c, and core/surface heat capacity (C_c, C_s)? Do I make assumptions about values?
    def thermal_update(self):
        self.Q = self.I * (self.V_oc - self.V_t)
        self.T_c += (self.T_s - self.T_c)/(R_c * C_c) + self.Q/C_c
        self.T_s += (self.T_f - self.T_s)/(R_u * C_s) - (self.T_s - self.T_c)/(R_c * C_s)
        self.T_m = (self.T_s + self.T_c)/2
    
    def aging_update(self, seconds):
        # Q_b is % capacity loss, C is C-rate (ratio of I to C_bat) and M(c) is shown in table II of optimal paper
        z = 0.5
        c = (self.I * 3600) / self.C_bat
        # R = 8.314 is ideal gas constant
        R = 8.314 

        
        if 0 <= c <= 0.5:
            self.M = 31630
        elif 0.5 < c <= 2:
            self.M = 21681
        elif 2 < c <= 6:
            self.M = 21681
        else:
            self.M = 15512

        # Seems like this is way to big. I'm raising M to the power of this divided by a relatively small number
        self.E_a = (31700 - 370.3 * c)

        # A is discharged Ah throughput dependent on C-rate (units amp-hr). NOT SURE ABOUT THIS EQUATION
        
        self.A = self.C_bat * c * seconds/3600
        
        # delta_Q_b is percentage of capacity lost [%]

        self.delta_Q_b = self.M * math.exp(-self.E_a/(R * self.T_c)) * self.A ** z

        # Right now this change is REALLY small
        self.C_bat -= self.delta_Q_b

        # Approaches infinity as argument to exponential increases!!!
        self.A_total = (20/(self.M * math.exp(-self.E_a/(R* self.T_c))))**(1/z)
        
        self.cycles_to_EOL = 3600 * self.A_total/self.C_bat
        
        self.N = 3600 * self.A_total / self.C_bat
        
        # C_bat in Amp seconds
        self.soh -= abs(self.I)/(2 * self.N * self.C_bat)
    
    def update(self, seconds, I = 1, T_f = 25):
        # Loop through electrical mode, thermal model, aging model, then update VOC

        while seconds:
            self.electrical_update(I, T_f)
            self.thermal_update()
            self.aging_update(seconds)
            self.V_oc = CalculateVOC.get_voc_from_soc(soc = self.soc, max_voc = self.max_voc)

            seconds -= 1
            
            # Rails 0 <= V_oc <= max_voc and 0 <= soc <= 1 if values go out of bounds  

            if self.V_oc > self.max_voc:
                self.V_oc = self.max_voc
            elif self.V_oc < 0:
                self.V_oc = 0
            if self.soc > 1:
                self.soc = 1
            elif self.soc < 0:
                self.soc = 0

# battery_example = Battery()
# battery_example.update(1000)
# battery_example.soc