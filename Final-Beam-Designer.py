from tkinter import *
from tkinter import ttk
import numpy as np
import math

root = Tk()
root.title("Beam Designer")

#TABLE FOR FSC VALUE

Fe415_Table = {
        0.00144: (288.7),
        0.00163: (306.7),
        0.00192: (324.8),
        0.00241: (342.8),
        0.00276: (351.8),
        0.00380: (360.9),
}
Fe500_Table = {
        0.00174: (347.8),
        0.00195: (369.6),
        0.00226: (391.3),
        0.00277: (413),
        0.00312: (423.9),
        0.00417: (434.8),
}

defined_Fe415 = list(Fe415_Table.keys())
defined_Fe415.sort()

defined_Fe500 = list(Fe500_Table.keys())
defined_Fe500.sort()

defined_Fe4151 = list(Fe415_Table.values())
defined_Fe4151.sort()

defined_Fe5001 = list(Fe500_Table.values())
defined_Fe5001.sort()


def getAppropriateData(fy,X):
        if fy == 415:
            return (Fe415_Table , defined_Fe415 , defined_Fe4151 )
        elif fy == 500:
            return (Fe500_Table, defined_Fe500 , defined_Fe5001 )
        
def interpolateValues(X,fy):
    if X<1:
        
        map_to_use, key_list, value_list = getAppropriateData(fy,X)
        
        if X >= key_list[0]:
    
            idx_low = idx_high = 0
            for idx, def_ang in enumerate(key_list):
                   
                if def_ang > X:
                    idx_high = idx
                    idx_low = idx - 1
                    break
            x0 = key_list[idx_low]
            x1 = key_list[idx_high]
            y0_list = map_to_use[x0]
            y1_list = map_to_use[x1]
            x = X
    
            #y = [ y0(x1-x) + y1(x-x0) ] / (x1 - x0)
            fsc = (y0_list * (x1 -x)  + y1_list * (x - x0) ) / (x1 - x0)
        else:
            fsc = X * 200000
    
    if X>1: 
        
        map_to_use, key_list, value_list = getAppropriateData(fy,X)
        
        if X>= value_list[0]:
            
            idx_low = idx_high = 0
            for idx, def_ang in enumerate(value_list):
               
                if def_ang > X:
                    idx_high = idx
                    idx_low = idx - 1
                    break
            x0 = value_list[idx_low]
            x1 = value_list[idx_high]
            y0_list = key_list[value_list.index(x0)]
            y1_list = key_list[value_list.index(x1)]
            x = X
                
            #y = [ y0(x1-x) + y1(x-x0) ] / (x1 - x0)
            fsc = (y0_list * (x1 -x)  + y1_list * (x - x0) ) / (x1 - x0)
        else:
            fsc = X / 200000    
            
            
    return fsc



#LABELS
ConcreteGrade_label = Label(root, text = "Concrete Grade (fck):").grid(row = 0, column = 0)
SteelGrade_label = Label(root, text = "Steel Grade (fy):").grid(row = 1, column = 0)
BeamWidth_label = Label(root, text = "Width of the beam, mm:").grid(row = 2, column = 0)
BeamDepth_label = Label(root, text = "Depth of the beam, mm:").grid(row = 3, column = 0)

MomentEntryFrame = LabelFrame(root, text="Enter the maximum values of respective moments and shears:", padx = 5, pady = 5)
MomentEntryFrame.grid(row =4 ,column =0 ,padx = 10, pady = 10, columnspan = 2)

MomentType_label = Label(MomentEntryFrame, text = "Type of Moment").grid(row = 5, column =5)
Left_label = Label(MomentEntryFrame, text = "Left Side").grid(row = 5, column =6)
Center_label = Label(MomentEntryFrame, text = "Center").grid(row = 5, column =7)
Right_label = Label(MomentEntryFrame, text = "Right Side").grid(row = 5, column =8)
HoggingMoment_label = Label(MomentEntryFrame, text = "Hogging Moment (-ve), kNm").grid(row = 6, column =5)
SaggingMoment_label = Label(MomentEntryFrame, text = "Sagging Moment (+ve), kNm").grid(row = 7, column =5)
MaxSF_label = Label(MomentEntryFrame, text = "Maximum Shear Force kNm").grid(row = 8, column = 5)

TDL = Label(root, text = "Total Dead Load (kN)").grid(row = 9, column = 0)
TLL = Label(root, text = "Total Live Load (kN)").grid(row = 10, column = 0)

ClearSpan_label = Label(root, text = "Clear Span (mm)").grid(row = 11, column = 0)
ClearCover_Cover = Label(root, text = "Clear Cover (mm)").grid(row = 12, column = 0)


#Dropdown Menus/EntryValues
SelectedCG = IntVar()
SelectedCG.set(20)
ConcreteCombo = OptionMenu(root,SelectedCG, 15, 20, 25, 30, 35).grid(row = 0, column = 1)
SelectedSG = IntVar()
SelectedSG.set(415)
SteelCombo = OptionMenu(root,SelectedSG, 250, 415, 500, 550).grid(row = 1, column = 1)

Width__Entry = DoubleVar()
Depth__Entry = DoubleVar()
Width_Entry = Entry(root, textvariable = Width__Entry).grid(row = 2, column = 1)
Depth_Entry = Entry(root, textvariable = Depth__Entry).grid(row = 3, column = 1)
Width__Entry.set(300)       #######REMOVE LATER
Depth__Entry.set(600)       #######REMOVE LATER

HogLeft__Entry = DoubleVar()
HogLeft_Entry = Entry(MomentEntryFrame, textvariable = HogLeft__Entry).grid(row =6 , column =6 )
HogLeft__Entry.set(369)     #######REMOVE LATER
HogCenter__Entry = DoubleVar()
HogCenter_Entry = Entry(MomentEntryFrame, textvariable = HogCenter__Entry ,state = DISABLED).grid(row =6 , column =7 )
HogRight__Entry = DoubleVar()
HogRight_Entry = Entry(MomentEntryFrame, textvariable = HogRight__Entry ).grid(row =6 , column =8 )
HogRight__Entry.set(371)    #######REMOVE LATER

SagLeft__Entry = DoubleVar()
SagLeft_Entry = Entry(MomentEntryFrame, textvariable = SagLeft__Entry).grid(row =7 , column =6 )
SagLeft__Entry.set(281)        #######REMOVE LATER

SagCenter__Entry = DoubleVar()
SagCenter_Entry = Entry(MomentEntryFrame, textvariable = SagCenter__Entry).grid(row =7 , column =7 )
SagCenter__Entry.set(65)       #######REMOVE LATER

SagRight__Entry = DoubleVar()
SagRight_Entry = Entry(MomentEntryFrame, textvariable = SagRight__Entry).grid(row =7 , column =8 )
SagRight__Entry.set(237)       #######REMOVE LATER

MaxSFLeft__Entry = DoubleVar()
MaxSFLeft_Entry = Entry(MomentEntryFrame, textvariable = MaxSFLeft__Entry).grid(row =8 , column =6 )
MaxSFLeft__Entry.set(195)       #######REMOVE LATER

MaxSFCenter__Entry = DoubleVar()
MaxSFCenter_Entry = Entry(MomentEntryFrame, textvariable = MaxSFCenter__Entry).grid(row =8 , column =7 )
MaxSFCenter__Entry.set(125)     #######REMOVE LATER

MaxSFRight__Entry = DoubleVar()
MaxSFRight_Entry = Entry(MomentEntryFrame, textvariable = MaxSFRight__Entry).grid(row =8 , column =8 )
MaxSFRight__Entry.set(207)      #######REMOVE LATER

DeadLoad__Entry = DoubleVar()
DeadLoad_Entry = Entry(root, textvariable =DeadLoad__Entry).grid(row = 9, column = 1)
DeadLoad__Entry.set(103)        #######REMOVE LATER

LiveLoad__Entry = DoubleVar()
LiveLoad_Entry = Entry(root, textvariable =LiveLoad__Entry).grid(row = 10, column = 1)
LiveLoad__Entry.set(36)         #######REMOVE LATER

Clear__Span = DoubleVar()
Clear_Span = Entry(root, textvariable =Clear__Span).grid(row = 11, column = 1)
Clear__Span.set(5000)       #######REMOVE LATER

Clear__Cover = DoubleVar()
Clear_Cover = Entry(root, textvariable = Clear__Cover).grid(row = 12, column = 1)
Clear__Cover.set(68)        #######REMOVE LATER

def Checker():
    global B, D, fck, fy, MinReinf, MaxReinf, Deff, CC, CL
    
    fck = SelectedCG.get()
    fy = SelectedSG.get()
    B = Width__Entry.get()
    D = Depth__Entry.get()
    CL = Clear__Span.get()
    CC = Clear__Cover.get()
    Deff = D - CC

    
    rootcheck = Toplevel()
    rootcheck.title("Results of Check")

    Label(rootcheck, text = "Clause 6.1.2; IS 13920:2016").grid(row = 0, column = 0)
    if B>200:
        Label(rootcheck, text = "SAFE").grid(row = 0, column = 1)
    else:
        Label(rootcheck, text = "UNSAFE").grid(row = 0, column = 1)
    
    Label(rootcheck, text ="Clause 6.1.3; IS 13920:2016" ).grid(row = 1,column = 0)
    if D / CL > 4:
        Label(rootcheck, text = "SAFE").grid(row =1 ,column =1 )
    else:
        Label(rootcheck, text = "SAFE").grid(row =1 ,column =1 )
    
    MinReinf = round(0.24 * fck**0.5 / fy * B * Deff,2)
    MaxReinf = 0.025 * B * Deff
    Label(rootcheck, text="Minimum Reinforcement Required (mm2):").grid(row =2 ,column =0)
    Label(rootcheck, text="Maximum Reinforcement Possible (mm2):").grid(row =3 ,column =0)
    Label(rootcheck, text=MinReinf).grid(row =2 ,column =1)
    Label(rootcheck, text=MaxReinf).grid(row =3 ,column =1)

def Designer():
    global xumaxbyd, xumax, Mulim, HML, HMR, SML, SMC, SMR
    
    HML = HogLeft__Entry.get()
    HMR = HogRight__Entry.get()
    SML = SagLeft__Entry.get()
    SMC = SagCenter__Entry.get()
    SMR = SagRight__Entry.get()

    rootcheck2 = Toplevel()
    rootcheck2.title("Calculated Reinforcement")
    
    xumaxbyd = ( 0.0035 / ( 0.0055 + 0.87 * fy / 200000 ) )
    xumax = Deff * xumaxbyd
    Mulim = round( ( 0.36 * xumaxbyd * (1 - 0.42 * xumaxbyd) * B * Deff**2 * fck ) / 10**6,3)

    def AreaofSteel(Mu):
        if Mulim > Mu:
            C1 = fy / ( fck * B * Deff )
            C2 = -1 
            C3 = Mu * 10**6 / 0.87 / fy / Deff
            p = np.poly1d([C1,C2,C3])
            roots = p.r
            Ast = round(min(roots[0],roots[1]),2)
            if Ast < 226.08:
                Ast = 226.08
            Asc = 226.08
        else:
            Mu2 = Mu - Mulim
            Ast1 = Mulim * 10**6 / ( 0.87 * fy * ( Deff - 0.42 * xumax ) ) 
            εsc = 0.0035 * ( 1 - CC / xumax)
            fcc = 0.446 * fck
            fsc = interpolateValues(εsc,fy)
            Asc = round(Mu2 * 10**6 / ( fsc - fcc ) / ( Deff - CC ),2)
            Ast2 = Asc * ( fsc - fcc ) / 0.87 / fy
            Ast = round(Ast1 + Ast2,2)
            
        Steels = (Ast , Asc)
        return Steels
    
    HogL = AreaofSteel(HML)
    HogLT = HogL[0]
    HogLB = HogL[1]

    HogR = AreaofSteel(HMR)
    HogRT = HogR[0]
    HogRB = HogR[1]

    if HogLT / 2 > HogLB:
        HogLB = HogLT / 2
    if HogRT / 2 > HogRB:
        HogRB = HogRT / 2

    SagL = AreaofSteel(SML)
    SagLT = SagL[1]
    SagLB = SagL[0]

    if SagLB < ( HogLT / 2 ):
        SagLB = HogLT / 2
    if ( SagLT < ( max(HogLT,HogRT) / 4) ) or ( SagLT < MinReinf ) or ( SagLT < ( SagLB / 2 ) ):
        SagLT = max(( max(HogLT,HogRT) / 4),MinReinf,( SagLB / 2 ))

    SagC = AreaofSteel(SMC)
    SagCT = SagC[1]
    SagCB = SagC[0]

    if ( SagCB < ( max(HogLT,HogRT) / 4) ) or ( SagCB < MinReinf ):
        SagCB = max( ( max( HogLT , HogRT ) / 4 ), MinReinf )

    if (SagCT < ( max( HogLT, HogRT ) / 4 ) ) or ( SagCT < MinReinf ) or ( SagCT < ( SagCB / 2 ) ):
        SagCT = max( max( HogLT, HogRT ) / 4 , MinReinf , ( SagCB / 2 ) )

    SagR = AreaofSteel(SMR)
    SagRT = SagR[1]
    SagRB = SagR[0]

    if SagRB < HogRT / 2:
        SagRB = HogRT / 2
    if ( SagRT < ( max(HogLT,HogRT) / 4) ) or ( SagRT < MinReinf ) or ( SagLT < ( SagRB / 2 ) ):
        SagRT = max(( max(HogLT,HogRT) / 4),MinReinf,( SagRB / 2 ))

    TopLeft = max(HogLT,SagLT)
    BottomLeft = max(HogLB,SagLB)
    TopRight = max(HogRT,SagRT)
    BottomRight = max(HogRB,SagRB)

    Label(rootcheck2, text ="Summary of Required Reinforcement").grid(row = 0, column = 0, columnspan = 4)
    Label(rootcheck2, text ="Left").grid(row = 1, column = 1)
    Label(rootcheck2, text ="Center").grid(row = 1, column = 2)
    Label(rootcheck2, text ="Right").grid(row = 1, column = 3)
    Label(rootcheck2, text ="Top").grid(row = 2, column = 0)
    Label(rootcheck2, text ="Bottom").grid(row = 3, column = 0)
    Label(rootcheck2, text = TopLeft ).grid(row = 2, column = 1)
    Label(rootcheck2, text = BottomLeft ).grid(row = 3, column = 1)
    Label(rootcheck2, text = TopRight ).grid(row = 2, column = 3)
    Label(rootcheck2, text = BottomRight ).grid(row = 3, column = 3)
    Label(rootcheck2, text = SagCT ).grid(row = 2, column = 2)
    Label(rootcheck2, text = SagCB ).grid(row = 3, column = 2)

    button11 = Button(rootcheck2, text = "Click here to enter Ast provided", command = AstProvided).grid(row = 4, column = 0, columnspan = 4)
    button12 = Button(rootcheck2, text = "Close this Window", command = rootcheck2.destroy).grid(row = 5, column = 0, columnspan = 4)

def AstProvided():
        rootcheck3 = Toplevel()
        rootcheck3.title("Entry of Provided Reinforcement")
        Label(rootcheck3, text ="Enter the Provided Reinforcement in mm2").grid(row = 0, column = 0, columnspan = 4)
        Label(rootcheck3, text ="Left").grid(row = 1, column = 1)
        Label(rootcheck3, text ="Center").grid(row = 1, column = 2)
        Label(rootcheck3, text ="Right").grid(row = 1, column = 3)
        Label(rootcheck3, text ="Top").grid(row = 2, column = 0)
        Label(rootcheck3, text ="Bottom").grid(row = 3, column = 0)

        global APTL, APTR, APTC, APBC, APBL, APBR

        APTL__Entry = DoubleVar()
        APTL_Entry = Entry(rootcheck3, textvariable = APTL__Entry ).grid(row = 2, column = 1)
        APTL__Entry.set(2374)           ###REMOVE LATER
        APBL__Entry = DoubleVar()
        APBL_Entry = Entry(rootcheck3, textvariable = APBL__Entry ).grid(row = 3, column = 1)
        APBL__Entry.set(1545)           ###REMOVE LATER
        APTR__Entry = DoubleVar()
        APTR_Entry = Entry(rootcheck3, textvariable = APTR__Entry ).grid(row = 2, column = 3)
        APTR__Entry.set(2374)           ###REMOVE LATER
        APBR__Entry = DoubleVar()
        APBR_Entry = Entry(rootcheck3, textvariable = APBR__Entry ).grid(row = 3, column = 3)
        APBR__Entry.set(1319)           ###REMOVE LATER
        APTC__Entry = DoubleVar()
        APTC_Entry = Entry(rootcheck3, textvariable = APTC__Entry ).grid(row = 2, column = 2)
        APTC__Entry.set(603)            ###REMOVE LATER
        APBC__Entry = DoubleVar()
        APBC_Entry = Entry(rootcheck3, textvariable = APBC__Entry ).grid(row = 3, column = 2)
        APBC__Entry.set(603)            ###REMOVE LATER

        DiaStirrup__Entry = DoubleVar()
        DiaStirrup_Entry = Entry(rootcheck3, textvariable = DiaStirrup__Entry).grid(row = 4, column = 1)
        DiaStirrup__Entry.set(8)        ###REMOVE LATER

        LegNo__Entry = DoubleVar()
        LegNo_Entry = Entry(rootcheck3, textvariable =LegNo__Entry).grid(row = 5, column = 1)
        LegNo__Entry.set(2)             ###REMOVE LATER

        SmallestLongBar__Entry = DoubleVar()
        SmallestLongBar_Entry = Entry(rootcheck3, textvariable = SmallestLongBar__Entry).grid(row = 6, column = 1)
        SmallestLongBar__Entry.set(16)  ###REMOVE LATER 

        ShearReinforcement = Label(rootcheck3, text = "Assume the diameter of stirrups (mm)").grid(row = 4, column = 0)
        LegsNumber = Label(rootcheck3, text = "Assume the number of legs").grid(row = 5, column = 0)
        SmallestDiaBar = Label(rootcheck3, text = "Enter the dia of smallest longitudinal bar").grid(row = 6, column = 0)
        def Answer():
                APTL = APTL__Entry.get()
                APBL = APBL__Entry.get()
                APTR = APTR__Entry.get()
                APBR = APBR__Entry.get()
                APTC = APTC__Entry.get()
                APBC = APBC__Entry.get()

                #OppositeBeam(Tensile,Compressive)
                MuLH = OppositeBeam(APTL, APBL)
                MuLS = OppositeBeam(APBL, APTL)
                MuRH = OppositeBeam(APTR, APBR)
                MuRS = OppositeBeam(APBR, APTR)

                global Vswaytoright, Vswaytoleft, MaxSFLeft, MaxSFRight, DL, LL

                Vswaytoright = (1.4 * (MuLS + MuRH) / CL)
                Vswaytoleft =  (1.4 * (MuLH + MuRS) / CL)
                DL = DeadLoad__Entry.get()
                LL = LiveLoad__Entry.get()
                LD = 1.2 * ( DL + LL ) / 2
                
                VALFR = abs(LD - Vswaytoright)      #Shear at left end for sway to right
                VALFL = abs(LD + Vswaytoleft)        #Shear at left end for sway to left
                VARFR = abs(LD + Vswaytoright)       #Shear at right end for sway to right
                VARFL = abs(LD - Vswaytoleft)        #Shear at right end for sway to left

                MaxSFLeft = MaxSFLeft__Entry.get()
                MaxSFRight = MaxSFRight__Entry.get()
                MaxSFCenter = MaxSFCenter__Entry.get()

                DesignSFLeft = max(VALFR,VALFL,MaxSFLeft)
                DesignSFRight = max(VARFR,VARFL,MaxSFRight)
                DesignSFCenter = max(Vswaytoright,Vswaytoleft,MaxSFCenter)           
                
                global NoOfLegs, DiaOfStirrup, LeftSpacing, RightSpacing, CenterSpacing
                NoOfLegs = LegNo__Entry.get()
                DiaOfStirrup = DiaStirrup__Entry.get()
                
                LeftSpacing = ShearDesign(DesignSFLeft)
                CenterSpacing = ShearDesign(DesignSFCenter)
                RightSpacing = ShearDesign(DesignSFRight)

                if CenterSpacing > Deff / 2:
                        CenterSpacing = Deff / 2
                Label(rootcheck3, text = "Left").grid(row = 8, column = 1)
                Label(rootcheck3, text = "Right").grid(row = 8, column = 3)
                Label(rootcheck3, text = "Center").grid(row = 8, column = 2)
                Label(rootcheck3, text = "Spacing in mm").grid(row = 9, column = 0)
                Label(rootcheck3, text = LeftSpacing).grid(row = 9, column = 1)
                Label(rootcheck3, text = RightSpacing).grid(row = 9, column = 3)
                Label(rootcheck3, text = CenterSpacing).grid(row = 9, column = 2)
                Label(rootcheck3, text = "Spacing for 2d distance (mm)").grid(row = 10, column =0)

                a11 = 100
                a12 = 8 * SmallestLongBar__Entry.get()
                a13 = Deff / 4
                Spacing2d = min(a11, a12, a13)
                Label(rootcheck3, text = Spacing2d).grid(row = 10, column = 1)
                return
        Button(rootcheck3, text = "Calculate Shear", command = Answer).grid(row = 7, column = 0)
	
def OppositeBeam(Ast,Asc):
        xumax = Deff * xumaxbyd
        Esc = 0.0035 * ( 1 - CC / xumax )
        fsc1 = interpolateValues(Esc,fy)
        fcc1 = 0.446 * fck
        x = xumax
        C = round(0.36*fck*B*x + (fsc1 - fcc1)*Asc,2)
        T = round(0.87*fy*Ast,2)
        if C > T:
            while C > T:
                x = x - 1
                Esc1 = 0.0035 * ( 1 - CC / x )
                fsc1 = interpolateValues(Esc1,fy)
                C = round(0.36*fck*B*x + (fsc1 - fcc1)*Asc,2)
        else:
            print('The section is over-reinforced. Please reconsider design.')

        Mu = round((0.36 * fck * B * x * ( Deff - 0.42 * x ) + (fsc1 - fcc1) * Asc * (Deff - CC)) / 10**6,2)
        return Mu

def ShearDesign(Vu):
        tauV = round(Vu * 1000 / B / Deff,2)
        if fck == 15:
                MaxtauV = 1.6
        elif fck == 20:
                MaxtauV = 1.8
        elif fck == 25:
                MaxtauV = 1.9
        elif fck == 30:
                MaxtauV = 2.2
        elif fck == 35:
                MaxtauV = 2.3
        elif ( fck == 40 ) or ( fck > 40 ):
                MaxtauV = 2.5
        if tauV > MaxtauV:
                print('The shear stress in the section with',Vu,' kN is greater than maximum shear stress in concrete of',fck,' Grade.')
        Sv = math.ceil(0.87 * fy * NoOfLegs * 3.14 / 4 * DiaOfStirrup**2 * Deff / Vu / 1000)
        Sv1 = NoOfLegs * 3.14 / 4 * DiaOfStirrup**2 * 0.87 * fy / 0.4 / B #IS 456 2000, Clause 26.5.1.6
        if Sv > Sv1:
                Sv = Sv1
        return Sv

#NOTE: According to the Explanatory Examples, shear strength of concrete is not considered. However, if we do consider the strength, here is the code:
#tauV = round(Vu * 1000 / B / Deff,2)
#Beta = 0.8 * fck / 6.89 / Pt
#if Beta < 1:
    #Beta = 1
#tauC = round(( 0.85 * ( 0.8 * fck )**0.5 * ( ( 1 + 5 * Beta )**0.5 - 1 ) ) / 6 / Beta,2)
#SCC = tauC * B * Deff / 1000
#Vus = Vu - SCC
#Sv = math.ceil(0.87 * fy * NoOfLegs * 3.14 / 4 * DiaOfStirrup**2 * Deff / Vus / 1000)


#CHECKS
Checkbutton = Button(root, text = "CHECK", command = Checker)
Checkbutton.grid(row = 13, column = 0)

Designbutton = Button(root, text= "DESIGN", command = Designer)
Designbutton.grid(row = 13, column = 1)


#DESIGNS


root.mainloop()

